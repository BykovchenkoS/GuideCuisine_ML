import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

#Config
NUMBER_OF_CLUSTERS = 3 #Max - number of data lines (companies)
NUMBER_OF_NEIGHBORS = 5 #It influence on number of best IDs
NUMBER_OF_PCA = 2

#New
user_data = [0.10,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]

#Learning
data = pd.read_csv("data.csv")
features = data.drop(columns=["id", "label_suitability"])

num_clusters = NUMBER_OF_CLUSTERS 
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(features)

knn = NearestNeighbors(n_neighbors=NUMBER_OF_NEIGHBORS)  
knn.fit(features)

new_data = np.array([user_data]) 
distances, indices = knn.kneighbors(new_data)

similar_ids = []
for i in indices[0]:
    similar_ids.append(data.iloc[i]['id'])

print("Best:", similar_ids[:10])

# Reduce the feature dimensionality to 2 for visualization
pca = PCA(n_components=NUMBER_OF_PCA)
features_2d = pca.fit_transform(features)

# Plot the clusters
plt.figure(figsize=(8, 6))

# Plot all points
plt.scatter(features_2d[:, 0], features_2d[:, 1], c=kmeans.labels_, cmap='viridis', alpha=0.5)

# Plot points from similar_ids[:10] with a different color
for i, txt in enumerate(data['id']):
    if txt in similar_ids[:10]:
        plt.scatter(features_2d[i, 0], features_2d[i, 1], color='red', label='Best')

# Annotate each point with its id
for i, txt in enumerate(data['id']):
    plt.annotate(txt, (features_2d[i, 0], features_2d[i, 1]), fontsize=8)

plt.colorbar(label='Cluster')
plt.title('Clusters Visualization (PCA)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.show()