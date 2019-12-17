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

def xs(ecms, data_path, D1_2420_path, psipp_path):
    f_data = open(data_path, 'r')
    lines_data = f_data.readlines()
    for line_data in lines_data:
        N_data = float(line_data.rstrip('\n'))

    f_psipp = open(psipp_path, 'r')
    lines_psipp = f_psipp.readlines()
    for line_psipp in lines_psipp:
        N_psipp = float(line_psipp.rstrip('\n'))
    if ecms == 4360 or ecms == 4420 or ecms == 4600:
        eff_psipp = N_psipp/500000.
    else:
        eff_psipp = N_psipp/50000.

    N_D1_2420 = 0.
    eff_D1_2420 = 0.
    if ecms >= 4310:
        f_D1_2420 = open(D1_2420_path, 'r')
        lines_D1_2420 = f_D1_2420.readlines()
        for line_D1_2420 in lines_D1_2420:
            N_D1_2420 = float(line_D1_2420.rstrip('\n'))
        if ecms == 4360 or ecms == 4420 or ecms == 4600:
            eff_D1_2420 = N_D1_2420/500000.
        else:
            eff_D1_2420 = N_D1_2420/50000.

    Br = 0.0938
    frac_D1_2420, frac_psipp, lum = data_base(ecms)
    eff = eff_psipp*frac_psipp + frac_D1_2420*eff_D1_2420
    xs = N_data/(2*eff*Br*lum)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_xs = './txts/xs_info_'+ str(ecms) +'.txt'
    f_xs = open(path_xs, 'w')
    out = '& '  + str(ecms) + 'MeV& ' + str(int(N_data)) + '& ' + str(int(N_D1_2420)) + '& ' + str(int(N_psipp))
    out += '& ' + str(round(eff_D1_2420*100, 2)) + '\%& ' + str(round(eff_psipp*100, 2)) + '\%& ' + str(round(eff*100, 2)) + '\%'
    out += '& ' + str(lum) + '& ' + str(Br*100) + '\%& ' + str(round(xs, 2))
    f_xs.write(out)
    f_xs.close()
    
if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        ecms = int(args[0])
    except:
        logging.error('python cal_xs.py [ecms]')
        sys.exit()

    if ecms < 4310:
        data_path = './txts/data_signal_events_' + str(ecms) + '.txt'
        psipp_path = './txts/psipp_signal_events_' + str(ecms) + '.txt'
        D1_2420_path = ''
        xs(ecms, data_path, D1_2420_path, psipp_path)

    if ecms >= 4310:
        data_path = './txts/data_signal_events_' + str(ecms) + '.txt'
        psipp_path = './txts/psipp_signal_events_' + str(ecms) + '.txt'
        D1_2420_path = './txts/D1_2420_signal_events_' + str(ecms) + '.txt'
        xs(ecms, data_path, D1_2420_path, psipp_path)
