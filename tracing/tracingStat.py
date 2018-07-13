# coding: utf-8

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

def derivativeComputing(k1, k0):
    p1 = xy_cm2pic(k1[1]['x'], k1[1]['y'])
    p0 = xy_cm2pic(k0[1]['x'], k0[1]['y'])
    derivative = (p1[1]-p0[1]) / (p1[0]-p0[0])
    return derivative

def compareChar(c1, c2):
    if len(str(c1)) > len(str(c2)):
        return 1
    elif len(str(c1)) == len(str(c2)):
        return 0
    else:
        return -1
    
def positionFix(k1, k0):
    pass

'''
************************************************
* - Main Functions
************************************************
'''

def dataProcessing():
    tracingDict = {}
    temTracingList = [[],[]]; mark = 0
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
        current_block = ubs.match(i).group(2)
        if current_block not in tracingDict:
            tracingDict[current_block] = {}
        if current_user not in tracingDict[current_block]:
            tracingDict[current_block][current_user] = {}
        lastFingerItem = next(fingerData.iterrows()); lastTlogItem = next(tlogData.iterrows())
        for j in tlogData.iterrows():
            if len(j[1]['message']) > 1:
                v = compareChar(j[1]['message'], lastTlogItem[1]['message'])
                if v != 0:
                    if v == 1 and mark == 0:
                        keyPair = j[1]['message'][-2:]
                    if v == 1 and mark != 0:
                        keyPair = '<' + j[1]['message'][-1:]; mark = 0
                    if v == -1:
                        keyPair = lastTlogItem[1]['message'][-1:] + '<'
                        mark += 1
                        if mark > 1:
                            keyPair = '<<'
                    if kb.key2xy(keyPair[0]) == False or kb.key2xy(keyPair[1]) == False: continue
                    if keyPair not in tracingDict[current_block][current_user]:
                        tracingDict[current_block][current_user][keyPair] = []
                    temTracingList[0].append(kb.key2xy(keyPair[0])), temTracingList[1].append(lastTlogItem[1]['wordtime'] + timeDeviation)
                    iterMarker = 0
                    for v, k in enumerate(fingerData.iterrows()):
                        # Fix the exception data in table for first two "if"
                        if type(k[1]['trialtime']) == str:
                            k[1]['trialtime'] = float(k[1]['trialtime'].split('.')[0] +'.000')
                        if type(lastFingerItem[1]['trialtime']) == str:
                            lastFingerItem[1]['trialtime'] = float(lastFingerItem[1]['trialtime'].split('.')[0] +'.000')
                        if k[1]['trialtime'] <= j[1]['wordtime'] + timeDeviation and k[1]['trialtime'] > timeDeviation and k[1]['trialtime'] > lastFingerItem[1]['trialtime']:
                            iterMarker = 1
                            temTracingList[0].append([x_cm2pic(k[1]['x']), y_cm2pic(k[1]['y'])]); temTracingList[1].append(k[1]['trialtime'])
                            lastFingerItem = k
                            #print(k[1]['trialtime'])
                        else:
                            if iterMarker != 0:
                                break
                    temTracingList[0].append(kb.key2xy(keyPair[1])); temTracingList[1].append(j[1]['wordtime'] + timeDeviation)
                    tracingDict[current_block][current_user][keyPair].append(temTracingList)
                    temTracingList = [[],[]]; lastTlogItem = j            
                    print(keyPair)
    with open(os.path.join(pklFolder, "tracingRawDict.pkl"),"wb") as k:
        pickle.dump(tracingDict, k)
    print("End")
    return tracingDict
#tracingRawDict = {"1": {"user": {"mi":[[[(x, y),..],[t,...]],[[(x1, y1),..],[t1,...]],..],..}, "user2":{...}}, "2":{...}}

