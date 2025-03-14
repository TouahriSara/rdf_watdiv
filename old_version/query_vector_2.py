import csv
import re
from datetime import datetime
from collections import defaultdict
import os
import tempfile  # pour la gestion des fichiers temporaires
import json

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

def count_distinct_triplets(nt_filename, num_buckets=1000):
    import re
    triple_pattern = re.compile(
        r'^(<[^>]+>)\s+'                      # Sujet
        r'(<[^>]+>)\s+'                       # Prédicat
        r'((?:"(?:\\"|[^"])*"(?:\^\^<[^>]+>|@[a-zA-Z\-]+)?)|(?:<[^>]+>))\s*\.\s*$'
    )
    
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
                    print(f"Ligne non reconnue : {line}")
    
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

# Fonction modifiée pour lire le fichier, analyser les requêtes
# et enregistrer les résultats dans un fichier SQL
def process_sparql_queries(input_filename, nt_filename, sql_filename, text_filename):
    results = []
    results2 = []
    
    # Lire le fichier contenant les requêtes
    with open(input_filename, 'r') as f:
        queries = f.read().split("#EOQ#")  # Vérifiez que le séparateur est correct
        nb_queries = len(queries)
        for query in queries:
            query = query.strip()
            if query:
                operation_vector = analyse_operations(query)
                # On crée un vecteur qui combine la requête et son vecteur d'opérations
                results.append([query] + operation_vector)
                results2.append(operation_vector)

    nb_distinct_triplets = count_distinct_triplets(nt_filename)
    
    os.makedirs("generated_files", exist_ok=True)
    sql_filepath = os.path.join("generated_files", sql_filename)
    text_filepath = os.path.join("generated_files", text_filename)
    
    # Création du fichier SQL
    with open(sql_filepath, 'w') as sqlfile:
        # On supprime la table existante et on la recrée
        sqlfile.write("DROP TABLE IF EXISTS query_vectors;\n")
        sqlfile.write("CREATE TABLE query_vectors (\n")
        sqlfile.write("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
        sqlfile.write("    query_vector TEXT\n")
        sqlfile.write(");\n\n")
        
        # Insertion de chaque vecteur de requête dans la table sous forme de JSON
        for row in results:
            # row contient [query, SELECT(n), JOIN(n), FILTER, UNION, ORDER BY, GROUP BY, LIMIT/OFFSET]
            json_data = json.dumps(row)
            # On écrit l'instruction INSERT en échappant les simples quotes
            sqlfile.write(f"INSERT INTO query_vectors (query_vector) VALUES ('{json_data}');\n")
    
    # Écriture d'un fichier texte de résumé
    with open(text_filepath, 'w') as txtfile:
        txtfile.write(f"Nombre total de requêtes: {nb_queries}\n")
        txtfile.write(f"Nombre total de triplets distincts dans le fichier .nt: {nb_distinct_triplets}\n\n")
        for query, operation_vector in zip(queries, results2):
            txtfile.write(f"Requête: {query}\n")
            txtfile.write(f"Vecteur d'opérations: {operation_vector}\n\n")
    
    print(f"Les résultats ont été enregistrés dans le fichier SQL : {sql_filename}")
    print(f"Les informations sur le nombre de requêtes ont été enregistrées dans le fichier texte : {text_filename}")

#_________________________________________ QUERIES_FILE_______________________________________________________________#
input_filename = '/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/lubm10240/string/workload_10k/all_batch_sequential.q'

#_________________________________________ NT_FILE_______________________________________________________________#
nt_file = '/home/adminlias/data/ddd/Downloads/10240_new_str/string/10240/lubm10240.nt'

# Générer des noms de fichiers de sortie avec horodatage
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
sql_filename = f'query_vector_{timestamp}.sql'
text_filename = f'query_vector_{timestamp}.txt'

# Exécuter l'analyse des requêtes et enregistrer dans un fichier SQL
process_sparql_queries(input_filename, nt_file, sql_filename, text_filename)
