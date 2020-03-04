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

# width for M(Kpipi)
def width(ecms):
    WIDTH = 999.
    if int(ecms) == 4360:
        WIDTH = 0.021238 + 0.002
    if int(ecms) == 4420:
        WIDTH = 0.021238 + 0.002
    if int(ecms) == 4600:
        WIDTH = 0.021238 + 0.002
    if not (int(ecms) == 4360 or int(ecms) == 4420 or int(ecms) == 4600):
        WIDTH = 0.021238 + 0.002
    return WIDTH

# signal window for RM(Dpipi)
def window(ecms):
    WINDOW = 999.
    if int(ecms) == 4360:
        WINDOW = 0.018
    if int(ecms) == 4420:
        WINDOW = 0.018
    if int(ecms) == 4600:
        WINDOW = 0.018
    if not (int(ecms) == 4360 or int(ecms) == 4420 or int(ecms) == 4600):
        WINDOW = 0.018
        if (int(ecms) == 4340 or int(ecms) == 4440):
            WINDOW = 0.014
        if (int(ecms) == 4380 or int(ecms) == 4390):
            WINDOW = 0.013
        if (int(ecms) == 4400):
            WINDOW = 0.015
    return WINDOW

# chi2 of kinematic fit(missing method)
def chi2_kf(ecms):
    CHI2_KF = 999.
    if int(ecms) == 4360:
        CHI2_KF = 20.
    if int(ecms) == 4420:
        CHI2_KF = 20.
    if int(ecms) == 4600:
        CHI2_KF = 20.
    if not (int(ecms) == 4360 or int(ecms) == 4420 or int(ecms) == 4600):
        CHI2_KF = 20.
    return CHI2_KF

# parameter of rm(Dpipi) fit
def num_rm_Dpipi(ecms):
    if ecms == 4190:
        NUM_LOW = -50000
        NUM_UP = 50000
    elif ecms == 4200:
        NUM_LOW = -50000
        NUM_UP = 50000
    elif ecms == 4210:
        NUM_LOW = -50000
        NUM_UP = 50000
    elif ecms == 4237:
        NUM_LOW = -50000
        NUM_UP = 50000
    elif ecms == 4245:
        NUM_LOW = -50000
        NUM_UP = 50000
    elif ecms == 4270:
        NUM_LOW = -50000
        NUM_UP = 50000
    elif ecms == 4280:
        NUM_LOW = -50000
        NUM_UP = 50000
    else:
        NUM_LOW = 0
        NUM_UP = 500000
    return NUM_LOW, NUM_UP

# parameter of rm(Dpipi) fit
def param_rm_Dpipi(ecms):
    MEAN_UP = 999.
    MEAN_LOW = 999.
    SIGMA_UP = 999.
    if int(ecms == 4190):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4200):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4210):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4220):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    elif int(ecms == 4230):
        MEAN_UP = 1.872
        MEAN_LOW = 1.869
        SIGMA_UP = 0.009
    elif int(ecms == 4237):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4245):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.012
    elif int(ecms == 4246):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4260):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4270):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.012
    elif int(ecms == 4280):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4290):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.007
    elif int(ecms == 4310):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.008
    elif int(ecms == 4315):
        MEAN_UP = 1.872
        MEAN_LOW = 1.868
        SIGMA_UP = 0.011
    elif int(ecms == 4340):
        MEAN_UP = 1.875
        MEAN_LOW = 1.865
        SIGMA_UP = 0.008
    elif int(ecms == 4360):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4380):
        MEAN_UP = 1.875
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    elif int(ecms == 4390):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    elif int(ecms == 4400):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    elif int(ecms == 4420):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.012
    elif int(ecms == 4440):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    elif int(ecms == 4470):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    elif int(ecms == 4530):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4600):
        MEAN_UP = 1.875
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    return MEAN_UP, MEAN_LOW, SIGMA_UP

