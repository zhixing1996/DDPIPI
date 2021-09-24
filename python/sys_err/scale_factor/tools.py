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

def scale_factor(ecms, mode):
    BR = 0.0938
    if int(ecms) == 4230:
        lum = 1100.94
        if mode == 'DDPIPI':
            XS = 4.77*BR
            Evt = 100000.0
        if mode == 'DDPI':
            XS = 31.79*BR
            Evt = 500000.0
        if mode == 'DD':
            XS = 3400.0*0.55
            Evt = 3700000.0
        if mode == 'qq':
            XS = 18300.0*0.55
            Evt = 20000000.0
    if int(ecms) == 4360:
        lum = 543.9
        if mode == 'DDPIPI':
            XS = 50.0*BR
            Evt = 50000.0
        if mode == 'DDPI':
            XS = 305.59*BR
            Evt = 250000.0
        if mode == 'DD':
            XS = 10600.0*0.7
            Evt = 17200000.0
        if mode == 'qq':
            XS = 17500.0*0.7
            Evt = 9400000.0
        if mode == 'bhabha':
            XS = 389000.0
            Evt = 10000000.0
        if mode == 'dimu':
            XS = 4800.0
            Evt = 2600000.0
        if mode == 'ditau':
            XS = 9200.0
            Evt = 5000000.0
        if mode == 'digamma':
            XS = 18500.0
            Evt = 10000000.0
        if mode == 'twogamma':
            XS = 1900.0
            Evt = 1000000.0
        if mode == 'ISR':
            XS = 1110.0
            Evt = 600000.0
        if mode == 'gammaXYZ':
            XS = 41.6
            Evt = 33000.0
        if mode == 'hadrons':
            XS = 249.9
            Evt = 190000.0
    if int(ecms) == 4420:
        lum = 46.80 + 1043.9
        if mode == 'DDPIPI':
            XS = 68.93*BR
            Evt = 100000.0
        if mode == 'DDPI':
            XS = 670.15*BR
            Evt = 500000.0
        if mode == 'DD':
            XS = 10200.0
            Evt = 40300000.0*0.75
        if mode == 'qq':
            XS = 7000.0*0.75
            Evt = 14000000.0
        if mode == 'bhabha':
            XS = 379300.0
            Evt = 38000000.0
        if mode == 'dimu':
            XS = 5828.6
            Evt = 6000000.0
        if mode == 'ditau':
            XS = 3472.6
            Evt = 7000000.0
        if mode == 'digamma':
            XS = 18600.0
            Evt = 18000000.0
    if int(ecms) == 4600:
        lum = 586.9
        if mode == 'DDPIPI':
            XS = 31.83*BR
            Evt = 50000.0
        if mode == 'DDPI':
            XS = 131.56*BR
            Evt = 250000.0
        if mode == 'DD':
            XS = 7800.0*1.4
            Evt = 12000000.0
        if mode == 'qq':
            XS = 6000.0*1.4
            Evt = 10000000.0
        if mode == 'bhabha':
            XS = 350000.0
            Evt = 60000000.0
        if mode == 'dimu':
            XS = 4200.0
            Evt = 6600000.0
        if mode == 'ditau':
            XS = 3400.0
            Evt = 15000000.0
        if mode == 'digamma':
            XS = 16600.0
            Evt = 30000000.0
        if mode == 'twogamma':
            XS = 774100.0
            Evt = 11000000.0
        if mode == 'LL':
            XS = 350.0
            Evt = 500000.0
    ratio = XS*lum/Evt
    return ratio

# width for M(Kpipi)
def width(ecms):
    WIDTH = 999.
    if int(ecms) < 4300:
        WIDTH = 0.011*2
    elif int(ecms) >= 4300 and int(ecms) < 4500:
        WIDTH = 0.011*2
    if int(ecms) >= 4500:
        WIDTH = 0.011*2
    return WIDTH

# signal window for RM(Dpipi)
def window(ecms):
    WINDOW = 999.
    if int(ecms) < 4300:
        WINDOW = 0.006*2
    elif int(ecms) >= 4300 and int(ecms) < 4500:
        WINDOW = 0.009*2
    if int(ecms) >= 4500:
        WINDOW = 0.009*2
    return WINDOW

