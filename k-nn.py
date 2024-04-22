from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np

from connect_db import get_data

X, y = get_data()
X = np.array(X)

name_encoder = OneHotEncoder()
name_encoded = name_encoder.fit_transform(X[:, 1].reshape(-1, 1)).toarray()

price_scaler = StandardScaler()
price_scaled = price_scaler.fit_transform(X[:, 2].reshape(-1, 1))


X_encoded = np.concatenate((name_encoded, price_scaled), axis=1)

print(X_encoded)
