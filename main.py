#! /usr/bin/env python

__author__ = 'WANG Chen'
__email__ = 'i@wangchen0413.cn'

from tracing.tracingStat import *
from tracing.tracingAlysis import *
from tracing.tracingModel import *
from tracing.tracingFeature import *
from speed.speedAlysis import *

'''
************************************************
* - Main Functions
************************************************
'''

if __name__ == '__main__':
    # ***** Data Processing Part *****
    GeneralDataProcessing()
    #dataProcessing()
    #dataFixed()
    #dataByBlock("tracingFixedDict.pkl")
    #tracingDataMerge("tracingFixedDict.pkl")

    # ***** Tracing Feature *****
    #IKIRawComputing()
    #IKIBlockComputing()
    #IKIBlockVisual()

    # ***** Tracing Analysis *****
    #tracingGraphGenerate("tracingDict.pkl")
    #speedGraphGenerate("speedDict.pkl")
    #keyPairFrequency("tracingDict.pkl")
    #tracingRangeConvergence("tracingDict.pkl")
    #tracingAverage("rangeDict.pkl")
    #tracingRangeDrawing("tracingAverageDict.pkl")
    #speedRangeConvergence("speedDict.pkl")
    #tracingNormalPoint("tracingDict.pkl")
    #trialNormalPointFilter("tracingNormalPointDict.pkl", 50)
    #tracingNormalPointRegress("tracingNormalPointFilterDict.pkl")
    #tracingNormalPointDrawing("tracingNormalPointDict.pkl", "parameterList.pkl")
    #tracingNormalPointDrawing("tracingNormalPointFilterDict.pkl", "parameterList.pkl")
    #tracingRegression("tracingDict.pkl")

    # ***** Speed Analysis *****
    #speedByblock()
    #speedBlockVisual()
    #speedANOVA()

    # ***** Test Part *****
    #dataOnME("tracingFixedDict.pkl")
    #speedOnME("meData.pkl")
    #vsulSpeedMe("meSpeed.pkl")