#! /usr/bin/env python

__author__ = 'WANG Chen'
__email__ = 'i@wangchen0413.cn'

from util.util import *

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

from util.util import *


'''
************************************************
* - Specific Util Classes & Functions
************************************************
'''

def speedComputing(k1, k0):
    p1 = xy_cm2pic(k1[1]['x'], k1[1]['y'])
    p0 = xy_cm2pic(k0[1]['x'], k0[1]['y'])
    speed = math.sqrt((p1[0]-p0[0])**2 + (p1[1]-p0[0])**2)/(k1[1]['trialtime']-k0[1]['trialtime'])
    return speed

def compareChar(c1, c2):
    if len(c1) > len(c2):
        return 1
    elif len(c1) == len(c2):
        return 0
    else:
        return -1

'''
************************************************
* - Main Functions
************************************************
'''

def dataProcessing():
    tracingDict = {}
    speedDict = {}; temSpeedList = [[],[]]
    mark = 0; xy = []; time = []
    kb = define_ex_kb()
    for i in dataIndex():
        try:
            tlogData = pd.read_csv(tlogFolder_ + 'tlog_' + i + '.csv').dropna()
            fingerData = pd.read_csv(fingerFolder_ + 'finger_' + i + '.csv')
        except FileNotFoundError as e:
            print('except:', e)
            continue
        ubs = re.compile(r'(\d+)_(\d+)_(\d+)')
        current_user = ubs.match(i).group(1)
        if current_user not in tracingDict:
            speedDict[current_user] = {}
            tracingDict[current_user] = {}
        lastFingerItem = next(fingerData.iterrows()); lastTlogItem = next(tlogData.iterrows())
        for j in tlogData.iterrows():
            if len(j[1]['message']) > 1:
                v = compareChar(j[1]['message'], lastTlogItem[1]['message'])
                if v != 0:
                    if v == 1 and mark == 0:
                        keyPair = j[1]['message'][-2:]
                    if v == 1 and mark != 0:
                        keyPair = 'B' + j[1]['message'][-1:]; mark = 0
                    if v == -1:
                        keyPair = lastTlogItem[1]['message'][-1:] + 'B'
                        mark += 1
                        if mark > 1:
                            keyPair = 'BB'
                    if keyPair not in speedDict[current_user]:
                        speedDict[current_user][keyPair] = []
                        tracingDict[current_user][keyPair] = [[],[]]
                    if kb.key2xy(keyPair[0]) == False or kb.key2xy(keyPair[1]) == False: continue
                    xy.append(kb.key2xy(keyPair[0]))
                    for v, k in enumerate(fingerData.iterrows()):
                        if type(k[1]['trialtime']) == str:
                            k[1]['trialtime'] = float(k[1]['trialtime'].split('.')[0] +'.000')
                        if type(lastFingerItem[1]['trialtime']) == str:
                            lastFingerItem[1]['trialtime'] = float(lastFingerItem[1]['trialtime'].split('.')[0] +'.000')
                        if k[1]['trialtime'] <= j[1]['wordtime'] + timeDeviation and k[1]['trialtime'] > timeDeviation and k[1]['trialtime'] > lastFingerItem[1]['trialtime']:
                            speed = speedComputing(k, lastFingerItem)
                            temSpeedList[0].append(k[1]['trialtime']); temSpeedList[1].append(speed)
                            time.append(k[1]['trialtime'])
                            xy.append((x_cm2pic(k[1]['x']), y_cm2pic(k[1]['y'])))
                            lastFingerItem = k
                        else:
                            if temSpeedList != [[],[]]:
                                break
                    xy.append(kb.key2xy(keyPair[1]))
                    tracingDict[current_user][keyPair][0].append(xy); tracingDict[current_user][keyPair][1].append(time)
                    speedDict[current_user][keyPair].append(temSpeedList)
                    temSpeedList = [[],[]]; xy = []; time = []
                    lastTlogItem = j                   
                    print(keyPair)
    with open("speedRawDict.pkl","wb") as f:
        pickle.dump(speedDict, f)
    with open("tracingRawDict.pkl","wb") as k:
        pickle.dump(tracingDict, k)
    print("End")
    return tracingDict, speedDict
#tracingDict = {"user": {"mi":[[(x, y),..],[(x1, y1),..],..],..}, "user2":{...}}

def tracingDataMerge(tracingRawDictPath):
    with open(tracingRawDictPath, "rb") as f:
        tracingRawDict = pickle.load(f)
    tracingDict = {}
    for u, l in tracingRawDict.items():
        print(u)
        for k, v in l.items():
            #print(k)
            if k not in tracingDict:
                tracingDict[k] = []
            for t, j in enumerate(v[0]):
                try:
                    tracingDict[k].insert((int(u)-uid+t)*userN, j)
                except IndexError as e:
                    print("except: " + str(e) + "******" + k + "******")
    with open("tracingDict.pkl", "wb") as f:
        pickle.dump(tracingDict, f)
    print("End")
    return tracingDict
         
