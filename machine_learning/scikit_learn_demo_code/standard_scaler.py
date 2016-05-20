# -*- coding: utf-8 -*-

'''
Unsupervised Learning:
StandardScaler
'''

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X, y = iris.data, iris.target
# print (X.shape)
print ("mean: %s" % X.mean(axis=0))
print ("standard deviation: %s" % X.std(axis=0))

'''
To use a preprocessing method, we first import the estimator,
here StandardScaler and instantiate it.
'''
scaler = StandardScaler()
'''
As with the classification and regression algorithms,
we call fit to learn the model from the data.
As this is an unsupervised model, we only pass X, not y.
'''
scaler.fit(X)
# rescale our data by applying the transform method
X_scaled = scaler.transform(X)
'''
X_scale has the same number of samples and features
but the mean was subtracted and all features were scaled to have unit standard deviation.
'''
print (X_scaled.shape)
print ("mean: %s" % X_scaled.mean(axis=0))
print ("standard deviation: %s" % X_scaled.std(axis=0))
