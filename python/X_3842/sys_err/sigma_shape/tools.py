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

def search(allfile, root, target):
    items = os.listdir(root)
    for item in items:
        if item[0] == '.':
            continue
        if 'tmp' in item: continue
        path = os.path.join(root, item)
        if os.path.isdir(path):
            search(allfile, path, target)
        else:
            if target in path:
                allfile.append(path)
    return allfile

def group_files_by_num(name_list, num_total):
    groups = []
    group = []
    num_sum = 0

    for name in name_list:
        if int(num_sum) < int(num_total):
            group.append(name)
            num_sum = num_sum + 1
        else:
            groups.append(group)
            group = []
            num_sum = 0
            group.append(name)
            num_sum = num_sum + 1

        if name == name_list[-1]:
            groups.append(group)    
    return groups

def scale_factor(ecms, mode):
    BR = 0.0938
    if int(ecms) == 4230:
        lum = 1100.94
        if mode == 'psipp':
            XS = 6.05*BR
            Evt = 100000.0
        if mode == 'DD':
            XS = 3400.0*0.55
            Evt = 3700000.0
        if mode == 'qq':
            XS = 18300.0*0.55
            Evt = 20000000.0
        if mode == 'DDPIPI':
            XS = 2.92*BR
            Evt = 100000.0
        if mode == 'DDPI':
            XS = 31.79*BR
            Evt = 100000.0
    if int(ecms) == 4360:
        lum = 543.9
        if mode == 'D1_2420':
            XS = 20.5*BR
            Evt = 50000.0
        if mode == 'psipp':
            XS = 46.6*BR
            Evt = 50000.0
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
        if mode == 'DDPIPI':
            XS = 46.96*BR
            Evt = 50000.0
        if mode == 'DDPI':
            XS = 305.59*BR
            Evt = 50000.0
    if int(ecms) == 4420:
        lum = 46.80 + 1043.9
        if mode == 'D1_2420':
            XS = 30.5*BR
            Evt = 100000.0
        if mode == 'psipp':
            XS = 45.1*BR
            Evt = 100000.0
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
        if mode == 'DDPIPI':
            XS = 63.32*BR
            Evt = 100000.0
        if mode == 'DDPI':
            XS = 670.75*BR
            Evt = 100000.0
    if int(ecms) == 4600:
        lum = 586.9
        if mode == 'D1_2420':
            XS = 11.9*BR
            Evt = 50000.0
        if mode == 'psipp':
            XS = 21.5*BR
            Evt = 50000.0
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
        if mode == 'DDPIPI':
            XS = 32.77*BR
            Evt = 50000.0
        if mode == 'DDPI':
            XS = 131.56*BR
            Evt = 50000.0
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

# luminosity
def luminosity(ecms):
    if int(ecms) == 4190:
        LUM = 523.9 + 43.33
    if int(ecms) == 4200:
        LUM = 525.2
    if int(ecms) == 4210:
        LUM = 517.2 + 54.95
    if int(ecms) == 4220:
        LUM = 513.4 + 54.60
    if int(ecms) == 4230:
        LUM = 44.54 + 1056.4
    if int(ecms) == 4237:
        LUM = 529.1
    if int(ecms) == 4245:
        LUM = 55.88
    if int(ecms) == 4246:
        LUM = 536.3
    if int(ecms) == 4260:
        LUM = 828.4
    if int(ecms) == 4270:
        LUM = 529.7
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
        LUM = 111.1
    if int(ecms) == 4530:
        LUM = 112.1
    if int(ecms) == 4575:
        LUM = 48.9
    if int(ecms) == 4600:
        LUM = 586.9
    if int(ecms) == 4610:
        LUM = 103.83
    if int(ecms) == 4620:
        LUM = 521.52
    if int(ecms) == 4640:
        LUM = 552.41
    if int(ecms) == 4660:
        LUM = 529.63
    if int(ecms) == 4680:
        LUM = 1669.31
    if int(ecms) == 4700:
        LUM = 536.45
    if int(ecms) == 4740:
        LUM = 164.27
    if int(ecms) == 4750:
        LUM = 367.21
    if int(ecms) == 4780:
        LUM = 512.78
    if int(ecms) == 4840:
        LUM = 527.29
    if int(ecms) == 4914:
        LUM = 208.11
    if int(ecms) == 4946:
        LUM = 160.37
    return LUM

# parameter of rm(pipi) fit
def param_rm_pipi(ecms):
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
        SIGMA_UP = 0.001
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
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
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

# upper limit parameter of rm(pipi) fit
def upl_rm_pipi(ecms):
    N_OFFSET = 0
    STEP_SIZE = 999.
    STEP_N = 999.
    if int(ecms == 4190):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4200):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4210):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4220):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4230):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4237):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4246):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4260):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4270):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4290):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4315):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4340):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4360):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4380):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4400):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4420):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4440):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4600):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4620):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    if int(ecms == 4640):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    elif int(ecms == 4660):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 800
    elif int(ecms == 4680):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 2000
    elif int(ecms == 4700):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    elif int(ecms == 4750):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    elif int(ecms == 4780):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    elif int(ecms == 4840):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    elif int(ecms == 4914):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    elif int(ecms == 4946):
        N_OFFSET = 0
        STEP_SIZE = 0.1
        STEP_N = 600
    return N_OFFSET, STEP_SIZE, STEP_N
