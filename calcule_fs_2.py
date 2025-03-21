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
    except Exception as e:
        print(f"Erreur: {e}")
        return

    q_file_path = '/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q'
    output_file = "resultats.csv"

    try:
        with open(q_file_path, "r", encoding="utf-8") as f:
            queries = f.read().split("#EOQ#")
    except FileNotFoundError:
        print(f"Fichier introuvable: {q_file_path}")
        return

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Query", "nb_Selections", "Selectivity"])
        writer.writeheader()

        for query in queries:
            query = query.strip()
            if not query:
                continue
            
            prefixes = extract_prefixes(query)
            where_content, _, _ = extract_where_clause(query)
            if not where_content:
                continue

            triple_re = re.compile(
                r'(?P<subject>\?[^\s]+|[\w:.-]+|<[^>]+>|"[^"]*"|\'[^\']*\')\s+'
                r'(?P<predicate>\?[^\s]+|[\w:.-]+|<[^>]+>|"[^"]*"|\'[^\']*\')\s+'
                r'(?P<object>\?[^\s]+|[\w:.-]+|<[^>]+>|"[^"]*"|\'[^\']*\')\s*\.',
                re.IGNORECASE
            )

            selectivities = []
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

            if selectivities:
                writer.writerow({
                    "Query": query,
                    "nb_Selections": len(selectivities),
                    "Selectivity": f"<{', '.join(map(str, selectivities))}>"
                })

if __name__ == "__main__":
    main()