# parameter of m(Kpipi) fit
def param_m_Kpipi(ecms):
    MEAN_LOW = 999.
    MEAN_UP = 999.
    SIGMA_UP = 999.
    if int(ecms == 4190):
        # for MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.008
        # for data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.006
    elif int(ecms == 4200):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.006
    elif int(ecms == 4210):
        # for data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.004
        # for MC
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.004
    elif int(ecms == 4220):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.004
    elif int(ecms == 4230):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4237):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.008
        # for MC
        # MEAN_LOW = -0.002
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.006
    elif int(ecms == 4245):
        # for data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.006
        # for MC
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4246):
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.004
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4260):
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.006
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.008
    elif int(ecms == 4270):
        # for MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
        # for data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.006
    elif int(ecms == 4280):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.006
    elif int(ecms == 4290):
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4310):
        # for MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
        # for data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.01
    elif int(ecms == 4315):
        # data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.008
        # MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4340):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.008
    elif int(ecms == 4360):
        # for data
        # MEAN_LOW = -0.002
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.006
        # for MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4380):
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.008
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4390):
        # for data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.006
        # for MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.008
    elif int(ecms == 4400):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.01
    elif int(ecms == 4420):
        # for data 
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.004
        # for MC 
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.008
    elif int(ecms == 4440):
        # data
        # MEAN_LOW = -0.002
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.006
        # data
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4470):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.007
    elif int(ecms == 4530):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.008
    elif int(ecms == 4575):
        # for MC
        # MEAN_LOW = -0.002
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.006
        # for data
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.004
    elif int(ecms == 4600):
        # for data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.008
        # for MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4610):
        # for MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
        # for data
        # MEAN_LOW = -0.002
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.003
    elif int(ecms == 4620):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
        # for MC
        # MEAN_LOW = -0.002
        # MEAN_UP = 0.002
        # SIGMA_UP = 0.01
    elif int(ecms == 4640):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4660):
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4680):
        # data
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
        # MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.008
    elif int(ecms == 4700):
        MEAN_LOW = -0.005
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4740):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4750):
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.004
    elif int(ecms == 4780):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4840):
        # for data
        MEAN_LOW = -0.003
        MEAN_UP = 0.004
        SIGMA_UP = 0.004
        # for MC
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.008
    elif int(ecms == 4914):
        # data
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.006
        # MC
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4946):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    return MEAN_LOW, MEAN_UP, SIGMA_UP

# parameter of rm(Dpipi) fit
def param_rm_Dpipi(ecms):
    MEAN_LOW = 999.
    MEAN_UP = 999.
    SIGMA_UP = 999.
    if int(ecms == 4190):
        MEAN_LOW = -0.003
        MEAN_UP = 0.0003
        SIGMA_UP = 0.0008
    elif int(ecms == 4200):
        MEAN_LOW = -0.0003
        MEAN_UP = 0.0003
        SIGMA_UP = 0.0008
    elif int(ecms == 4210):
        MEAN_LOW = -0.0005
        MEAN_UP = 0.0005
        SIGMA_UP = 0.001
    elif int(ecms == 4220):
        MEAN_LOW = -0.0005
        MEAN_UP = 0.0005
        SIGMA_UP = 0.002
    elif int(ecms == 4230):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.002
    elif int(ecms == 4237):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.002
    elif int(ecms == 4245):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.001
        SIGMA_UP = 0.0012
    elif int(ecms == 4246):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.002
    elif int(ecms == 4260):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.004
    elif int(ecms == 4270):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.0015
        SIGMA_UP = 0.001
        # MEAN_LOW = -0.003
        # MEAN_UP = 0.003
        # SIGMA_UP = 0.008
    elif int(ecms == 4280):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.001
        SIGMA_UP = 0.001
    elif int(ecms == 4290):
        MEAN_LOW = -0.002
        MEAN_UP = 0.005
        SIGMA_UP = 0.01
    elif int(ecms == 4310):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4315):
        MEAN_LOW = -0.002
        MEAN_UP = 0.005
        SIGMA_UP = 0.006
    elif int(ecms == 4340):
        MEAN_LOW = -0.002
        MEAN_UP = 0.005
        SIGMA_UP = 0.006
    elif int(ecms == 4360):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4380):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4390):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4400):
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4420):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.008
    elif int(ecms == 4440):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4470):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4530):
        MEAN_LOW = -0.002
        MEAN_UP = 0.005
        SIGMA_UP = 0.004
    elif int(ecms == 4575):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4600):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.008
    elif int(ecms == 4610):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4620):
        MEAN_LOW = -0.002
        MEAN_UP = 0.007
        SIGMA_UP = 0.004
    elif int(ecms == 4640):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
        SIGMA_UP = 0.004
    elif int(ecms == 4660):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
        SIGMA_UP = 0.01
    elif int(ecms == 4680):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
        SIGMA_UP = 0.006
    elif int(ecms == 4700):
        MEAN_LOW = -0.005
        MEAN_UP = 0.005
        SIGMA_UP = 0.002
    elif int(ecms == 4740):
        MEAN_LOW = -0.005
        MEAN_UP = 0.005
        SIGMA_UP = 0.002
    elif int(ecms == 4750):
        MEAN_LOW = -0.005
        MEAN_UP = 0.005
        SIGMA_UP = 0.002
    elif int(ecms == 4780):
        MEAN_LOW = -0.002
        MEAN_UP = 0.007
        SIGMA_UP = 0.004
    elif int(ecms == 4840):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
        SIGMA_UP = 0.008
    elif int(ecms == 4914):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
        SIGMA_UP = 0.01
    elif int(ecms == 4946):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
        SIGMA_UP = 0.006
    return MEAN_LOW, MEAN_UP, SIGMA_UP

