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
    ./significance.py [ECMS]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def significance(path, r):
    try:
        f = open(path, 'r')
    except:
        logging.error(path + ' is invalid!')
        sys.exit()

    lines = f.readlines()
    likelihood_sig = float(lines[0].rstrip('\n'))
    likelihood_none_sig = float(lines[1].rstrip('\n'))
    prob = TMath.Prob(2*fabs(likelihood_sig - likelihood_none_sig), r)
    sig = RooStats.PValueToSignificance(prob * 0.5)
    print 'significance = ' + str(sig)

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()

    ecms = int(args[0])

    if ecms == 4360:
        path = './txts/significance_likelihood_' + str(ecms) + '.txt'
        num_free_para  = 1
        significance(path, num_free_para)
    if ecms == 4420:
        path = './txts/significance_likelihood_' + str(ecms) + '.txt'
        num_free_para  = 1
        significance(path, num_free_para)
    if ecms == 4600:
        path = './txts/significance_likelihood_' + str(ecms) + '.txt'
        num_free_para  = 1
        significance(path, num_free_para)

if __name__ == '__main__':
    main()
