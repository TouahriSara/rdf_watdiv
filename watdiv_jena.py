import requests
from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_power import YPower
import time
import csv

# Configuration de l'URL de jena
SPARQL_ENDPOINT = 'http://localhost:3030/dataset/query'

# Configuration des fichiers CSV pour les résultats
power_log_file = 'power_log_watdiv_jena.csv'  # Fichier CSV pour les données de consommation énergétique
query_time_log = 'query_time_log_watdiv_jena.csv'  # Fichier CSV pour les temps d'exécution des requêtes

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
    print(f"Executing SPARQL query: {query[:100]}...")  # Log the query (first 100 chars for readability)
    
    # Directly passing the raw query without URL encoding
    response = requests.get(SPARQL_ENDPOINT, headers=headers, params={'query': query})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de l'exécution de la requête : {response.status_code}")
        print(response.text)  # Output the error message from the server
        return None

# Fonction pour obtenir la consommation actuelle en watt
def get_power_consumption():
    valeur = sensor.get_currentValue()  # Lecture de la consommation actuelle
    return valeur

# Fonction principale pour exécuter les requêtes SPARQL et enregistrer les résultats
def execute_queries_and_log(q_file_path):
    query_times = []
    energy_data = []

    
    with open(q_file_path, 'r') as file:
        queries = file.read().split('#EOQ#')  

    # Exécution de chaque requête SPARQL
    for query in queries:
        query = query.strip()
        if query: 
            start_time = time.time()
            
            
            result = run_sparql_query(query)
            execution_time = time.time() - start_time
            
            
            energy_consumption_w = get_power_consumption()
            
            
            query_times.append({
                'query': query[:50],  # Limiter la taille de la requête pour la lisibilité
                'execution_time_s': execution_time
            })
            
            energy_data.append({
                'query': query[:50],  # Limiter la taille de la requête pour la lisibilité
                'execution_time_s': execution_time,
                'energy_consumption_w': energy_consumption_w
            })

           

   
    with open(query_time_log, 'w', newline='') as csvfile:
        fieldnames = ['query', 'execution_time_s']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in query_times:
            writer.writerow(row)
    
    with open(power_log_file, 'w', newline='') as csvfile:
        fieldnames = ['query', 'execution_time_s', 'energy_consumption_w']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in energy_data:
            writer.writerow(row)

    print(f"Les données des requêtes et de la consommation énergétique ont été enregistrées dans {query_time_log} et {power_log_file}.")

# Exécution du script
if __name__ == '__main__':
    q_file_path = '/home/adminlias/ddd/Downloads/rdf-exp-master/queries/individual/watdiv-100m/string/complex.q'
    execute_queries_and_log(q_file_path)

    # Libération des ressources Yoctopuce à la fin
    YAPI.FreeAPI()
