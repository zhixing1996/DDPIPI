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
    ./cal_diff.py [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    February 2020
\n''')

def sys_err(patch):
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    path_xs_old = '../../python/txts/xs_total_' + patch + '.txt'
    f_xs_old = open(path_xs_old, 'r')
    lines_xs_old = f_xs_old.readlines()
    path_xs_new = './txts/xs_total_' + patch + '.txt'
    f_xs_new = open(path_xs_new, 'r')
    lines_xs_new = f_xs_new.readlines()
    path_sys_err = './txts/sys_err.txt'
    f_sys_err = open(path_sys_err, 'w')

    for line_xs_old, line_xs_new in zip(lines_xs_old, lines_xs_new):
        rs_xs_old = line_xs_old.rstrip('\n')
        rs_xs_old = filter(None, rs_xs_old.split(' '))
        ecms = float(rs_xs_old[0])
        xs_old = float(rs_xs_old[1])
        xs_err_old = float(rs_xs_old[2])
        rs_xs_new = line_xs_new.rstrip('\n')
        rs_xs_new = filter(None, rs_xs_new.split(' '))
        xs_new = float(rs_xs_new[1])
        xs_err_new = float(rs_xs_new[2])
        if xs_old == 0:
            diff = 0.
        else:
            diff = abs((xs_new - xs_old)/xs_old)
        out = str(ecms) + ' ' + str(round(diff*100, 3)) + '\n'
        f_sys_err.write(out)

    f_sys_err.close()
    f_xs_old.close()
    f_xs_new.close()
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    patch = str(args[0])

    sys_err(patch)
