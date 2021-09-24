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

# parameter pull values' range
def pull_range(ecms):
    RANGE_LOW = 999.
    RANGE_UP = 999.
    if int(ecms == 4190):
        RANGE_LOW = -0.6
        RANGE_UP = 0.6
    elif int(ecms == 4200):
        RANGE_LOW = -0.6
        RANGE_UP = 0.6
    elif int(ecms == 4210):
        RANGE_LOW = -0.5
        RANGE_UP = 0.5
    elif int(ecms == 4220):
        RANGE_LOW = -0.03
        RANGE_UP = 0.03
    elif int(ecms == 4230):
        RANGE_LOW = -0.03
        RANGE_UP = 0.03
    elif int(ecms == 4237):
        RANGE_LOW = -0.02
        RANGE_UP = 0.02
    elif int(ecms == 4245):
        RANGE_LOW = -0.08
        RANGE_UP = 0.08
    elif int(ecms == 4246):
        RANGE_LOW = -0.21
        RANGE_UP = 0.21
    elif int(ecms == 4260):
        RANGE_LOW = -0.013
        RANGE_UP = 0.013
    elif int(ecms == 4270):
        RANGE_LOW = -0.02
        RANGE_UP = 0.02
    elif int(ecms == 4280):
        RANGE_LOW = -0.02
        RANGE_UP = 0.02
    elif int(ecms == 4290):
        RANGE_LOW = -0.02
        RANGE_UP = 0.02
    elif int(ecms == 4310):
        RANGE_LOW = -0.01
        RANGE_UP = 0.01
    elif int(ecms == 4315):
        RANGE_LOW = -0.006
        RANGE_UP = 0.006
    elif int(ecms == 4340):
        RANGE_LOW = -0.01
        RANGE_UP = 0.01
    elif int(ecms == 4360):
        RANGE_LOW = -0.005
        RANGE_UP = 0.005
    elif int(ecms == 4380):
        RANGE_LOW = -0.01
        RANGE_UP = 0.01
    elif int(ecms == 4390):
        RANGE_LOW = -0.023
        RANGE_UP = 0.023
    elif int(ecms == 4400):
        RANGE_LOW = -0.02
        RANGE_UP = 0.02
    elif int(ecms == 4420):
        RANGE_LOW = -0.07
        RANGE_UP = 0.07
    elif int(ecms == 4440):
        RANGE_LOW = -0.06
        RANGE_UP = 0.06
    elif int(ecms == 4470):
        RANGE_LOW = -0.2
        RANGE_UP = 0.2
    elif int(ecms == 4530):
        RANGE_LOW = -0.2
        RANGE_UP = 0.2
    elif int(ecms == 4575):
        RANGE_LOW = -0.1
        RANGE_UP = 0.1
    elif int(ecms == 4600):
        RANGE_LOW = -0.05
        RANGE_UP = 0.05
    elif int(ecms == 4610):
        RANGE_LOW = -0.04
        RANGE_UP = 0.04
    elif int(ecms == 4620):
        RANGE_LOW = -0.04
        RANGE_UP = 0.04
    elif int(ecms == 4640):
        RANGE_LOW = -0.04
        RANGE_UP = 0.04
    elif int(ecms == 4660):
        RANGE_LOW = -0.04
        RANGE_UP = 0.04
    elif int(ecms == 4680):
        RANGE_LOW = -0.02
        RANGE_UP = 0.02
    elif int(ecms == 4700):
        RANGE_LOW = -0.03
        RANGE_UP = 0.03
    elif int(ecms == 4740):
        RANGE_LOW = -0.03
        RANGE_UP = 0.03
    elif int(ecms == 4750):
        RANGE_LOW = -0.04
        RANGE_UP = 0.04
    elif int(ecms == 4780):
        RANGE_LOW = -0.04
        RANGE_UP = 0.04
    elif int(ecms == 4840):
        RANGE_LOW = -0.03
        RANGE_UP = 0.03
    elif int(ecms == 4914):
        RANGE_LOW = -0.04
        RANGE_UP = 0.04
    elif int(ecms == 4946):
        RANGE_LOW = -0.05
        RANGE_UP = 0.05
    return RANGE_LOW, RANGE_UP

