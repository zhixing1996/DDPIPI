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

    path_xs_old = '../../txts/xs_' + patch + '.txt'
    f_xs_old = open(path_xs_old, 'r')
    lines_xs_old = f_xs_old.readlines()
    path_xs_new = './txts/xs_' + patch + '.txt'
    f_xs_new = open(path_xs_new, 'r')
    lines_xs_new = f_xs_new.readlines()
    path_sys_err = './txts/sys_err_background_shape.txt'
    f_sys_err = open(path_sys_err, 'w')

    for line_xs_old in lines_xs_old:
        fargs_old = map(float, line_xs_old.strip().split())
        ecms = fargs_old[0]
        xs_old = fargs_old[1]
        err_xs_old = fargs_old[2]
        for line_xs_new in lines_xs_new:
            fargs_new = map(float, line_xs_new.strip().split())
            if not ecms == fargs_new[0]: continue
            xs_new = fargs_new[1]
            err_xs_new = fargs_new[2]
            if xs_old == 0:
                diff = 0.
            else:
                if xs_new > xs_old:
                    diff = abs((xs_new - xs_old)/xs_new)
                    err_diff = sqrt(xs_old**2/xs_new**4*err_xs_new**2 + 1./xs_new**2*err_xs_new**2)
                else:
                    diff = abs((xs_new - xs_old)/xs_old)
                    err_diff = sqrt(xs_new**2/xs_old**4*err_xs_old**2 + 1./xs_old**2*err_xs_new**2)

    for line_xs_old in lines_xs_old:
        fargs_old = map(float, line_xs_old.strip().split())
        ecms = fargs_old[0]
        out = str(ecms) + '\t' + str(round(diff*100, 1)) + '\n'
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
