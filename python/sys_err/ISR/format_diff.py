#!/usr/bin/env python
"""
Calculate systematic uncertainty caused by branching fraction of D->Kpipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-04-07 Tue 23:29]"

import ROOT
from ROOT import *
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    cal_diff.py

SYNOPSIS
    ./cal_diff.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    April 2020
\n''')

def cal_diff():
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_sys_err = './txts/sys_err_ISR.txt'
    f_sys_err = open(path_sys_err, 'w')

    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    for ecm in ecms:
        out = str(ecm/1000.) + '\t' + str(2.8) + '\n'
        f_sys_err.write(out)
    f_sys_err.close()

if __name__ == '__main__':
    cal_diff()
