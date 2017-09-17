# -*- coding: utf-8 -*-

import numpy as np


class KMeansClassifier():

    def __init__(self, k, initCent='random', max_iter=500):

        self._k = k
        self._initCent = initCent
        self._max_iter = max_iter
        self._clusterAssment = None
        self._labels = None
        self._sse = None

    def _calEDist(self, arrA, arrB):
        return np.math.sqrt(sum(np.power(arrA - arrB, 2)))

    def _calMDist(self, arrA, arrB):
        return sum(np.abs(arrA - arrB))

    def _randCent(self, data_X, k):
        n = data_X.shape[1]
        centroids = np.empty((k, n))
        # print(data_X)
        for j in range(n):
            minJ = min(data_X[:, j])
            rangeJ = float(max(data_X[:, j] - minJ))
            centroids[:, j] = (minJ + rangeJ * np.random.rand(k, 1)).flatten()
        return centroids

    def fit(self, data_X,data_od):
        if not isinstance(data_X, np.ndarray) or \
                isinstance(data_X, np.matrixlib.defmatrix.matrix):
            try:
                data_X = np.asarray(data_X)
            except:
                raise TypeError("numpy.ndarray resuired for data_X")

        m = data_X.shape[0]
        self._clusterAssment = np.zeros((m, 2))

        if self._initCent == 'random':
            self._centroids = self._randCent(data_X, self._k)
        clusterChanged = True
        for _ in range(self._max_iter):
            # print (_)
            centerod = [4000 for i in range(self._k)]
            clusterChanged = False
            for i in range(m):
                minDist = np.inf
                minIndex = -1
                for j in range(self._k):
                    arrA = self._centroids[j, :]
                    arrB = data_X[i, :]
                    distJI = self._calEDist(arrA, arrB)
                    if distJI < minDist and centerod[j] - data_od[i][0] > 0:
                        minDist = distJI
                        minIndex = j
                        # centerod[j] -= data_od[i][0]
                centerod[minIndex] -= data_od[i][0]
                if self._clusterAssment[i, 0] != minIndex:
                    clusterChanged = True
                    self._clusterAssment[i, :] = minIndex, minDist ** 2
            if not clusterChanged:
                break
            for i in range(self._k):
                index_all = self._clusterAssment[:, 0]
                value = np.nonzero(index_all == i)
                ptsInClust = data_X[value[0]]
                self._centroids[i, :] = np.mean(ptsInClust, axis=0)

        self._labels = self._clusterAssment[:, 0]
        self._sse = sum(self._clusterAssment[:, 1])

    def predict(self, X):
        if not isinstance(X, np.ndarray):
            try:
                X = np.asarray(X)
            except:
                raise TypeError("numpy.ndarray required for X")

        m = X.shape[0]
        preds = np.empty((m,))
        for i in range(m):
            minDist = np.inf
            for j in range(self._k):
                distJI = self._calEDist(self._centroids[j, :], X[i, :])
                if distJI < minDist:
                    minDist = distJI
                    preds[i] = j
        return preds