# parameter pull fit
def param_mean(ecms):
    MEAN_LOW = 999.
    MEAN_UP = 999.
    if int(ecms == 4190):
        MEAN_LOW = -0.1
        MEAN_UP = 0.1
    elif int(ecms == 4200):
        MEAN_LOW = -0.1
        MEAN_UP = 0.1
    elif int(ecms == 4210):
        MEAN_LOW = -0.01
        MEAN_UP = 0.01
    elif int(ecms == 4220):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
    elif int(ecms == 4230):
        MEAN_LOW = -0.001
        MEAN_UP = 0.001
    elif int(ecms == 4237):
        MEAN_LOW = -0.024
        MEAN_UP = 0.024
    elif int(ecms == 4245):
        MEAN_LOW = -0.15
        MEAN_UP = 0.1
    elif int(ecms == 4246):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4260):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
    elif int(ecms == 4270):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.0015
    elif int(ecms == 4280):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.001
    elif int(ecms == 4290):
        MEAN_LOW = -0.002
        MEAN_UP = 0.005
    elif int(ecms == 4310):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4315):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
    elif int(ecms == 4340):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4360):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4380):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4390):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4400):
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
    elif int(ecms == 4420):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
    elif int(ecms == 4440):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4470):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4530):
        MEAN_LOW = -0.002
        MEAN_UP = 0.005
    elif int(ecms == 4575):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4600):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
    elif int(ecms == 4610):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
    elif int(ecms == 4620):
        MEAN_LOW = -0.002
        MEAN_UP = 0.007
    elif int(ecms == 4640):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
    elif int(ecms == 4660):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
    elif int(ecms == 4680):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
    elif int(ecms == 4700):
        MEAN_LOW = -0.005
        MEAN_UP = 0.005
    elif int(ecms == 4740):
        MEAN_LOW = -0.005
        MEAN_UP = 0.005
    elif int(ecms == 4750):
        MEAN_LOW = -0.005
        MEAN_UP = 0.005
    elif int(ecms == 4780):
        MEAN_LOW = -0.002
        MEAN_UP = 0.007
    elif int(ecms == 4840):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
    elif int(ecms == 4914):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
    elif int(ecms == 4946):
        MEAN_LOW = -0.02
        MEAN_UP = 0.02
    return MEAN_LOW, MEAN_UP

# parameter pull fit
def param_sigma(ecms):
    SIGMA_MEAN = 99.
    SIGMA_LOW = 999.
    SIGMA_UP = 999.
    if int(ecms == 4190):
        SIGMA_MEAN = 0.1
        SIGMA_LOW = 0.
        SIGMA_UP = 0.2
    elif int(ecms == 4200):
        SIGMA_MEAN = 0.1
        SIGMA_LOW = 0.
        SIGMA_UP = 0.2
    elif int(ecms == 4210):
        SIGMA_MEAN = 0.1
        SIGMA_LOW = 0.
        SIGMA_UP = 0.3
    elif int(ecms == 4220):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4230):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4237):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4245):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4246):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4260):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4270):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4280):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4290):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4310):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4315):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4340):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4360):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4380):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4390):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4400):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4420):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4440):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4470):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4530):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4575):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4600):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4610):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4620):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4640):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4660):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4680):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4700):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4740):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4750):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4780):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4840):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4914):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    elif int(ecms == 4946):
        SIGMA_MEAN = 0.01
        SIGMA_LOW = 0.
        SIGMA_UP = 0.1
    return SIGMA_MEAN, SIGMA_LOW, SIGMA_UP

