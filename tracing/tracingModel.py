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

########################

# Regression

def tracingRegression(tracingDictPath):
    with open(os.path.join(pklFolder, tracingDictPath), "rb") as f:
        tracingDict = pickle.load(f)
    LinearDocumentPath = os.path.join(srcFolder, "linear.txt")
    SquareDocumentPath = os.path.join(srcFolder, "square.txt")
    SquareParameterPath = os.path.join(srcFolder, "parameter.txt")
    px = []
    kb = define_ex_kb()
    for k, v in tracingDict.items():
        print(k)
        # 500, 1720
        x = []
        y = []
        try:
            startKey = kb.key2xy(k[0])
            endKey = kb.key2xy(k[1])
            print(startKey)
            print(endKey)
            try:
                slope = (endKey[1]-startKey[1])/(endKey[0]-startKey[0])
                print(slope)
            except ZeroDivisionError as e:
                print(e)
                slope = None
            except TypeError as e:
                print(e)
                continue
            for i in v:
                for j in i:
                    if j[0] >= 500 and j[1] >= 1720:
                        x.append(j[0]-startKey[0])
                        y.append(j[1]-startKey[1])
                        # print(x)
                        # print(y)
            plt.figure()
            plt.scatter(x, y)

            #f1 = np.polyfit(x, y, 1)  
            
            f1 = np.polyfit(x, y, 2)

            p1 = np.poly1d(f1, True)  
            print(p1)
            print(p1.c)
            px = p1.c
            yvals = p1(x)
            plt.plot(x, yvals, 'r')
            print(len(yvals))
            print(len(y))
            #cov = np.cov(yvals, y)
            yvalsmean = np.mean(yvals)
            ymean = np.mean(y)  
            cov = sum(map(lambda x, y: x*y, list(map(lambda y: y - yvalsmean, yvals)), list(map(lambda y1: y1 - ymean, y)))) / (len(y) -1)
            var = np.var(yvals)
            var1 = np.var(y)
            eff = cov / (math.sqrt(var*var1))
            plt.title(k)
            plt.xlim(xmin = min(x), xmax = max(y))
            plt.ylim(ymin = min(y), ymax = max(y))
            plt.xlabel('x')  
            plt.ylabel('y')  
            plt.savefig(squareFolder + k + '.jpg')
            #plt.savefig(testFolder + k + '.jpg')  

            #with open(LinearDocumentPath, "a+") as f:
            with open(SquareDocumentPath, "a+") as f:
                f.write(printReport(k, p1, var, var1, cov, eff))
            with open(SquareParameterPath, "a+") as f:
                if slope != 0 and slope != None:
                    f.write(k + ": " + str(px[0]) + ", " + str(px[1]) + ", " + str(px[2]) + ", " + str(slope) + ", " + str(startKey)+", "+ str(endKey) +"\n")
        except IndexError as e:
            print(e)    
    return "end"

def printReport(k, p1, var, var1, cov, eff):
    sum = 'Keypair: ' + k + " | " + 'Fit: ' + str(p1) + "\n" + "Yvals Variance: " + str(var) + "\n" + "yvals Variance: " + str(var1) + "\n" + "Covariance: " + str(cov) + "\n" + "Coefficient: " + str(eff) + "\n" + "----------------------------" + "\n"
    return sum

