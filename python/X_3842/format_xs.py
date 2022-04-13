#!/usr/bin/env python
"""
Format cross sections at each energy point
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
    format_xs.py

SYNOPSIS
    ./format_xs.py [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def format(patch):
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_xs = './txts/xs_' + patch + '.txt'
    f_xs = open(path_xs, 'w')

    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4246, 4260, 4270, 4290, 4315, 4340, 4360, 4380, 4400, 4420, 4440, 4600, 4620, 4640, 4660, 4680, 4700, 4750, 4780, 4840, 4914, 4946]
    for ecm in ecms:
        xs_info_path = './txts/xs_info_' + str(ecm) + '_read_' + patch + '.txt'
        f_xs_info = open(xs_info_path, 'r')
        lines_xs = f_xs_info.readlines()
        for line_xs in lines_xs:
            rs_xs = line_xs.rstrip('\n')
            rs_xs = filter(None, rs_xs.split(' '))
            N_data = int(rs_xs[1])
            eff_X_3842 = float(rs_xs[8])/100.
            ISR_X_3842 = float(rs_xs[9])
            VP = float(rs_xs[10])
            lum = float(rs_xs[11])
            Br = float(rs_xs[12])/100.
            xs = float(rs_xs[13])
            xs_err = float(rs_xs[14])

        out_total = str(ecm/1000.) + ' ' + str(xs) + ' ' + str(xs_err) + '\n'
        f_xs.write(out_total)
    f_xs.close()
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    patch = str(args[0])

    format(patch)
