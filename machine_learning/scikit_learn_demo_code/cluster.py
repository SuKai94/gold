# -*- coding: utf-8 -*-

'''
Unsupervised Learning: Clustering.
'''

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import adjusted_rand_score

X, y = make_blobs(random_state=42)
'''
There are clearly three separate groups of points in the data..
Even if the groups are obvious in the data, it is hard to find them when the data lives in a high-dimensional space.
'''
# plt.scatter(X[:,0], X[:,1])
# plt.show()
kmeans = KMeans(n_clusters=3, random_state=42)
'''
the result contains the ID of the cluster that each point is assigned to.
'''
labels = kmeans.fit_predict(X)
# print labels
# print np.all(labels==kmeans.labels_)
# plt.scatter(X[:,0], X[:,1], c=labels)
# plt.show()

'''
A more quantitative evalution.
How about we compare our cluster labels with the ground truth we got when generating the blobs?
'''
# print (accuracy_score(y, labels))
# print (confusion_matrix(y, labels))
# print (np.mean(y == labels))

'''
Even though we recovered the partitioning of the data into clusters perfectly.
The cluster IDs we assigned were arbitrary.
And we can not hope to recover them.
Therefore, we must use a different scoring metric, such as adjusted_rand_score,
which is invariant to permutations of the labels:
'''
# print adjusted_rand_score(y, labels)
'''
In general, there is no guarantee that structure found by a clustering algorithm has anything to do with what you were interested in.
We can easily create a dataset that has non-isotropic clusters, on which kmeans will fail:
'''
XX, yy = make_blobs(random_state=60, n_samples=600)
rng = np.random.RandomState(74)
transformation = rng.normal(size=(2, 2))
XX = np.dot(XX, transformation)

y_pred = KMeans(n_clusters=3).fit_predict(XX)

plt.scatter(XX[:, 0], XX[:, 1], c=y_pred)
plt.show()