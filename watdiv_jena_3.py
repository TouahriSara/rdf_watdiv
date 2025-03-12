import os
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
power_log_file = f'power_log_watdiv_jena_withbuffer_{timestamp}.csv'


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

# Mesurer l'énergie consommée par une requête directement
def measure_query_energy(query, sampling_interval=0.1):
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
            print(f"Mesure : {power:.2f} W")
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

    # Calcul d'énergie
    energy_consumed = sum(p * sampling_interval for p in sampling_data)
    avg_power = sum(sampling_data) / len(sampling_data) if sampling_data else 0

    print(f"Temps d'exécution : {execution_time:.2f}s")
    print(f"Énergie consommée : {energy_consumed:.4f} J")
    print(f"Puissance moyenne : {avg_power:.4f} W")

    return result_container.get('result'), energy_consumed, execution_time, avg_power

# Fonction principale pour exécuter les requêtes et enregistrer les mesures
def execute_queries_and_log(q_file_path):
    
    energy_data = []

    with open(q_file_path, 'r') as file:
        queries = file.read().split('#EOQ#')
    
    # Exécution de chaque requête SPARQL
    for query in queries:
        query = query.strip()
        if query:
            result, energy_consumed, execution_time, avg_power = measure_query_energy(query)
            
            
            energy_data.append({
                'query': query[:50],
                'execution_time_s': execution_time,
                'puissance_moyenne_W': avg_power,
                'energy_consumed_J': energy_consumed
            })
            print(f"Requête exécutée en {execution_time:.2f}s, énergie consommée: {energy_consumed:.4f} J")
    
    # Création du répertoire "generated_files" s'il n'existe pas
    os.makedirs("generated_files", exist_ok=True)

    # Définition des chemins de sortie des fichiers
    
    power_log_file_result = os.path.join("generated_files", power_log_file)
    # Enregistrement des résultats dans des fichiers CSV
    
    
    with open(power_log_file_result, 'w', newline='') as csvfile:
        fieldnames = ['query', 'execution_time_s', 'puissance_moyenne_W', 'energy_consumed_J']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(energy_data)

    print(f"Les données des requêtes et de la consommation énergétique ont été enregistrées dans {query_time_log} et {power_log_file}.")

# Exécution du script
if __name__ == '__main__':

    q_file_path = '/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q'
    execute_queries_and_log(q_file_path)
    YAPI.FreeAPI()