# range of RM(pipi)
def param_rm_pipi(ecms):
    LOW = 999.
    UP = 999.
    if int(ecms) == 4190:
        LOW = 3.73
        UP = 3.89
    if int(ecms) == 4200:
        LOW = 3.73
        UP = 3.9
    if int(ecms) == 4210:
        LOW = 3.735
        UP = 3.88
    if int(ecms) == 4220:
        LOW = 3.735
        UP = 3.91
    if int(ecms) == 4230:
        LOW = 3.735
        UP = 3.91
    if int(ecms) == 4237:
        LOW = 3.735
        UP = 3.9
    if int(ecms) == 4245:
        LOW = 3.735
        UP = 3.9
    if int(ecms) == 4246:
        LOW = 3.735
        UP = 3.935
    if int(ecms) == 4260:
        LOW = 3.733
        UP = 3.935
    if int(ecms) == 4270:
        LOW = 3.735
        UP = 3.92
    if int(ecms) == 4280:
        LOW = 3.73
        UP = 3.91
    if int(ecms) == 4290:
        LOW = 3.73
        UP = 3.94
    if int(ecms) == 4310:
        LOW = 3.73
        UP = 3.96
    if int(ecms) == 4315:
        LOW = 3.735
        UP = 3.97
    if int(ecms) == 4340:
        LOW = 3.735
        UP = 3.955
    if int(ecms) == 4360:
        LOW = 3.735
        UP = 4.
    if int(ecms) == 4380:
        LOW = 3.74
        UP = 4.01
    if int(ecms) == 4390:
        LOW = 3.74
        UP = 4.01
    if int(ecms) == 4400:
        LOW = 3.735
        UP = 4.06
    if int(ecms) == 4420:
        LOW = 3.735
        UP = 4.045
    if int(ecms) == 4440:
        LOW = 3.735
        UP = 4.045
    if int(ecms) == 4470:
        LOW = 3.735
        UP = 4.135
    if int(ecms) == 4530:
        LOW = 3.73
        UP = 4.16
    if int(ecms) == 4575:
        LOW = 3.73
        UP = 4.18
    if int(ecms) == 4600:
        LOW = 3.73
        UP = 4.26
    if int(ecms) == 4610:
        LOW = 3.73
        UP = 4.26
    if int(ecms) == 4620:
        LOW = 3.735
        UP = 4.265
    if int(ecms) == 4640:
        LOW = 3.735
        UP = 4.295
    if int(ecms) == 4660:
        LOW = 3.73
        UP = 4.34
    if int(ecms) == 4680:
        LOW = 3.735
        UP = 4.37
    if int(ecms) == 4700:
        LOW = 3.73
        UP = 4.365
    if int(ecms) == 4740:
        LOW = 3.725
        UP = 4.335
    if int(ecms) == 4750:
        LOW = 3.725
        UP = 4.42
    if int(ecms) == 4780:
        LOW = 3.735
        UP = 4.44
    if int(ecms) == 4840:
        LOW = 3.735
        UP = 4.485
    if int(ecms) == 4914:
        LOW = 3.735
        UP = 4.585
    if int(ecms) == 4946:
        LOW = 3.735
        UP = 4.625
    return LOW, UP

