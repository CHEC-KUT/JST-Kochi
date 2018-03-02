#! /usr/bin/env python

__author__ = 'WANG Chen'
__email__ = 'i@wangchen0413.cn'

'''
************************************************
* - Key speed graph & Finger tracing graph
* - Analysis
* - 38001 Trials
************************************************
'''

import numpy as np
import pandas as pd
import re
import os
import math
import matplotlib.pyplot as plt
import pickle
import random
from PIL import Image, ImageDraw, ImageFont
from functools import reduce

from ../util.util import *

'''
************************************************
* - Graph Generate Functions
************************************************
'''

def tracingGraphGenerate(tracingDictPath):
    with open(tracingDictPath, "rb") as f:
        tracingDict = pickle.load(f)
    for k, v in tracingDict.items():
        tracingImage = Image.open(bg)
        draw = ImageDraw.Draw(tracingImage)
        for i in range(len(v)):
            xy = v[i]
            draw_finger_position(draw, xy, offx = 0, offy = 0, i=i)
        #tracingImage.save(tracingFolder + k + ".png")
        tracingImage.save(tracingSunFolder + k + ".png")
        print(k)    

def keyPairFrequency(tracingDictPath):
    frequencyDict = {}
    x = []; y = []
    with open(tracingDictPath, "rb") as f:
        tracingDict = pickle.load(f)
    plt.figure(figsize=(90, 10))
    plt.title("Key Pair Frequency")
    plt.xlabel("Frequency")
    plt.ylabel("Key Pair")
    for k,v in tracingDict.items():
        frequencyDict[k] = len(v)
        x.append(k); y.append(len(v))
    frequencyList = list(map(lambda x, y: (x, y), x, y))
    frequencyList = sorted(frequencyList, key = lambda x: x[1])
    print(frequencyList)
    print(reduce(lambda a,b: a + b, y))
    plt.xticks(range(len(x)), x)
    plt.bar(x, height=y, align='center')
    plt.savefig("keyPairFrequency.jpg")
    with open("frequencyDict.pkl", "wb") as f:
        pickle.dump(frequencyDict, f)
    return frequencyDict

def errorRateForKey(frequencyDict):
    pass

'''
************************************************
* - Analysis Functions
************************************************
'''

def tracingRangeConvergence(tracingDictPath):
    rangeDict = {}
    groupNumber = 10
    with open(tracingDictPath, "rb") as f:
        tracingDict = pickle.load(f)
    for k, v in tracingDict.items():
        #print(k)
        rangeDict[k] = []
        try:
            center = ((v[0][0][0] + v[0][-1][0])/2, (v[0][0][1] + v[0][-1][1])/2)
        except IndexError as e:
            print('except:', str(e) + "******" + k + "******")
            continue
        j = 0
        groupDistance = []
        for i in v:
            #print(i)
            j += 1
            for s in i[1: -1]:
                distance = math.sqrt((s[0]-center[0])**2 + (s[1]-center[1])**2)
                groupDistance.append(distance)
            #print(groupDistance)
            if j == groupNumber:
                rangeDict[k].append(groupDistance)
                j = 0
                groupDistance = []
        if j != 0:
            #print(j)       
            rangeDict[k].append(groupDistance) 
            #print(rangeDict[k])
    with open("rangeDict.pkl","wb") as f:
        pickle.dump(rangeDict, f)  
    #print(rangeDict["mi"])
    return rangeDict

def tracingNormalPoint(tracingDictPath):
    with open(tracingDictPath, "rb") as f:
        tracingDict = pickle.load(f)
    tracingNormalPointDict = {}
    for k, v in tracingDict.items():
        tracingNormalPointDict[k] = []
        print(k)
        try:
            center = ((v[0][0][0] + v[0][-1][0])/2, (v[0][0][1] + v[0][-1][1])/2)
        except IndexError as e:
            print('except:', str(e) + "******" + k + "******")
            continue
        for i in v:
            trialDistance = []
            for s in i[1: -1]:
                distance = math.sqrt((s[0]-center[0])**2 + (s[1]-center[1])**2)
                trialDistance.append(distance)  
            tracingNormalPointDict[k].append(trialDistance)  
        try: 
            #print(tracingNormalPointDict[k])
            #print(len(tracingNormalPointDict[k]))
            trialAver = list(map(lambda x: sum(x)/len(x), list(filter(lambda x: x != [], tracingNormalPointDict[k]))))
            print(trialAver)
        except ZeroDivisionError as e:
            print("except: " + str(e) + "******" + k + "******")
        tracingNormalPointDict[k] = trialAver
        with open("tracingNormalPointDict.pkl", "wb") as f:
            pickle.dump(tracingNormalPointDict, f)
    return tracingNormalPointDict
    
