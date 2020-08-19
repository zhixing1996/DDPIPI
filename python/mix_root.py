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
    ./mix_root.py [ecms] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    April 2020
\n''')

def mix(path_in, path_out, mode, ecms, patch):
    factor_path = './txts/fit_rm_D_' + str(ecms) + '_read_' + patch + '.txt'
    f_factor = open(factor_path, 'r')
    lines_factor = f_factor.readlines()
    omega = array('d', 3*[999.])
    for line_factor in lines_factor:
        rs_factor = line_factor.rstrip('\n')
        rs_factor = filter(None, rs_factor.split(' '))
        omega[0] = float(rs_factor[1])
        omega[1] = float(rs_factor[2])
        omega[2] = float(rs_factor[3])

    n = 0
    if ecms <= 4311:
        n += 1
    f_out = TFile(path_out[0], 'RECREATE')
    t_out = TTree('save', 'save')
    m_rawm_D = array('d', [999.])
    t_out.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
    for i in xrange(len(path_in)/2):
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
                m_rawm_D[0] = t_in.m_rawm_D
                t_out.Fill()
        n += 1
    f_out.cd()
    t_out.Write()
    f_out.Close()
    print '--> End of processing file: ' + path_out[0]

    n = 0
    if ecms <= 4311:
        n += 1
    f_out = TFile(path_out[1], 'RECREATE')
    t_out = TTree('save', 'save')
    m_rm_Dpipi = array('d', [999.])
    t_out.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    for i in xrange(len(path_in)/2):
        try:
            f_in = TFile(path_in[i + len(path_in)/2])
            t_in = f_in.Get('save')
            entries = t_in.GetEntries()
            logging.info(mode[i] + ' entries :' + str(entries))
        except:
            logging.error(path_in[i + len(path_in)/2] + ' is invalid!')
            sys.exit()
        print '--> Begin to process file: ' + path_in[i + len(path_in)/2]
        nentries = t_in.GetEntries()
        for ientry in xrange(int(nentries*omega[n])):
            t_in.GetEntry(ientry)
            if t_in.m_rm_Dpipi > 0.:
                m_rm_Dpipi[0] = t_in.m_rm_Dpipi
                t_out.Fill()
        n += 1
    f_out.cd()
    t_out.Write()
    f_out.Close()
    print '--> End of processing file: ' + path_out[1]

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    patch = args[1]

    path_in = []
    path_out = []
    mode = []
    if ecms > 4311:
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/' + str(ecms) + '/sigMC_D1_2420_' + str(ecms) + '_raw.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sigMC_mixed_width_' + str(ecms) + '.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/' + str(ecms) + '/sigMC_D1_2420_' + str(ecms) + '_raw_before.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw_before.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_before.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sigMC_mixed_window_' + str(ecms) + '.root')
        mode.append('D1_2420')
        mode.append('psipp')
        mode.append('DDPIPI')
        mix(path_in, path_out, mode, ecms, patch)

    if ecms <= 4311:
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sigMC_mixed_width_' + str(ecms) + '.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw_before.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_before.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sigMC_mixed_window_' + str(ecms) + '.root')
        mode.append('psipp')
        mode.append('DDPIPI')
        mix(path_in, path_out, mode, ecms, patch)

if __name__ == '__main__':
    main()
