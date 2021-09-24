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
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

Nrand = 500

def readN(f_path):
    with open(f_path, 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().split())
    return fargs

def xs(ecms, patch, signal_path, sideband_path):
    '''
    Efficiency
    '''
    fargs = readN(signal_path[0])
    N_data, Err_data = fargs[0], fargs[1]

    N_D1_2420 = 0.
    if ecms > 4316:
        fargs = readN(signal_path[1])
        N_D1_2420 = fargs[0]

    fargs = readN(signal_path[2])
    N_psipp = fargs[0]

    fargs = readN(signal_path[3])
    N_DDPIPI = fargs[0]

    N_data_sideband = 0
    Err_data_sideband = 0
    fargs = readN(sideband_path[0])
    N_data_sideband, Err_data_sideband = fargs[0], fargs[1]

    N_D1_2420_sideband = 0.
    if ecms > 4316:
        fargs = readN(sideband_path[1])
        N_D1_2420_sideband = fargs[0]

    fargs = readN(sideband_path[2])
    N_psipp_sideband = fargs[0]

    fargs = readN(sideband_path[3])
    N_DDPIPI_sideband = fargs[0]

    if (ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420 or ecms == 4680):
        eff_psipp = (N_psipp - N_psipp_sideband/2.)/100000.
        eff_DDPIPI = (N_DDPIPI - N_DDPIPI_sideband/2.)/100000.
    else:
        eff_psipp = (N_psipp - N_psipp_sideband/2.)/50000.
        eff_DDPIPI = (N_DDPIPI - N_DDPIPI_sideband/2.)/50000.

    eff_D1_2420 = 0.
    if ecms > 4316:
        if ecms == 4420 or ecms == 4680:
            eff_D1_2420 = (N_D1_2420 - N_D1_2420_sideband/2.)/100000.
        else:
            eff_D1_2420 = (N_D1_2420 - N_D1_2420_sideband/2.)/50000.

    '''
    ISR_D1_2420, VP, lum, Br
    '''
    xs_D1_2420, xserr_D1_2420, ISR_D1_2420, VP, lum, Br = 0., 0., 0, 1., 1., 0.0938
    if ecms > 4316:
        D1_2420_path = '../../fit_xs/txts/xs_D1_2420_' + patch + '.txt'
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
    DDPIPI_path = '../../fit_xs/txts/xs_DDPIPI_' + patch + '.txt'
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
    psipp_path = '../../fit_xs/txts/xs_psipp_' + patch + '.txt'
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
        with open('../../txts/factor_info_' + str(ecms) + '_D1_2420_' + patch + '.txt', 'r') as f:
            for line in f.readlines():
                fargs = map(float, line.strip().strip('\n').split())
                ISR_D1_2420, VP = fargs[0], fargs[1]
    with open('../../txts/factor_info_' + str(ecms) + '_DDPIPI_' + patch + '.txt', 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().strip('\n').split())
            ISR_DDPIPI, VP = fargs[0], fargs[1]
    with open('../../txts/factor_info_' + str(ecms) + '_psipp_' + patch + '.txt', 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().strip('\n').split())
            ISR_psipp, VP = fargs[0], fargs[1]
    omega_D1_2420 = xs_D1_2420/(xs_D1_2420 + xs_DDPIPI + xs_psipp)
    omega_DDPIPI = xs_DDPIPI/(xs_D1_2420 + xs_DDPIPI + xs_psipp)
    omega_psipp = xs_psipp/(xs_D1_2420 + xs_DDPIPI + xs_psipp)

    '''
    f factor
    '''
    fargs = readN('../K_p/txts/f_K_p.txt')
    factor_K_p = fargs[0]

    fargs = readN('../m_pipi/txts/f_m_pipi.txt')
    factor_m_pipi = fargs[0]

    fargs = readN('../VrVz/txts/f_VrVz.txt')
    factor_VrVz = fargs[0]

    with open('../../fit_xs/txts/factor_m_Kpipi_' + str(ecms) + '_data_' + patch + '.txt', 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().split())
            mKpipi_data, mKpipi_data_err = fargs[0], fargs[1]
    with open('../../fit_xs/txts/factor_m_Kpipi_' + str(ecms) + '_MC_' + patch + '.txt', 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().split())
            mKpipi_MC, mKpipi_MC_err = fargs[0], fargs[1]
    f = mKpipi_data/mKpipi_MC
    f_err = sqrt(f**2*(mKpipi_data_err**2/mKpipi_data**2 + mKpipi_MC_err**2/mKpipi_MC**2))
    if abs(1 - f)/f_err > 1.: factor_m_Kpipi = f
    else: factor_m_Kpipi = 1.

    fargs = readN('../window/txts/f_rm_Dpipi.txt')
    factor_rm_Dpipi = fargs[0]

    '''
    xs calculation
    '''
    if omega_D1_2420 == 0:
        flag_D1_2420 = 0
        eff_ISR_VP_D1_2420 = 1
    else:
        flag_D1_2420 = 1
        eff_ISR_VP_D1_2420 = eff_D1_2420*ISR_D1_2420*VP*factor_K_p*factor_m_pipi*factor_VrVz*factor_m_Kpipi*factor_rm_Dpipi
    if omega_psipp == 0:
        flag_psipp = 0
        eff_ISR_VP_psipp = 1
    else:
        flag_psipp = 1
        eff_ISR_VP_psipp = eff_psipp*ISR_psipp*VP*factor_K_p*factor_m_pipi*factor_VrVz*factor_m_Kpipi*factor_rm_Dpipi
    if omega_DDPIPI == 0:
        flag_DDPIPI = 0
        eff_ISR_VP_DDPIPI = 1
    else:
        flag_DDPIPI = 1
        eff_ISR_VP_DDPIPI = eff_DDPIPI*ISR_DDPIPI*VP*factor_K_p*factor_m_pipi*factor_VrVz*factor_m_Kpipi*factor_rm_Dpipi
    xs_old = (N_data - N_data_sideband/2.)/(2*(flag_D1_2420*eff_ISR_VP_D1_2420*omega_D1_2420 + flag_psipp*eff_ISR_VP_psipp*omega_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI*omega_DDPIPI)*Br*lum)
    # print flag_D1_2420, eff_D1_2420, ISR_D1_2420, omega_D1_2420, flag_psipp, eff_psipp, ISR_psipp, omega_psipp, flag_DDPIPI, eff_DDPIPI, ISR_DDPIPI, omega_DDPIPI

    '''
    Output
    '''
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_diff = './txts/xs_diff_' + str(ecms) + '.txt'
    f_diff = open(path_diff, 'w')
    out = ''

    for i in xrange(Nrand):
        with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/omega/' + str(ecms) + '/omega_' + str(ecms) + '_' +str(i) + '.txt', 'r') as f:
            if ecms < 4316:
                omega_D1_2420 = 0.
                line = f.readlines()[0]
                fargs = map(float, line.strip().split())
                omega_psipp, omega_DDPIPI = fargs[0], fargs[1]
            else:
                line = f.readlines()[0]
                fargs = map(float, line.strip().split())
                omega_D1_2420, omega_psipp, omega_DDPIPI = fargs[0], fargs[1], fargs[2]
        xs_new = (N_data - N_data_sideband/2.)/(2*(flag_D1_2420*eff_ISR_VP_D1_2420*omega_D1_2420 + flag_psipp*eff_ISR_VP_psipp*omega_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI*omega_DDPIPI)*Br*lum)
        # print flag_D1_2420, eff_D1_2420, ISR_D1_2420, omega_D1_2420, flag_psipp, eff_psipp, ISR_psipp, omega_psipp, flag_DDPIPI, eff_DDPIPI, ISR_DDPIPI, omega_DDPIPI
        # if xs_new > xs_old: diff = abs((xs_new - xs_old)/xs_new)
        # else: diff = abs((xs_new - xs_old)/xs_old)
        diff = (xs_old - xs_new)/xs_old
        out = str(diff) + '\n'
        f_diff.write(out)
    f_diff.close()

