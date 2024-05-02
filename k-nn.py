import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

#Config
NUMBER_OF_NEIGHBORS = 10 #It influence on number of best IDs
NUMBER_OF_PCA = 2
#New
user_data = [1,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0]

data = pd.read_csv("data.csv")
features = data.drop(columns=["id", "label_suitability"])

knn = NearestNeighbors(n_neighbors=NUMBER_OF_NEIGHBORS)  
knn.fit(features)

new_data = np.array([user_data]) 
distances, indices = knn.kneighbors(new_data)

similar_ids = []
for i in indices[0]:
    similar_ids.append(data.iloc[i]['id'])

print("Best:", similar_ids[:NUMBER_OF_NEIGHBORS])

pca = PCA(n_components=NUMBER_OF_PCA)
features_2d = pca.fit_transform(features)

plt.figure(figsize=(8, 6))
plt.scatter(features_2d[:, 0], features_2d[:, 1], alpha=0.5)

for i, txt in enumerate(data['id']):
    if txt in similar_ids[:NUMBER_OF_NEIGHBORS]:
        plt.scatter(features_2d[i, 0], features_2d[i, 1], color='red')

for i, txt in enumerate(data['id']):
    plt.annotate(txt, (features_2d[i, 0], features_2d[i, 1]), fontsize=12)

plt.title('PCA')
plt.xlabel('C 1')
plt.ylabel('C 2')
plt.legend()
plt.show()