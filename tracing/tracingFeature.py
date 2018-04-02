
import os
import pickle

from util.util import *
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# 
def wpmComputing():
    pass

# 
def IKIRawComputing():
    block = {}
    for j in range(1, 5):    
        with open(os.path.join(pklFolder, "block"+ str(j)+".pkl"), "rb") as f:
            tracingFixedDict = pickle.load(f)
        block[j] = {}
        for u, l in tracingFixedDict.items():
            print(u)
            block[j][u] = {}
            for k, v in l.items():
                print(k)
                try:
                    n = list(map(lambda x: (x[1][-1]-x[1][0])/(len(x[1])-1), v))
                    time = reduce(lambda x,y: x+y, n)/len(n)
                    block[j][u][k] = time
                except Exception as e:
                    print(e)
    with open(os.path.join(pklFolder, "IKI.pkl"), "wb") as f:
        pickle.dump(block, f)
    return block

def IKIBlockComputing():
    block = {}
    with open(os.path.join(pklFolder, "IKI.pkl"), "rb") as f:
        IKIRaw = pickle.load(f)
    for b, t in IKIRaw.items():
        print(b)
        block[b] = {}
        for u, l in t.items():
            print(u)
            n = list(map(lambda o: o[1], list(l.items())))
            block[b][u] = reduce(lambda x,y: x+y, n)/len(n)
    with open(os.path.join(pklFolder, "IKIBlock.pkl"), "wb") as f:
        pickle.dump(block, f)
    return block

def IKIBlockVisual():
    with open(os.path.join(pklFolder, "IKIBlock.pkl"), "rb") as f:
        IKIBlock = pickle.load(f)
    plt.figure(figsize=(20,10))
    plt.xticks(list(range(502,522)))
    color = ['r','g','b','c']
    n = 0
    for b, t in IKIBlock.items():
        #print(b)
        y = []
        for u, l in t.items():
            #print(u)
            y.append(l)
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
    plt.savefig(os.path.join(graphFolder, "IKIBlock.jpg"))
    return 1
    
            
