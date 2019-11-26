#!/usr/bin/env python
"""
Common tools 
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-13 Tue 15:05]" 

import sys 
import os
import ROOT 


# ---------------------------------------------
# Function 
# ---------------------------------------------

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
    
def scale_factor(energy, mode):
    BR = 0.0938
    if int(energy) == 4360:
        lum = 539.84
        if mode == 'D1_2420':
            XS = 41.8*BR
            Evt = 500000.0
        if mode == 'psipp':
            XS = 17.3*BR
            Evt = 500000.0
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
    if int(energy) == 4420:
        lum = 44.67 + 1028.89
        if mode == 'D1_2420':
            XS = 65.4*BR
            Evt = 500000.0
        if mode == 'psipp':
            XS = 23.8*BR
            Evt = 500000.0
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
    if int(energy) == 4600:
        lum = 566.93
        if mode == 'D1_2420':
            XS = 27.7*BR
            Evt = 500000.0
        if mode == 'psipp':
            XS = 7.2*BR
            Evt = 500000.0
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
    if int(ecms) == 4360:
        WIDTH = 0.018648
    if int(ecms) == 4420:
        WIDTH = 0.019166
    if int(ecms) == 4600:
        WIDTH = 0.021238
    return WIDTH

# signal window for RM(Dpipi)
def window(ecms):
    if int(ecms) == 4360:
        WINDOW = 0.0146666666667
    if int(ecms) == 4420:
        WINDOW = 0.0146666666667
    if int(ecms) == 4600:
        WINDOW = 0.018
    return WINDOW
