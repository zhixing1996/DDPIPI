#!/usr/bin/env python
"""
Smear likelihood distribution according to systematic uncertainty
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-12-03 Thu 20:42]"

import math
from array import array
from ROOT import *
import sys, os
import logging
from math import *
from tools import *
import random
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetPaperSize(20,30)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadRightMargin(0.08)
gStyle.SetPadBottomMargin(0.18)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    smear.py

SYNOPSIS
    ./smear.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2020
\n''')

def smear(path, ecms):
    try:
        f = open(path, 'r')
    except:
        logging.error(path + ' is invalid!')
        sys.exit()

    with open(path, 'r') as f:
        lines = f.readlines()
        N = len(lines) - 1
        n_set = array('f', N*[0])
        likelihood = array('f', N*[0])
        count = 0
        for i in xrange(N):
            fargs = map(float, lines[i].strip('\n').strip().split())
            n_set[i] = fargs[0]
            likelihood[i] = fargs[1]
            count += 1
    
    n_smear = 5000
    a = array('f', N*[0])

    with open('./sys_err/sum/txts/sys_err_total.txt', 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip('\n').strip().split())
            if int(fargs[0]*1000) == ecms: sys_err = fargs[1]/100.
    print 'Systematic uncertainty of {0} is {1}'.format(ecms, sys_err)

    for nbin in xrange(N):
        nevt = int(n_smear*likelihood[nbin])
        numevt = 0
        while numevt < nevt:
            bin_num = int(random.gauss(0, sys_err + 1)*(nbin)) + 1
            numevt += 1
            if bin_num < 0 or bin_num > N: continue
            a[bin_num-1] += 1
        print 'Filling {0} bin...'.format(nbin)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    with open('./txts/likelihood_smear_' + str(ecms) + '.txt', 'w') as f:
        for nbin in xrange(N):
            f.write(str(round(n_set[nbin], 2)) + ' ' + str(a[nbin]/n_smear) + '\n')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = int(args[0])

    path = './txts/upper_limit_likelihood_total_' + str(ecms) + '.txt'
    smear(path, ecms)

if __name__ == '__main__':
    main()
