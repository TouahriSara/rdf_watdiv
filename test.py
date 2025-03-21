import csv
import re
from datetime import datetime
import os

def extract_where_clause(query):
    """Extrait correctement la clause WHERE même avec des sous-requêtes imbriquées"""
    query_lower = query.lower()
    where_start = query_lower.find("where")
    if where_start == -1:
        return ""
    
    # Trouver la position de la première accolade après WHERE
    brace_start = query.find("{", where_start)
    if brace_start == -1:
        return ""
    
    depth = 1
    in_string = False
    for i in range(brace_start + 1, len(query)):
        c = query[i]
        
        if c in ['"', "'"]:
            in_string = not in_string
            
        if not in_string:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return query[brace_start+1:i].strip()
    
    return query[brace_start+1:].strip()

def analyse_operations(query):
    keys = ["SELECT(n)", "SELECTION", "JOIN(n)", "FILTER(1ou 0)", 
            "UNION(n ou 0)", "ORDER BY(1ou 0)", "GROUP BY(1ou 0)", "LIMIT/OFFSET(1ou 0)"]
    operations = {key: 0 for key in keys}

    # Analyse SELECT
    select_match = re.search(r'\bSELECT\s+([^}]+?)\s+WHERE', query, re.IGNORECASE | re.DOTALL)
    if select_match:
        operations["SELECT(n)"] = len([v for v in select_match.group(1).split() if v.startswith('?')])

    # Analyse WHERE avec gestion des sous-requêtes
    where_content = extract_where_clause(query)
    if where_content:
        triple_pattern = re.compile(
            r'(?P<subject>\?[^\s]+|<[^>]+>|".*?")\s+'
            r'(?P<predicate><[^>]+>)\s+'
            r'(?P<object>\?[^\s]+|<[^>]+>|".*?")'
        )
        triples = triple_pattern.finditer(where_content)
        
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

def process_sparql_queries(input_filename, output_filename):
    results = []
    
    with open(input_filename, 'r') as f:
        query_blocks = f.read().split("#EOQ#")
        
        for block in query_blocks:
            block = block.strip()
            if not block:
                continue
                
            # Extraction de la méthode
            method_match = re.search(r'#\s*Méthode\s+(\d+)', block, re.IGNORECASE)
            method = method_match.group(1) if method_match else 'Inconnu'
            
            # Extraction de la requête nettoyée
            query = re.sub(r'^\s*#.*?$', '', block, flags=re.MULTILINE).strip()
            
            # Analyse des opérations
            operation_vector = analyse_operations(query)
            
            # Ajout du résultat avec la méthode
            results.append([method, query] + operation_vector)

    os.makedirs("generated_files", exist_ok=True)
    output_filepath = os.path.join("generated_files", output_filename)
    
    with open(output_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = ['Méthode', 'Requête', 'SELECT(n)', 'SELECTION', 'JOIN(n)', 
                   'FILTER(1ou 0)', 'UNION(n ou 0)', 'ORDER BY(1ou 0)', 
                   'GROUP BY(1ou 0)', 'LIMIT/OFFSET(1ou 0)']
        writer.writerow(headers)
        writer.writerows(results)

    print(f"Résultats enregistrés dans : {output_filepath}")

# Exécution
input_filename = '/home/adminlias/data/PFE /generated_files/max_queries_wv1_reorganized.q'
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f'query_vector_watdiv_{timestamp}.csv'

process_sparql_queries(input_filename, output_filename)