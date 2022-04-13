#!/usr/bin/env python
"""
Calculate system error at each energy point
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-02-10 Mon 18:15]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TPaveText
import sys, os
import logging
from math import *
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    cal_diff.py

SYNOPSIS
    ./cal_diff.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    February 2020
\n''')

def diff(v1, v2):
    if v1 > v2:
        return abs((v1 - v2)/v1)
    else:
        return abs((v1 - v2)/v2)

def sys_err(iloop):
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    path_params_old = '../../multi_solution/txts/params_BW_4390_BW_4700_PHSP_' + str(iloop) + '.txt'
    path_params_new = './txts/params_BW_4390_BW_4700_PHSP_' + str(iloop) + '.txt'
    path_mass_width = './txts/sys_err_spread_' + str(iloop) + '.txt'

    params_old = {}
    with open(path_params_old, 'r') as f:
        for line in f.readlines():
            fargs = line.strip().split()
            fargs[1] = float(fargs[1])
            if 'phase' in fargs[0]:
                while not (fargs[1] > 0 and fargs[1] < 2 * pi):
                    if fargs[1] > 0: fargs[1] -= 2 * pi
                    else: fargs[1] += 2 * pi
            if fargs[0] == 'phsp_c' and fargs[1] < 0: fargs[1] = abs(fargs[1])
            params_old[fargs[0]] = float(fargs[1])

    params_new = {}
    with open(path_params_new, 'r') as f:
        for line in f.readlines():
            fargs = line.strip().split()
            fargs[1] = float(fargs[1])
            if 'phase' in fargs[0]:
                fargs[1] = float(fargs[1])
                while not (fargs[1] > 0 and fargs[1] < 2 * pi):
                    if fargs[1] > 0: fargs[1] -= 2 * pi
                    else: fargs[1] += 2 * pi
            if fargs[0] == 'phsp_c' and fargs[1] < 0: fargs[1] = abs(fargs[1])
            params_new[fargs[0]] = float(fargs[1])

    with open(path_mass_width, 'w') as f:
        for k1, v1 in params_new.items():
            for k2, v2 in params_old.items():
                if k1 == k2:
                    sys_err = diff(v1, v2)*100
                    f.write(k1 + ' ' + str(round(sys_err, 1)) + ' ' + str(sys_err/100. * v1) + '\n')

if __name__ == '__main__':
    S1, S2, S3, S4 = 8, 12, 26, 28
    sys_err(S1)
    sys_err(S2)
    sys_err(S3)
    sys_err(S4)
