# -*- coding: utf-8 -*-

import numpy as np


class KMeansClassifier():
    "this is a k-means classifier"

    def __init__(self, k, initCent='random', max_iter=500):

        self._k = k
        self._initCent = initCent
        self._max_iter = max_iter
        self._clusterAssment = None
        self._labels = None
        self._sse = None

    def _calEDist(self, arrA, arrB):
        """
        功能：欧拉距离距离计算
        输入：两个一维数组
        """
        return np.math.sqrt(sum(np.power(arrA - arrB, 2)))

    def _calMDist(self, arrA, arrB):
        """
        功能：曼哈顿距离距离计算
        输入：两个一维数组
        """
        return sum(np.abs(arrA - arrB))

    def _randCent(self, data_X, k):
        """
        功能：随机选取k个质心
        输出：centroids #返回一个m*n的质心矩阵
        """
        n = data_X.shape[1]  # 获取特征的维数
        centroids = np.empty((k, n))  # 使用numpy生成一个k*n的矩阵，用于存储质心
        for j in range(n):
            minJ = min(data_X[:, j])
            rangeJ = float(max(data_X[:, j] - minJ))
            # 使用flatten拉平嵌套列表(nested list)
            centroids[:, j] = (minJ + rangeJ * np.random.rand(k, 1)).flatten()
        return centroids

    def fit(self, data_X):
        """
        输入：一个m*n维的矩阵
        """
        if not isinstance(data_X, np.ndarray) or \
                isinstance(data_X, np.matrixlib.defmatrix.matrix):
            try:
                data_X = np.asarray(data_X)
            except:
                raise TypeError("numpy.ndarray resuired for data_X")

        m = data_X.shape[0]  # 获取样本的个数
        # 一个m*2的二维矩阵，矩阵第一列存储样本点所属的族的索引值，
        # 第二列存储该点与所属族的质心的平方误差
        self._clusterAssment = np.zeros((m, 2))

        if self._initCent == 'random':
            self._centroids = self._randCent(data_X, self._k)

        clusterChanged = True
        for _ in range(self._max_iter):
            clusterChanged = False
            for i in range(m):
                minDist = np.inf
                minIndex = -1
                for j in range(self._k):
                    arrA = self._centroids[j, :]
                    arrB = data_X[i, :]
                    distJI = self._calEDist(arrA, arrB)
                    if distJI < minDist:
                        minDist = distJI
                        minIndex = j
                if self._clusterAssment[i, 0] != minIndex:
                    clusterChanged = True
                    self._clusterAssment[i, :] = minIndex, minDist ** 2
            if not clusterChanged:
                break
            for i in range(self._k):  # 更新质心，将每个族中的点的均值作为质心
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


class biKMeansClassifier():
    "this is a binary k-means classifier"

    def __init__(self, k=3):

        self._k = k
        self._centroids = None
        self._clusterAssment = None
        self._labels = None
        self._sse = None

    def _calEDist(self, arrA, arrB):
        """
        功能：欧拉距离距离计算
        输入：两个一维数组
        """
        return np.math.sqrt(sum(np.power(arrA - arrB, 2)))

    def fit(self, X):
        m = X.shape[0]
        self._clusterAssment = np.zeros((m, 2))
        centroid0 = np.mean(X, axis=0).tolist()
        centList = [centroid0]
        for j in range(m):
            self._clusterAssment[j, 1] = self._calEDist(np.asarray(centroid0), X[j, :]) ** 2

        while (len(centList) < self._k):
            lowestSSE = np.inf
            for i in range(len(centList)):
                index_all = self._clusterAssment[:, 0]
                value = np.nonzero(index_all == i)
                ptsInCurrCluster = X[value[0], :]
                clf = KMeansClassifier(k=2)
                clf.fit(ptsInCurrCluster)
                centroidMat, splitClustAss = clf._centroids, clf._clusterAssment
                sseSplit = sum(splitClustAss[:, 1])
                index_all = self._clusterAssment[:, 0]
                value = np.nonzero(index_all == i)
                sseNotSplit = sum(self._clusterAssment[value[0], 1])
                if (sseSplit + sseNotSplit) < lowestSSE:
                    bestCentToSplit = i
                    bestNewCents = centroidMat
                    bestClustAss = splitClustAss.copy()
                    lowestSSE = sseSplit + sseNotSplit

            bestClustAss[np.nonzero(bestClustAss[:, 0] == 1)[0], 0] = len(centList)
            bestClustAss[np.nonzero(bestClustAss[:, 0] == 0)[0], 0] = bestCentToSplit
            centList[bestCentToSplit] = bestNewCents[0, :].tolist()
            centList.append(bestNewCents[1, :].tolist())
            self._clusterAssment[np.nonzero(self._clusterAssment[:, 0] == \
                                            bestCentToSplit)[0], :] = bestClustAss

        self._labels = self._clusterAssment[:, 0]
        self._sse = sum(self._clusterAssment[:, 1])
        self._centroids = np.asarray(centList)

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