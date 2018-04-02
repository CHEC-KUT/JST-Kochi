import numpy as np
import math

serial = [0, 11.855751744991242, 18.017286969510984, 14.888642326440227, 7.0778029134665248, 3.8390692006563922, 4.4112281442484971, 2.9050295666057533, 7.5555916499529809, 6.3306718222551197, 1.3901999920458674, 0.91404605170833442] 
#time = [0,0.04,0.07,0.11,0.14,0.16,0.2,0.23,0.27,0.3,0.34,0.37,0.4]

dataAuto = {} 

# Rotate Slope
def rotateSeries(serial):
    slope = (serial[-1]-serial[0])/(len(serial)-1)
    serialR = []
    for i in range(len(serial)):
        distance = abs(slope*i-serial[i])/math.sqrt(slope**2+1)
        serialR.append(distance)
    return serialR

# Main Function
def FTTOMain(serial):
    serialLen = len(serial)
    marker = [''] * serialLen
    marker[0] = serial[0]
    marker[-1] = serial[-1]
    if serialLen >= 3:
        for i in range(serialLen-3):
            P = (serial[i+2] - serial[i]) * (serial[i+3] - serial[i+1])
            marker = FTTOFilter(P, i, serial[i], serial[i+1], serial[i+2], serial[i+3], marker)
    print(marker)
    return marker

def FTTOFilter(P, i, x0, x1, x2, x3, marker):
    if P < 0:
        if (x3 - x1 > 0):
            if (x1 <= x2):
                marker[i+1] = x1
            if (x1 > x2):
                marker[i+2] = x2
        if (x2 - x0 > 0):
            if (x1 >= x2):
                marker[i+1] = x1
            if (x1 < x2):
                marker[i+2] = x2
    if P == 0:
        if ((x3 - x1 != 0) and (x2 - x0 == 0)):
            if (x1 > x2 and x2 > x3):
                marker[i+1] = x1  
            elif (x1 < x2 and x2 < x3):
                marker[i+1] = x1 
            else:
                marker[i+2] = x2
        if ((x3 - x1 == 0) and (x2 - x0 != 0)):
            if (x2 > x1 and x1 > x0):
                marker[i+2] = x2  
            elif (x2 < x1 and x1 < x0):
                marker[i+2] = x2  
            else:
                marker[i+1] = x1 
    return marker

# Seeking Max Points and Min Points
def Processing(marker):
    aver = np.mean(list(filter(lambda x: x!='', marker)))
    maxL = [0]*len(marker)
    minL = [0]*len(marker)
    for i,j in enumerate(marker):
        if j != '':
            if j > aver:
                maxL[i] = j
            else:
                minL[i] = j
    print(maxL) 
    print(minL)
    return maxL, minL           

if __name__ == '__main__':
    serial = rotateSeries(serial)
    print(serial)
    marker = FTTOMain(serial)
    maxL, minL = Processing(marker)