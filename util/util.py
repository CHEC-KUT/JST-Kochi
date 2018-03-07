#! /usr/bin/env/ python

import random
import os

'''
************************************************
* - Varibles
************************************************
'''

Folder = os.path.abspath("./../PJ0009")
print(Folder)

srcFolder = os.path.abspath('.')
pklFolder = os.path.join(srcFolder, "pkl")
graphFolder = os.path.join(srcFolder, "graph")

bg = '../img/back.png'

fingerFolder_ = Folder + '/data/finger_/'
tlogFolder_ = Folder + '/data/tlogs_/'
fingerFixedFolder_ = Folder + '/data/finger_fixed/'

tracingFolder = '../graph/tracing/'
tracingSunFolder = '../graph/tracing-sun/'
tracingGraFolder = '../graph/tracing-gra/'
speedFolder = '../graph/speed/'
tracingRange = '../graph/tracingRange/'
tracingNormalPointFolder = '../graph/tracingNormalPoint/'
tracingNormalPointFilterFolder = '../graph/tracingNormalPointFilter/'

uid = 502
userN = 20
bid = 1
blockN = 4
sid = 1
senN = 140

dataIndex = lambda: [str(u)+'_'+str(b)+'_'+str(s) for u in range(uid, uid + userN) for b in range(bid, bid + blockN) for s in range(sid, sid + senN)]

color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

suncolor_sequence = ['#FF1E1E', '#FF7215', '#FFBB04', '#FFF72C', '#D1FF3F',
                '#97FF4D', '#1ACD00', '#008930', '#00D3E8', '#27A3FF',
                '#005EFE', '#0200AC', '#9975FF', '#8724FF', '#CD44FF',
                '#FF2ED6']

gradient_sequence = ['#CAD6FF', '#A0CEFF', '#8CBAFF', '#669CFF', '#2698FF',
                '#0081F6', '#0069D8', '#004ED8', '#003984', '#001D8B',
                '#000027']

timeDeviation = -120

'''
************************************************
* - General Util Classes & Functions
************************************************
'''

# Convert x and y to pixels 
def x_cm2pic(x):
    xscale =1838-594 ; x0 = 94; xim = 500
    return x*xscale+x0+xim
    
def y_cm2pic(y):
    yscale =2524-1920 ; y0 = 1720; yim = 200
    return y*yscale+y0+yim

def xy_cm2pic(x,y):
    return [x_cm2pic(x),y_cm2pic(y)]

def draw_finger_position(draw,xy,offx = 0,offy = 0,i = 0):
    #r = 2;
    option = 1
    if option == 0:
        n = random.randint(0, len(color_sequence)-1)
        fill = color_sequence[n]
    elif option == 1:
        n = i // userN if i <= (userN * (len(suncolor_sequence)-1)) else len(suncolor_sequence)-1
        fill = suncolor_sequence[n]
    elif option == 2:
        n = i // userN if i <= (userN * (len(gradient_sequence)-1)) else len(gradient_sequence)-1
        fill = gradient_sequence[n]  
    else:
        fill = "#000000"      
    draw.line(xy, fill=fill, width=6)

# keyboard
class keys:    
    specialkey = []
    specialkeywidth = []
    specialkeyheight = []
    keyheight = None
    keywidth = None
    def __init__(self,key,x,y):  
        self.key = key
        self.x = x
        self.y = y
        if key not in keys.specialkey:
            self.left = x - keys.keywidth/2
            self.right = x + keys.keywidth/2
            self.top = y - keys.keyheight/2
            self.bottom = y + keys.keyheight/2
        else:
            self.left = x - keys.specialkeywidth[keys.specialkey.index(key)]/2
            self.right = x + keys.specialkeywidth[keys.specialkey.index(key)]/2
            self.top = y - keys.specialkeyheight[keys.specialkey.index(key)]/2
            self.bottom = y + keys.specialkeyheight[keys.specialkey.index(key)]/2

class keyboard:
    kbkeys = []
    def __init__(self,skkeys,skwid,skhei,keys_,xs,ys,kw,kh):
        keys.keyheight = kh
        keys.keywidth =kw
        keys.spicalkey = skkeys
        keys.specialkeywidth = skwid
        keys.specialkeyheight = skhei
        for k,x,y in zip(keys_,xs,ys):
            keyboard.kbkeys.append(keys(k,x,y))

    def xy2key(self,x,y):
        for k in keyboard.kbkeys:
            if y>k.top and y<=k.bottom and x>k.left and x<=k.right:
                return k.key

    def key2xy(self,key):
        for k in keyboard.kbkeys:
            if key == k.key:
                return ((k.left+k.right)/2, (k.top+k.bottom)/2)
        return False

def define_ex_kb():
        kw = 130.9
        kh = 2248-2048
        keys_ = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'å', 'a', 's', 'd', 'f', 
                 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', ' ']
        xs = [566. ,   696.9,   827.8,   958.7,  1089.6,  1220.5,  1351.4, 1482.3,  1613.2,  1744.1,  1875., 
              566. ,   696.9,   827.8,   958.7,  1089.6,  1220.5,  1351.4, 1482.3,  1613.2,  1744.1,  1875.,
              740. ,   901.71428571,  1063.42857143,  1225.14285714, 1386.85714286,  1548.57142857,  1710.28571429,  1872., 1220]
        ys = [2044, 2044, 2044, 2044, 2044, 2044, 2044, 2044, 2044, 2044, 2044,
              2248, 2248, 2248, 2248, 2248, 2248, 2248, 2248, 2248, 2248, 2248,
              2452, 2452, 2452, 2452, 2452, 2452, 2452, 2455, 2656]
        skkeys = [' ']
        skwid= [kw*5]
        skhei = [kh]
        return keyboard(skkeys,skwid,skhei,keys_,xs,ys,kw,kh)
