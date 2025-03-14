import requests
import os
import subprocess
from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_power import YPower
import time
import csv
import threading
from datetime import datetime

SPARQL_ENDPOINT = 'http://localhost:8890/sparql'
DOCKER_CONTAINER_NAME = 'my_virtdb'  # Remplacez par le nom exact de votre conteneur

# Générer un suffixe basé sur la date et l'heure actuelle
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
power_log_file = f'power_log_watdiv_virtuoso_withoutbuffer_{timestamp}.csv'


# Initialisation de l'API Yoctopuce
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    print("Échec de connexion au hub Yoctopuce :", errmsg.value)
    exit()

sensor = YPower.FirstPower()
if sensor is None:
    print("Aucun capteur détecté")
    YAPI.FreeAPI()
    exit()

print("Capteur détecté :", sensor.get_friendlyName())

def restart_container():
    print(f"Redémarrage du conteneur {DOCKER_CONTAINER_NAME}...")
    subprocess.run(["docker", "restart", DOCKER_CONTAINER_NAME], check=True)
    print("Conteneur redémarré.")
    time.sleep(10)  # Pause pour s'assurer que le service est bien redémarré

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

def measure_baseline(duration=5, sampling_interval=0.1):
    readings = []
    start = time.time()
    while time.time() - start < duration:
        power = sensor.get_currentValue()
        readings.append(power)
        time.sleep(sampling_interval)
    return sum(readings) / len(readings) if readings else 0

def measure_query_energy(query, baseline, sampling_interval=0.1):
    result_container = {}
    sampling_data = []
    stop_sampling_event = threading.Event()
    
    def query_thread():
        result_container['result'] = run_sparql_query(query)
    
    def sampling_thread():
        while not stop_sampling_event.is_set():
            power = sensor.get_currentValue()
            sampling_data.append(power)
            time.sleep(sampling_interval)
    
    qt = threading.Thread(target=query_thread)
    st = threading.Thread(target=sampling_thread)
    
    start_time = time.time()
    st.start()
    qt.start()
    qt.join()
    stop_sampling_event.set()
    st.join()
    execution_time = time.time() - start_time
    
    energy_consumed = sum(p * sampling_interval for p in sampling_data)
    avg_power = sum(sampling_data) / len(sampling_data) if sampling_data else 0
    
    return result_container.get('result'), energy_consumed, execution_time, avg_power

def execute_queries_and_log(q_file_path):
    
    energy_data = []
    
    with open(q_file_path, 'r') as file:
        queries = file.read().split('#EOQ#')
    
    baseline = measure_baseline()
    
    for query in queries:
        query = query.strip()
        if query:
            result, energy_consumed, execution_time, avg_power = measure_query_energy(query, baseline)
            
            
            energy_data.append({'query': query[:50], 'execution_time_s': round(execution_time,4), 'puissance_moyenne_W': round(avg_power,4), 'energy_consumed_J': round(energy_consumed,4)})
            
            print(f"Requête exécutée en {execution_time:.2f}s, énergie consommée: {energy_consumed:.4f} J")
            restart_container()  # Redémarrer le conteneur après chaque requête
    
    
    
    with open(power_log_file, 'w', newline='') as csvfile:
        fieldnames = ['query', 'execution_time_s', 'puissance_moyenne_W', 'energy_consumed_J']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(energy_data)
    
    print(f"Les données ont été enregistrées dans {power_log_file}.")

if __name__ == '__main__':
    q_file_path =  '/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q'
    execute_queries_and_log(q_file_path)
    YAPI.FreeAPI()
