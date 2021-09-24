#!/usr/bin/env python
"""
Calculate significance of X(3842)
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-05 Thu 19:11]"

import math
from array import array
from ROOT import *
import sys, os
import logging
from math import *
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    significance.py

SYNOPSIS
    ./significance.py [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def significance(mode, path):
    likelihood = []
    ndf = []
    for p in path:
        with open(p, 'r') as f:
            lines = f.readlines()
            likelihood.append(float(lines[0].rstrip('\n')))
            ndf.append(float(lines[1].rstrip('\n')))
    r = int(abs(ndf[0] - ndf[1]))
    if mode == 'DDPIPI': r += 1
    prob = TMath.Prob(2*fabs(likelihood[0] - likelihood[1]), r)
    sig = RooStats.PValueToSignificance(prob * 0.5)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_out = './txts/significance_' + mode + '.txt'
    f_out = open(path_out, 'w')
    out = '@' + mode + ' ' + str(round(sig, 3)) + '\n'
    f_out.write(out)
    f_out.close()

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    mode = args[0]

    path = []
    path.append('/besfs5/groups/cal/dedx/jingmq/bes/fit_xs/txts/likelihood_' + mode + '.txt')
    path.append('./txts/likelihood_' + mode + '.txt')
    significance(mode, path)

if __name__ == '__main__':
    main()
