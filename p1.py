import pandas as pd
import re

# Charger le fichier CSV d'entrée
input_file = "/home/adminlias/Downloads/power_log_LUBM_virtuoso_withbuffer_20250312_095432.csv"
df = pd.read_csv(input_file)

# Fonction pour analyser les requêtes SPARQL et extraire les caractéristiques
def parse_query(query):
    # Initialiser les variables pour chaque clause
    jointure = "JOIN" if "JOIN" in query.upper() else "NO_JOIN"
    selection = "SELECT" if "SELECT" in query.upper() else "NO_SELECT"
    projection = "PROJECTION" if "?" in query else "NO_PROJECTION"
    filter_n = len(re.findall(r"FILTER", query, re.IGNORECASE))
    union_n = len(re.findall(r"UNION", query, re.IGNORECASE))
    order_by_n = len(re.findall(r"ORDER BY", query, re.IGNORECASE))
    group_by_n = len(re.findall(r"GROUP BY", query, re.IGNORECASE))
    limit_offset_n = len(re.findall(r"(LIMIT|OFFSET)", query, re.IGNORECASE))
    
    return {
        "JOINTURE": jointure,
        "SELECETION": selection,
        "PROJECTION": projection,
        "FILTER_n": filter_n,
        "UNION_n": union_n,
        "ORDER_BY_n": order_by_n,
        "GROUP_BY_n": group_by_n,
        "LIMIT_OFFSET_n": limit_offset_n
    }

# Appliquer la fonction d'analyse à chaque requête
parsed_data = df['query'].apply(parse_query)

# Créer un DataFrame à partir des données analysées
parsed_df = pd.DataFrame(parsed_data.tolist())

# Fusionner les données analysées avec le DataFrame original
df = pd.concat([df, parsed_df], axis=1)

# Regrouper les données par les colonnes spécifiées et calculer les agrégations
grouped_df = df.groupby(
    ["JOINTURE", "SELECETION", "PROJECTION", "FILTER_n", "UNION_n", "ORDER_BY_n", "GROUP_BY_n", "LIMIT_OFFSET_n"]
).agg({
    "energy_consumed_J": ["count", "mean", "max"],
    "execution_time_s": "mean"
}).reset_index()

# Renommer les colonnes pour correspondre à la sortie demandée
grouped_df.columns = [
    "JOINTURE", "SELECETION", "PROJECTION", "FILTER_n", "UNION_n", "ORDER_BY_n", "GROUP_BY_n", "LIMIT_OFFSET_n",
    "COUNT(*)", "AVG(energy_consumed_J)", "MAX(energy_consumed_J)", "AVG(execution_time_s)"
]

# Sauvegarder le résultat dans un fichier CSV de sortie
output_file = "query_metrics_wv1_output.csv"
grouped_df.to_csv(output_file, index=False)

print(f"Le fichier de sortie a été généré : {output_file}")