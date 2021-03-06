#!/usr/bin/env python
"""
Common tools 
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-13 Tue 15:05]" 

import sys 
import os, errno
import shutil
import ROOT 

# ---------------------------------------------
# Function 
# ---------------------------------------------

# parameter of rm(Dpipi) fit
def num_rm_D(ecms):
    N_D1_2420 = 9999999
    N_PSIPP = 9999999
    N_DDPIPI = 9999999
    if int(ecms == 4190):
        N_D1_2420 = 0
        N_PSIPP = 100
        N_DDPIPI = 100
    if int(ecms == 4200):
        N_D1_2420 = 0
        N_PSIPP = 100
        N_DDPIPI = 100
    if int(ecms == 4210):
        N_D1_2420 = 0
        N_PSIPP = 100
        N_DDPIPI = 200
    if int(ecms == 4220):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    if int(ecms == 4230):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    if int(ecms == 4237):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    if int(ecms == 4245):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 300
    if int(ecms == 4246):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 300
    if int(ecms == 4260):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    if int(ecms == 4270):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    if int(ecms == 4280):
        N_D1_2420 = 0
        N_PSIPP = 200
        N_DDPIPI = 200
    elif int(ecms == 4290):
        N_D1_2420 = 0
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4310):
        N_D1_2420 = 1000
        N_PSIPP = 1000
        N_DDPIPI = 400
    elif int(ecms == 4315):
        N_D1_2420 = 500
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4340):
        N_D1_2420 = 1200
        N_PSIPP = 2000
        N_DDPIPI = 2000
    elif int(ecms == 4360):
        N_D1_2420 = 5000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4380):
        N_D1_2420 = 4000
        N_PSIPP = 2000
        N_DDPIPI = 2000
    elif int(ecms == 4390):
        N_D1_2420 = 5000
        N_PSIPP = 2000
        N_DDPIPI = 1000
    elif int(ecms == 4400):
        N_D1_2420 = 2000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4420):
        N_D1_2420 = 500000
        N_PSIPP = 500000
        N_DDPIPI = 500000
    elif int(ecms == 4440):
        N_D1_2420 = 5000
        N_PSIPP = 3000
        N_DDPIPI = 3000
    elif int(ecms == 4470):
        N_D1_2420 = 1000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4530):
        N_D1_2420 = 500
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4575):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4600):
        N_D1_2420 = 3000
        N_PSIPP = 3000
        N_DDPIPI = 3000
    elif int(ecms == 4610):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4620):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4640):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4660):
        N_D1_2420 = 10000
        N_PSIPP = 10000
        N_DDPIPI = 10000
    elif int(ecms == 4680):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4700):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    return N_D1_2420, N_PSIPP, N_DDPIPI

# range of RM(D/Dmiss)
def param_rm_D(ecms):
    LOW = 999.
    UP = 999.
    BINS = 999
    if int(ecms) == 4190:
        LOW = 2.15
        UP = 2.33
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4200:
        LOW = 2.15
        UP = 2.34
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4210:
        LOW = 2.16
        UP = 2.34
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4220:
        LOW = 2.16
        UP = 2.35
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4230:
        LOW = 2.15
        UP = 2.36
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4237:
        LOW = 2.17
        UP = 2.37
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4245:
        LOW = 2.17
        UP = 2.38
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4246:
        LOW = 2.16
        UP = 2.38
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4260:
        LOW = 2.19
        UP = 2.39
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4270:
        LOW = 2.21
        UP = 2.4
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4280:
        LOW = 2.18
        UP = 2.41
        BINS = int((UP - LOW)/0.002)
    if int(ecms) == 4290:
        LOW = 2.25
        UP = 2.419
        BINS = 300
    if int(ecms) == 4310:
        LOW = 2.21
        UP = 2.49
        BINS = 400
    if int(ecms) == 4315:
        LOW = 2.25
        UP = 2.4425
        BINS = 300
    if int(ecms) == 4340:
        LOW = 2.25
        UP = 2.47
        BINS = 350
    if int(ecms) == 4360:
        LOW = 2.18
        UP = 2.49
        BINS = 300
    if int(ecms) == 4380:
        LOW = 2.25
        UP = 2.505
        BINS = 400
    if int(ecms) == 4390:
        LOW = 2.28
        UP = 2.52
        BINS = 300
    if int(ecms) == 4400:
        LOW = 2.25
        UP = 2.53
        BINS = 400
    if int(ecms) == 4420:
        LOW = 2.16
        UP = 2.55
        BINS = 300
    if int(ecms) == 4440:
        LOW = 2.2
        UP = 2.57
        BINS = 450
    if int(ecms) == 4470:
        LOW = 2.25
        UP = 2.60
        BINS = 400
    if int(ecms) == 4530:
        LOW = 2.2
        UP = 2.66
        BINS = 400
    if int(ecms) == 4575:
        LOW = 2.2
        UP = 2.732
        BINS = 400
    if int(ecms) == 4600:
        LOW = 2.215
        UP = 2.732
        BINS = 400
    if int(ecms) == 4610:
        LOW = 2.2
        UP = 2.8
        BINS = 400
    if int(ecms) == 4620:
        LOW = 2.2
        UP = 2.8
        BINS = 400
    if int(ecms) == 4640:
        LOW = 2.18
        UP = 2.78
        BINS = 400
    if int(ecms) == 4660:
        LOW = 2.22
        UP = 2.8
        BINS = 400
    if int(ecms) == 4680:
        LOW = 2.25
        UP = 2.85
        BINS = 400
    if int(ecms) == 4700:
        LOW = 2.20
        UP = 2.84
        BINS = 400
    return LOW, UP, BINS

# range of RM(pipi)
def param_rm_pipi(ecms):
    LOW = 999.
    UP = 999.
    if int(ecms) == 4190:
        LOW = 3.72
        UP = 3.89
    if int(ecms) == 4200:
        LOW = 3.73
        UP = 3.89
    if int(ecms) == 4210:
        LOW = 3.72
        UP = 3.89
    if int(ecms) == 4220:
        LOW = 3.72
        UP = 3.91
    if int(ecms) == 4230:
        LOW = 3.73
        UP = 3.91
    if int(ecms) == 4237:
        LOW = 3.72
        UP = 3.93
    if int(ecms) == 4245:
        LOW = 3.72
        UP = 3.94
    if int(ecms) == 4246:
        LOW = 3.72
        UP = 3.90
    if int(ecms) == 4260:
        LOW = 3.72
        UP = 3.96
    if int(ecms) == 4270:
        LOW = 3.72
        UP = 3.95
    if int(ecms) == 4280:
        LOW = 3.72
        UP = 3.95
    if int(ecms) == 4290:
        LOW = 3.73
        UP = 3.95
    if int(ecms) == 4310:
        LOW = 3.7
        UP = 3.97
    if int(ecms) == 4315:
        LOW = 3.73
        UP = 3.95
    if int(ecms) == 4340:
        LOW = 3.72
        UP = 4.0
    if int(ecms) == 4360:
        LOW = 3.74
        UP = 4.03
    if int(ecms) == 4380:
        LOW = 3.72
        UP = 4.07
    if int(ecms) == 4390:
        LOW = 3.7
        UP = 4.07
    if int(ecms) == 4400:
        LOW = 3.7
        UP = 4.08
    if int(ecms) == 4420:
        LOW = 3.72
        UP = 4.11
    if int(ecms) == 4440:
        LOW = 3.7
        UP = 4.08
    if int(ecms) == 4470:
        LOW = 3.73
        UP = 4.07
    if int(ecms) == 4530:
        LOW = 3.7
        UP = 4.18
    if int(ecms) == 4575:
        LOW = 3.7
        UP = 4.20
    if int(ecms) == 4600:
        LOW = 3.73
        UP = 4.22
    if int(ecms) == 4610:
        LOW = 3.73
        UP = 4.22
    if int(ecms) == 4620:
        LOW = 3.73
        UP = 4.22
    if int(ecms) == 4640:
        LOW = 3.72
        UP = 4.31
    if int(ecms) == 4660:
        LOW = 3.72
        UP = 4.3
    if int(ecms) == 4680:
        LOW = 3.72
        UP = 4.29
    if int(ecms) == 4700:
        LOW = 3.70
        UP = 4.35
    return LOW, UP
