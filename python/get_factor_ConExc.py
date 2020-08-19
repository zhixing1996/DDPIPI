#!/usr/bin/env python
"""
Get radiative correction factor and vacuum polarization factor
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-01-03 Fri 19:59]"

from array import array
import sys, os
import logging
from math import *
from tools import *
from ROOT import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    get_factor.py

SYNOPSIS
    ./get_factor.py [file_in] [ecms] [mode] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    January 2020
\n''')

def find_factor(file_in, ecms, mode, patch):
    target_ISR_VP = 'f_ISR'
    target_VP = '1/|1-Pi|^2'
    with open (file_in, 'r') as f_in:
        for line in f_in:
            if target_ISR_VP in line:
                rs_ISR = line.rstrip('\n')
                ISR_VP = float(rs_ISR.split(' ')[-1].split(',')[0].split('+/-')[0])
            if target_VP in line:
                rs_VP = line.rstrip('\n')
                VP = float(rs_VP.split(' ')[-1].split(',')[0].split('+/-')[0])
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_factor = './txts/factor_info_' + ecms + '_' + mode + '_' + patch + '.txt'
    f_factor = open(path_factor, 'w')
    out = str(ISR_VP/VP) + ' ' + str(VP) + '\n'
    f_factor.write(out)
    f_factor.close()

def main():
    args = sys.argv[1:]
    if len(args)<4:
        return usage()
    file_in = args[0]
    ecms = args[1]
    mode = args[2]
    patch = args[3]

    find_factor(file_in, ecms, mode, patch)

if __name__ == '__main__':
    main()
