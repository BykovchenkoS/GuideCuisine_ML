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

# Открытие файла CSV для записи
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Запись заголовков столбцов
    writer.writerow(
        ['id', 'price', 'type_1', 'type_2', 'type_3', 'type_4', 'type_5', 'type_6', 'type_7', 'type_8', 'type_9',
         'cuisine_1', 'cuisine_2', 'cuisine_3', 'cuisine_4', 'cuisine_5', 'cuisine_6', 'cuisine_7', 'cuisine_8',
         'cuisine_9', 'cuisine_10', 'cuisine_11', 'cuisine_12', 'cuisine_13', 'label_suitability'])

    # Запись данных
    writer.writerows(X)

with open(output_file, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['label_suitability'])
    writer.writerows([[label] for label in y])
#
# data = pd.read_csv('data.csv')
# X = data.drop(['id'], axis=1)
# y = data['label_suitability']
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=42, random_state=42)
#
# scaler = MinMaxScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)
#
# k = 5
# knn = KNeighborsClassifier(n_neighbors=k)
# knn.fit(X_train_scaled, y_train)
#
# y_pred = knn.predict(X_test_scaled)
#
# print("cheto:", y_pred)