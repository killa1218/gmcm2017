import pandas as pd
import numpy as np
import codecs
from src.kmeanscluster.kmeans import KMeansClassifier
from multiprocessing import Pool
import matplotlib.pyplot as plt
import time


def loadDataset(infile):
    df = pd.read_csv(infile, sep = '\t', header = None, dtype = str, na_filter = False)
    return np.array(df).astype(np.float)


def output(k, clf, data_X, data_od):
    outname = "../../data/kmeansresult/k_clusters_result_919" + str(k) + ".txt"
    fw = codecs.open(outname, 'w')
    cents = clf._centroids
    labels = clf._labels
    tmpcnt = 1
    for i in range(k):
        index = np.nonzero(labels == i)[0]
        x0 = data_X[index, 0]
        x1 = data_X[index, 1]
        tmpsum = 0
        for j in range(len(x0)):
            fw.write(
                str(tmpcnt) + ":" + str(cents[i, 0]) + "," + str(cents[i, 1]) + "\t" + str(index[j] + 4) + ":" + str(
                    x0[j]) + "," + str(x1[j]) + "\n")
            tmpsum += data_od[index, 0][j]
        if len(x0) != 0:
            fw.write(str(tmpcnt) + ":" + str(tmpsum) + "\n")
            tmpcnt += 1


def getkmeansresult(k, data_X, data_od):
    clf = KMeansClassifier(k)
    clf.fit(data_X, data_od)
    cents = clf._centroids
    labels = clf._labels
    flag = True
    for i in range(k):
        index = np.nonzero(labels == i)[0]
        x0 = data_X[index, 0]
        x1 = data_X[index, 1]
        y_i = i
        tmpsum = 0
        for j in range(len(x0)):
            tmpl = np.math.sqrt(np.power(cents[i, 0] - x0[j], 2) + np.power(cents[i, 1] - x1[j], 2))
            tmpsum += data_od[index, 0][j]
            if tmpl > 3000:
                flag = False
                break
        if tmpsum > 4000:
            flag = False
        if flag == False:
            break
    return flag, clf


def bi_search_k(data_X, data_od):
    lc = 1
    rc = len(data_X)
    while lc < rc:
        mc = int((lc + rc) / 2)
        flag, clf = getkmeansresult(mc, data_X, data_od)
        if flag == True:
            ansclf = clf
            rc = mc
        else:
            lc = mc + 1
    output(rc, ansclf, data_X, data_od)
    return rc

def kmeanshelper(n):
    data_X, data_od, i = n

    tmpk = bi_search_k(data_X, data_od)
    print(tmpk, i)

if __name__ == "__main__":
    data_X = loadDataset(r"../../data/kmeansdata/input.txt")
    data_od = loadDataset(r"../../data/kmeansdata/od.txt")
    mink = np.inf

    pool = Pool()

    pool.map(kmeanshelper, [(data_X, data_od, i) for i in range(100)])
