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
    ./significance.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def significance(ecms, path, r):
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

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_out = './txts/significance.txt'
    f_out = open(path_out, 'a')
    out = '@' + str(ecms) + ' ' + str(round(sig, 3)) + '\n'
    f_out.write(out)
    f_out.close()

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    try:
        ecms = int(args[0])
    except:
        ecms = args[0]

    path = './txts/significance_likelihood_total_' + str(ecms) + '.txt'
    if ecms == 4680: num_free_para  = 3
    else: num_free_para = 1
    significance(ecms, path, num_free_para)

if __name__ == '__main__':
    main()
