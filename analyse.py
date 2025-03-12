import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# Étape 1 : Charger les données
file_path = "/home/adminlias/data/PFE /generated_files/merged_watdiv_jena.csv"
data = pd.read_csv(file_path)

# Afficher les premières lignes et informations sur les données
print(data.head())
print(data.info())

# Étape 2 : Prétraitement des données
# Gérer les valeurs manquantes
data = data.dropna()

# Encodage des variables catégoriques
categorical_columns = data.select_dtypes(include=['object']).columns
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Normalisation des données numériques
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Étape 3 : Déterminer le nombre optimal de clusters (K-Means)
inertia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

# Tracer la méthode du coude
plt.figure(figsize=(8, 5))
plt.plot(k_range, inertia, marker='o')
plt.title("Méthode du coude")
plt.xlabel("Nombre de clusters (k)")
plt.ylabel("Inertie")
plt.show()

# Étape 4 : Appliquer K-Means avec le nombre optimal de clusters
optimal_k = 4  # À ajuster selon la méthode du coude
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Ajouter les labels de cluster au DataFrame
data['Cluster'] = clusters

# Étape 5 : Visualisation des clusters avec PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

plt.figure(figsize=(10, 7))
sns.scatterplot(x=pca_data[:, 0], y=pca_data[:, 1], hue=clusters, palette='viridis', s=100)
plt.title("Visualisation des clusters avec PCA")
plt.xlabel("Composante principale 1")
plt.ylabel("Composante principale 2")
plt.show()

# Afficher les caractéristiques des clusters
print(data.groupby('Cluster').mean())