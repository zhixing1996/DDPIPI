#!/usr/bin/env python
"""
Modify cross section
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
    modify_xs.py

SYNOPSIS
    ./modify_xs.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def modify():
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_xs = './txts/xs_info_modified.txt'
    f_xs = open(path_xs, 'w')
    path_xs_read = './txts/xs_info_modified_read.txt'
    f_xs_read = open(path_xs_read, 'w')
    path_xs_D1_2420 = './txts/xs_info_D1_2420.txt'
    f_xs_D1_2420 = open(path_xs_D1_2420, 'w')
    path_xs_psipp = './txts/xs_info_psipp.txt'
    f_xs_psipp = open(path_xs_psipp, 'w')
    path_xs_DDPIPI = './txts/xs_info_DDPIPI.txt'
    f_xs_DDPIPI = open(path_xs_DDPIPI, 'w')

    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4310, 4360, 4390, 4420, 4470, 4530, 4600]
    for ecm in ecms:
        double_path = './txts/fit_rm_D_' + str(ecm) + '_read.txt'
        f_double = open(double_path, 'r')
        lines_double = f_double.readlines()
        for line_double in lines_double:
            rs_double = line_double.rstrip('\n')
            rs_double = filter(None, rs_double.split(' '))
            lum = float(rs_double[5])
            Br = float(rs_double[6])/100.
            xs_D1_2420 = float(rs_double[7])
            xs_psipp = float(rs_double[8])

        total_path = './txts/xs_info_' + str(ecm) + '_read.txt'
        f_total = open(total_path, 'r')
        lines_total = f_total.readlines()
        for line_total in lines_total:
            rs_total = line_total.rstrip('\n')
            rs_total = filter(None, rs_total.split(' '))
            N_data = float(rs_total[1])
            eff_D1_2420 = float(rs_total[4])/100.
            eff_psipp = float(rs_total[5])/100.
            xs_total = float(rs_total[-4])
            xs_total_err = float(rs_total[-3])
            eff_DDPIPI = float(rs_total[-2])/100.
            Err_N_data = float(rs_total[-1])

        xs_DDPIPI = xs_total - xs_D1_2420 - xs_psipp
        if xs_DDPIPI >= 0:
            xs_DDPIPI = xs_DDPIPI
        else:
            xs_DDPIPI = 0

        eff = eff_D1_2420*xs_D1_2420/(xs_D1_2420 + xs_psipp + xs_DDPIPI) + eff_psipp*xs_psipp/(xs_D1_2420 + xs_psipp + xs_DDPIPI) + eff_DDPIPI*xs_DDPIPI/(xs_D1_2420 + xs_psipp + xs_DDPIPI)
        xs = N_data/2./Br/eff/lum
        xs_err = Err_N_data/2./Br/eff/lum
        out = '& @'  + str(ecm) + 'MeV& ' + str(int(N_data))
        out += '& ' + str(round(eff_D1_2420*100, 2)) + '\%& ' + str(round(eff_psipp*100, 2)) + '\%& ' + str(round(eff_DDPIPI*100, 2)) + '\%& ' + str(round(eff*100, 2)) + '\%'
        out += '& ' + str(lum) + '& ' + str(Br*100) + '\%& ' + str(round(xs, 2)) + '\pm' + str(round(xs_err, 2)) + '& \\\\\n'
        f_xs.write(out)
        out_read = str(ecm) + ' ' + str(int(N_data))
        out_read += ' ' + str(round(eff_D1_2420*100, 2)) + ' ' + str(round(eff_psipp*100, 2)) + ' ' + str(round(eff_DDPIPI*100, 2)) + ' ' + str(round(eff*100, 2))
        out_read += ' ' + str(lum) + ' ' + str(Br*100) + ' ' + str(round(xs, 2)) + ' ' + str(round(xs_err, 2)) + ' \n'
        f_xs_read.write(out_read)
        if ecm >= 4290:
            out_D1_2420 = str(ecm/1000.) + ' ' + str(xs_D1_2420) + '\n'
            f_xs_D1_2420.write(out_D1_2420)
        out_psipp = str(ecm/1000.) + ' ' + str(xs_psipp) + '\n'
        f_xs_psipp.write(out_psipp)
        out_DDPIPI = str(ecm/1000.) + ' ' + str(xs_DDPIPI) + '\n'
        f_xs_DDPIPI.write(out_DDPIPI)
    f_xs.close()
    f_xs_read.close()
    f_xs_D1_2420.close()
    f_xs_psipp.close()
    f_xs_DDPIPI.close()
    
if __name__ == '__main__':
    usage()
    modify()
