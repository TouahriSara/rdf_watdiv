import csv
import re
from datetime import datetime
from collections import defaultdict
import os
import tempfile  # added for temporary file management

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

def count_distinct_triplets(nt_filename, num_buckets=1000):
    import re
    # Expression régulière pour capturer :
    # - un sujet sous forme d'URI (entre < et >)
    # - un prédicat sous forme d'URI
    # - un objet qui peut être un littéral entre guillemets (avec éventuel tag ou datatype) ou un URI
    triple_pattern = re.compile(
        r'^(<[^>]+>)\s+'                      # Sujet
        r'(<[^>]+>)\s+'                       # Prédicat
        r'((?:"(?:\\"|[^"])*"(?:\^\^<[^>]+>|@[a-zA-Z\-]+)?)|(?:<[^>]+>))\s*\.\s*$'
    )
    
    # Créer des fichiers temporaires pour chaque bucket
    bucket_files = {}
    for i in range(num_buckets):
        bucket_files[i] = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    
    with open(nt_filename, 'r', encoding='utf-8') as nt_file:
        for line in nt_file:
            line = line.strip()
            if line and not line.startswith('#'):
                match = triple_pattern.match(line)
                if match:
                    subject = match.group(1)
                    predicate = match.group(2)
                    object_val = match.group(3)
                    triple = (subject, predicate, object_val)
                    bucket = hash(triple) % num_buckets
                    bucket_files[bucket].write(' '.join(triple) + '\n')
                else:
                    # Si la ligne ne correspond pas au pattern, vous pouvez gérer l'exception ou l'ignorer
                    print(f"Ligne non reconnue : {line}")
    
    # Fermer et traiter les fichiers temporaires
    for f in bucket_files.values():
        f.close()
    
    distinct_count = 0
    for i in range(num_buckets):
        bucket_file_name = bucket_files[i].name
        seen = set()
        with open(bucket_file_name, 'r', encoding='utf-8') as f:
            for line in f:
                triple = tuple(line.strip().split(' ', 2))
                seen.add(triple)
        distinct_count += len(seen)
        os.remove(bucket_file_name)
    
    return distinct_count


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

    # Utiliser la nouvelle fonction pour compter les triplets distincts sans charger tout en mémoire
    nb_distinct_triplets = count_distinct_triplets(nt_filename)
    
    # Création du répertoire "generated_files" s'il n'existe pas
    os.makedirs("generated_files", exist_ok=True)

    # Définition des chemins de sortie des fichiers
    output_filepath = os.path.join("generated_files", output_filename)
    text_filepath = os.path.join("generated_files", text_filename)
    # Écriture des résultats dans un fichier CSV
    with open(output_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Requête', 'SELECT(n)', 'JOIN(n)', 'FILTER(1ou 0)', 'UNION(n ou 0)', 'ORDER BY(1ou 0)', 'GROUP BY(1ou 0)', 'LIMIT/OFFSET(1ou 0)'])
        writer.writerows(results)

    # Écriture des résultats dans un fichier texte
    with open(text_filepath, 'w') as txtfile:
        txtfile.write(f"Nombre total de requêtes: {nb_queries}\n")
        txtfile.write(f"Nombre total de triplets distincts dans le fichier .nt: {nb_distinct_triplets}\n\n")
        for query, operation_vector2 in zip(queries, results2):
            # Écrire la requête et son vecteur d'opérations dans le fichier texte
            txtfile.write(f"Requête: {query}\n")
            txtfile.write(f"Vecteur d'opérations: [SELECT(n), JOIN(n), FILTER(1ou 0), UNION(n ou 0), ORDER BY(1ou 0), GROUP BY(1ou 0), LIMIT/OFFSET(1ou 0)]\n")
            txtfile.write(f"Vecteur d'opérations: {operation_vector2}\n\n")

    print(f"Les résultats ont été enregistrés dans le fichier : {output_filename}")
    print(f"Le nombre total de requêtes a été enregistré dans le fichier : {text_filename}")

#_________________________________________ QUERIES_FILE_______________________________________________________________#
#/home/adminlias/ddd/Downloads/rdf-exp-master/queries/workloads/lubm10240/string/workload_10k/all_batch_sequential.q

input_filename = '/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/lubm10240/string/workload_10k/all_batch_sequential.q'

#input_filename = '/home/adminlias/data/PFE_/queries_test.q'
#_________________________________________ NT_FILE_______________________________________________________________#
#/home/adminlias/data/ddd/Downloads/10240_new_str/string/10240/lubm10240.nt
nt_file = '/home/adminlias/data/ddd/Downloads/10240_new_str/string/10240/lubm10240.nt'
#nt_file='/home/adminlias/data/PFE_/queries_test_2.nt'
#nt_file = '/home/adminlias/Downloads/data2.nt'
# Générer un nom de fichier de sortie avec horodatage
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f'query_vector_{timestamp}.csv'
text_filename = f'query_vector_{timestamp}.txt'

# Exécuter l'analyse des requêtes
process_sparql_queries(input_filename, nt_file, output_filename, text_filename)