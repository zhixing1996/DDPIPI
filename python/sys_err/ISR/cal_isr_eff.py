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

def readN(f_path):
    fargs = []
    with open(f_path, 'r') as f:
        for line in f.readlines():
            fargs.append(map(float, line.strip().split())[0])
    return fargs

def cal(ecms, patch, signal_path):
    '''
    omega
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
                    xs_psipp = fargs[4]
                    xserr_psipp = fargs[5]
            except:
                '''
                '''
    omega_D1_2420 = xs_D1_2420/(xs_D1_2420 + xs_DDPIPI + xs_psipp)
    omega_DDPIPI = xs_DDPIPI/(xs_D1_2420 + xs_DDPIPI + xs_psipp)
    omega_psipp = xs_psipp/(xs_D1_2420 + xs_DDPIPI + xs_psipp)

    '''
    ISR*eff
    '''
    if ecms > 4316:
        isr_eff_D1_2420_list = []
        fargs = readN(signal_path[0])
        isr_eff_D1_2420_list = fargs

    isr_eff_psipp_list = []
    fargs = readN(signal_path[1])
    isr_eff_psipp_list = fargs

    isr_eff_DDPIPI_list = []
    fargs = readN(signal_path[2])
    isr_eff_DDPIPI_list = fargs
    
    with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/isr_eff_' + str(ecms) + '.txt', 'w') as f:
        if ecms > 4316:
            for isr_eff_D1_2420, isr_eff_psipp, isr_eff_DDPIPI in zip(isr_eff_D1_2420_list, isr_eff_psipp_list, isr_eff_DDPIPI_list):
                isr_eff = isr_eff_D1_2420*omega_D1_2420 + isr_eff_psipp*omega_psipp + isr_eff_DDPIPI*omega_DDPIPI
                f.write(str(isr_eff) + '\n')
        else:
            for isr_eff_psipp, isr_eff_DDPIPI in zip(isr_eff_psipp_list, isr_eff_DDPIPI_list):
                isr_eff = isr_eff_psipp*omega_psipp + isr_eff_DDPIPI*omega_DDPIPI
                f.write(str(isr_eff) + '\n')

if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        ecms = int(args[0])
        patch = args[1]
    except:
        logging.error('python cal_isr_eff.py [ecms] [patch]')
        sys.exit()

    signal_path = []
    if ecms <= 4316:
        signal_path.append('')
        signal_path.append('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/psipp_isr_eff_' + str(ecms) + '.txt')
        signal_path.append('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/DDPIPI_isr_eff_' + str(ecms) + '.txt')
        cal(ecms, patch, signal_path)

    if ecms > 4316:
        signal_path.append('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/D1_2420_isr_eff_' + str(ecms) + '.txt')
        signal_path.append('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/psipp_isr_eff_' + str(ecms) + '.txt')
        signal_path.append('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/DDPIPI_isr_eff_' + str(ecms) + '.txt')
        cal(ecms, patch, signal_path)
