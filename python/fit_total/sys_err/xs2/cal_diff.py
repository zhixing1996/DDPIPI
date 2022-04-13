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

def sys_err():
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    path_params_old = '../../txts/params_BW_4390_BW_4700_PHSP.txt'
    path_sys_com = '../xs1/txts/sys_err_com.txt'
    path_xs2 = './txts/sys_err_xs2.txt'

    params_old = {}
    with open(path_params_old, 'r') as f:
        for line in f.readlines():
            fargs = line.strip().split()
            params_old[fargs[0]] = float(fargs[1])

    sys_com = 0.
    with open(path_sys_com, 'r') as f:
        fargs = f.readlines()[0].strip().split()
        sys_com = float(fargs[1])

    with open(path_xs2, 'w') as f:
        for k, v in params_old.items():
            if 'BrGam' in k:
                sys_err = sys_com/100.
                f.write(k + ' ' + str(round(sys_com, 1)) + ' ' + str(v * sys_err) + '\n')

if __name__ == '__main__':
    sys_err()
