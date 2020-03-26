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

def xs(ecms, patch, data_path, sideband_path, D1_2420_path, psipp_path, DDPIPI_path):
    f_data = open(data_path, 'r')
    lines_data = f_data.readlines()
    for line_data in lines_data:
        rs_data = line_data.rstrip('\n')
        rs_data = filter(None, rs_data.split(" "))
        N_data = float(float(rs_data[0]))
        Err_data = float(float(rs_data[1]))

    f_sideband = open(sideband_path, 'r')
    lines_sideband = f_sideband.readlines()
    for line_sideband in lines_sideband:
        rs_sideband = line_sideband.rstrip('\n')
        rs_sideband = filter(None, rs_sideband.split(" "))
        N_sideband = float(float(rs_sideband[0]))
        Err_sideband = float(float(rs_sideband[1]))

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
        eff_psipp = N_psipp/100000.
        eff_DDPIPI = N_DDPIPI/100000.
    else:
        eff_psipp = N_psipp/50000.
        eff_DDPIPI = N_DDPIPI/50000.

    N_D1_2420 = 0.
    eff_D1_2420 = 0.
    if ecms > 4290:
        f_D1_2420 = open(D1_2420_path, 'r')
        lines_D1_2420 = f_D1_2420.readlines()
        for line_D1_2420 in lines_D1_2420:
            rs_D1_2420 = line_D1_2420.rstrip('\n')
            rs_D1_2420 = filter(None, rs_D1_2420.split(" "))
            N_D1_2420 = float(float(rs_D1_2420[0]))
        if ecms == 4420:
            eff_D1_2420 = N_D1_2420/100000.
        else:
            eff_D1_2420 = N_D1_2420/50000.

    factor_path = './txts/fit_rm_D_' + str(ecms) + '_read_' + patch + '.txt'
    f_factor = open(factor_path, 'r')
    lines_factor = f_factor.readlines()
    for line_factor in lines_factor:
        rs_factor = line_factor.rstrip('\n')
        rs_factor = filter(None, rs_factor.split(' '))
        omega_D1_2420 = float(rs_factor[1])
        omega_psipp = float(rs_factor[2])
        omega_DDPIPI = float(rs_factor[3])
        ISR_D1_2420 = float(rs_factor[7])
        ISR_psipp = float(rs_factor[8])
        ISR_DDPIPI = float(rs_factor[9])
        VP = float(rs_factor[10])
        lum = float(rs_factor[11])
        Br = float(rs_factor[12])
        xs_D1_2420 = float(rs_factor[13])
        xs_psipp = float(rs_factor[14])
        xs_DDPIPI = float(rs_factor[15])
        xserr_D1_2420 = float(rs_factor[16])
        xserr_psipp = float(rs_factor[17])
        xserr_DDPIPI = float(rs_factor[18])

    if omega_D1_2420 == 0:
        flag_D1_2420 = 0
        eff_ISR_VP_D1_2420 = 1
    else:
        flag_D1_2420 = 1
        eff_ISR_VP_D1_2420 = eff_D1_2420*omega_D1_2420
    if omega_psipp == 0:
        flag_psipp = 0
        eff_ISR_VP_psipp = 1
    else:
        flag_psipp = 1
        eff_ISR_VP_psipp = eff_psipp*omega_psipp
    if omega_DDPIPI == 0:
        flag_DDPIPI = 0
        eff_ISR_VP_DDPIPI = 1
    else:
        flag_DDPIPI = 1
        eff_ISR_VP_DDPIPI = eff_DDPIPI*omega_DDPIPI
    xs = (N_data - N_sideband/2.)/(2*(flag_D1_2420*eff_ISR_VP_D1_2420 + flag_psipp*eff_ISR_VP_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI)*Br*lum)
    xs_err = (sqrt(Err_data*Err_data + (Err_sideband/2.)*(Err_sideband/2.)))/(2*(flag_D1_2420*eff_ISR_VP_D1_2420 + flag_psipp*eff_ISR_VP_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI)*Br*lum)

    if not patch == 'round0':
        if omega_D1_2420 == 0:
            flag_D1_2420 = 0
            eff_ISR_VP_D1_2420 = 1
        else:
            flag_D1_2420 = 1
            eff_ISR_VP_D1_2420 = eff_D1_2420*ISR_D1_2420*omega_D1_2420*VP
        if omega_psipp == 0:
            flag_psipp = 0
            eff_ISR_VP_psipp = 1
        else:
            flag_psipp = 1
            eff_ISR_VP_psipp = eff_psipp*ISR_psipp*omega_psipp*VP
        if omega_DDPIPI == 0:
            flag_DDPIPI = 0
            eff_ISR_VP_DDPIPI = 1
        else:
            flag_DDPIPI = 1
            eff_ISR_VP_DDPIPI = eff_DDPIPI*ISR_DDPIPI*omega_DDPIPI*VP
        xs = (N_data - N_sideband/2.)/(2*(flag_D1_2420*eff_ISR_VP_D1_2420 + flag_psipp*eff_ISR_VP_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI)*Br*lum)
        xs_err = (sqrt(Err_data*Err_data + (Err_sideband/2.)*(Err_sideband/2.)))/(2*(flag_D1_2420*eff_ISR_VP_D1_2420 + flag_psipp*eff_ISR_VP_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI)*Br*lum)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_xs = './txts/xs_info_' + str(ecms) + '_' + patch + '.txt'

    f_xs = open(path_xs, 'w')
    out = '& @' + str(ecms) + 'MeV&\n'
    out += str(int(N_data)) + '&\n'
    out += str(round(eff_D1_2420*100, 2)) + '\%&\n'
    out += str(round(eff_psipp*100, 2)) + '\%&\n'
    out += str(round(eff_DDPIPI*100, 2)) + '\%&\n'
    out += str(round(omega_D1_2420, 2)) + '&\n'
    out += str(round(omega_psipp, 2)) + '&\n'
    out += str(round(omega_DDPIPI, 2)) + '&\n'
    out += str(round(ISR_D1_2420, 2)) + '&\n' 
    out += str(round(ISR_psipp, 2)) + '&\n'
    out += str(round(ISR_DDPIPI, 2)) + '&\n'
    out += str(round(VP, 2)) + '&\n'
    out += str(lum) + '&\n'
    out += str(Br*100) + '\%&\n'
    out += str(round(xs, 2)) + '\pm' + str(round(xs_err, 2)) + '&\n'
    f_xs.write(out)
    f_xs.close()

    path_xs_read = './txts/xs_info_' + str(ecms) + '_read_' + patch + '.txt'
    f_xs_read = open(path_xs_read, 'w')
    out_read = str(ecms) + ' '
    out_read += str(int(N_data)) + ' '
    out_read += str(round(eff_D1_2420*100, 2)) + ' '
    out_read += str(round(eff_psipp*100, 2)) + ' '
    out_read += str(round(eff_DDPIPI*100, 2)) + ' '
    out_read += str(round(omega_D1_2420, 2)) + ' '
    out_read += str(round(omega_psipp, 2)) + ' '
    out_read += str(round(omega_DDPIPI, 2)) + ' '
    out_read += str(round(ISR_D1_2420, 2)) + ' '
    out_read += str(round(ISR_psipp, 2)) + ' '
    out_read += str(round(ISR_DDPIPI, 2)) + ' '
    out_read += str(round(VP, 2)) + ' '
    out_read += str(lum) + ' ' 
    out_read += str(Br*100) + ' '
    out_read += str(round(xs, 2)) + ' '
    out_read += str(round(xs_err, 2)) + ' '
    out_read += str(round(xs_D1_2420, 2)) + ' '
    out_read += str(round(xs_psipp, 2)) + ' '
    out_read += str(round(xs_DDPIPI, 2)) + ' '
    out_read += str(round(xserr_D1_2420, 2)) + ' '
    out_read += str(round(xserr_psipp, 2)) + ' '
    out_read += str(round(xserr_DDPIPI, 2))
    out_read += '\n'
    f_xs_read.write(out_read)
    f_xs_read.close()

