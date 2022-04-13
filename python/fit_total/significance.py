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

def significance(path, target, others):
    likelihood = []
    ndf = []
    for p in path:
        with open(p, 'r') as f:
            lines = f.readlines()
            likelihood.append(float(lines[0].rstrip('\n')))
            ndf.append(float(lines[1].rstrip('\n')))
    r = int(abs(ndf[0] - ndf[1]))
    prob = TMath.Prob(2*fabs(likelihood[0] - likelihood[1]), r)
    sig = RooStats.PValueToSignificance(prob * 0.5)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    label = target
    for o in others: label += '/' + o
    path_out = './txts/significance.txt'
    f_out = open(path_out, 'a+')
    out = target + '@' + label + ':' + str(round(sig, 3)) + '\n'
    f_out.write(out)
    f_out.close()

def find_file(path):
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            os.listdir(file_path)  
        else:  
            file_list.append(file_path)  
    return file_list

def main(target, others):
    files = find_file('./txts/')
    path = []
    for file in files:
        if 'likelihood' not in file: continue
        if all([o in file and target in file for o in others]):
            if (file.count('BW') + file.count('PHSP')) == len(others) + 1:
                path.append(file)
                print 'input target file: ' + file
        elif all([o in file for o in others]):
            if (file.count('BW') + file.count('PHSP')) == len(others):
                path.append(file)
                print 'input others file: ' + file
    significance(path, target, others)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    target = args[0]
    others = args[1:]
    main(target, others)
