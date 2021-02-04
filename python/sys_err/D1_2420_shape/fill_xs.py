#!/usr/bin/env python
"""
Plot cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-11-06 Fri 23:18]"

from ROOT import TGraphAsymmErrors, TGraphErrors
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    fill_xs.py

SYNOPSIS
    ./fill_xs.py [mode] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def fill_xs(mode, patch):
    lines_out = []
    for line in open('./txts/xs_' + mode + '_' + patch + '_num.txt'):
        if '#' in line: line = line.replace('#', '')
        try:
            fargs = map(float, line.strip().split())
            sample, ecms, lum, br, nsig, nsigerrl, nsigerrh = fargs[0], fargs[1], fargs[2], fargs[3], fargs[4], fargs[5], fargs[6]
            eff, isr, vp, N0 = fargs[7],  fargs[8],  fargs[9], fargs[10]
            xs = nsig/(2*lum*eff*br*isr*vp)
            xserrl = sqrt(3)*nsigerrl/(2*lum*eff*br*isr*vp)
            xserrh = sqrt(3)*nsigerrh/(2*lum*eff*br*isr*vp)
            lines_out.append('{:<7.0f}{:<10.5f}{:<10.2f}{:<10.5f}{:<10.3f}{:<10.3f}{:<10.3f}{:<10.3f}{:<10.5f}{:<10.5f}{:<10.5f}\n'.format(sample, ecms, lum, br, xs, xserrl, xserrh, eff, isr, vp, N0))
        except Exception as e:
            lines_out.append(line.replace('nsignal', 'xs').replace('nserrl', 'xserrl').replace('nserrh', 'xserrh'))
    with open('./txts/xs_' + mode + '_' + patch + '.txt', 'w') as f:
        for line_out in lines_out:
            f.write(line_out)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    mode = args[0]
    patch = args[1]

    fill_xs(mode, patch)