# upper limit parameter of rm(Dpipi) fit
def upl_rm_Dpipi(ecms):
    N_OFFSET = 0
    STEP_SIZE = 999.
    STEP_N = 999.
    if int(ecms == 4190):
        N_OFFSET = 0
        STEP_SIZE = 0.8
        STEP_N = 180
    elif int(ecms == 4200):
        N_OFFSET = 0
        STEP_SIZE = 0.4
        STEP_N = 300
    elif int(ecms == 4210):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 160
    elif int(ecms == 4220):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 240
    elif int(ecms == 4237):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 240
    elif int(ecms == 4245):
        N_OFFSET = 0
        STEP_SIZE = 0.2
        STEP_N = 200
    elif int(ecms == 4246):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 200
    elif int(ecms == 4270):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 200
    elif int(ecms == 4280):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 100
    elif int(ecms == 4310):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 110
    elif int(ecms == 4530):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 350
    elif int(ecms == 4575):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 150
    elif int(ecms == 4610):
        N_OFFSET = 0
        STEP_SIZE = 1
        STEP_N = 350
    return N_OFFSET, STEP_SIZE, STEP_N

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
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
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
    elif int(ecms == 4740):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4750):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4780):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4840):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4914):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4946):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    return N_D1_2420, N_PSIPP, N_DDPIPI

