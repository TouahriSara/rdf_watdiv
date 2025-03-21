import csv
import re
from SPARQLWrapper import SPARQLWrapper, JSON

def extract_prefixes(query):
    prefix_lines = []
    lines = query.split('\n')
    for line in lines:
        line_clean = line.strip()
        if line_clean.upper().startswith(('PREFIX ', 'BASE ')):
            prefix_lines.append(line_clean)
    return '\n'.join(prefix_lines)

def extract_where_clause(query):
    query_lower = query.lower()
    where_start = query_lower.find("where")
    if where_start == -1:
        return ("", -1, -1)
    
    brace_start = query.find("{", where_start)
    if brace_start == -1:
        return ("", -1, -1)
    
    depth = 1
    in_string = False
    start = brace_start + 1
    end_pos = -1
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
                    end_pos = i
                    break
    return (query[start:end_pos].strip(), brace_start, end_pos) if end_pos != -1 else (query[brace_start+1:].strip(), brace_start, len(query))

def is_selection_triple(subj, pred, obj):
    def is_variable(term):
        term = term.strip()
        return term.startswith(('?', '$'))
    
    variable_count = sum([
        is_variable(subj),
        is_variable(pred),
        is_variable(obj)
    ])
    
    return variable_count <= 1

def create_count_query(prefixes, triple):
    return f"{prefixes}\nSELECT (COUNT(*) AS ?count) WHERE {{ {triple} }}"

def run_count(sparql, count_query):
    sparql.setQuery(count_query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return int(results["results"]["bindings"][0]["count"]["value"])
    except:
        return 0

def get_total_triples(sparql):
    sparql.setQuery("SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return int(results["results"]["bindings"][0]["count"]["value"])

def main():
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    
    try:
        total_triples = get_total_triples(sparql)
        print(f"Total triples in dataset: {total_triples}")
    except Exception as e:
        print(f"Erreur lors de la récupération du nombre total de triples: {e}")
        return

    q_file_path = '/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q'
    output_file = "resultats_final.csv"

    try:
        with open(q_file_path, "r", encoding="utf-8") as f:
            file_content = f.read().strip()
            queries = [q.strip() for q in file_content.split("#EOQ#") if q.strip()]
            print(f"Nombre total de requêtes détectées: {len(queries)}")
    except FileNotFoundError:
        print(f"Fichier introuvable: {q_file_path}")
        return

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "Query_ID",
            "Original_Query",
            "nb_Selections",
            "Selectivities",
            "Total_Triples",
            "Query_Status"
        ])
        writer.writeheader()

        stats = {
            "processed": 0,
            "skipped_no_where": 0,
            "valid": 0,
            "errors": 0
        }

        for idx, query in enumerate(queries, 1):
            try:
                if not query:
                    stats["skipped_no_where"] += 1
                    continue

                stats["processed"] += 1
                print(f"\nTraitement requête {idx}/{len(queries)}")

                prefixes = extract_prefixes(query)
                where_content, _, _ = extract_where_clause(query)

                if not where_content:
                    stats["skipped_no_where"] += 1
                    writer.writerow({
                        "Query_ID": idx,
                        "Original_Query": query,
                        "Query_Status": "SKIPPED (NO WHERE CLAUSE)"
                    })
                    continue

                stats["valid"] += 1
                triple_re = re.compile(
                    r'(?P<subject>\?[^\s]+|[\w:.-]+|<[^>]+>|"[^"]*"|\'[^\']*\')\s+'
                    r'(?P<predicate>\?[^\s]+|[\w:.-]+|<[^>]+>|"[^"]*"|\'[^\']*\')\s+'
                    r'(?P<object>\?[^\s]+|[\w:.-]+|<[^>]+>|"[^"]*"|\'[^\']*\')\s*\.',
                    re.IGNORECASE
                )

                selectivities = []
                counts = []

                for match in triple_re.finditer(where_content):
                    subj = match.group('subject')
                    pred = match.group('predicate')
                    obj = match.group('object')
                    triple = f"{subj} {pred} {obj}."

                    if not is_selection_triple(subj, pred, obj):
                        continue

                    count = run_count(sparql, create_count_query(prefixes, triple))
                    selectivity = count / total_triples if total_triples else 0
                    selectivities.append(round(selectivity, 4))
                    counts.append(count)

                writer.writerow({
                    "Query_ID": idx,
                    "Original_Query": query,
                    "nb_Selections": len(selectivities),
                    "Selectivities": f"<{', '.join(map(str, selectivities))}>" if selectivities else "NONE",
                    
                })

            except Exception as e:
                stats["errors"] += 1
                print(f"Erreur lors du traitement de la requête {idx}: {str(e)}")
                writer.writerow({
                    "Query_ID": idx,
                    "Original_Query": query,
                    "Query_Status": f"ERROR: {str(e)}"
                })

        print("\n" + "="*50)
        print(f"Statistiques finales :")
        print(f"Requêtes totales : {len(queries)}")
        print(f"Requêtes traitées : {stats['processed']}")
        print(f"Requêtes valides : {stats['valid']}")
        print(f"Requêtes ignorées (sans WHERE) : {stats['skipped_no_where']}")
        print(f"Erreurs rencontrées : {stats['errors']}")
        print("="*50)

if __name__ == "__main__":
    main()