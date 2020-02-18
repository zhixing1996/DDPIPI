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

# remove path or bachelor file
def rm_r(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError, exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def search(allfile, root, target):
    items = os.listdir(root)
    for item in items:
        if item[0] == '.':
            continue
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

def duration(seconds):
    seconds = long(round(seconds))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365.242199)
 
    minutes = long(minutes)
    hours = long(hours)
    days = long(days)
    years = long(years)
 
    duration = []
    if years > 0:
        duration.append('%d year' % years + 's'*(years != 1))
    else:
        if days > 0:
            duration.append('%d day' % days + 's'*(days != 1))
        if hours > 0:
            duration.append('%d hour' % hours + 's'*(hours != 1))
        if minutes > 0:
            duration.append('%d minute' % minutes + 's'*(minutes != 1))
        if seconds > 0:
            duration.append('%d second' % seconds + 's'*(seconds != 1))
    return ' '.join(duration)

def set_root_style(stat=0, grid=0, PadTopMargin=0.08, PadBottomMargin=0.08,
                   PadLeftMargin=0.15, PadRightMargin=0.15):
    # must be used in the beginning
    ROOT.gROOT.SetBatch(1)
    ROOT.gROOT.Reset()

    ROOT.gStyle.SetOptTitle(0) 
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTitleFillColor(0) 
    ROOT.gStyle.SetTitleBorderSize(0)
    
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetCanvasColor(0)
    ROOT.gStyle.SetCanvasDefX(0)
    ROOT.gStyle.SetCanvasDefY(0)
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetFrameBorderSize(1)
    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetFrameFillStyle(0)
    ROOT.gStyle.SetFrameLineColor(1)
    ROOT.gStyle.SetFrameLineStyle(1)
    ROOT.gStyle.SetFrameLineWidth(1)

    ROOT.gStyle.SetPadTopMargin(PadTopMargin) 
    ROOT.gStyle.SetPadBottomMargin(PadBottomMargin) 
    ROOT.gStyle.SetPadLeftMargin(PadLeftMargin) 
    ROOT.gStyle.SetPadRightMargin(PadRightMargin) 
    ROOT.gStyle.SetPadRightMargin(0.05) 

    ROOT.gStyle.SetLabelSize(0.02, "XYZ") 
    ROOT.gStyle.SetTitleSize(0.02, "XYZ") 
    ROOT.gStyle.SetTitleOffset(1.2, "Y") 

    ROOT.gStyle.SetPadBorderMode(0) 
    ROOT.gStyle.SetPadColor(0) 
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetPadGridX(grid)
    ROOT.gStyle.SetPadGridY(grid)

    ROOT.gStyle.SetOptStat(stat)
    ROOT.gStyle.SetStatColor(0)
    ROOT.gStyle.SetStatBorderSize(1)

def scale_factor(ecms, mode):
    BR = 0.0938
    if int(ecms) == 4360:
        lum = 543.9
        if mode == 'D1_2420':
            XS = 41.8*BR
            Evt = 50000.0
        if mode == 'psipp':
            XS = 17.3*BR
            Evt = 50000.0
        if mode == 'DD':
            XS = 10600.0
            Evt = 17200000.0
        if mode == 'qq':
            XS = 17500.0
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
        if mode == 'D1_2420':
            XS = 65.4*BR
            Evt = 100000.0
        if mode == 'psipp':
            XS = 23.8*BR
            Evt = 100000.0
        if mode == 'DD':
            XS = 10200.0
            Evt = 40300000.0
        if mode == 'qq':
            XS = 7000.0
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
        if mode == 'D1_2420':
            XS = 27.7*BR
            Evt = 50000.0
        if mode == 'psipp':
            XS = 7.2*BR
            Evt = 50000.0
        if mode == 'DD':
            XS = 7800.0
            Evt = 12000000.0*1.5
        if mode == 'qq':
            XS = 6000.0
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
    if int(ecms) == 4360:
        WIDTH = 0.021238
    if int(ecms) == 4420:
        WIDTH = 0.021238
    if int(ecms) == 4600:
        WIDTH = 0.021238
    if not (int(ecms) == 4360 or int(ecms) == 4420 or int(ecms) == 4600):
        WIDTH = 0.021238
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
        NUM_LOW = 0
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
        MEAN_UP = 1.875
        MEAN_LOW = 1.866
        SIGMA_UP = 0.02
    elif int(ecms == 4200):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.012
    elif int(ecms == 4210):
        MEAN_UP = 1.871
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4220):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    elif int(ecms == 4230):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.0095
    elif int(ecms == 4237):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4245):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4246):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.012
    elif int(ecms == 4260):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4270):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4280):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4290):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4310):
        MEAN_UP = 1.875
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    elif int(ecms == 4315):
        MEAN_UP = 1.876
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4340):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4360):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.015
    elif int(ecms == 4380):
        MEAN_UP = 1.874
        MEAN_LOW = 1.868
        SIGMA_UP = 0.012
    elif int(ecms == 4390):
        MEAN_UP = 1.874
        MEAN_LOW = 1.868
        SIGMA_UP = 0.01
    elif int(ecms == 4400):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.008
    elif int(ecms == 4420):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4440):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.009
    elif int(ecms == 4470):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.009
    elif int(ecms == 4530):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.008
    elif int(ecms == 4600):
        MEAN_UP = 1.873
        MEAN_LOW = 1.865
        SIGMA_UP = 0.012
    return MEAN_UP, MEAN_LOW, SIGMA_UP

