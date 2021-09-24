#!/usr/bin/env python
"""
Format systematic uncertainty at each energy point
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-20 Fri 21:03]"

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
    format_diff.py

SYNOPSIS
    ./format_diff.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def format():
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_sys = './txts/sys_err_omega.txt'
    f_sys = open(path_sys, 'w')

    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    for ecm in ecms:
        info_path = './txts/sys_err_' + str(ecm) + '.txt'
        f_info = open(info_path, 'r')
        lines = f_info.readlines()
        for line in lines:
            rs = line.rstrip('\n')
            rs = filter(None, rs.split(' '))
            sys_err = float(rs[0])

        out = str(ecm/1000.) + '\t' + str(sys_err) + '\n'
        f_sys.write(out)
    f_sys.close()
   
if __name__ == '__main__':
    format()
