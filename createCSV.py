from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
import csv
from connect_db import get_data

X, y = get_data()

scaler = MinMaxScaler()
X_normalized = scaler.fit_transform([[row[1]] for row in X])
for i, row in enumerate(X):
    row[1] = X_normalized[i][0]

output_file = 'data.csv'

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(
        ['id', 'price', 'type_1', 'type_2', 'type_3', 'type_4', 'type_5', 'type_6', 'type_7', 'type_8', 'type_9',
         'cuisine_1', 'cuisine_2', 'cuisine_3', 'cuisine_4', 'cuisine_5', 'cuisine_6', 'cuisine_7', 'cuisine_8',
         'cuisine_9', 'cuisine_10', 'cuisine_11', 'cuisine_12', 'cuisine_13', 'label_suitability'])

    for row in X:
        writer.writerow(row + [0])

with open(output_file, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
