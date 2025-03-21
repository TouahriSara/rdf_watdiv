import csv
import os

# Fichiers d'entrée
powerlog_file = "/home/adminlias/data/PFE /generated_files/power_log_watdiv_virtuoso_withbuffer_20250311_170521.csv"
stats_file = "/home/adminlias/data/PFE /generated_files/query_vector_watdiv_20250320_093424.csv"
selectivity_file = "/home/adminlias/data/PFE /resultats_final.csv"  # 3ème fichier

output_filename = "merged_watdiv_virtuoso_withbuffer_3.csv"  # Sortie en CSV

# Vérification des fichiers
for file in [powerlog_file, stats_file, selectivity_file]:
    if not os.path.isfile(file):
        print(f"Erreur : Le fichier {file} n'existe pas.")
        exit(1)

# Lecture des trois fichiers
with open(powerlog_file, newline="", encoding="utf-8") as f1, \
     open(stats_file, newline="", encoding="utf-8") as f2, \
     open(selectivity_file, newline="", encoding="utf-8") as f3:

    reader1 = csv.DictReader(f1)
    reader2 = csv.DictReader(f2)
    reader3 = csv.DictReader(f3)
    
    powerlog = list(reader1)
    stats = list(reader2)
    selectivity = list(reader3)

# Vérification des tailles
if not (len(powerlog) == len(stats) == len(selectivity)):
    print("Erreur : Les fichiers n'ont pas le même nombre de lignes.")
    exit(1)

# Préparation des données fusionnées
merged_data = []
for pl, st, sel in zip(powerlog, stats, selectivity):
    merged_row = {
        "Requête": st["Requête"],
        "execution_time_s": pl["execution_time_s"],
        "puissance_moyenne_W": pl["puissance_moyenne_W"],
        "energy_consumed_J": pl["energy_consumed_J"],
        "PROJECTION": st["SELECT(n)"],
        "SELECTION": st["SELECTION"],
        "SELECTIVITE": sel["Selectivities"],  # Nouvelle colonne
        "JOINTURE": st["JOIN(n)"],
        "FILTER": st["FILTER(1ou 0)"],
        "UNION": st["UNION(n ou 0)"],
        "ORDER_BY": st["ORDER BY(1ou 0)"],
        "GROUP_BY": st["GROUP BY(1ou 0)"],
        "LIMIT_OFFSET": st["LIMIT/OFFSET(1ou 0)"]
    }
    merged_data.append(merged_row)

# Création du répertoire de sortie
os.makedirs("generated_files", exist_ok=True)
output_path = os.path.join("generated_files", output_filename)

# Écriture du CSV final
with open(output_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "Requête", "execution_time_s", "puissance_moyenne_W", "energy_consumed_J",
        "PROJECTION", "SELECTION", "SELECTIVITE", "JOINTURE", "FILTER",
        "UNION", "ORDER_BY", "GROUP_BY", "LIMIT_OFFSET"
    ]
    
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_data)

print(f"Fichier CSV généré avec succès : {output_path}")