# -*- coding: utf-8 -*-

'''
Supervised Learning - Regression
linear_regression
'''

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression

def plot_2d_separator(classifier, X, fill=False, ax=None, eps=None):
    if eps is None:
        eps = X.std() / 2.
    x_min, x_max = X[:, 0].min() - eps, X[:, 0].max() + eps
    y_min, y_max = X[:, 1].min() - eps, X[:, 1].max() + eps
    xx = np.linspace(x_min, x_max, 100)
    yy = np.linspace(y_min, y_max, 100)

    X1, X2 = np.meshgrid(xx, yy)
    X_grid = np.c_[X1.ravel(), X2.ravel()]
    try:
        decision_values = classifier.decision_function(X_grid)
        levels = [0]
        fill_levels = [decision_values.min(), 0, decision_values.max()]
    except AttributeError:
        # no decision_function
        decision_values = classifier.predict_proba(X_grid)[:, 1]
        levels = [.5]
        fill_levels = [0, .5, 1]

    if ax is None:
        ax = plt.gca()
    if fill:
        ax.contourf(X1, X2, decision_values.reshape(X1.shape),
                    levels=fill_levels, colors=['blue', 'red'])
    else:
        ax.contour(X1, X2, decision_values.reshape(X1.shape), levels=levels,
                   colors="black")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(())
    ax.set_yticks(())

'''
create a dataset out of a sinus curve with some noise
'''
x = np.linspace(-3,3,100)
# print (x)
'''
RandomState is a pseudorandom number generator.
The parameter you pass to RandomState is the seed for generator,
which specifies the starting point for a sequence of pseudorandom numbers.
The uniform() method returns a pseudorandom number between zero and one.

'''
rng = np.random.RandomState(42)
y = np.sin(4*x) + x + rng.uniform(size=len(x))
# plt.plot(x, y, 'o')
# plt.show()

X = x[:,np.newaxis]
# print (x.shape)
# print (X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred_train = regressor.predict(X_train)
# plt.plot(X_train, y_train, 'o', label="data")
# plt.plot(X_train, y_pred_train, 'o', label="prediction")
# plt.legend(loc="best")
# plt.show()
y_pred_test = regressor.predict(X_test)
print regressor.score(X_test, y_test)
