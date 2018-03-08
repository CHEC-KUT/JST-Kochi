#! /usr/bin/env python

__author__ = 'WANG Chen'
__email__ = 'i@wangchen0413.cn'

from tracing.tracingStat import *
from tracing.tracingAlysis import *

'''
************************************************
* - Main Functions
************************************************
'''

if __name__ == '__main__':
    #dataProcessing()
    #dataFixed()
    #tracingDataMerge("tracingFixedDict.pkl")
    tracingGraphGenerate("tracingDict.pkl")
    #speedGraphGenerate("speedDict.pkl")
    keyPairFrequency("tracingDict.pkl")
    #tracingRangeConvergence("tracingDict.pkl")
    #tracingAverage("rangeDict.pkl")
    #tracingRangeDrawing("tracingAverageDict.pkl")
    #speedRangeConvergence("speedDict.pkl")
    #tracingNormalPoint("tracingDict.pkl")
    #trialNormalPointFilter("tracingNormalPointDict.pkl", 50)
    #tracingNormalPointRegress("tracingNormalPointFilterDict.pkl")
    #tracingNormalPointDrawing("tracingNormalPointDict.pkl", "parameterList.pkl")
    #tracingNormalPointDrawing("tracingNormalPointFilterDict.pkl", "parameterList.pkl")
