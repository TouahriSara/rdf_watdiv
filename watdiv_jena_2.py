import requests
from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_power import YPower
import time
import csv
import threading
from datetime import datetime

# Configuration de l'URL de jena
SPARQL_ENDPOINT = 'http://localhost:3030/dataset/query'

# Générer un suffixe basé sur la date et l'heure actuelle
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
power_log_file = f'power_log_watdiv_jena_{timestamp}.csv'
query_time_log = f'query_time_log_watdiv_jena_{timestamp}.csv'

# Initialisation de l'API Yoctopuce
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    print("Échec de connexion au hub Yoctopuce :", errmsg.value)
    exit()
else:
    print("Connexion réussie au hub Yoctopuce")

# Recherche du capteur de consommation d'énergie
sensor = YPower.FirstPower()
if sensor is None:
    print("Aucun capteur détecté")
    YAPI.FreeAPI()
    exit()

print("Capteur détecté :", sensor.get_friendlyName())

# Fonction pour exécuter une requête SPARQL sur Virtuoso
def run_sparql_query(query):
    headers = {'Accept': 'application/json'}
    print(f"Exécution de la requête SPARQL : {query[:100]}...")
    response = requests.get(SPARQL_ENDPOINT, headers=headers, params={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de l'exécution de la requête : {response.status_code}")
        print(response.text)
        return None

# Mesurer la consommation de base du système sur une durée donnée (en l'absence de requête)
def measure_baseline(duration=5, sampling_interval=0.1):
    readings = []
    start = time.time()
    print("Mesure du baseline en cours...")
    while time.time() - start < duration:
        power = sensor.get_currentValue()
        readings.append(power)
        print(f"Baseline mesure : {power:.2f} W")  # Ajout de l'affichage de chaque mesure
        time.sleep(sampling_interval)

    baseline = sum(readings) / len(readings)
    print(f"Puissance de base moyenne mesurée: {baseline:.2f} W")
    return baseline

# Mesurer l'énergie consommée par une requête en isolant la consommation excédentaire
def measure_query_energy(query, baseline, sampling_interval=0.1):
    result_container = {}
    sampling_data = []
    stop_sampling = [False]  # Drapeau mutable pour arrêter le thread d'échantillonnage

    def query_thread():
        result_container['result'] = run_sparql_query(query)

    def sampling_thread():
        last_sample_time = time.time()
        while not stop_sampling[0]:
            current_time = time.time()
            delta_t = current_time - last_sample_time
            last_sample_time = current_time
            p = sensor.get_currentValue()
            extra_power = max(p - baseline, 0)
            sampling_data.append(extra_power)
            
            # Affichage de chaque mesure pour vérifier les calculs
            print(f"Mesure : {p:.2f} W, Puissance: {extra_power:.2f} W")

            time.sleep(sampling_interval)
    
    qt = threading.Thread(target=query_thread)
    st = threading.Thread(target=sampling_thread)
    start_time = time.time()
    st.start()
    qt.start()
    qt.join()  # Attendre la fin de la requête
    stop_sampling[0] = True
    st.join()
    execution_time = time.time() - start_time
    puissance=sum(sampling_data)
    
    energy_consumed = sum(sampling_data)*execution_time
    print (f"le temps d'execution est : {execution_time}")
    print (f"l'energie consomée est : {energy_consumed}")
   

    return result_container.get('result'), energy_consumed, execution_time ,puissance

# Fonction principale pour exécuter les requêtes et enregistrer les mesures
def execute_queries_and_log(q_file_path):
    query_times = []
    energy_data = []

    with open(q_file_path, 'r') as file:
        queries = file.read().split('#EOQ#')
    
    # Mesurer le baseline avant d'exécuter les requêtes
    baseline = measure_baseline()

    # Exécution de chaque requête SPARQL
    for query in queries:
        query = query.strip()
        if query:
            result, energy_consumed, execution_time , puissance= measure_query_energy(query, baseline)
            
            query_times.append({
                'query': query[:50],
                'execution_time_s': execution_time
            })
            energy_data.append({
                'query': query[:50],
                'execution_time_s': execution_time,
                'puissance': puissance ,
                'energy_consumed_joules': energy_consumed
            })
            print(f"Requête exécutée en {execution_time:.2f}s, énergie consommée: {energy_consumed:.2f} J")
   
    # Enregistrement des résultats dans des fichiers CSV
    with open(query_time_log, 'w', newline='') as csvfile:
        fieldnames = ['query', 'execution_time_s']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in query_times:
            writer.writerow(row)
    
    with open(power_log_file, 'w', newline='') as csvfile:
        fieldnames = ['query', 'execution_time_s', 'puissance', 'energy_consumed_joules']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in energy_data:
            writer.writerow(row)

    print(f"Les données des requêtes et de la consommation énergétique ont été enregistrées dans {query_time_log} et {power_log_file}.")

# Exécution du script
if __name__ == '__main__':
    q_file_path = '/home/adminlias/Desktop/PFE /queries_test.q'
    execute_queries_and_log(q_file_path)
    YAPI.FreeAPI()