if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        ecms = int(args[0])
        patch = args[1]
    except:
        logging.error('python cal_xs.py [ecms] [patch]')
        sys.exit()

    if ecms <= 4290:
        data_path = '../../python/txts/data_signal_events_' + str(ecms) + '_' + patch + '.txt'
        sideband_path = '../../python/txts/sideband_signal_events_' + str(ecms) + '_' + patch + '.txt'
        psipp_path = '../../python/txts/psipp_signal_events_' + str(ecms) + '_' + patch + '.txt'
        D1_2420_path = ''
        DDPIPI_path = '../../python/txts/DDPIPI_signal_events_' + str(ecms) + '_' + patch + '.txt'
        xs(ecms, patch, data_path, sideband_path, D1_2420_path, psipp_path, DDPIPI_path)

    if ecms > 4290:
        data_path = '../../python/txts/data_signal_events_' + str(ecms) + '_' + patch + '.txt'
        sideband_path = '../../python/txts/sideband_signal_events_' + str(ecms) + '_' + patch + '.txt'
        psipp_path = '../../python/txts/psipp_signal_events_' + str(ecms) + '_' + patch + '.txt'
        D1_2420_path = '../../python/txts/D1_2420_signal_events_' + str(ecms) + '_' + patch + '.txt'
        DDPIPI_path = '../../python/txts/DDPIPI_signal_events_' + str(ecms) + '_' + patch + '.txt'
        xs(ecms, patch, data_path, sideband_path, D1_2420_path, psipp_path, DDPIPI_path)
