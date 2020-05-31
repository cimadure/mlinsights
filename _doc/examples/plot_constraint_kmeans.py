"""
=================
Constraint KMeans
=================

Simple example to show how to cluster keeping
approximatively the same number of points in every
cluster.

.. contents::
    :local:

Data
====
"""
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from mlinsights.mlmodel import ConstraintKMeans


n_samples = 100
data = make_blobs(n_samples=n_samples, n_features=2, centers=2, cluster_std=1.0,
                  center_box=(-10.0, 0.0), shuffle=True, random_state=2)
X1 = data[0]
data = make_blobs(n_samples=n_samples // 2, n_features=2, centers=2, cluster_std=1.0,
                  center_box=(0.0, 10.0), shuffle=True, random_state=2)
X2 = data[0]

import numpy
X = numpy.vstack([X1, X2])
X.shape

###############################
# Plots.

fig, ax = plt.subplots(1, 1, figsize=(4, 4))
ax.plot(X[:, 0], X[:, 1], '.')
ax.set_title('4 clusters')

###############################
# Standard KMeans
# ===============

km = KMeans(n_clusters=4)
km.fit(X)
cl = km.predict(X)
hist = Counter(cl)

colors = 'brgy'
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
for i in range(0, max(cl) + 1):
    ax.plot(X[cl == i, 0], X[cl == i, 1], colors[i] + '.', label='cl%d' % i)
    x = [km.cluster_centers_[i, 0], km.cluster_centers_[i, 0]]
    y = [km.cluster_centers_[i, 1], km.cluster_centers_[i, 1]]
    ax.plot(x, y, colors[i] + '+')
ax.set_title('KMeans 4 clusters\n%r' % hist)
ax.legend()

#####################################
# Constraint KMeans
# =================

km = ConstraintKMeans(n_clusters=4, balanced_predictions=True)
km.fit(X)


##########################
# This algorithm tries to exchange points
# between clusters following
# `Same-size k-Means Variation
# <https://elki-project.github.io/tutorial/same-size_k_means>`_.

cl = km.predict(X)
hist = Counter(cl)

fig, ax = plt.subplots(1, 1, figsize=(4, 4))
for i in range(0, max(cl) + 1):
    ax.plot(X[cl == i, 0], X[cl == i, 1], colors[i] + '.', label='cl%d' % i)
    x = [km.cluster_centers_[i, 0], km.cluster_centers_[i, 0]]
    y = [km.cluster_centers_[i, 1], km.cluster_centers_[i, 1]]
    ax.plot(x, y, colors[i] + '+')
ax.set_title('ConstraintKMeans 4 clusters\n%r' % hist)
ax.legend()


##########################
# Another algorithm tries to extend the area of attraction of
# each cluster.

km = ConstraintKMeans(n_clusters=4, strategy='weights', max_iter=1000,
                      history=True)
km.fit(X)

cl = km.predict(X)
hist = Counter(cl)

################################
# Let's plot Delaunay edges as well.


def plot_delaunay(ax, edges, points):
    for a, b in edges:
        ax.plot(points[[a, b], 0], points[[a, b], 1], '--', color="#555555")


edges = km.cluster_edges()


fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for i in range(0, max(cl) + 1):
    ax[0].plot(X[cl == i, 0], X[cl == i, 1], colors[i] + '.', label='cl%d' % i)
    x = [km.cluster_centers_[i, 0], km.cluster_centers_[i, 0]]
    y = [km.cluster_centers_[i, 1], km.cluster_centers_[i, 1]]
    ax[0].plot(x, y, colors[i] + '+')
ax[0].set_title("ConstraintKMeans 4 clusters\nstrategy='weights'\n%r" % hist)
ax[0].legend()

cls = km.cluster_centers_iter_
ax[1].plot(X[:, 0], X[:, 1], '.', label='X', color='#AAAAAA', ms=3)
for i in range(0, max(cl) + 1):
    ms = numpy.arange(
        cls.shape[-1]).astype(numpy.float64) / cls.shape[-1] * 50 + 1
    ax[1].scatter(cls[i, 0, :], cls[i, 1, :],
                  color=colors[i], s=ms, label='cl%d' % i)
    plot_delaunay(ax[1], edges, km.cluster_centers_)
ax[1].set_title("Centers movement")

plt.show()
