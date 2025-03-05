import csv
import re
from datetime import datetime
from collections import defaultdict

# Fonction pour analyser les opérations dans une requête SPARQL
def analyse_operations(query):
    # Initialiser un dictionnaire pour compter les opérations
    operations = {
        "SELECT(n)": 0,  # Le nombre de variables à retourner
        "JOIN(n)": 0,  # Nombre de jointures
        "FILTER(1ou 0)": 0,  # Présence d'un FILTER
        "UNION(n ou 0)": 0,  # Présence d'un UNION
        "ORDER BY(1ou 0)": 0,  # Présence d'un ORDER BY
        "GROUP BY(1ou 0)": 0,  # Présence d'un GROUP BY
        "LIMIT/OFFSET(1ou 0)": 0  # Présence de LIMIT ou OFFSET
    }

    # Détection du nombre de variables dans SELECT
    select_match = re.search(r'\bSELECT\s+(.*?)\s+WHERE', query, re.IGNORECASE)
    if select_match:
        # Extraire les variables après SELECT
        select_vars = select_match.group(1).strip()
        operations["SELECT(n)"] = len([var for var in select_vars.split() if var.startswith('?')])

    # Analyser les occurrences des autres mots-clés SPARQL
    for operation in operations.keys():
        if operation != "SELECT(n)":  # On ne compte pas encore SELECT(n) ici
            operations[operation] = len(re.findall(r'\b' + re.escape(operation.split('(')[0]) + r'\b', query, re.IGNORECASE))

    # Détection des jointures (en supposant des jointures dans les triplets)
    where_section = re.search(r'WHERE\s*{(.*)}', query, re.DOTALL | re.IGNORECASE)
    if where_section:
        where_content = where_section.group(1)

        # Trouver tous les triplets avec des variables
        triplets = re.findall(r'(\?[a-zA-Z0-9_]+)\s+<[^>]+>\s+(\?[a-zA-Z0-9_]+)', where_content)

        # Construire un ensemble des jointures uniques
        jointures = set()
        for var1, var2 in triplets:
            if var1 != var2:  # Exclure les auto-jointures
                jointures.add(tuple(sorted([var1, var2])))

        operations["JOIN(n)"] = len(jointures)

    # Détection de l'opération FILTER (1 ou 0)
    if "FILTER" in query:
        operations["FILTER(1ou 0)"] = 1

    # Détection de l'opération UNION (n ou 0)
    if "UNION" in query:
        operations["UNION(n ou 0)"] = 1

    # Détection de l'opération ORDER BY (1 ou 0)
    if "ORDER BY" in query:
        operations["ORDER BY(1ou 0)"] = 1

    # Détection de l'opération GROUP BY (1 ou 0)
    if "GROUP BY" in query:
        operations["GROUP BY(1ou 0)"] = 1

    # Détection de l'opération LIMIT ou OFFSET (1 ou 0)
    if "LIMIT" in query or "OFFSET" in query:
        operations["LIMIT/OFFSET(1ou 0)"] = 1

    # Retourner le vecteur des opérations
    return list(operations.values())

# Fonction pour lire le fichier et analyser les requêtes
def process_sparql_queries(input_filename, nt_filename, output_filename, text_filename):
    results = []
    results2 = []
    
    # Lire le fichier contenant les requêtes
    with open(input_filename, 'r') as f:
        queries = f.read().split("#EOQ#")  # Assurez-vous que le séparateur est correct
        nb_queries = len(queries)
        for query in queries:
            query = query.strip()
            if query:
                operation_vector = analyse_operations(query)
                results.append([query] + operation_vector)
            if query:
                operation_vector2 = analyse_operations(query)
                results2.append(operation_vector2)

    # Lire le fichier .nt et compter les triplets distincts
    distinct_triplets = set()
    with open(nt_filename, 'r') as nt_file:
        for line in nt_file:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignorer les commentaires
                parts = line.split(' ')
                if len(parts) == 3:
                    subject, predicate, obj = parts
                    distinct_triplets.add((subject, predicate, obj))

    nb_distinct_triplets = len(distinct_triplets)

    # Écriture des résultats dans un fichier CSV
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Requête', 'SELECT(n)', 'JOIN(n)', 'FILTER(1ou 0)', 'UNION(n ou 0)', 'ORDER BY(1ou 0)', 'GROUP BY(1ou 0)', 'LIMIT/OFFSET(1ou 0)'])
        writer.writerows(results)

    # Écriture des résultats dans un fichier texte
    with open(text_filename, 'w') as txtfile:
        txtfile.write(f"Nombre total de requêtes: {nb_queries}\n")
        txtfile.write(f"Nombre total de triplets distincts dans le fichier .nt: {nb_distinct_triplets}\n\n")
        for query, operation_vector2 in zip(queries, results2):
            # Écrire la requête et son vecteur d'opérations dans le fichier texte
            txtfile.write(f"Requête: {query}\n")
            txtfile.write(f"Vecteur d'opérations: [SELECT(n), JOIN(n), FILTER(1ou 0), UNION(n ou 0), ORDER BY(1ou 0), GROUP BY(1ou 0), LIMIT/OFFSET(1ou 0)]\n")
            txtfile.write(f"Vecteur d'opérations: {operation_vector2}\n\n")

    print(f"Les résultats ont été enregistrés dans le fichier : {output_filename}")
    print(f"Le nombre total de requêtes a été enregistré dans le fichier : {text_filename}")

# Exemple d'utilisation
input_filename = '/home/adminlias/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q'
nt_file = '/home/adminlias/ddd/Downloads/wsdts_100m.nt'

# Générer un nom de fichier de sortie avec horodatage
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f'query_vector_{timestamp}.csv'
text_filename = f'query_vector_{timestamp}.txt'

# Exécuter l'analyse des requêtes
process_sparql_queries(input_filename, nt_file, output_filename, text_filename)