# range of RM(D/Dmiss)
def param_rm_D(ecms):
    LOW = 999.
    UP = 999.
    BINS = 999
    if int(ecms) == 4190:
        LOW = 2.16
        UP = 2.32
        BINS = 400
    if int(ecms) == 4200:
        LOW = 2.16
        UP = 2.33
        BINS = 400
    if int(ecms) == 4210:
        LOW = 2.18
        UP = 2.345
        BINS = 400
    if int(ecms) == 4220:
        LOW = 2.2
        UP = 2.35
        BINS = 400
    if int(ecms) == 4230:
        LOW = 2.16
        UP = 2.36
        BINS = 400
    if int(ecms) == 4237:
        LOW = 2.18
        UP = 2.37
        BINS = 400
    if int(ecms) == 4245:
        LOW = 2.2
        UP = 2.38
        BINS = 400
    if int(ecms) == 4246:
        LOW = 2.21
        UP = 2.38
        BINS = 400
    if int(ecms) == 4260:
        LOW = 2.2
        UP = 2.39
        BINS = 400
    if int(ecms) == 4270:
        LOW = 2.17
        UP = 2.4
        BINS = 400
    if int(ecms) == 4280:
        LOW = 2.22
        UP = 2.41
        BINS = 400
    if int(ecms) == 4290:
        LOW = 2.25
        UP = 2.419
        BINS = 300
    if int(ecms) == 4310:
        LOW = 2.22
        UP = 2.45
        BINS = 400
    if int(ecms) == 4315:
        LOW = 2.24
        UP = 2.45
        BINS = 300
    if int(ecms) == 4340:
        LOW = 2.235
        UP = 2.47
        BINS = 350
    if int(ecms) == 4360:
        LOW = 2.22
        UP = 2.495
        BINS = 300
    if int(ecms) == 4380:
        LOW = 2.23
        UP = 2.51
        BINS = 400
    if int(ecms) == 4390:
        LOW = 2.255
        UP = 2.52
        BINS = 300
    if int(ecms) == 4400:
        LOW = 2.23
        UP = 2.53
        BINS = 400
    if int(ecms) == 4420:
        LOW = 2.23
        UP = 2.55
        BINS = 300
    if int(ecms) == 4440:
        LOW = 2.22
        UP = 2.57
        BINS = 450
    if int(ecms) == 4470:
        LOW = 2.19
        UP = 2.60
        BINS = 400
    if int(ecms) == 4530:
        LOW = 2.22
        UP = 2.665
        BINS = 400
    if int(ecms) == 4575:
        LOW = 2.22
        UP = 2.72
        BINS = 400
    if int(ecms) == 4600:
        LOW = 2.19
        UP = 2.73
        BINS = 400
    if int(ecms) == 4610:
        LOW = 2.175
        UP = 2.745
        BINS = 400
    if int(ecms) == 4620:
        LOW = 2.22
        UP = 2.77
        BINS = 400
    if int(ecms) == 4640:
        LOW = 2.19
        UP = 2.78
        BINS = 400
    if int(ecms) == 4660:
        LOW = 2.19
        UP = 2.8
        BINS = 400
    if int(ecms) == 4680:
        LOW = 2.18
        UP = 2.825
        BINS = 400
    if int(ecms) == 4700:
        LOW = 2.235
        UP = 2.835
        BINS = 400
    if int(ecms) == 4740:
        LOW = 2.215
        UP = 2.885
        BINS = 400
    if int(ecms) == 4750:
        LOW = 2.195
        UP = 2.885
        BINS = 400
    if int(ecms) == 4780:
        LOW = 2.205
        UP = 2.915
        BINS = 400
    if int(ecms) == 4840:
        LOW = 2.185
        UP = 2.975
        BINS = 400
    if int(ecms) == 4914:
        LOW = 2.175
        UP = 3.045
        BINS = 400
    if int(ecms) == 4946:
        LOW = 2.185
        UP = 3.095
        BINS = 400
    return LOW, UP, BINS

# luminosity
def luminosity(ecms):
    if int(ecms) == 4190:
        LUM = 526.7 + 43.33
    if int(ecms) == 4200:
        LUM = 526.0
    if int(ecms) == 4210:
        LUM = 517.1 + 54.95
    if int(ecms) == 4220:
        LUM = 514.6 + 54.60
    if int(ecms) == 4230:
        LUM = 44.54 + 1056.4
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
        LUM = 502.4
    if int(ecms) == 4310:
        LUM = 45.08
    if int(ecms) == 4315:
        LUM = 501.2
    if int(ecms) == 4340:
        LUM = 505.0
    if int(ecms) == 4360:
        LUM = 543.9
    if int(ecms) == 4380:
        LUM = 522.7
    if int(ecms) == 4390:
        LUM = 55.57
    if int(ecms) == 4400:
        LUM = 507.8
    if int(ecms) == 4420:
        LUM = 46.8 + 1043.9
    if int(ecms) == 4440:
        LUM = 569.9
    if int(ecms) == 4470:
        LUM = 111.09
    if int(ecms) == 4530:
        LUM = 112.12
    if int(ecms) == 4575:
        LUM = 48.93
    if int(ecms) == 4600:
        LUM = 586.9
    if int(ecms) == 4610:
        LUM = 102.50
    if int(ecms) == 4620:
        LUM = 511.06
    if int(ecms) == 4640:
        LUM = 541.37
    if int(ecms) == 4660:
        LUM = 528.63
    if int(ecms) == 4680:
        LUM = 528.46 + 1103.27
    if int(ecms) == 4700:
        LUM = 526.20
    if int(ecms) == 4740:
        LUM = 143.28
    if int(ecms) == 4750:
        LUM = 339.6
    if int(ecms) == 4780:
        LUM = 493.83
    if int(ecms) == 4840:
        LUM = 514.07
    if int(ecms) == 4914:
        LUM = 202.43
    if int(ecms) == 4946:
        LUM = 153.7
    return LUM

