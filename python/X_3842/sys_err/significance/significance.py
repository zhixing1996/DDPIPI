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

def significance(ref, target, r):
    try:
        f_ref = open(ref, 'r')
        f_target = open(target, 'r')
    except:
        logging.error(ref + ' or ' + target + ' is invalid!')
        sys.exit()

    lines_ref = f_ref.readlines()
    likelihood_none_sig = float(lines_ref[0].rstrip('\n'))
    lines_target = f_target.readlines()
    likelihood_sig = float(lines_target[0].rstrip('\n'))
    prob = TMath.Prob(2*fabs(likelihood_sig - likelihood_none_sig), r)
    sig = RooStats.PValueToSignificance(prob * 0.5)
    return sig

def main():
    ref = './txts/significance_likelihood_all_none_sig.txt'
    targets = []
    targets.append('./txts/significance_likelihood_all_fit_range.txt')
    targets.append('./txts/significance_likelihood_all_background_shape.txt')
    targets.append('./txts/significance_likelihood_all_sigma_shape.txt')
    num_free_para = 1
    sigs = []
    for target in targets:
        sigs.append(significance(ref, target, num_free_para))

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_out = './txts/significance.txt'
    f_out = open(path_out, 'w')
    out = '@all ' + str(round(min(sigs), 3)) + '\n'
    f_out.write(out)
    f_out.close()

if __name__ == '__main__':
    main()
