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
    path_xs_D1_2420 = './txts/xs_D1_2420_' + patch + '.txt'
    f_xs_D1_2420 = open(path_xs_D1_2420, 'w')
    path_xs_psipp = './txts/xs_psipp_' + patch + '.txt'
    f_xs_psipp = open(path_xs_psipp, 'w')
    path_xs_DDPIPI = './txts/xs_DDPIPI_' + patch + '.txt'
    f_xs_DDPIPI = open(path_xs_DDPIPI, 'w')
    path_xs_total = './txts/xs_total_' + patch + '.txt'
    f_xs_total = open(path_xs_total, 'w')

    # ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4620, 4640, 4660, 4680]
    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600]
    for ecm in ecms:
        xs_info_path = './txts/xs_info_' + str(ecm) + '_read_' + patch + '.txt'
        f_xs_info = open(xs_info_path, 'r')
        lines_xs = f_xs_info.readlines()
        for line_xs in lines_xs:
            rs_xs = line_xs.rstrip('\n')
            rs_xs = filter(None, rs_xs.split(' '))
            N_data = int(rs_xs[1])
            eff_D1_2420 = float(rs_xs[2])/100.
            eff_psipp = float(rs_xs[3])/100.
            eff_DDPIPI = float(rs_xs[4])/100.
            omega_D1_2420 = float(rs_xs[5])
            omega_psipp = float(rs_xs[6])
            omega_DDPIPI = float(rs_xs[7])
            ISR_D1_2420 = float(rs_xs[8])
            ISR_psipp = float(rs_xs[9])
            ISR_DDPIPI = float(rs_xs[10])
            VP = float(rs_xs[11])
            lum = float(rs_xs[12])
            Br = float(rs_xs[13])/100.
            xs = float(rs_xs[14])
            xs_err = float(rs_xs[15])
            xs_D1_2420 = float(rs_xs[16])
            xs_psipp = float(rs_xs[17])
            xs_DDPIPI = float(rs_xs[18])
            xserr_D1_2420 = float(rs_xs[19])
            xserr_psipp = float(rs_xs[20])
            xserr_DDPIPI = float(rs_xs[21])

        out = '& @'  + str(ecm) + 'MeV& ' + str(N_data)
        out += '& ' + str(eff_D1_2420*100) + '\%& ' + str(eff_psipp*100) + '\%& ' + str(eff_DDPIPI*100) + '\%'
        out += '& ' + str(omega_D1_2420) + '& ' + str(omega_psipp) + '& ' + str(omega_DDPIPI)
        out += '& ' + str(ISR_D1_2420) + '& ' + str(ISR_psipp) + '& ' + str(ISR_DDPIPI) + '& ' + str(VP)
        out += '& ' + str(lum) + '& ' + str(Br*100) + '\%& ' + str(xs) + '\pm' + str(xs_err) + '&\\\\\n'
        f_xs.write(out)

        if ecm > 4290:
            if xserr_D1_2420 > 9999.:
                xserr_D1_2420 = 0.
            out_D1_2420 = str(ecm/1000.) + ' ' + str(xs_D1_2420) + ' ' + str(xserr_D1_2420) + '\n'
            f_xs_D1_2420.write(out_D1_2420)

        if xserr_psipp > 9999.:
            xserr_psipp = 0.
        out_psipp = str(ecm/1000.) + ' ' + str(xs_psipp) + ' ' + str(xserr_psipp) + '\n'
        f_xs_psipp.write(out_psipp)

        if xserr_DDPIPI > 9999.:
            xserr_DDPIPI = 0.
        out_DDPIPI = str(ecm/1000.) + ' ' + str(xs_DDPIPI) + ' ' + str(xserr_DDPIPI) + '\n'
        f_xs_DDPIPI.write(out_DDPIPI)

        out_total = str(ecm/1000.) + ' ' + str(xs) + ' ' + str(xs_err) + '\n'
        f_xs_total.write(out_total)
    f_xs.close()
    f_xs_D1_2420.close()
    f_xs_psipp.close()
    f_xs_DDPIPI.close()
    f_xs_total.close()
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    patch = str(args[0])

    format(patch)
