from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np
import csv
from connect_db import get_data

X, y = get_data()
X = np.array(X)

id_price = X[:, [0, 1]]
type = X[:, 2].reshape(-1, 1)
cuisine = X[:, 3].reshape(-1, 1)

type_encoder = OneHotEncoder()
cuisine_encoder = OneHotEncoder()

type_encoded = type_encoder.fit_transform(type).toarray()
cuisine_encoded = cuisine_encoder.fit_transform(cuisine).toarray()


X_encoded = np.concatenate((id_price, type_encoded, cuisine_encoded), axis=1)

output_file = 'conder.csv'

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'price',
                     'type_1', 'type_2', 'type_3', 'type_4', 'type_5', 'type_6', 'type_7', 'type_8', 'type_9',
                     'cuisine_1', 'cuisine_2', 'cuisine_3', 'cuisine_4', 'cuisine_5', 'cuisine_6',
                     'cuisine_7', 'cuisine_8', 'cuisine_9', 'cuisine_10', 'cuisine_11', 'cuisine_12', 'cuisine_13'])
    writer.writerows(X_encoded)
