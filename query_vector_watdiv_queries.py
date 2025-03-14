import csv
import re
from datetime import datetime
from collections import defaultdict, Counter
import os



def analyse_operations(query):
    keys = ["SELECT(n)", "SELECTION", "JOIN(n)", "FILTER(1ou 0)", 
            "UNION(n ou 0)", "ORDER BY(1ou 0)", "GROUP BY(1ou 0)", "LIMIT/OFFSET(1ou 0)"]
    operations = {key: 0 for key in keys}

    # Analyse SELECT
    select_match = re.search(r'\bSELECT\s+([^}]+?)\s+WHERE', query, re.IGNORECASE | re.DOTALL)
    if select_match:
        operations["SELECT(n)"] = len([v for v in select_match.group(1).split() if v.startswith('?')])

    # Analyse WHERE
    where_section = re.search(r'WHERE\s*{(.*?)}', query, re.DOTALL | re.IGNORECASE)
    if where_section:
        content = where_section.group(1)
        triple_pattern = re.compile(
            r'(?P<subject>\?[^\s]+|<[^>]+>|".*?")\s+'
            r'(?P<predicate><[^>]+>)\s+'
            r'(?P<object>\?[^\s]+|<[^>]+>|".*?")'
        )
        triples = triple_pattern.finditer(content)
        
        # Compteurs
        selection_count = 0
        join_count = 0
        
        for triple in triples:
            subj = triple.group('subject')
            obj = triple.group('object')
            
            # Sélection : exactement 1 variable
            if (subj.startswith('?') and not obj.startswith('?')) or \
               (not subj.startswith('?') and obj.startswith('?')):
                selection_count += 1
                
            # Jointure : 2 variables dans le triplet
            if subj.startswith('?') and obj.startswith('?'):
                join_count += 1

        operations["SELECTION"] = selection_count
        operations["JOIN(n)"] = join_count

    # Autres opérations
    operations["FILTER(1ou 0)"] = 1 if re.search(r'\bFILTER\b', query, re.IGNORECASE) else 0
    operations["UNION(n ou 0)"] = 1 if re.search(r'\bUNION\b', query, re.IGNORECASE) else 0
    operations["ORDER BY(1ou 0)"] = 1 if re.search(r'\bORDER BY\b', query, re.IGNORECASE) else 0
    operations["GROUP BY(1ou 0)"] = 1 if re.search(r'\bGROUP BY\b', query, re.IGNORECASE) else 0
    operations["LIMIT/OFFSET(1ou 0)"] = 1 if re.search(r'\bLIMIT\b|\bOFFSET\b', query, re.IGNORECASE) else 0

    return [operations[k] for k in keys]

# Fonction process_sparql_queries reste inchangée

def process_sparql_queries(input_filename, output_filename):
    results = []
    results2 = []
    
    with open(input_filename, 'r') as f:
        queries = f.read().split("#EOQ#")
        nb_queries = len(queries)
        for query in queries:
            query = query.strip()
            if query:
                operation_vector = analyse_operations(query)
                results.append([query] + operation_vector)
                results2.append(operation_vector)

    os.makedirs("generated_files", exist_ok=True)
    output_filepath = os.path.join("generated_files", output_filename)
    

    with open(output_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = ['Requête', 'SELECT(n)', 'SELECTION', 'JOIN(n)', 
                   'FILTER(1ou 0)', 'UNION(n ou 0)', 'ORDER BY(1ou 0)', 
                   'GROUP BY(1ou 0)', 'LIMIT/OFFSET(1ou 0)']
        writer.writerow(headers)
        writer.writerows(results)

    

    print(f"Les résultats ont été enregistrés dans le fichier : {output_filename}")


# Chemins des fichiers et exécution
input_filename = '/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q'
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f'query_vector_watdiv_{timestamp}.csv'


process_sparql_queries(input_filename, output_filename)