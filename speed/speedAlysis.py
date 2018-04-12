import os
import pickle
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import f_oneway 

from functools import reduce

from util.util import *

def speedComputing(k1, k0):
    p1 = xy_cm2pic(k1[1]['x'], k1[1]['y'])
    p0 = xy_cm2pic(k0[1]['x'], k0[1]['y'])
    speed = math.sqrt((p1[0]-p0[0])**2 + (p1[1]-p0[1])**2)/(k1[1]['trialtime']-k0[1]['trialtime'])
    return speed

def speedByblock():
    wholeBlock = {}
    for j in range(1, 5):   
        with open(os.path.join(pklFolder, "block"+ str(j)+".pkl"), "rb") as f:
            blockData = pickle.load(f)
        block = {} 
        wholeBlock[j] = {}
        for u, l in blockData.items():
            print(u)
            block[u] = {}
            wholeBlock[j][u] = {}
            #print(l)
            for k, v in l.items():
                print(k)
                speedList = []
            #try:
                for i in v:
                    distance = 0
                    #print(i)
                    for m in range(1, len(i)):          
                        distance += math.sqrt((i[0][m][0]-i[0][m-1][0])**2 + (i[0][m][1]-i[0][m-1][1])**2)
                    speedList.append(distance/(i[1][-1]-i[1][0]))
                speed = np.mean(speedList)
                block[u][k] = speed
                wholeBlock[j][u][k] = speed
            #except Exception as e:
                    #print(e)
        with open(os.path.join(pklFolder, "BlockSpeed" + str(j) +".pkl"), "wb") as f:
            pickle.dump(block, f)
    with open(os.path.join(pklFolder, "WholeBlockSpeed.pkl"), "wb") as f:
        pickle.dump(wholeBlock, f)
    return 1
    
def speedBlockVisual():
    with open(os.path.join(pklFolder, "WholeBlockSpeed.pkl"), "rb") as f:
        BlockSpeed = pickle.load(f)
    plt.figure(figsize=(20,10))
    plt.xticks(list(range(502,522)))
    color = ['r','g','b','c']
    n = 0
    data = {}
    for b, t in BlockSpeed.items():
        #print(b)        
        y = []
        for u, l in t.items():
            #print(u)
            speed = []
            for k, v in l.items():
                print(k)
                if v <= 60:
                    speed.append(v)
            aver = np.mean(speed)
            y.append(aver)
        data[b] = y
        plt.plot(range(502,522), y, color=color[n])
        
        print(np.mean(y))
        print(np.var(y))
        print("----------")
        n += 1
    red = mpatches.Patch(color="r", label = "block" + str(1))
    green = mpatches.Patch(color="g", label = "block" + str(2))
    blue = mpatches.Patch(color="b", label = "block" + str(3))
    cyan = mpatches.Patch(color="c", label = "block" + str(4))
    plt.legend(handles=[red, green, blue, cyan])
    plt.savefig(os.path.join(graphFolder, "BlockSpeed.jpg"))
    with open(os.path.join(pklFolder, "WholeBlockSpeedMerge.pkl"), "wb") as f:
        pickle.dump(data, f)
    return 1

def speedANOVA():
    with open(os.path.join(pklFolder, "WholeBlockSpeedMerge.pkl"), "rb") as f:
        dataList = pickle.load(f)
    f,p = f_oneway(dataList[1],dataList[2],dataList[3],dataList[4])
    print(f)
    print(p)
    


# ************************

def speedRangeConvergence(speedDictPath):
    with open(speedDictPath, "rb") as f:
        speedDict = pickle.load(f)
    speedRangeDict = {}
    groupNumber = 10
    for k, v in speedDict.items():
        print(k)
        speedRangeDict[k] = []
        j = 0
        groupSpeed = []
        #print(v)
        for i in v:
            j += 1
            #print(i[0])
            try:
                averageSpeed = reduce(lambda x, y: x + y, i[1])/len(i[1])
            except TypeError as e:
                print('except:', str(e) + "******" + k + "******")
                continue
            if j == groupNumber:
                speedRangeDict[k].append(averageSpeed)
                j = 0
                groupSpeed = []
        if j != 0:
            speedRangeDict[k].append(averageSpeed)
        print(speedRangeDict[k])
    with open("speedRangeDict.pkl", "wb") as f:
        pickle.dump(speedRangeDict, f)
    print(speedRangeDict)
    return speedRangeDict

def speedGraphGenerate(speedDictPath):
    with open(speedDictPath, "rb") as f:
        speedDict = pickle.load(f)
    for k, v in speedDict.items():
        plt.figure()
        plt.ylim(0,100)
        for i in range(len(v)):
            x = list(map(lambda x: x-v[i][0][0], v[i][0])); y = v[i][1]
            #plt.plot(x, y, color = color_sequence[random.randint(0, len(color_sequence)-1)])
            n = i // 10 if i <= 150 else 15
            plt.plot(x, y, color = suncolor_sequence[n])
        plt.xlabel("Time/milliseconds")
        plt.ylabel("Speed/Pixel")
        plt.title(k)
        plt.savefig(speedFolder + k + ".jpg")
        print(k)