if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        ecms = int(args[0])
        patch = args[1]
    except:
        logging.error('python cal_diff.py [ecms] [patch]')
        sys.exit()

    signal_path = []
    sideband_path = []
    if ecms <= 4316:
        signal_path.append('../../fit_xs/txts/data_events_' + str(ecms) + '_' + patch + '.txt')
        signal_path.append('')
        signal_path.append('../../fit_xs/txts/psipp_events_' + str(ecms) + '_' + patch + '.txt')
        signal_path.append('../../fit_xs/txts/DDPIPI_events_' + str(ecms) + '_' + patch + '.txt')
        sideband_path.append('../../fit_xs/txts/data_sideband_events_' + str(ecms) + '_' + patch + '.txt')
        sideband_path.append('')
        sideband_path.append('../../fit_xs/txts/psipp_sideband_events_' + str(ecms) + '_' + patch + '.txt')
        sideband_path.append('../../fit_xs/txts/DDPIPI_sideband_events_' + str(ecms) + '_' + patch + '.txt')
        xs(ecms, patch, signal_path, sideband_path)

    if ecms > 4316:
        signal_path.append('../../fit_xs/txts/data_events_' + str(ecms) + '_' + patch + '.txt')
        signal_path.append('../../fit_xs/txts/D1_2420_events_' + str(ecms) + '_' + patch + '.txt')
        signal_path.append('../../fit_xs/txts/psipp_events_' + str(ecms) + '_' + patch + '.txt')
        signal_path.append('../../fit_xs/txts/DDPIPI_events_' + str(ecms) + '_' + patch + '.txt')
        sideband_path.append('../../fit_xs/txts/data_sideband_events_' + str(ecms) + '_' + patch + '.txt')
        sideband_path.append('../../fit_xs/txts/D1_2420_sideband_events_' + str(ecms) + '_' + patch + '.txt')
        sideband_path.append('../../fit_xs/txts/psipp_sideband_events_' + str(ecms) + '_' + patch + '.txt')
        sideband_path.append('../../fit_xs/txts/DDPIPI_sideband_events_' + str(ecms) + '_' + patch + '.txt')
        xs(ecms, patch, signal_path, sideband_path)