# center of mass energy
def ECMS(ecms):
    if int(ecms) == 4190:
        ecm = 4.18880
    if int(ecms) == 4200:
        ecm = 4.19890
    if int(ecms) == 4210:
        ecm = 4.20770
    if int(ecms) == 4220:
        ecm = 4.21710
    if int(ecms) == 4230:
        ecm = 4.22630
    if int(ecms) == 4237:
        ecm = 4.23570
    if int(ecms) == 4245:
        ecm = 4.24170
    if int(ecms) == 4246:
        ecm = 4.24380
    if int(ecms) == 4260:
        ecm = 4.25797
    if int(ecms) == 4270:
        ecm = 4.26680
    if int(ecms) == 4280:
        ecm = 4.27770
    if int(ecms) == 4290:
        ecm = 4.28788
    if int(ecms) == 4310:
        ecm = 4.30790
    if int(ecms) == 4315:
        ecm = 4.31205
    if int(ecms) == 4340:
        ecm = 4.33739
    if int(ecms) == 4360:
        ecm = 4.35826
    if int(ecms) == 4380:
        ecm = 4.37737
    if int(ecms) == 4390:
        ecm = 4.38740
    if int(ecms) == 4400:
        ecm = 4.39645
    if int(ecms) == 4420:
        ecm = 4.41558
    if int(ecms) == 4440:
        ecm = 4.43624
    if int(ecms) == 4470:
        ecm = 4.46710
    if int(ecms) == 4530:
        ecm = 4.52710
    if int(ecms) == 4575:
        ecm = 4.57450
    if int(ecms) == 4600:
        ecm = 4.59953
    if int(ecms) == 4610:
        ecm = 4.61208
    if int(ecms) == 4620:
        ecm = 4.63129
    if int(ecms) == 4640:
        ecm = 4.64366
    if int(ecms) == 4660:
        ecm = 4.66414
    if int(ecms) == 4680:
        ecm = 4.68188
    if int(ecms) == 4700:
        ecm = 4.70044
    if int(ecms) == 4740:
        ecm = 4.73967
    if int(ecms) == 4750:
        ecm = 4.75010
    if int(ecms) == 4780:
        ecm = 4.78038
    if int(ecms) == 4840:
        ecm = 4.84211
    if int(ecms) == 4914:
        ecm = 4.91802
    if int(ecms) == 4946:
        ecm = 4.95030
    return ecm

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
        LOW = 2.2
        UP = 2.37
        BINS = 400
    if int(ecms) == 4245:
        LOW = 2.22
        UP = 2.38
        BINS = 400
    if int(ecms) == 4246:
        LOW = 2.2
        UP = 2.38
        BINS = 400
    if int(ecms) == 4260:
        LOW = 2.22
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
        LOW = 2.23
        UP = 2.47
        BINS = 350
    if int(ecms) == 4360:
        LOW = 2.235
        UP = 2.495
        BINS = 300
    if int(ecms) == 4380:
        LOW = 2.24
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
        LOW = 2.22
        UP = 2.55
        BINS = 300
    if int(ecms) == 4440:
        LOW = 2.19
        UP = 2.57
        BINS = 450
    if int(ecms) == 4470:
        LOW = 2.21
        UP = 2.60
        BINS = 400
    if int(ecms) == 4530:
        LOW = 2.225
        UP = 2.665
        BINS = 400
    if int(ecms) == 4575:
        LOW = 2.24
        UP = 2.72
        BINS = 400
    if int(ecms) == 4600:
        LOW = 2.19
        UP = 2.73
        BINS = 400
    if int(ecms) == 4610:
        LOW = 2.215
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
        LOW = 2.195
        UP = 2.825
        BINS = 400
    if int(ecms) == 4700:
        LOW = 2.195
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
        LOW = 2.195
        UP = 2.975
        BINS = 400
    if int(ecms) == 4914:
        LOW = 2.175
        UP = 3.045
        BINS = 400
    if int(ecms) == 4946:
        LOW = 2.195
        UP = 3.095
        BINS = 400
    return LOW, UP, BINS

# range of RM(pipi)
def param_rm_pipi(ecms):
    LOW = 999.
    UP = 999.
    if int(ecms) == 4190:
        LOW = 3.73
        UP = 3.88
    if int(ecms) == 4200:
        LOW = 3.73
        UP = 3.9
    if int(ecms) == 4210:
        LOW = 3.735
        UP = 3.88
    if int(ecms) == 4220:
        LOW = 3.735
        UP = 3.88
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
        UP = 3.93
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
        UP = 4.03
    if int(ecms) == 4390:
        LOW = 3.74
        UP = 4.01
    if int(ecms) == 4400:
        LOW = 3.735
        UP = 4.045
    if int(ecms) == 4420:
        LOW = 3.735
        UP = 4.095
    if int(ecms) == 4440:
        LOW = 3.735
        UP = 4.085
    if int(ecms) == 4470:
        LOW = 3.735
        UP = 4.135
    if int(ecms) == 4530:
        LOW = 3.73
        UP = 4.16
    if int(ecms) == 4575:
        LOW = 3.73
        UP = 4.19
    if int(ecms) == 4600:
        LOW = 3.73
        UP = 4.26
    if int(ecms) == 4610:
        LOW = 3.73
        UP = 4.23
    if int(ecms) == 4620:
        LOW = 3.735
        UP = 4.265
    if int(ecms) == 4640:
        LOW = 3.735
        UP = 4.335
    if int(ecms) == 4660:
        LOW = 3.73
        UP = 4.34
    if int(ecms) == 4680:
        LOW = 3.735
        UP = 4.365
    if int(ecms) == 4700:
        LOW = 3.73
        UP = 4.37
    if int(ecms) == 4740:
        LOW = 3.725
        UP = 4.345
    if int(ecms) == 4750:
        LOW = 3.725
        UP = 4.405
    if int(ecms) == 4780:
        LOW = 3.735
        UP = 4.44
    if int(ecms) == 4840:
        LOW = 3.735
        UP = 4.515
    if int(ecms) == 4914:
        LOW = 3.735
        UP = 4.585
    if int(ecms) == 4946:
        LOW = 3.735
        UP = 4.625
    return LOW, UP
