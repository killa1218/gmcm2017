import sys
import pandas as pd
import numpy as np
import codecs
from collections import defaultdict
from heapq import *
import json

def loadDataset(infile):
    df = pd.read_csv(infile, sep = '\t', header = None, dtype = str, na_filter = False)
    return np.array(df).astype(np.float)

def _calEDist( arrA, arrB):
    return np.math.sqrt(sum(np.power(arrA - arrB, 2)))

def getpointod(nodeid,nodedict,odmatrix):
    odsum = 0
    for k,v in nodedict[str(nodeid)][2].items():
        cityid = int(k) - 4
        odsum += odmatrix[cityid]
    return odsum

def getlinks(campusid,cpoint,ctood,cfromod,nodedict,linksinfo):
    allto = sum(ctood)
    allfrom = sum(cfromod)
    mindistance = np.inf
    usenode = -1
    tmpdict = {}
    allcost = 0
    for item in linksinfo:
        if "node_id" not in item.keys():
            continue
        nowid = item["node_id"]
        ccdistance = _calEDist(cpoint,item["node_axis"])
        if ccdistance > mindistance or item["node_status"] == 2:
            continue
        odneedto = allto - getpointod(item["node_id"],nodedict,ctood)
        odneedfrom = allfrom - getpointod(nowid,nodedict,cfromod)
        usetood = 0
        usefromod = 0
        for  i in item["links"]:
            usetood += i["edgeod"]
            newnode = i["endnode"]
            for j in linksinfo:
                if "node_id" in j.keys() and j["node_id"] == newnode:
                    for k in j["links"]:
                        if k["endnode"] == nowid:
                            usefromod += k["edgeod"]
        mindistance = ccdistance
        tmpdict["campus_id"] = campusid + 1
        tmpdict["campus_axis"] = (cpoint[0],cpoint[1])
        tmpdict["campus_capacity"] = allto
        tmpdict["endnode"] = nowid
        tmpdict["endnode_axis"] = (item["node_axis"][0],item["node_axis"][1])
        tmpdict["distance"] = ccdistance/1000
        tmpdict["cost_travel"] = allto * ccdistance / 1000 + allfrom * ccdistance / 1000
        tmpdict["cost_tunnel"] = (500000000 if allto > 7200 else 500000000) * ccdistance / 1000 / 36500
        campuscost = (tmpdict["cost_travel"] + tmpdict["cost_tunnel"])
    tmpdict["campuscost"] = campuscost
    # print(usenode,mindistance)
    return  tmpdict


def build_campus_tube(clustercnt = 42):
    campus_axis = loadDataset("../../data/campus_coordinates.txt")

    uls_od = np.loadtxt('../../res/Question1/uls_od.txt')
    campus2citys = uls_od[:4, 4:]
    citys2campus = uls_od[4:, :4].transpose()
    distance = loadDataset("../../data/campus2areas_distance.txt")
    with open("../../res/Question2/links_{}.json".format(clustercnt), 'r') as f:
        linksinfo = json.load(f)
    with open("../../res/Question2/node4citys_{}.json".format(clustercnt),'r') as f:
        nodedict = json.load(f)
    tmplist = []
    allcost = 0
    for i in range(4):
        tmpdict = getlinks(i,campus_axis[i],campus2citys[i],citys2campus[i],nodedict,linksinfo)
        tmplist.append(tmpdict)
        allcost += tmpdict["campuscost"]
    tmplist.append({"allcost":allcost})
    print(tmplist)
    with open("../../res/Question2/campuslink_{}.json".format(clustercnt),'w') as f:
        json.dump(tmplist,f,indent=2)

    # print(linksinfo)
