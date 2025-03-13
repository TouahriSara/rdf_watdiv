import re
from datetime import datetime

def sparql_to_sql(sparql_query):
    # Extraction des variables SELECT
    select_match = re.search(r'SELECT\s+(.*?)\s+WHERE', sparql_query, re.IGNORECASE | re.DOTALL)
    if not select_match:
        raise ValueError("Invalid SPARQL query: SELECT clause not found")
    select_vars = [v.strip('?') for v in select_match.group(1).split()]

    # Extraction de la clause WHERE
    where_match = re.search(r'WHERE\s*{([^}]*)}', sparql_query, re.IGNORECASE | re.DOTALL)
    if not where_match:
        raise ValueError("Invalid SPARQL query: WHERE clause not found")
    where_clause = where_match.group(1).strip()

    # Récupération des triple patterns ligne par ligne
    patterns = []
    for line in where_clause.splitlines():
        line = line.strip()
        if not line or line.startswith("FILTER"):
            continue
        # Suppression du point final s'il est présent
        if line.endswith('.'):
            line = line[:-1].strip()
        patterns.append(line)

    # Traitement de chaque triple pattern
    tables = []
    joins = []
    conditions = []
    var_map = {}
    table_alias_counter = 1

    for pattern in patterns:
        optional = False
        if pattern.upper().startswith('OPTIONAL'):
            optional = True
            pattern = pattern[8:].strip().lstrip('{').rstrip('}').strip()

        parts = re.split(r'\s+', pattern)
        if len(parts) != 3:
            raise ValueError(f"Invalid triple pattern: {pattern}")

        subj, pred, obj = parts
        alias = f"t{table_alias_counter}"
        table_alias_counter += 1
        current_conditions = []

        if pred.startswith('?'):
            raise NotImplementedError("Variable predicates not supported")
        current_conditions.append(f"{alias}.predicate = '{pred}'")

        if subj.startswith('?'):
            var = subj[1:]
            if var in var_map:
                prev_alias, prev_col = var_map[var]
                join_condition = f"{prev_alias}.{prev_col} = {alias}.subject"
                joins.append((prev_alias, alias, join_condition))
            else:
                var_map[var] = (alias, 'subject')
        else:
            current_conditions.append(f"{alias}.subject = '{subj}'")

        if obj.startswith('?'):
            var = obj[1:]
            if var in var_map:
                prev_alias, prev_col = var_map[var]
                join_condition = f"{prev_alias}.{prev_col} = {alias}.object"
                joins.append((prev_alias, alias, join_condition))
            else:
                var_map[var] = (alias, 'object')
        else:
            current_conditions.append(f"{alias}.object = '{obj}'")

        conditions.extend(current_conditions)
        tables.append(alias)

    sql = "SELECT " + ", ".join([
        f"{var_map[v][0]}.{var_map[v][1]} AS {v}" 
        for v in select_vars
    ])

    sql += " FROM triples " + " ".join([
        f"{alias}" if i == 0 else f"JOIN triples {alias}"
        for i, alias in enumerate(tables)
    ])

    join_conds = []
    for left, right, cond in joins:
        join_conds.append(f"{left} JOIN {right} ON {cond}")
    if join_conds:
        sql += " ON " + " AND ".join(join_conds)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    return sql

def process_queries(input_file, output_file):
    """
    Lit les requêtes SPARQL depuis 'input_file' séparées par le délimiteur '#EOQ#',
    les convertit en SQL, puis enregistre les résultats dans 'output_file'.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Utilisation du bon séparateur '#EOQ#'
    queries = [q.strip() for q in content.split("#EOQ#") if q.strip()]
    results = []

    for query in queries:
        try:
            sql_query = sparql_to_sql(query)
            results.append(sql_query)
        except Exception as e:
            results.append(f"-- Error processing query: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(results))

    print(f"Processed {len(queries)} queries saved to {output_file}")

# Exemple d'utilisation
if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    process_queries(
        "/home/adminlias/data/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q", 
        f"sparql_to_sql_{timestamp}.q"
    )
