#!/usr/bin/env python
"""
Calculate significance and efficiency
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-10-13 Thu 00:14]"

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

def xs(ecms, data_path, D1_2420_path, psipp_path, DDPIPI_path):
    f_data = open(data_path, 'r')
    lines_data = f_data.readlines()
    for line_data in lines_data:
        rs_data = line_data.rstrip('\n')
        rs_data = filter(None, rs_data.split(" "))
        N_data = float(float(rs_data[0]))
        Err_data = float(float(rs_data[1]))

    f_psipp = open(psipp_path, 'r')
    lines_psipp = f_psipp.readlines()
    for line_psipp in lines_psipp:
        rs_psipp = line_psipp.rstrip('\n')
        rs_psipp = filter(None, rs_psipp.split(" "))
        N_psipp = float(float(rs_psipp[0]))

    f_DDPIPI = open(DDPIPI_path, 'r')
    lines_DDPIPI = f_DDPIPI.readlines()
    for line_DDPIPI in lines_DDPIPI:
        rs_DDPIPI = line_DDPIPI.rstrip('\n')
        rs_DDPIPI = filter(None, rs_DDPIPI.split(" "))
        N_DDPIPI = float(float(rs_DDPIPI[0]))

    if (ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420):
        eff_psipp = N_psipp/40000.
        eff_DDPIPI = N_DDPIPI/40000.
    else:
        eff_psipp = N_psipp/20000.
        eff_DDPIPI = N_DDPIPI/20000.

    N_D1_2420 = 0.
    eff_D1_2420 = 0.
    if ecms >= 4290:
        f_D1_2420 = open(D1_2420_path, 'r')
        lines_D1_2420 = f_D1_2420.readlines()
        for line_D1_2420 in lines_D1_2420:
            rs_D1_2420 = line_D1_2420.rstrip('\n')
            rs_D1_2420 = filter(None, rs_D1_2420.split(" "))
            N_D1_2420 = float(float(rs_D1_2420[0]))
        if ecms == 4420:
            eff_D1_2420 = N_D1_2420/40000.
        else:
            eff_D1_2420 = N_D1_2420/20000.

    Br = 0.0938
    frac_D1_2420, frac_psipp, lum = data_base(ecms)
    eff = eff_psipp*frac_psipp + frac_D1_2420*eff_D1_2420
    xs = N_data/(2*eff*Br*lum)
    xs_err = Err_data/(2*eff*Br*lum)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_xs = './txts/xs_info_' + str(ecms) + '.txt'
    f_xs = open(path_xs, 'w')
    out = '& @'  + str(ecms) + 'MeV& ' + str(int(N_data)) + '& ' + str(int(N_D1_2420)) + '& ' + str(int(N_psipp))
    out += '& ' + str(round(eff_D1_2420*100, 2)) + '\%& ' + str(round(eff_psipp*100, 2)) + '\%& ' + str(round(eff*100, 2)) + '\%'
    out += '& ' + str(lum) + '& ' + str(Br*100) + '\%& ' + str(round(xs, 2)) + '\pm' + str(round(xs_err, 2)) + '& ' + str(round(eff_DDPIPI*100, 2))  + '\%& ' + str(round(Err_data, 2)) + '& \\\\\n'
    f_xs.write(out)
    f_xs.close()

    path_xs_read = './txts/xs_info_' + str(ecms) + '_read.txt'
    f_xs_read = open(path_xs_read, 'w')
    out_read = str(ecms) + ' ' + str(int(N_data)) + ' ' + str(int(N_D1_2420)) + ' ' + str(int(N_psipp))
    out_read += ' ' + str(round(eff_D1_2420*100, 2)) + ' ' + str(round(eff_psipp*100, 2)) + ' ' + str(round(eff*100, 2))
    out_read += ' ' + str(lum) + ' ' + str(Br*100) + ' ' + str(round(xs, 2)) + ' ' + str(round(xs_err, 2)) + ' ' + str(round(eff_DDPIPI*100, 2)) + ' ' + str(round(Err_data, 2)) + ' \n'
    f_xs_read.write(out_read)
    f_xs_read.close()
    
if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        ecms = int(args[0])
    except:
        logging.error('python cal_xs.py [ecms]')
        sys.exit()

    if ecms < 4290:
        data_path = './txts/data_signal_events_' + str(ecms) + '.txt'
        psipp_path = './txts/psipp_signal_events_' + str(ecms) + '.txt'
        D1_2420_path = ''
        DDPIPI_path = './txts/DDPIPI_signal_events_' + str(ecms) + '.txt'
        xs(ecms, data_path, D1_2420_path, psipp_path, DDPIPI_path)

    if ecms >= 4290:
        data_path = './txts/data_signal_events_' + str(ecms) + '.txt'
        psipp_path = './txts/psipp_signal_events_' + str(ecms) + '.txt'
        D1_2420_path = './txts/D1_2420_signal_events_' + str(ecms) + '.txt'
        DDPIPI_path = './txts/DDPIPI_signal_events_' + str(ecms) + '.txt'
        xs(ecms, data_path, D1_2420_path, psipp_path, DDPIPI_path)
