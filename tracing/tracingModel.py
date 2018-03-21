#! /usr/local/bin python3

from util.util import *

import random
import os
import pickle
import math
import numpy as np
import matplotlib.pyplot as plt

def dataOnME(tracingFixedDictPath):
    with open(os.path.join(pklFolder, tracingFixedDictPath), "rb") as f:
        tracingFixedDict = pickle.load(f)
    me = {}
    for b, v in tracingFixedDict.items():
        print(b)
        if b not in me:
            me[b] = {}
        for u, d in v.items():
            print(u)
            if u not in me[b]:
                me[b][u] = {}
            if "me" in d:
                me[b][u]['me'] = d["me"]
    with open(os.path.join(pklFolder, "meData.pkl"), "wb") as f:
        pickle.dump(me, f)
    print (me)
    return me

def speedOnME(meDataPath):
    with open(os.path.join(pklFolder, meDataPath), "rb") as f:
        meData = pickle.load(f)
    meSpeed = {}
    for b, v in meData.items():
        print(b)
        if b not in meSpeed:
            meSpeed[b] = {}
        for u, d in v.items():
            print(u)
            if u not in meSpeed[b]:
                meSpeed[b][u] = {}
            meSpeed[b][u]["me"] = [[],[]]
            for l in d["me"]:
                distance = []
                time = []
                print(l)
                for i, j in enumerate(l[0]):
                    if i > 0:
                        distance.append((j[0]-l[0][i-1][0])**2 + (j[1]-l[0][i-1][1])**2)
                time = list(map(lambda x: x-l[1][0], l[1]))
                print(time)
                meSpeed[b][u]["me"][1].append(time)
                for i, j in enumerate(time[::-1]):
                    if i > 0:
                        time[i] = time[i] - time[i-1]             
                print(time)
                print(len(distance))
                print(len(time))
                s
                meSpeed[b][u]["me"][0].append(list(map(lambda x, y: math.sqrt(x)/y, distance, time)))
                meSpeed[b][u]["me"][1].append(time)
    with open(os.path.join(pklFolder, "meSpeed.pkl"), "wb") as f:
        pickle.dump(meSpeed, f)
    return meSpeed

def vsulSpeedMe(meSpeedPath):
    with open(os.path.join(pklFolder, meSpeedPath), "rb") as f:
        meSpeed = pickle.load(f)
    plt.figure()
    plt.title("me speed")
    plt.ylim(0, 100)
    n = 0
    for b, v in meSpeed.items():
        print(b)
        for u, d in v.items():
            print(u)
            for l in d["me"]:
                plt.plot(l[1], l[0], color = suncolor_sequence[n])
        n += 1
    plt.xlabel("time")
    plt.ylabel("speed")
    plt.savefig(os.path.join(graphFolder, "meSpeed.png"))


def tracingFitting():
    pass
                    
                
                
                
    
 
def tracingModel(start, end):
    upper = 0
    lower = 0
    point = random.uniform(upper, lower)
    tracingList = []
    return tracingList