#!/usr/bin/env python
"""
Calculate cross section differences between two patches
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-02-14 Fri 16:09]"

import ROOT
from ROOT import *
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    cal_diff.py

SYNOPSIS
    ./cal_diff.py [patch1] [patch2]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    January 2020
\n''')

def cal_diff(patch1, patch2):
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    path_xs_diff = './txts/sys_err_ISR.txt'
    f_xs_diff = open(path_xs_diff, 'w')

    path1 = './txts/xs_total_' + patch1 + '_plot.txt'
    path2 = '../../fit_xs/txts/xs_total_' + patch2 + '_plot.txt'
    XS1, XS2 = open(path1, 'r'), open(path2, 'r')
    for line1, line2 in zip(XS1, XS2):
        info1 = line1.strip().split()
        info2 = line2.strip().split()
        finfo1 = map(float, info1)
        finfo2 = map(float, info2)
        ecms, xs1 = finfo1[0], finfo1[1]
        ecms, xs2 = finfo2[0], finfo2[1]
        if xs1 == 0 or xs2 == 0:
            diff = 0
        else:
            diff = abs((xs2 - xs1)/xs2)
        out = str(ecms) + '\t' + str(round(diff*100, 1)) + '\n'
        f_xs_diff.write(out)
    f_xs_diff.close()

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    patch1 = str(args[0])
    patch2 = str(args[1])

    cal_diff(patch1, patch2)
