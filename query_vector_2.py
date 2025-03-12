import csv
import re
from datetime import datetime
import os
import json

# Fonction pour analyser les opérations dans une requête SPARQL
def analyse_operations(query):
    # Initialiser un dictionnaire pour compter les opérations
    operations = {
        "SELECT(n)": 0,        # Nombre de variables à retourner
        "JOIN(n)": 0,          # Nombre de jointures
        "FILTER(1ou 0)": 0,    # Présence d'un FILTER
        "UNION(n ou 0)": 0,    # Présence d'un UNION
        "ORDER BY(1ou 0)": 0,  # Présence d'un ORDER BY
        "GROUP BY(1ou 0)": 0,  # Présence d'un GROUP BY
        "LIMIT/OFFSET(1ou 0)": 0  # Présence de LIMIT ou OFFSET
    }

    # Détection du nombre de variables dans SELECT
    select_match = re.search(r'\bSELECT\s+(.*?)\s+WHERE', query, re.IGNORECASE)
    if select_match:
        select_vars = select_match.group(1).strip()
        operations["SELECT(n)"] = len([var for var in select_vars.split() if var.startswith('?')])

    # Analyser les occurrences des autres mots-clés SPARQL
    for operation in operations.keys():
        if operation != "SELECT(n)":
            operations[operation] = len(re.findall(r'\b' + re.escape(operation.split('(')[0]) + r'\b', query, re.IGNORECASE))

    # Détection des jointures dans la clause WHERE
    where_section = re.search(r'WHERE\s*{(.*)}', query, re.DOTALL | re.IGNORECASE)
    if where_section:
        where_content = where_section.group(1)
        triplets = re.findall(r'(\?[a-zA-Z0-9_]+)\s+<[^>]+>\s+(\?[a-zA-Z0-9_]+)', where_content)
        jointures = set()
        for var1, var2 in triplets:
            if var1 != var2:  # Exclure les auto-jointures
                jointures.add(tuple(sorted([var1, var2])))
        operations["JOIN(n)"] = len(jointures)

    # Détection de FILTER, UNION, ORDER BY, GROUP BY, LIMIT/OFFSET
    if "FILTER" in query:
        operations["FILTER(1ou 0)"] = 1
    if "UNION" in query:
        operations["UNION(n ou 0)"] = 1
    if "ORDER BY" in query:
        operations["ORDER BY(1ou 0)"] = 1
    if "GROUP BY" in query:
        operations["GROUP BY(1ou 0)"] = 1
    if "LIMIT" in query or "OFFSET" in query:
        operations["LIMIT/OFFSET(1ou 0)"] = 1

    # Retourner le vecteur des opérations sous forme de liste
    return list(operations.values())

# Fonction pour lire le fichier, analyser les requêtes et enregistrer les résultats dans un fichier CSV
def process_sparql_queries(input_filename, csv_filename, text_filename):
    results = []
    
    # Lire le fichier contenant les requêtes
    with open(input_filename, 'r') as f:
        queries = f.read().split("#EOQ#")  # Vérifiez que le séparateur est correct
        nb_queries = len(queries)
        for query in queries:
            query = query.strip()
            if query:
                operation_vector = analyse_operations(query)
                results.append((query, operation_vector))
    
    os.makedirs("generated_files", exist_ok=True)
    csv_filepath = os.path.join("generated_files", csv_filename)
    text_filepath = os.path.join("generated_files", text_filename)
    
    # Création du fichier CSV avec deux colonnes : query et query_vector
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["query", "query_vector"])
        for query_text, query_vector in results:
            vector_json = json.dumps(query_vector)
            writer.writerow([query_text, vector_json])
    
    # Création d'un fichier texte pour récapituler le nombre de requêtes et afficher les détails
    with open(text_filepath, 'w', encoding='utf-8') as txtfile:
        txtfile.write(f"Nombre total de requêtes: {nb_queries}\n")
        for query_text, query_vector in results:
            txtfile.write(f"Requête: {query_text}\n")
            txtfile.write(f"Vecteur d'opérations: {query_vector}\n\n")
    
    print(f"Les résultats ont été enregistrés dans le fichier CSV : {csv_filename}")
    print(f"Le résumé a été enregistré dans le fichier texte : {text_filename}")

#_________________________________________ QUERIES_FILE_______________________________________________________________#
input_filename = '/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q'

# Générer des noms de fichiers de sortie avec horodatage
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f'query_vector_watdiv_{timestamp}.csv'
text_filename = f'query_vector_watdiv_{timestamp}.txt'

# Exécuter l'analyse des requêtes et enregistrer dans un fichier CSV
process_sparql_queries(input_filename, csv_filename, text_filename)
