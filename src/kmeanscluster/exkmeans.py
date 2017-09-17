import numpy as np
import pandas as pd
from kmeans import KMeansClassifier

def loadDataset(infile):
    df = pd.read_csv(infile, sep='\t', header=None, dtype=str, na_filter=False)
    return np.array(df).astype(np.float)

if __name__ == "__main__":
    k = 9
    data_X = loadDataset(r"../../data/kmeansdata/input.txt")
    data_od = loadDataset(r"../../data/kmeansdata/od.txt")
    clf = KMeansClassifier(k)
    clf.fit(data_X)
    cents = clf._centroids
    labels = clf._labels
    print cents, labels