def dataFixed():
    kw = 130.9/2
    kh = 204/2
    with open(os.path.join(pklFolder, "tracingRawDict.pkl"),"rb") as f:
        tracingFixedDict = pickle.load(f)
    for b, v in tracingFixedDict.items():
        print(b)
        for u, d in v.items():
            print(u)
            for k, g in d.items():
                print(k)
                for i in g:
                    l = len(i[0])
                    if l > 4:
                        xfd = i[0][1][0] - i[0][0][0]
                        xed = i[0][-2][0] - i[0][-1][0]
                        yfd = i[0][1][1] - i[0][0][1]
                        yed = i[0][-2][1] - i[0][-1][1]
                        if xfd >= kw:
                            x1 = xfd - kw
                            i[0][1][0] = i[0][0][0] + kw
                        elif xfd <= -kw:
                            x1 = xfd + kw
                            i[0][1][0] = i[0][0][0] - kw
                        else:
                            x1 = 0
                        if xed >= kw:
                            x2 = xed - kw
                            i[0][-2][0] = i[0][-1][0] + kw
                        elif xed <= -kw:
                            x2 = xed + kw
                            i[0][-2][0] = i[0][-1][0] - kw
                        else:
                            x2 = 0
                        if yfd >= kh:
                            y1 = yfd - kh
                            i[0][1][1] = i[0][0][1] + kh
                        elif yfd <= -kh:
                            y1 = yfd + kh
                            i[0][1][1] = i[0][0][1] - kh
                        else:
                            y1 = 0
                        if yed >= kh:
                            y2 = yed - kh
                            i[0][-2][1] = i[0][-1][1] + kh
                        elif yed <= -kh:
                            y2 = yed + kh
                            i[0][-2][1] = i[0][-1][1] - kh
                        else:
                            y2 = 0
                        i[0][2:-3] = map(lambda x: [(1/(l-4))*(x1-x2) + x[0], (1/(l-4))*(y1-y2) + x[1]], i[0][2:-3])   
    with open(os.path.join(pklFolder, "tracingFixedDict.pkl"), "wb") as f:
        pickle.dump(tracingFixedDict, f)                     
    return tracingFixedDict

def dataByBlock(tracingFixedDictPath):
    with open(os.path.join(pklFolder, tracingFixedDictPath), "rb") as f:
        tracingFixedDict = pickle.load(f)
    for b, v in tracingFixedDict.items():
        print(b)
        with open(os.path.join(pklFolder, "block" + b + ".pkl"), "wb") as f:
            pickle.dump(v, f)
    return 0

def tracingDataMerge(tracingFixedDictPath):
    with open(os.path.join(pklFolder, tracingFixedDictPath), "rb") as f:
        tracingFixedDict = pickle.load(f)
    tracingDict = {}
    for b, v in tracingFixedDict.items():
        print(b)
        for u, d in v.items():
            print(u)
            for k, g in d.items():
                print(k)
                if k not in tracingDict:
                    tracingDict[k] = []
                for t, j in enumerate(g):
                    try:
                        tracingDict[k].insert((int(u)-uid+t)*userN, j[0])
                    except IndexError as e:
                        print("except: " + str(e) + "******" + k + "******")
    with open(os.path.join(pklFolder, "tracingDict.pkl"), "wb") as f:
        pickle.dump(tracingDict, f)
    print("End")
    return tracingDict
#tracingDict = {"mi":[(x, y),...],}

'''
************************************************
* - Finger Data Functions
************************************************
'''

