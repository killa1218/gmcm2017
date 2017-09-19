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

def readdata(infile):
    nodedict = {}
    tmpdict = {}
    tmpcontent = []
    with codecs.open(infile,'r') as f:
        for line in f.readlines():
            if line == "\n":continue
            if "\t" in line:
                nodestr = line.strip().split("\t")[0]
                citystr = line.strip().split("\t")[1]
                nodeid = int(nodestr.split(":")[0])
                nodex = float(nodestr.split(":")[1].split(",")[0])
                nodey = float(nodestr.split(":")[1].split(",")[1])
                if len(tmpcontent) == 0:
                    tmpcontent.append((nodex,nodey))
                cityid = int(citystr.split(":")[0])
                cityx = float(citystr.split(":")[1].split(",")[0])
                cityy = float(citystr.split(":")[1].split(",")[1])
                tmpdict[cityid] = (cityx,cityy)

            else:
                nodeid = int(line.strip().split(":")[0])
                od = float(line.strip().split(":")[1])
                tmpcontent.append(od)
                tmpcontent.append(tmpdict)
                nodedict[nodeid] = tmpcontent
                tmpcontent = []
                tmpdict = {}
    return  nodedict

def getdistance(p1,p2):
    return np.math.sqrt(np.power(p1[0] - p2[0], 2) + np.power(p1[1] - p2[1], 2))

def getlinks(nodedict):
    firstnodedict = {}
    secondenodedict = {}
    for k, v in nodedict.items():
        nodeid = k
        nodepoint = v[0]
        nodeod = v[1]
        minndist = np.inf
        connectfirst = -1
        tmpdict = {}
        for k2, v2 in nodedict.items():
            if k2 == k:
                continue
            nodeid2 = k2
            nodepoint2 = v2[0]
            nodeod2 = v2[1]
            distance = getdistance(nodepoint, nodepoint2)
            if distance < minndist and nodeod2 > 3000:
                minndist = distance
                connectfirst = nodeid2
            if nodeod > 3000 and nodeod2 > 3000:
                tmpdict[nodeid2] = distance
        if nodeod > 3000:
            firstnodedict[nodeid] = tmpdict
        else:
            secondenodedict[nodeid] = [(connectfirst,minndist)]
            # secondenodedict[connectfirst] = [(nodeid, minndist)]
    return firstnodedict,secondenodedict

def prime(vertexs,deges):
    # print(vertexs)
    adjacent_vertex = defaultdict(list)
    for v1, v2, length in edges:
        adjacent_vertex[v1].append((length, v1, v2))
    # print(adjacent_vertex)
    mst = {}
    chosed = set()
    chosed.add(vertexs[0])
    adjacent_vertexs_edges = adjacent_vertex[vertexs[0]]
    heapify(adjacent_vertexs_edges)
    while adjacent_vertexs_edges:
        w, v1, v2 = heappop(adjacent_vertexs_edges)
        if v2 not in chosed:
            chosed.add(v2)
            # print(mst.setdefault(v1,[]))
            mst.setdefault(v1,[]).append((v2,w))
            mst.setdefault(v2, []).append((v1, w))
            for next_vertex in adjacent_vertex[v2]:
                if next_vertex[2] not in chosed:
                    heappush(adjacent_vertexs_edges, next_vertex)

    return mst

def getcityid(nownode,nodedict):
    onenodecityid = []
    for k,v in nodedict[nownode][2].items():
        citynode = k-4
        onenodecityid.append(citynode)
    return onenodecityid

def getcityod(sid,eid,data_od_matrix):
    sumod = 0
    for i in sid:
        for j in eid:
            sumod += data_od_matrix[i][j]
    return  sumod

def getedgeod(startnode,root,alledges,nodedict,data_od_matrix):
    startcityid = getcityid(startnode,nodedict)
    flag = [0 for i in range(120)]
    flag[startnode] = 1
    nodeuse = []
    nodeuse.append(root)
    sumod = 0
    while len(nodeuse) != 0:
        nownode = nodeuse[0]
        flag[nownode] = 1
        del nodeuse[0]
        nowcityid = getcityid(nownode,nodedict)
        cityod = getcityod(startcityid,nowcityid,data_od_matrix)
        sumod += cityod
        for v in alledges[nownode]:
            newnode = v[0]
            if flag[newnode] == 1:
                continue
            nodeuse.append(newnode)
    return  sumod

def output(data_x,data_od,data_od_matrix,nodedict,firstnodedict,secondenodedict,mst):
    outlist = []
    alledges = mst
    f = open("../../data/linksresult/links.json", 'w')
    for k,v in secondenodedict.items():
        alledges[k] = v
        alledges[v[0][0]].append((k,v[0][1]))
    tmpmax = 0
    travelcost = 0.0
    devicecost = 0.0
    tunnelcost = 0.0
    for k,v in nodedict.items():
        print(k,v)
        outdict = {}
        outdict["node_id"] = k
        if v[1] > 3000:
            outdict["node_status"] = 1
        else:
            outdict["node_status"] = 2
        outdict["node_axis"] = v[0]
        outdict["node_capacity"] = v[1]
        outdict["node_cost"] = 150000000 / (36500*1.0) if outdict["node_status"] == 1 else (100000000 / (36500*1.0))
        devicecost += outdict["node_cost"]
        links = alledges[k]
        linkslist = []
        for link in links:
            tmpdict = {}
            endnode = link[0]
            distance = link[1]
            edgeod = getedgeod(k,endnode,alledges,nodedict,data_od_matrix)
            tmpmax = max(tmpmax,edgeod)
            tmpdict["endnode"] = endnode
            tmpdict["distance"] = distance
            tmpdict["edgeod"] = edgeod
            tmpdict["cost_travel"] = distance / 1000.0 * edgeod
            tmpdict["cost_tunnel"] = (350000000 if edgeod > 3600 else 300000000) * (distance / 1000.0) / (36500*1.0)
            tunnelcost += tmpdict["cost_tunnel"]
            travelcost += tmpdict["cost_travel"]
            linkslist.append(tmpdict)
        outdict["links"] = linkslist
        outlist.append(outdict)
    outlist.append({"maxtunnelod": tmpmax})
    outlist.append({"devicecost": devicecost})
    outlist.append({"travelcost": travelcost})
    outlist.append({"tunnelcost": tunnelcost / 2})
    outlist.append({"allcost":(devicecost + travelcost + tunnelcost / 2)})
    print(tmpmax,(devicecost + travelcost + tunnelcost / 2 ))
    json.dump(outlist,f,indent = 2)


if __name__ == "__main__":
    data_x = loadDataset(r"../../data/kmeansdata/input.txt")
    data_od = loadDataset(r"../../data/kmeansdata/od.txt")
    nodedict = readdata(r"../../data/kmeansresult/k_clusters_result35.txt")
    data_od_matrix = loadDataset(r"../../data/kmeansdata/odmatrix.txt")
    # print(data_x)
    # print(data_od)
    # for k,v in nodedict.items():
    #     print(k,v)
    firstnodedict, secondenodedict = getlinks(nodedict)
    vertexs = []
    edges = []
    tmpset = set()
    for k,v in firstnodedict.items():
        vertexs.append(k)
        for k2,v2 in v.items():
            edges.append((k,k2,v2))
    mst = prime(vertexs,edges)
    # print(mst)
    # print(firstnodedict,secondenodedict)
    output(data_x,data_od,data_od_matrix,nodedict,firstnodedict,secondenodedict,mst)