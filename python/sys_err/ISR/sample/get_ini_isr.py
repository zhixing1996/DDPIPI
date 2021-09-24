#!/usr/bin/env python
"""
Get initialized ISR factors
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2021-04-25 Sun 04:01]"

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
    get_ini_isr.py

SYNOPSIS
    ./get_ini_isr.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    April 2021
\n''')

def format(mode):
    if not os.path.exists('./log/'):
        os.makedirs('./log/')
    path_sys = './log/isr_' + mode + '_ini.txt'
    f_sys = open(path_sys, 'w')
    f_sys.write('sample isr\n')

    if not mode == 'D1_2420': samples = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    else: samples = [4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    for sample in samples:
        info_path = '../txts/factor_info_' + str(sample) + '_' + mode + '_round0.txt'
        f_info = open(info_path, 'r')
        lines = f_info.readlines()
        for line in lines:
            rs = line.rstrip('\n')
            rs = filter(None, rs.split(' '))
            isr = float(rs[0])

        out = str(sample) + '    ' + str(isr) + '\n'
        f_sys.write(out)
    f_sys.close()
   
if __name__ == '__main__':
    args = sys.argv[1:]
    mode = args[0]

    format(mode)