def GeneralDataProcessing():
    generalDict = {}
    kb = define_ex_kb()

    # Initialization
    for i in dataIndex():
        startMarker = 0
        mark = 0
        try:
            #if i != '505_1_4': continue
            tlogData = pd.read_csv(tlogFolder_ + 'tlog_' + i + '.csv').replace(np.nan, '', regex=True)
            fingerData = pd.read_csv(fingerFolder_ + 'finger_' + i + '.csv')
            #fixationData = pd.read_csv(fixationFolder_ + 'fixations_' + i + '.csv')
        except FileNotFoundError as e:
            print('except:', e)
            continue
        ubs = re.compile(r'(\d+)_(\d+)_(\d+)')
        current_user = ubs.match(i).group(1)
        current_block = ubs.match(i).group(2)
        current_sentence = ubs.match(i).group(3)
        print(current_sentence)
        if current_user not in generalDict:
            generalDict[current_user] = {}
        if current_block not in generalDict[current_user]:
            generalDict[current_user][current_block] = {}
        if current_sentence not in generalDict[current_user][current_block]:
            generalDict[current_user][current_block][current_sentence] = {}            
            generalDict[current_user][current_block][current_sentence]['systemtime'] = []
            generalDict[current_user][current_block][current_sentence]['wordtime'] = []
            generalDict[current_user][current_block][current_sentence]['key'] = []
            generalDict[current_user][current_block][current_sentence]['x'] = []
            generalDict[current_user][current_block][current_sentence]['y'] = []
            generalDict[current_user][current_block][current_sentence]['xf'] = []
            generalDict[current_user][current_block][current_sentence]['yf'] = []
            generalDict[current_user][current_block][current_sentence]['t'] = []

        lastActionItem = next(fingerData.iterrows()); lastTlogItem = next(tlogData.iterrows())

        for j in tlogData.iterrows():
            if len(str(j[1]['message'])) == 1 and startMarker == 0:
                if kb.key2xy(j[1]['message']) == False: 
                    lastTlogItem = j 
                    continue
                generalDict[current_user][current_block][current_sentence]['systemtime'].append(j[1]['systemtime'])
                generalDict[current_user][current_block][current_sentence]['wordtime'].append(j[1]['wordtime'] + timeDeviation)
                generalDict[current_user][current_block][current_sentence]['key'].append(j[1]['message'])
                generalDict[current_user][current_block][current_sentence]['x'].append([kb.key2xy(j[1]['message'])[0]])
                generalDict[current_user][current_block][current_sentence]['y'].append([kb.key2xy(j[1]['message'])[1]])
                generalDict[current_user][current_block][current_sentence]['xf'].append([kb.key2xy(j[1]['message'])[0]])
                generalDict[current_user][current_block][current_sentence]['yf'].append([kb.key2xy(j[1]['message'])[1]])
                generalDict[current_user][current_block][current_sentence]['t'].append([j[1]['wordtime'] + timeDeviation])
                startMarker = 1
                print(j[1]['message'])
                lastTlogItem = j 
                continue
                
            if startMarker == 1:
                v = compareChar(j[1]['message'], lastTlogItem[1]['message'])
                #print(j[1]['message'], lastTlogItem[1]['message'])
                #print(v)
                if v != 0:
                    if v == 1 and mark == 0:
                        keyPair = j[1]['message'][-2:]; key = j[1]['message'][-1:]
                    if v == 1 and mark != 0:
                        keyPair = '<' + j[1]['message'][-1:]; key = j[1]['message'][-1:]; mark = 0
                    if v == -1:
                        keyPair = lastTlogItem[1]['message'][-1:] + '<'; key = '<' 
                        mark += 1
                        if mark > 1:
                            keyPair = '<<'; key = '<'
                    
                    if kb.key2xy(keyPair[0]) == False or kb.key2xy(keyPair[1]) == False: 
                        lastTlogItem = j
                        continue
                        
                    generalDict[current_user][current_block][current_sentence]['systemtime'].append(j[1]['systemtime'])
                    generalDict[current_user][current_block][current_sentence]['wordtime'].append(j[1]['wordtime'] + timeDeviation)
                    generalDict[current_user][current_block][current_sentence]['key'].append(key)

                    lastKey = kb.key2xy(keyPair[0])

                    iterMarker = 0; x = []; y = []; t = []

                    for v, k in enumerate(fingerData.iterrows()):
                        # Fix the exception data in table for first two "if"
                        if type(k[1]['trialtime']) == str:
                            k[1]['trialtime'] = float(k[1]['trialtime'].split('.')[0] +'.000')
                        if type(lastActionItem[1]['trialtime']) == str:
                            lastActionItem[1]['trialtime'] = float(lastActionItem[1]['trialtime'].split('.')[0] +'.000')
                        if k[1]['trialtime'] <= j[1]['wordtime'] + timeDeviation and k[1]['trialtime'] > timeDeviation and k[1]['trialtime'] > lastActionItem[1]['trialtime']:
                            iterMarker = 1
                            t.append(k[1]['trialtime']); x.append(x_cm2pic(k[1]['x'])); y.append(y_cm2pic(k[1]['y']))
                            lastActionItem = k
                        else:
                            if iterMarker != 0:
                                break
                    t.append(j[1]['wordtime'] + timeDeviation); x.append(kb.key2xy(key)[0]); y.append(kb.key2xy(key)[1])
                    generalDict[current_user][current_block][current_sentence]['t'].append(t)
                    generalDict[current_user][current_block][current_sentence]['x'].append(x)
                    generalDict[current_user][current_block][current_sentence]['y'].append(y)
                    #print(x)
                    #print(t)
                    
                    xf, yf = dataFixedProcessing(x, y, lastKey)
                    #print(xf)

                    generalDict[current_user][current_block][current_sentence]['xf'].append(xf)
                    generalDict[current_user][current_block][current_sentence]['yf'].append(yf)

                    lastTlogItem = j            
                    print(key)
                    #print(generalDict)

    with open(os.path.join(pklFolder, "tracingTotalDict.pkl"),"wb") as k:
        pickle.dump(generalDict, k)
    print("End")
    return generalDict
