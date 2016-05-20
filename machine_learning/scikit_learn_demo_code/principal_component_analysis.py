# -*- coding: utf-8 -*-

'''
Unsupervised Learning: Principal Component Analysis.
PCA is a technique to reduce the dimensionality of the data, by creating a linear projection.
That is, we find new features to represent the data that are a linear combination of the old data.

The way PCA finds these new directions is by looking for the directions of maximum variance.
Usually only few components that explain most of the variance in the data are kept.
'''

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

rnd = np.random.RandomState(5)
'''
Draw random samples from a normal (Gaussian) distribution.
'''
X_ = rnd.normal(size=(300,2))
X_blob = np.dot(X_, rnd.normal(size=(2,2))) + rnd.normal(size=2)
y = X_[:,0] > 0
plt.scatter(X_blob[:,0], X_blob[:,1], c=y, linewidths=0, s=30)
plt.xlabel("feature 1")
plt.ylabel("feature 2")
plt.show()

pca = PCA()
pca.fit(X_blob)
X_pca = pca.transform(X_blob)
plt.scatter(X_pca[:,0], X_pca[:,1], c=y, linewidths=0, s=30)
plt.xlabel("first principal component")
plt.ylabel("second principal component")
plt.show()