def trialNormalPointFilter(tracingNormalPointDictPath, e):
    with open(tracingNormalPointDictPath, "rb") as f:
        td = pickle.load(f)
    tdFilter = {}
    for k, v in td.items():
        if len(v) >= e:
            aver = np.mean(v)
            for i, j in enumerate(v):
                if j >= 3 * aver:
                    v.pop(i)
            tdFilter[k] = v
            print(k)
    with open("tracingNormalPointFilterDict.pkl", "wb") as f:
        pickle.dump(tdFilter, f)
    return tdFilter        

def tracingNormalPointRegress(tracingNormalPointDictPath):
    with open(tracingNormalPointDictPath, "rb") as f:
        tnpd = pickle.load(f)
    parameterList = {}
    for k, v in tnpd.items():
        print(k)
        xTrialMat = np.mat([range(len(v)),[1.000 for i in range(len(v))]]).T
        yRangeMat = np.mat(v).T
        xTx = xTrialMat.T * xTrialMat
        if np.linalg.det(xTx) == 0.0:
            print("This matrix is singular, cannot do inverse")
            continue
        ws = xTx.I * (xTrialMat.T * yRangeMat)
        parameterList[k] = ws
    with open("parameterList.pkl", "wb") as f:
        pickle.dump(parameterList, f)
    return parameterList

def tracingNormalPointInverseRegress(tracingNormalPointDictPath):
    with open(tracingNormalPointDictPath, "rb") as f:
        tnpd = pickle.load(f)
    parameterList = {}
    for k, v in tnpd.items():
        print(k)
        xTrialMat = np.mat([range(len(v)),[1.000 for i in range(len(v))]]).T
        yRangeMat = np.mat(v).T
        xTx = xTrialMat.T * xTrialMat
        if np.linalg.det(xTx) == 0.0:
            print("This matrix is singular, cannot do inverse")
            continue
        ws = xTx.I * (xTrialMat.T * yRangeMat)
        parameterList[k] = ws
    with open("parameterList.pkl", "wb") as f:
        pickle.dump(parameterList, f)
    return parameterList

def tracingNormalPointDrawing(tracingNormalPointDictPath, parameterListPath):
    with open(tracingNormalPointDictPath, "rb") as f:
        tnpd = pickle.load(f)
    with open(parameterListPath, "rb") as b:
        pl = pickle.load(b)
    corr = {}
    for k, v in tnpd.items():
        print(k)
        plt.figure()
        plt.title(k)
        plt.xlabel("Trials")
        plt.ylabel("Range")       
        plt.scatter(list(range(len(v))), v)
        xTrialMat = np.mat([range(len(v)),[1.000 for i in range(len(v))]]).T
        yRangeMat = np.mat(v).T
        if k in pl:
            xCopy = xTrialMat.copy()
            xCopy.sort(0)
            yRangeHat = xCopy * pl[k]
            plt.plot(xCopy[:,0], yRangeHat, color = "red")
            corr[k] = np.corrcoef(yRangeHat.T, yRangeMat.T)
        with open("corr.pkl", "wb") as f:
            pickle.dump(corr, f)
        #plt.savefig(tracingNormalPointFolder  + str(k) + ".jpg")
        plt.savefig(tracingNormalPointFilterFolder  + str(k) + ".jpg")        
    return "End"

def tracingAverage(rangeDictPath):
    with open(rangeDictPath, "rb") as f:
        rangeDict = pickle.load(f)
    tracingAverageDict = {}
    for k, v in rangeDict.items():
        tracingAverageDict[k] = []
        for i in v:
            print(i)
            try:
                r = reduce(lambda x, y: x + y, sorted(i)[0:int(len(i)*0.8)]) / len(i)
                tracingAverageDict[k].append(r)
            except TypeError as e:
                print('except:', str(e) + "******" + k + "******")
                continue
    with open("tracingAverageDict.pkl", "wb") as f:
        pickle.dump(tracingAverageDict, f)
    print(tracingAverageDict)
    return tracingAverageDict

def tracingRangeDrawing(tracingAverageDictPath):
    with open(tracingAverageDictPath, "rb") as f:
        tracingAverageDict = pickle.load(f)
    for k, v in tracingAverageDict.items():
        plt.figure()
        plt.title("Key Pair Range")
        plt.xlabel("Trials")
        plt.ylabel("Traing Range")
        plt.plot(range(len(v)), v)
        plt.savefig(tracingRange + k + ".jpg")
    return 1