# tracingDict = {"502": {"1": {"7": {
#                                    "systemtime": [],
#                                    "wordtime": [],
#                                    "key": [],
#                                    "x": [],
#                                    "y": [],
#                                    "xf": [],
#                                    "yf": [],
#                                    "t": [],
#                                    }, "15": {...}
#                               }, "2": {...}
#                        }, "503":{...}, ...
#                }

def dataFixedProcessing(x, y, lastKey):
    kw = 130.9/2
    kh = 204/2
    xf = x[:]; yf = y[:]
    xf.insert(0, lastKey[0]); yf.insert(0, lastKey[1])

    l = len(x)
    if l > 4:
        xfd = x[1] - x[0]
        xed = x[-2] - x[-1]
        yfd = y[1] - y[0]
        yed = y[-2] - y[-1]
        if xfd >= kw:
            x1 = xfd - kw
            xf[1] = xf[0] + kw
        elif xfd <= -kw:
            x1 = xfd + kw
            xf[1] = xf[0] - kw
        else:
            x1 = 0
        if xed >= kw:
            x2 = xed - kw
            xf[-2] = xf[-1] + kw
        elif xed <= -kw:
            x2 = xed + kw
            xf[-2] = xf[-1] - kw
        else:
            x2 = 0
        if yfd >= kh:
            y1 = yfd - kh
            yf[1] = yf[0] + kh
        elif yfd <= -kh:
            y1 = yfd + kh
            yf[1] = yf[0] - kh
        else:
            y1 = 0
        if yed >= kh:
            y2 = yed - kh
            yf[-2] = yf[-1] + kh
        elif yed <= -kh:
            y2 = yed + kh
            yf[-2] = yf[-1] - kh
        else:
            y2 = 0
        xf[2:-3] = map(lambda x: (1/(l-4))*(x1-x2) + x, xf[2:-3])
        yf[2:-3] = map(lambda y: (1/(l-4))*(y1-y2) + y, yf[2:-3]) 
        # xf[2:-3] = map(lambda x: (1/2)*(x1+x2) + x, xf[2:-3])
        # yf[2:-3] = map(lambda y: (1/2)*(y1+y2) + y, yf[2:-3])                    
    return xf[1:], yf[1:]

