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

def readN(f_path):
    with open(f_path, 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().split())
    return fargs

def xs(ecms, patch, path):
    '''
    Efficiency
    '''
    fargs = readN(path[0])
    N_data, Err_data = fargs[0], fargs[1]

    f_X_3842 = TFile(path[1])
    t_X_3842 = f_X_3842.Get('save')
    eff_X_3842 = float(t_X_3842.GetEntries('rm_pipi > %.5f && rm_pipi < %.5f' %(3.79, 3.89)))/50000.

    '''
    ISR, VP, lum, Br
    '''
    Br = 0.0938
    lum = luminosity(ecms)
    with open('../txts/factor_info_' + str(ecms) + '_X_3842_' + patch + '.txt', 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().strip('\n').split())
            ISR_X_3842, VP = fargs[0], fargs[1]

    '''
    f factor
    '''
    fargs = readN('../sys_err/K_p/txts/f_K_p.txt')
    factor_K_p = fargs[0]

    fargs = readN('../sys_err/m_pipi/txts/f_m_pipi.txt')
    factor_m_pipi = fargs[0]

    fargs = readN('../sys_err/VrVz/txts/f_VrVz.txt')
    factor_VrVz = fargs[0]

    fargs = readN('../sys_err/width/txts/f_m_Kpipi.txt')
    factor_m_Kpipi = fargs[0]

    fargs = readN('../sys_err/window/txts/f_rm_Dpipi.txt')
    factor_rm_Dpipi = fargs[0]

    '''
    xs calculation
    '''
    eff_ISR_VP_X_3842 = eff_X_3842*ISR_X_3842*VP*factor_K_p*factor_m_pipi*factor_VrVz*factor_m_Kpipi*factor_rm_Dpipi
    xs = N_data/(2*eff_ISR_VP_X_3842*Br*lum)
    xs_err = Err_data/(2*eff_ISR_VP_X_3842*Br*lum)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_xs = './txts/xs_info_' + str(ecms) + '_' + patch + '.txt'

    '''
    Output
    '''
    f_xs = open(path_xs, 'w')
    out = '@' + str(ecms) + 'MeV\n'
    out += str(int(N_data)) + ' $\pm$ ' + str(int(Err_data)) + '\n'
    out += str(round(factor_K_p, 4)) + '\n'
    out += str(round(factor_m_pipi, 4)) + '\n'
    out += str(round(factor_VrVz, 4)) + '\n'
    out += str(round(factor_m_Kpipi, 4)) + '\n'
    out += str(round(factor_rm_Dpipi, 4)) + '\n'
    out += str(round(eff_X_3842*100, 2)) + '\%\n'
    out += str(round(ISR_X_3842, 2)) + '\n'
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
    out_read += str(round(factor_K_p, 4)) + ' '
    out_read += str(round(factor_m_pipi, 4)) + ' '
    out_read += str(round(factor_VrVz, 4)) + ' '
    out_read += str(round(factor_m_Kpipi, 4)) + ' '
    out_read += str(round(factor_rm_Dpipi, 4)) + ' '
    out_read += str(round(eff_X_3842*100, 2)) + ' '
    out_read += str(round(ISR_X_3842, 2)) + ' '
    out_read += str(round(VP, 2)) + ' '
    out_read += str(lum) + ' ' 
    out_read += str(Br*100) + ' '
    out_read += str(round(xs, 2)) + ' '
    out_read += str(round(xs_err, 2)) + ' '
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

    path = []
    path.append('./txts/data_events_' + str(ecms) + '_' + patch + '.txt')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/' + str(ecms) + '/sigMC_X_3842_' + str(ecms) + '_after.root')
    xs(ecms, patch, path)
