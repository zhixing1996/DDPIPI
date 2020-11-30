#!/usr/bin/env python
"""
Calculate system error at each energy point
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-02-10 Mon 18:15]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TPaveText
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
    ./cal_diff.py [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    February 2020
\n''')

def sys_err(patch):
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_sys_err = './txts/sys_err_width.txt'
    f_sys_err = open(path_sys_err, 'w')

    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700]
    for ecm in ecms:
        path_factor_data = '../../fit_xs/txts/fit_xs/factor_m_Kpipi_' + str(ecm) + '_data.txt'
        f_factor_data = open(path_factor_data, 'r')
        lines_factor_data = f_factor_data.readlines()
        path_factor_MC = '../../fit_xs/txts/fit_xs/factor_m_Kpipi_' + str(ecm) + '_MC.txt'
        f_factor_MC = open(path_factor_MC, 'r')
        lines_factor_MC = f_factor_MC.readlines()

        for line_factor_data, line_factor_MC in zip(lines_factor_data, lines_factor_MC):
            rs_factor_data = line_factor_data.rstrip('\n')
            rs_factor_data = filter(None, rs_factor_data.split(' '))
            factor_data = float(rs_factor_data[0])
            factor_data_err = float(rs_factor_data[1])
            rs_factor_MC = line_factor_MC.rstrip('\n')
            rs_factor_MC = filter(None, rs_factor_MC.split(' '))
            factor_MC = float(rs_factor_MC[0])
            factor_MC_err = float(rs_factor_MC[1])
            diff = 0.
            if (factor_MC - factor_data) <= 0.01:
                diff = (abs(factor_MC - factor_data) + sqrt(factor_data_err**2 + factor_MC_err**2))/factor_data
            else:
                diff = sqrt(factor_data_err**2/factor_data + factor_MC_err**2/factor_MC)
            out = str(ecm/1000.) + '\t' + str(round(diff*100, 1)) + '\n'
            f_sys_err.write(out)

        f_factor_data.close()
        f_factor_MC.close()
    f_sys_err.close()
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    patch = str(args[0])

    sys_err(patch)