# parameter of rm(D) fit
def num_rm_D(ecms):
    N_D1_2420 = 9999999
    N_PSIPP = 9999999
    N_DDPIPI = 9999999
    if int(ecms == 4190):
        N_D1_2420 = 0
        N_PSIPP = 200
        N_DDPIPI = 300
    elif int(ecms == 4200):
        N_D1_2420 = 0
        N_PSIPP = 300
        N_DDPIPI = 300
    elif int(ecms == 4210):
        N_D1_2420 = 0
        N_PSIPP = 200
        N_DDPIPI = 500
    elif int(ecms == 4220):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4230):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4237):
        N_D1_2420 = 0
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4245):
        N_D1_2420 = 0
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4246):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 700
    elif int(ecms == 4260):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4270):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4280):
        N_D1_2420 = 0
        N_PSIPP = 200
        N_DDPIPI = 200
    elif int(ecms == 4290):
        N_D1_2420 = 500
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4310):
        N_D1_2420 = 1000
        N_PSIPP = 1000
        N_DDPIPI = 400
    elif int(ecms == 4315):
        N_D1_2420 = 500
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4340):
        N_D1_2420 = 1000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4360):
        N_D1_2420 = 5000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4380):
        N_D1_2420 = 2000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4390):
        N_D1_2420 = 500
        N_PSIPP = 200
        N_DDPIPI = 100
    elif int(ecms == 4400):
        N_D1_2420 = 2000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4420):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4440):
        N_D1_2420 = 2000
        N_PSIPP = 2000
        N_DDPIPI = 2000
    elif int(ecms == 4470):
        N_D1_2420 = 1000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4530):
        N_D1_2420 = 500
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4600):
        N_D1_2420 = 3000
        N_PSIPP = 3000
        N_DDPIPI = 3000
    return N_D1_2420, N_PSIPP, N_DDPIPI

# luminosity
def luminosity(ecms):
    if int(ecms) == 4190:
        LUM = 570.03
    if int(ecms) == 4200:
        LUM = 526.0
    if int(ecms) == 4210:
        LUM = 572.05
    if int(ecms) == 4220:
        LUM = 569.2
    if int(ecms) == 4230:
        LUM = 1100.94
    if int(ecms) == 4237:
        LUM = 530.3
    if int(ecms) == 4245:
        LUM = 55.88
    if int(ecms) == 4246:
        LUM = 538.1
    if int(ecms) == 4260:
        LUM = 828.4
    if int(ecms) == 4270:
        LUM = 531.1
    if int(ecms) == 4280:
        LUM = 175.7
    if int(ecms) == 4290:
        LUM = 500.
    if int(ecms) == 4310:
        LUM = 45.08
    if int(ecms) == 4315:
        LUM = 500.
    if int(ecms) == 4340:
        LUM = 500.
    if int(ecms) == 4360:
        LUM = 543.9
    if int(ecms) == 4380:
        LUM = 500.
    if int(ecms) == 4390:
        LUM = 55.57
    if int(ecms) == 4400:
        LUM = 500.
    if int(ecms) == 4420:
        LUM = 46.8 + 1043.9
    if int(ecms) == 4440:
        LUM = 570.
    if int(ecms) == 4470:
        LUM = 111.09
    if int(ecms) == 4530:
        LUM = 112.12
    if int(ecms) == 4600:
        LUM = 586.9
    return LUM

# range of D1(2420) when getting shape
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
        UP = 2.44
        BINS = 350
    if int(ecms) == 4315:
        LOW = 2.25
        UP = 2.4425
        BINS = 300
    if int(ecms) == 4340:
        LOW = 2.25
        UP = 2.47
        BINS = 350
    if int(ecms) == 4360:
        LOW = 2.17
        UP = 2.494
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
        LOW = 2.14
        UP = 2.55
        BINS = 300
    if int(ecms) == 4440:
        LOW = 2.3
        UP = 2.57
        BINS = 450
    if int(ecms) == 4470:
        LOW = 2.18
        UP = 2.60
        BINS = 400
    if int(ecms) == 4530:
        LOW = 2.3
        UP = 2.6
        BINS = 500
    if int(ecms) == 4600:
        LOW = 2.22
        UP = 2.732
        BINS = 400
    return LOW, UP, BINS
