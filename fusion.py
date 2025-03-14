import csv
import os

# Noms de fichiers d'entrée et de sortie
powerlog_file = "/home/adminlias/data/PFE /generated_files/power_log_watdiv_virtuoso_withbuffer_20250311_170521.csv"  # Contient : query, execution_time_s, puissance_moyenne_W, energy_consumed_J
stats_file = "/home/adminlias/data/PFE /generated_files/query_vector_watdiv_20250313_162737.csv"          # Contient : Requête, SELECT(n), JOIN(n), FILTER(1ou 0), UNION(n ou 0), ORDER BY(1ou 0), GROUP BY(1ou 0), LIMIT/OFFSET(1ou 0)
output_filename = "merged_watdiv_virtuoso_withbuffer_2.csv"           # Fichier final à générer

# Vérifier que les fichiers existent
for file in [powerlog_file, stats_file]:
    if not os.path.isfile(file):
        print(f"Erreur : Le fichier {file} n'existe pas.")
        exit(1)

# Lecture des deux fichiers CSV
with open(powerlog_file, newline="", encoding="utf-8") as f1, open(stats_file, newline="", encoding="utf-8") as f2:
    reader1 = csv.DictReader(f1)
    reader2 = csv.DictReader(f2)
    powerlog_rows = list(reader1)
    stats_rows = list(reader2)

# Vérifier que le nombre de lignes est identique
if len(powerlog_rows) != len(stats_rows):
    print("Erreur : Les fichiers n'ont pas le même nombre de lignes.")
    exit(1)

# Fusion ligne par ligne
merged_rows = []
for pl_row, st_row in zip(powerlog_rows, stats_rows):
    merged_row = {
        "Requête": st_row["Requête"],                    # Requête complète provenant du fichier statistiques
        "execution_time_s": pl_row["execution_time_s"],   # Valeurs provenant du fichier powerlog
        "puissance_moyenne_W": pl_row["puissance_moyenne_W"],
        "energy_consumed_J": pl_row["energy_consumed_J"],
        "SELECT(n)": st_row["SELECT(n)"],
        "SELECTION": st_row["SELECTION"],
        "JOIN(n)": st_row["JOIN(n)"],
        "FILTER(1ou 0)": st_row["FILTER(1ou 0)"],
        "UNION(n ou 0)": st_row["UNION(n ou 0)"],
        "ORDER BY(1ou 0)": st_row["ORDER BY(1ou 0)"],
        "GROUP BY(1ou 0)": st_row["GROUP BY(1ou 0)"],
        "LIMIT/OFFSET(1ou 0)": st_row["LIMIT/OFFSET(1ou 0)"],
    }
    merged_rows.append(merged_row)

# Écriture du fichier CSV final
fieldnames = [
    "Requête",
    "execution_time_s",
    "puissance_moyenne_W",
    "energy_consumed_J",
    "SELECT(n)",
    "SELECTION",
    "JOIN(n)",
    "FILTER(1ou 0)",
    "UNION(n ou 0)",
    "ORDER BY(1ou 0)",
    "GROUP BY(1ou 0)",
    "LIMIT/OFFSET(1ou 0)"
]
 # Création du répertoire "generated_files" s'il n'existe pas
os.makedirs("generated_files", exist_ok=True)

# Définition des chemins de sortie des fichiers
output_filepath = os.path.join("generated_files", output_filename)
with open(output_filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_rows)

print(f"Fichier fusionné créé : {output_filename} ({len(merged_rows)} lignes)")
