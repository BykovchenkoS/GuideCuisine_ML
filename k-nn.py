import pandas as pd
import numpy as np
import random
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from connect_db import record_id, user_cuisines, user_types, user_price, insert_similar_ids, filter_similar_ids

NUMBER_OF_NEIGHBORS = 30 # It influences the number of best IDs


def one_hot_encoding(categories, values):
    encoded_values = np.zeros(len(categories))
    for value in values.split(','):
        index = int(value) - 1
        if 0 <= index < len(categories):
            encoded_values[index] = 1
        else:
            print(f"Значение {value} выходит за границы для категорий с размером {len(categories)}")
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
transformed_price = float(transform_price(user_price))

user_data = [record_id] + encoded_cuisines + encoded_types + [transformed_price] + [0]
print(user_data)

data = pd.read_csv("data.csv")
features = data.drop(columns=["id", "label_suitability"])

knn = NearestNeighbors(n_neighbors=NUMBER_OF_NEIGHBORS)
knn.fit(features)

new_data = np.array([user_data])

distances, indices = knn.kneighbors(new_data)

similar_ids_str = ','.join(map(str, data.iloc[indices[0]]['id'].values))
print("Best:", similar_ids_str)
print("Расстояния до ближайших соседей:", ', '.join(map(str, distances[0])))

filtered_result = filter_similar_ids(similar_ids_str)
print(filtered_result)
insert_similar_ids(record_id, filtered_result)


