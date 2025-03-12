import requests
from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_power import YPower
import time
import csv
import threading
from datetime import datetime

SPARQL_ENDPOINT = 'http://localhost:8890/sparql'


# Générer un suffixe basé sur la date et l'heure actuelle
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
power_log_file = f'power_log_watdiv_virtuoso_withbuffer_{timestamp}.csv'

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
        print(f"Baseline mesure : {power:.2f} W")
        time.sleep(sampling_interval)

    baseline = sum(readings) / len(readings) if readings else 0
    print(f"Puissance de base moyenne mesurée: {baseline:.2f} W")
    return baseline

# Mesurer l'énergie consommée par une requête en isolant la consommation excédentaire
def measure_query_energy(query, baseline, sampling_interval=0.1):
    result_container = {}
    sampling_data = []
    
    # Event pour contrôler la fin du thread d'échantillonnage
    stop_sampling_event = threading.Event()

    def query_thread():
        result_container['result'] = run_sparql_query(query)

    def sampling_thread():
        while not stop_sampling_event.is_set():  # Utilisation de l'Event pour arrêter le thread
            power = sensor.get_currentValue()
            
            sampling_data.append(power)
            print(f"Mesure : {power:.2f} W, Puissance excédentaire: {power:.2f} W")
            time.sleep(sampling_interval)
    
    qt = threading.Thread(target=query_thread)
    st = threading.Thread(target=sampling_thread)

    start_time = time.time()
    st.start()
    qt.start()
    qt.join()  # Attendre la fin de la requête
    stop_sampling_event.set()  # Arrêter l'échantillonnage
    st.join()  # Attendre que le thread d'échantillonnage se termine
    execution_time = time.time() - start_time

    # Correction du calcul d'énergie
    energy_consumed = sum(p * sampling_interval for p in sampling_data)
    avg_power = sum(sampling_data) / len(sampling_data) if sampling_data else 0

    print(f"Temps d'exécution : {execution_time:.2f}s")
    print(f"Énergie consommée : {energy_consumed:.4f} J")
    print(f"Puissance moyenne excédentaire : {avg_power:.4f} W")

    return result_container.get('result'), energy_consumed, execution_time, avg_power

# Fonction principale pour exécuter les requêtes et enregistrer les mesures
def execute_queries_and_log(q_file_path):
 
    energy_data = []

    with open(q_file_path, 'r') as file:
        queries = file.read().split('#EOQ#')
    
    # Mesurer le baseline avant d'exécuter les requêtes
    baseline = measure_baseline()

    # Exécution de chaque requête SPARQL
    for query in queries:
        query = query.strip()
        if query:
            result, energy_consumed, execution_time, avg_power = measure_query_energy(query, baseline)
            
            
            energy_data.append({
                'query': query[:50],
                'execution_time_s': round(execution_time, 4),  # Arrondi à 3 décimales
                'puissance_moyenne_W': round(avg_power, 4),    # Arrondi à 3 décimales
                'energy_consumed_J': round(energy_consumed, 4) # Arrondi à 3 décimales
            })
            print(f"Requête exécutée en  énergie consommée: {energy_consumed:.4f} J")
   
   
    with open(power_log_file, 'w', newline='') as csvfile:
        fieldnames = ['query', 'execution_time_s', 'puissance_moyenne_W', 'energy_consumed_J']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(energy_data)

    print(f"Les données des requêtes et de la consommation énergétique ont été enregistrées dans {power_log_file}.")

# Exécution du script
if __name__ == '__main__':
    q_file_path = '/home/adminlias/data/PFE /test.q'

    execute_queries_and_log(q_file_path)
    YAPI.FreeAPI()
