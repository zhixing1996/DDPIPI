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

    if (ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420 or ecms == 4680):
        eff_psipp = N_psipp/100000.
        eff_DDPIPI = N_DDPIPI/100000.
    else:
        eff_psipp = N_psipp/50000.
        eff_DDPIPI = N_DDPIPI/50000.

    N_D1_2420 = 0.
    eff_D1_2420 = 0.
    if ecms > 4316:
        f_D1_2420 = open(D1_2420_path, 'r')
        lines_D1_2420 = f_D1_2420.readlines()
        for line_D1_2420 in lines_D1_2420:
            rs_D1_2420 = line_D1_2420.rstrip('\n')
            rs_D1_2420 = filter(None, rs_D1_2420.split(" "))
            N_D1_2420 = float(float(rs_D1_2420[0]))
        if ecms == 4420 or ecms == 4680:
            eff_D1_2420 = N_D1_2420/100000.
        else:
            eff_D1_2420 = N_D1_2420/50000.

    xs_D1_2420, xserr_D1_2420, ISR_D1_2420, VP, lum, Br = 0., 0., 0, 1., 1., 0.0938
    if ecms > 4316:
        D1_2420_path = './txts/xs_D1_2420_' + patch + '.txt'
        with open(D1_2420_path, 'r') as f:
            for line in f.readlines():
                if '#' in line: line = line.strip('#')
                try:
                    fargs = map(float, line.strip().strip('\n').split())
                    if fargs[0] == ecms:
                        lum = fargs[2]
                        Br = fargs[3]
                        xs_D1_2420 = fargs[4]
                        xserr_D1_2420 = fargs[5]
                except:
                    '''
                    '''
    DDPIPI_path = './txts/xs_DDPIPI_' + patch + '.txt'
    with open(DDPIPI_path, 'r') as f:
        for line in f.readlines():
            if '#' in line: line = line.strip('#')
            try:
                fargs = map(float, line.strip().strip('\n').split())
                if fargs[0] == ecms:
                    lum = fargs[2]
                    Br = fargs[3]
                    xs_DDPIPI = fargs[4]
                    xserr_DDPIPI = fargs[5]
            except:
                '''
                '''
    psipp_path = './txts/xs_psipp_' + patch + '.txt'
    with open(psipp_path, 'r') as f:
        for line in f.readlines():
            if '#' in line: line = line.strip('#')
            try:
                fargs = map(float, line.strip().strip('\n').split())
                if fargs[0] == ecms:
                    lum = fargs[2]
                    Br = fargs[3]
                    xs_psipp = fargs[4]
                    xserr_psipp = fargs[5]
            except:
                '''
                '''
    if ecms > 4316:
        with open('../txts/factor_info_' + str(ecms) + '_D1_2420_' + patch + '.txt', 'r') as f:
            for line in f.readlines():
                fargs = map(float, line.strip().strip('\n').split())
                ISR_D1_2420, VP = fargs[0], fargs[1]
    with open('../txts/factor_info_' + str(ecms) + '_DDPIPI_' + patch + '.txt', 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().strip('\n').split())
            ISR_DDPIPI, VP = fargs[0], fargs[1]
    with open('../txts/factor_info_' + str(ecms) + '_psipp_' + patch + '.txt', 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().strip('\n').split())
            ISR_psipp, VP = fargs[0], fargs[1]
    omega_D1_2420 = xs_D1_2420/(xs_D1_2420 + xs_DDPIPI + xs_psipp)
    omega_DDPIPI = xs_DDPIPI/(xs_D1_2420 + xs_DDPIPI + xs_psipp)
    omega_psipp = xs_psipp/(xs_D1_2420 + xs_DDPIPI + xs_psipp)

    mKpipi_data = open('./txts/factor_m_Kpipi_' + str(ecms) + '_data.txt', 'r')
    lines_mKpipi_data = mKpipi_data.readlines()
    for line_mKpipi_data in lines_mKpipi_data:
        rs_mKpipi_data = line_mKpipi_data.rstrip('\n')
        rs_mKpipi_data = filter(None, rs_mKpipi_data.split(" "))
        mKpipi_data = float(float(rs_mKpipi_data[0]))
        mKpipi_data_err = float(float(rs_mKpipi_data[1]))

    mKpipi_MC = open('./txts/factor_m_Kpipi_' + str(ecms) + '_MC.txt', 'r')
    lines_mKpipi_MC = mKpipi_MC.readlines()
    for line_mKpipi_MC in lines_mKpipi_MC:
        rs_mKpipi_MC = line_mKpipi_MC.rstrip('\n')
        rs_mKpipi_MC = filter(None, rs_mKpipi_MC.split(" "))
        mKpipi_MC = float(float(rs_mKpipi_MC[0]))
        mKpipi_MC_err = float(float(rs_mKpipi_MC[1]))

    factor_mKpipi = 1.
    if (fabs(mKpipi_MC - mKpipi_data)) > 0.01:
        factor_mKpipi = mKpipi_data/mKpipi_MC

    if omega_D1_2420 == 0:
        flag_D1_2420 = 0
        eff_ISR_VP_D1_2420 = 1
    else:
        flag_D1_2420 = 1
        eff_ISR_VP_D1_2420 = eff_D1_2420*ISR_D1_2420*omega_D1_2420*VP*factor_mKpipi
    if omega_psipp == 0:
        flag_psipp = 0
        eff_ISR_VP_psipp = 1
    else:
        flag_psipp = 1
        eff_ISR_VP_psipp = eff_psipp*ISR_psipp*omega_psipp*VP*factor_mKpipi
    if omega_DDPIPI == 0:
        flag_DDPIPI = 0
        eff_ISR_VP_DDPIPI = 1
    else:
        flag_DDPIPI = 1
        eff_ISR_VP_DDPIPI = eff_DDPIPI*ISR_DDPIPI*omega_DDPIPI*VP*factor_mKpipi
    xs = (N_data - N_sideband/2.)/(2*(flag_D1_2420*eff_ISR_VP_D1_2420 + flag_psipp*eff_ISR_VP_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI)*Br*lum)
    xs_err = (sqrt(Err_data*Err_data + (Err_sideband/2.)*(Err_sideband/2.)))/(2*(flag_D1_2420*eff_ISR_VP_D1_2420 + flag_psipp*eff_ISR_VP_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI)*Br*lum)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_xs = './txts/xs_info_' + str(ecms) + '_' + patch + '.txt'

    f_xs = open(path_xs, 'w')
    out = '@' + str(ecms) + 'MeV\n'
    out += str(int(N_data)) + ' $\pm$ ' + str(int(Err_data)) + '\n'
    out += str(int(N_sideband)) + ' $\pm$ ' + str(int(Err_sideband)) + '\n'
    out += str(round(factor_mKpipi, 4)) + '\n'
    out += str(round(eff_D1_2420*100, 2)) + '\%\n'
    out += str(round(eff_psipp*100, 2)) + '\%\n'
    out += str(round(eff_DDPIPI*100, 2)) + '\%\n'
    out += str(round(omega_D1_2420, 2)) + '\n'
    out += str(round(omega_psipp, 2)) + '\n'
    out += str(round(omega_DDPIPI, 2)) + '\n'
    out += str(round(ISR_D1_2420, 2)) + '\n' 
    out += str(round(ISR_psipp, 2)) + '\n'
    out += str(round(ISR_DDPIPI, 2)) + '\n'
    out += str(round(VP, 2)) + '\n'
    out += str(Br*100) + '\%\n'
    out += str(lum) + '\n'
    out += str(round(xs, 2)) + ' $\pm$ ' + str(round(xs_err, 2)) + '\n'
    f_xs.write(out)
    f_xs.close()

    path_xs_read = './txts/xs_info_' + str(ecms) + '_read_' + patch + '.txt'
    f_xs_read = open(path_xs_read, 'w')
    out_read = str(ecms) + ' '
    out_read += str(int(N_data)) + ' ' + str(int(Err_data)) + ' '
    out_read += str(int(N_sideband)) + ' ' + str(int(Err_sideband)) + ' '
    out_read += str(round(factor_mKpipi, 4)) + ' '
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

    if ecms <= 4316:
        data_path = './txts/data_signal_events_' + str(ecms) + '_' + patch + '.txt'
        sideband_path = './txts/sideband_signal_events_' + str(ecms) + '_' + patch + '.txt'
        psipp_path = './txts/psipp_signal_events_' + str(ecms) + '_' + patch + '.txt'
        D1_2420_path = ''
        DDPIPI_path = './txts/DDPIPI_signal_events_' + str(ecms) + '_' + patch + '.txt'
        xs(ecms, patch, data_path, sideband_path, D1_2420_path, psipp_path, DDPIPI_path)

    if ecms > 4316:
        data_path = './txts/data_signal_events_' + str(ecms) + '_' + patch + '.txt'
        sideband_path = './txts/sideband_signal_events_' + str(ecms) + '_' + patch + '.txt'
        psipp_path = './txts/psipp_signal_events_' + str(ecms) + '_' + patch + '.txt'
        D1_2420_path = './txts/D1_2420_signal_events_' + str(ecms) + '_' + patch + '.txt'
        DDPIPI_path = './txts/DDPIPI_signal_events_' + str(ecms) + '_' + patch + '.txt'
        xs(ecms, patch, data_path, sideband_path, D1_2420_path, psipp_path, DDPIPI_path)