# upper limit parameter of rm(Dpipi) fit
def upl_rm_Dpipi(ecms):
    PARAM_BKG = 999.
    STEP_SIZE = 999.
    STEP_N = 999.
    if int(ecms == 4190):
        PARAM_BKG = -1.00344e+00
        STEP_SIZE = 0.1
        STEP_N = 600
    elif int(ecms == 4200):
        PARAM_BKG = -9.69253e-01
        STEP_SIZE = 0.1
        STEP_N = 600
    elif int(ecms == 4210):
        PARAM_BKG = -9.57997e-01
        STEP_SIZE = 0.1
        STEP_N = 1200
    elif int(ecms == 4220):
        PARAM_BKG = -9.05634e-01
        STEP_SIZE = 0.1
        STEP_N = 1500
    elif int(ecms == 4230):
        PARAM_BKG = -8.82550e-01
        STEP_SIZE = 1
        STEP_N = 500
    elif int(ecms == 4237):
        PARAM_BKG = -8.17887e-01
        STEP_SIZE = 0.1
        STEP_N = 2000
    elif int(ecms == 4245):
        PARAM_BKG = -7.80923e-01
        STEP_SIZE = 0.1
        STEP_N = 500
    elif int(ecms == 4246):
        PARAM_BKG = -8.05249e-01 
        STEP_SIZE = 1
        STEP_N = 500
    elif int(ecms == 4270):
        PARAM_BKG = 1.63352e-07
        STEP_SIZE = 1
        STEP_N = 350
    elif int(ecms == 4280):
        PARAM_BKG = -7.75574e-01
        STEP_SIZE = 0.1
        STEP_N = 1500
    elif int(ecms == 4310):
        PARAM_BKG = -6.35878e-01
        STEP_SIZE = 0.1
        STEP_N = 1500
    elif int(ecms == 4530):
        PARAM_BKG = -1.80799e-01
        STEP_SIZE = 1
        STEP_N = 500
    return PARAM_BKG, STEP_SIZE, STEP_N

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
        N_PSIPP = 500
        N_DDPIPI = 500
    elif int(ecms == 4245):
        N_D1_2420 = 0
        N_PSIPP = 500
        N_DDPIPI = 300
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
        N_D1_2420 = 5000
        N_PSIPP = 600
        N_DDPIPI = 600
    elif int(ecms == 4360):
        N_D1_2420 = 5000
        N_PSIPP = 1000
        N_DDPIPI = 1000
    elif int(ecms == 4380):
        N_D1_2420 = 2000
        N_PSIPP = 600
        N_DDPIPI = 300
    elif int(ecms == 4390):
        N_D1_2420 = 500
        N_PSIPP = 200
        N_DDPIPI = 100
    elif int(ecms == 4400):
        N_D1_2420 = 2000
        N_PSIPP = 1000
        N_DDPIPI = 300
    elif int(ecms == 4420):
        N_D1_2420 = 5000
        N_PSIPP = 5000
        N_DDPIPI = 5000
    elif int(ecms == 4440):
        N_D1_2420 = 2000
        N_PSIPP = 1000
        N_DDPIPI = 1000
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
        LUM = 539.84
    if int(ecms) == 4380:
        LUM = 500.
    if int(ecms) == 4390:
        LUM = 55.57
    if int(ecms) == 4400:
        LUM = 500.
    if int(ecms) == 4420:
        LUM = 44.67 + 1028.89
    if int(ecms) == 4440:
        LUM = 570.
    if int(ecms) == 4470:
        LUM = 111.09
    if int(ecms) == 4530:
        LUM = 112.12
    if int(ecms) == 4600:
        LUM = 566.93
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
