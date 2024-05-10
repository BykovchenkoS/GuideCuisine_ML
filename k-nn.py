import pandas as pd
import numpy as np
import random
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from connect_db import record_id, user_cuisines, user_types, user_price, insert_similar_ids

NUMBER_OF_NEIGHBORS = 3  # It influences the number of best IDs
NUMBER_OF_PCA = 2


def one_hot_encoding(categories, values):
    encoded_values = np.zeros(len(categories))
    for value in values.split(','):
        encoded_values[int(value) - 1] = 1
    return encoded_values.tolist()


def transform_price(price):
    if price == '0':
        return str(random.uniform(0.2, 0.8))
    elif price == '1':
        return '0'
    elif price == '2':
        return '0.5'
    elif price == '3':
        return '1'
    else:
        return None


user_cuisines = str(user_cuisines)
user_types = str(user_types)
user_price = str(user_price)

encoded_cuisines = one_hot_encoding(range(1, 13), user_cuisines)
encoded_types = one_hot_encoding(range(1, 9), user_types)
transformed_price = transform_price(user_price)

user_data = [record_id] + encoded_cuisines + encoded_types + [transformed_price] + [0]

data = pd.read_csv("data.csv")
features = data.drop(columns=["id", "label_suitability"])

knn = NearestNeighbors(n_neighbors=NUMBER_OF_NEIGHBORS)
knn.fit(features)

new_data = np.array([user_data])

distances, indices = knn.kneighbors(new_data)

similar_ids = ','.join(map(str, data.iloc[indices[0]]['id'].values))

print("Best:", similar_ids)
print("Расстояния до ближайших соседей:", ', '.join(map(str, distances[0])))

insert_similar_ids(record_id, similar_ids)

pca = PCA(n_components=NUMBER_OF_PCA)
features_2d = pca.fit_transform(features)

plt.figure(figsize=(8, 6))
plt.scatter(features_2d[:, 0], features_2d[:, 1], alpha=0.5)

for i, txt in enumerate(data['id']):
    if txt in similar_ids:
        plt.scatter(features_2d[i, 0], features_2d[i, 1], color='red')

for i, txt in enumerate(data['id']):
    plt.annotate(txt, (features_2d[i, 0], features_2d[i, 1]), fontsize=12)

plt.title('PCA')
plt.xlabel('C 1')
plt.ylabel('C 2')
plt.legend()
plt.show()