'''
************************************************
* - Finger Data Functions
************************************************
'''

def GeneralFixationDataProcessing():
    generalDict = {}
    kb = define_ex_kb()
    
    # Initialization
    for i in dataIndex():
        startMarker = 0
        mark = 0
        try:
            tlogData = pd.read_csv(tlogFolder_ + 'tlog_' + i + '.csv').replace(np.nan, '', regex=True)
            #fingerData = pd.read_csv(fingerFolder_ + 'finger_' + i + '.csv')
            fixationData = pd.read_csv(fixationFolder_ + 'fixations_' + i + '.csv')

        except FileNotFoundError as e:
            print('except:', e)
            continue
        ubs = re.compile(r'(\d+)_(\d+)_(\d+)')
        current_user = ubs.match(i).group(1)
        current_block = ubs.match(i).group(2)
        current_sentence = ubs.match(i).group(3)
        print(current_sentence)
        if current_user not in generalDict:
            generalDict[current_user] = {}
        if current_block not in generalDict[current_user]:
            generalDict[current_user][current_block] = {}
        if current_sentence not in generalDict[current_user][current_block]:
            generalDict[current_user][current_block][current_sentence] = {}            
            generalDict[current_user][current_block][current_sentence]['systemtime'] = []
            generalDict[current_user][current_block][current_sentence]['wordtime'] = []
            generalDict[current_user][current_block][current_sentence]['key'] = []
            generalDict[current_user][current_block][current_sentence]['x'] = []
            generalDict[current_user][current_block][current_sentence]['y'] = []
            generalDict[current_user][current_block][current_sentence]['xf'] = []
            generalDict[current_user][current_block][current_sentence]['yf'] = []
            generalDict[current_user][current_block][current_sentence]['t'] = []
            generalDict[current_user][current_block][current_sentence]['fixnum'] = []
            generalDict[current_user][current_block][current_sentence]['fixdur'] = []

        lastActionItem = next(fixationData.iterrows()); lastTlogItem = next(tlogData.iterrows())

        for j in tlogData.iterrows():
            if len(j[1]['message']) == 1 and startMarker == 0:
                if kb.key2xy(j[1]['message']) == False: 
                    lastTlogItem = j 
                    continue
                generalDict[current_user][current_block][current_sentence]['systemtime'].append(j[1]['systemtime'])
                generalDict[current_user][current_block][current_sentence]['wordtime'].append(j[1]['wordtime'] + timeDeviation)
                generalDict[current_user][current_block][current_sentence]['key'].append(j[1]['message'])
                generalDict[current_user][current_block][current_sentence]['x'].append([kb.key2xy(j[1]['message'])[0]])
                generalDict[current_user][current_block][current_sentence]['y'].append([kb.key2xy(j[1]['message'])[1]])
                generalDict[current_user][current_block][current_sentence]['xf'].append([kb.key2xy(j[1]['message'])[0]])
                generalDict[current_user][current_block][current_sentence]['yf'].append([kb.key2xy(j[1]['message'])[1]])
                generalDict[current_user][current_block][current_sentence]['t'].append([j[1]['wordtime'] + timeDeviation])
                generalDict[current_user][current_block][current_sentence]['fixnum'].append(-1)
                generalDict[current_user][current_block][current_sentence]['fixdur'].append(-1)
                startMarker = 1
                print(j[1]['message'])
                lastTlogItem = j 
                continue

            if startMarker == 1:
                v = compareChar(j[1]['message'], lastTlogItem[1]['message'])
                if v != 0:
                    if v == 1 and mark == 0:
                        keyPair = j[1]['message'][-2:]; key = j[1]['message'][-1:]
                    if v == 1 and mark != 0:
                        keyPair = '<' + j[1]['message'][-1:]; key = j[1]['message'][-1:]; mark = 0
                    if v == -1:
                        keyPair = lastTlogItem[1]['message'][-1:] + '<'; key = '<' 
                        mark += 1
                        if mark > 1:
                            keyPair = '<<'; key = '<'
                    #if key == 'A': continue
                    if kb.key2xy(keyPair[0]) == False or kb.key2xy(keyPair[1]) == False: 
                        lastTlogItem = j 
                        continue
                    generalDict[current_user][current_block][current_sentence]['systemtime'].append(j[1]['systemtime'])
                    generalDict[current_user][current_block][current_sentence]['wordtime'].append(j[1]['wordtime'] + timeDeviation)
                    generalDict[current_user][current_block][current_sentence]['key'].append(key)

                    iterMarker = 0; x = []; y = []; t = []; fixnum = []; fixdur = []

                    for v, k in enumerate(fixationData.iterrows()):
                        # Fix the exception data in table for first two "if"
                        if type(k[1]['trialtime']) == str:
                            continue
                        if k[1]['trialtime'] > 100000:
                            continue
                        if k[1]['trialtime'] <= j[1]['wordtime'] + timeDeviation and k[1]['trialtime'] > timeDeviation and k[1]['trialtime'] > lastActionItem[1]['trialtime']:
                            iterMarker = 1
                            t.append(k[1]['trialtime']); x.append(x_cm2pic(k[1]['x'])); y.append(y_cm2pic(k[1]['y'])); fixnum.append(k[1]['fixnum']); fixdur.append(k[1]['fixdur']) 
                            lastActionItem = k
                        else:
                            if iterMarker != 0:
                                break
                    #t.append(j[1]['wordtime'] + timeDeviation); x.append(kb.key2xy(key)[0]); y.append(kb.key2xy(key)[1]); fixnum.append(fixnum[-1]); fixdur.append(fixdur[-1]) 
                    generalDict[current_user][current_block][current_sentence]['t'].append(t)
                    generalDict[current_user][current_block][current_sentence]['x'].append(x)
                    generalDict[current_user][current_block][current_sentence]['y'].append(y)
                    generalDict[current_user][current_block][current_sentence]['fixnum'].append(fixnum)
                    generalDict[current_user][current_block][current_sentence]['fixdur'].append(fixdur)
                    #print(fixnum)
                    #print(fixdur)
                    #print(x)
                    #print(t)
                    
                    xf, yf = fixationFixedProcessing(x, y, current_user, current_block )
                    #print(xf)

                    generalDict[current_user][current_block][current_sentence]['xf'].append(xf)
                    generalDict[current_user][current_block][current_sentence]['yf'].append(yf)

                    lastTlogItem = j            
                    print(key)
                    #print(generalDict)

    with open(os.path.join(pklFolder, "fixationTotalDict.pkl"),"wb") as k:
        pickle.dump(generalDict, k)
    print("End")
    return generalDict
# tracingDict = {"502": {"1": {"7": {
#                                    "systemtime": [],
#                                    "wordtime": [],
#                                    "key": [],
#                                    "x": [],
#                                    "y": [],
#                                    "xf": [],
#                                    "yf": [],
#                                    "t": [],
#                                    "fixnum": [],
#                                    "fixdur": [],    
#                                    }, "15": {...}
#                               }, "2": {...}
#                        }, "503":{...}, ...
#                }

def fixationFixedProcessing(x, y, user, block):
    offsetD = readPickle('fixationOffset_R=300_withoutB&Space.pickle')
    xf = []
    yf = []
    for i in range(len(x)):
        xf.append(x[i]-offsetD[user][1][int(block)-1])
        yf.append(y[i]-offsetD[user][2][int(block)-1])
    return xf, yf

def readPickle(filename):
    # reload a file to a variable
    with open(os.path.join(pklFolder, filename), 'rb') as file:
        a_dict1 =pickle.load(file)
    return a_dict1
