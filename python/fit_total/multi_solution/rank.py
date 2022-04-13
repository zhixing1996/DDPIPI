#!/usr/bin/env python
"""
Calculate significance of X(3842)
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-05 Thu 19:11]"

import math
from array import array
import sys, os
import logging
from math import *
# from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    significance.py

SYNOPSIS
    ./significance.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def find_file(path):
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            os.listdir(file_path)  
        else:  
            file_list.append(file_path)  
    return file_list

def main():
    args = sys.argv[1:]
    if len(args)<1:
        sys.exit()
    mode = args[0]

    files = find_file('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/txts/' + mode)
    chi2 = []
    for file in files:
        if 'fit_result_' not in file: continue
        with open(file, 'r') as f:
            fargs = list(map(float, f.readlines()[0].strip().split()))
            chi2.append({'order': int(fargs[0]), 'chi2': fargs[1]})
    chi2_new = sorted(chi2, key = lambda e:e.__getitem__('chi2'))
    
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    with open('./txts/rank_chi2_' + mode + '.txt', 'w') as f:
        for chi in chi2_new:
            f.write(str(chi['order']) + ' ' + str(chi['chi2']) + '\n')

if __name__ == '__main__':
    main()
