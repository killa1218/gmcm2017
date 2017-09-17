import pandas as pd
import numpy as np
import codecs
from kmeans import KMeansClassifier
from kmeans import biKMeansClassifier
import matplotlib.pyplot as plt


def loadDataset(infile):
    df = pd.read_csv(infile, sep='\t', header=None, dtype=str, na_filter=False)
    return np.array(df).astype(np.float)

def output(chooseinit,k,clf):
    outname = "../../data/kmeansresult/k_clusters_result" + chooseinit + str(k) + ".txt"
    fw = codecs.open(outname,'w')
    cents = clf._centroids
    labels = clf._labels
    tmpcnt = 1
    for i in range(k):
        index = np.nonzero(labels == i)[0]
        # print(index)
        x0 = data_X[index, 0]
        x1 = data_X[index, 1]
        y_i = i
        for j in range(len(x0)):
            fw.write(str(tmpcnt) + ":" + str(cents[i, 0]) + "," + str(cents[i, 1]) + "\t" + str(index[j] + 4) + ":" + str(x0[j]) + "," + str(x1[j]) + "\n")
        if len(x0) != 0:
            tmpcnt += 1

def getkmeansresult(k,data_X):
    print(k)
    # clf = KMeansClassifier(k)
    clf = biKMeansClassifier(k)
    clf.fit(data_X)
    cents = clf._centroids
    labels = clf._labels
    flag = True
    for i in range(k):
        index = np.nonzero(labels == i)[0]
        # print(index)
        x0 = data_X[index, 0]
        x1 = data_X[index, 1]
        y_i = i
        for j in range(len(x0)):
            tmpl = np.math.sqrt( np.power(cents[i, 0] - x0[j],2) +  np.power(cents[i, 1] - x1[j],2))
            if tmpl > 3000:
                flag = False
                break
        if flag == False:
            break
    return flag,clf


def bi_search_k(data_X):
    lc = 1
    rc = len(data_X)
    while lc < rc:
        mc = int((lc + rc) / 2)
        flag,clf = getkmeansresult(mc,data_X)
        if flag == True:
            rc = mc
        else:
            lc = mc + 1
    print(mc)
    # if (mc > 40 and mc < 50) or (mc > 20 and mc < 30):
    # output("random_init",mc,clf)
    output("update_init",mc,clf)


if __name__ == "__main__":
    data_X = loadDataset(r"../../data/kmeansdata/input.txt")
    bi_search_k(data_X)
    # k = 3
    # clf = KMeansClassifier(k)
    # clf.fit(data_X)
    # cents = clf._centroids
    # labels = clf._labels
    # sse = clf._sse
    # colors = ['b', 'g', 'r', 'k', 'c', 'm', 'y', '#e24fff', '#524C90', '#845868']
    # print(cents)
    # for i in range(k):
    #     index = np.nonzero(labels == i)[0]
    #     print( len(index))
    #     x0 = data_X[index, 0]
    #     x1 = data_X[index, 1]
    #     # print(x0,x1)
    #     y_i = i
    #     for j in range(len(x0)):
    #         plt.text(x0[j], x1[j], str(y_i), color=colors[i], \
    #                  fontdict={'weight': 'bold', 'size': 6})
    #     plt.scatter(cents[i, 0]  , cents[i, 1], marker='x', color=colors[i], \
    #                 linewidths=7)
    #
    # plt.title("SSE={:.2f}".format(sse))
    # plt.axis([130000, 170000, 130000, 170000])
    # outname = "./result/k_clusters" + str(k) + ".png"
    # plt.savefig(outname)
    # plt.show()