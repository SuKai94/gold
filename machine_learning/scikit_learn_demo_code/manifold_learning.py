# -*- coding: utf-8 -*-

'''
Unsupervised Learning: Manifold Learning.
One weakness of PCA is that it cannot detect non-linear features.
Manifold Learning have been developed to address this deficiency.
'''

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_s_curve
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap
from mpl_toolkits.mplot3d import Axes3D

X, y = make_s_curve(n_samples=1000)
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(X[:,0], X[:,1], X[:,2], c=y)
# ax.view_init(10, -60)
# plt.show()

# X_pca = PCA(n_components=2).fit_transform(X)
# plt.scatter(X_pca[:,0], X_pca[:,1], c=y)
# plt.show()

iso = Isomap(n_neighbors=15, n_components=2)
X_iso = iso.fit_transform(X)
plt.scatter(X_iso[:,0], X_iso[:,1], c=y)
plt.show()