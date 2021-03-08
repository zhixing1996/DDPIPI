#!/usr/bin/env python
"""
Get M(Kpipi) by mixing three MC samples
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-30 Sat 17:25]"

import math
from array import array
import ROOT
from ROOT import TCanvas, gStyle, TLorentzVector, TTree
from ROOT import TFile, TH1F, TLegend, TArrow, TChain, TVector3
import sys, os
import logging
from math import *
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    mix_root.py

SYNOPSIS
    ./mix_root.py [ecms] [sample] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    April 2020
\n''')

def mix(path_in, path_out, mode, ecms, patch, sample):
    omega = array('d', 3*[999.])
    omega_err = array('d', 3*[999.])
    omega_path = '../../fit_xs/txts/omega_' + str(ecms) + '.txt'
    with open(omega_path, 'r') as f:
        lines = f.readlines()
        count = 0
        if len(lines) == 2:
            omega[0] = 0.
            omega_err[0] = 0.
            count = 1
        for line in lines:
            fargs = map(float, line.strip().strip('\n').split())
            omega[count] = fargs[0]
            omega_err[count] = fargs[1]
            count += 1
    omega[0] = omega[0] + omega_err[0]
    omega[1] = omega[1] + omega_err[1]
    omega[2] = omega[2] - omega_err[0] - omega_err[1]

    SUM = 0
    for i in xrange(len(omega)): SUM += omega[i]
    for i in xrange(len(omega)): omega[i] /= SUM

    n = 0
    if ecms <= 4316:
        n += 1
    f_out = TFile(path_out[0], 'RECREATE')
    t_out = TTree('save', 'save')
    if sample == 'raw': m_rawm_D = array('d', [999.])
    if sample == 'raw_after': m_rm_Dpipi = array('d', [999.])
    if sample == 'raw': t_out.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
    if sample == 'raw_after': t_out.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    for i in xrange(len(path_in)):
        try:
            f_in = TFile(path_in[i])
            t_in = f_in.Get('save')
            entries = t_in.GetEntries()
            logging.info(mode[i] + ' entries :' + str(entries))
        except:
            logging.error(path_in[i] + ' is invalid!')
            sys.exit()
        print '--> Begin to process file: ' + path_in[i]
        nentries = t_in.GetEntries()
        for ientry in xrange(int(nentries*omega[n])):
            t_in.GetEntry(ientry)
            if t_in.m_rawm_D > 0.:
                if sample == 'raw': m_rawm_D[0] = t_in.m_rawm_D
                if sample == 'raw_after': m_rm_Dpipi[0] = t_in.m_rm_Dpipi
                t_out.Fill()
        n += 1
    f_out.cd()
    t_out.Write()
    f_out.Close()
    print '--> End of processing file: ' + path_out[0]

def main():
    args = sys.argv[1:]
    if len(args)<3:
        return usage()
    ecms = int(args[0])
    sample = args[1]
    patch = args[2]

    path_in = []
    path_out = []
    mode = []
    if sample == 'raw':
        if ecms > 4316:
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/' + str(ecms) + '/sigMC_D1_2420_' + str(ecms) + '_raw.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw.root')
            path_out.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/omega/sigMC_mixed_width_' + str(ecms) + '_raw.root')
            mode.append('D1_2420')
            mode.append('psipp')
            mode.append('DDPIPI')
            mix(path_in, path_out, mode, ecms, patch, sample)

        if ecms <= 4316:
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw.root')
            path_out.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/omega/sigMC_mixed_width_' + str(ecms) + '_raw.root')
            mode.append('psipp')
            mode.append('DDPIPI')
            mix(path_in, path_out, mode, ecms, patch, sample)

    if sample == 'raw_after':
        if ecms > 4316:
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/' + str(ecms) + '/sigMC_D1_2420_' + str(ecms) + '_raw_after.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw_after.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_after.root')
            path_out.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/omega/sigMC_mixed_window_' + str(ecms) + '_raw_after.root')
            mode.append('D1_2420')
            mode.append('psipp')
            mode.append('DDPIPI')
            mix(path_in, path_out, mode, ecms, patch, sample)

        if ecms <= 4316:
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw_after.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_after.root')
            path_out.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/omega/sigMC_mixed_window_' + str(ecms) + '_raw_after.root')
            mode.append('psipp')
            mode.append('DDPIPI')
            mix(path_in, path_out, mode, ecms, patch, sample)

if __name__ == '__main__':
    main()
