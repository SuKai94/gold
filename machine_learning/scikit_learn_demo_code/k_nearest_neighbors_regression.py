# -*- coding: utf-8 -*-

'''
Supervised Learning - Regression
KNeighborsRegression
'''

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsRegressor

'''
create a dataset out of a sinus curve with some noise
'''
x = np.linspace(-3,3,100)
# print (x)
rng = np.random.RandomState(42)
y = np.sin(4*x) + x + rng.uniform(size=len(x))
# plt.plot(x, y, 'o')
# plt.show()

X = x[:,np.newaxis]
# print (x.shape)
# print (X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
kneighbor_regression = KNeighborsRegressor(n_neighbors=3)
kneighbor_regression.fit(X_train, y_train)
y_pred_train = kneighbor_regression.predict(X_train)
plt.plot(X_train, y_train, 'o', label="data")
plt.plot(X_train, y_pred_train, 'o', label="prediction")
plt.legend(loc="best")
plt.show()
# y_pred_test = kneighbor_regression.predict(X_test)
# plt.plot(X_test, y_test, 'o', label="data")
# plt.plot(X_test, y_pred_test, 'o', label="prediction")
# plt.legend(loc="best")
# plt.show()
# print kneighbor_regression.score(X_test, y_test)