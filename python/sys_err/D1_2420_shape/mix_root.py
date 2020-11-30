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
    D1_2420_path = './txts/xs_D1_2420_' + patch + '.txt'
    with open(D1_2420_path, 'r') as f:
        for line in f.readlines():
            if '#' in line: line = line.strip('#')
            try:
                fargs = map(float, line.strip().strip('\n').split())
                if fargs[0] == ecms: omega[0] = fargs[4]
            except:
                '''
                '''
    else: omega[0] = 0.
    DDPIPI_path = './txts/xs_DDPIPI_' + patch + '.txt'
    with open(DDPIPI_path, 'r') as f:
        for line in f.readlines():
            if '#' in line: line = line.strip('#')
            try:
                fargs = map(float, line.strip().strip('\n').split())
                if fargs[0] == ecms: omega[1] = fargs[4]
            except:
                '''
                '''
    psipp_path = './txts/xs_psipp_' + patch + '.txt'
    with open(psipp_path, 'r') as f:
        for line in f.readlines():
            if '#' in line: line = line.strip('#')
            try:
                fargs = map(float, line.strip().strip('\n').split())
                if fargs[0] == ecms: omega[2] = fargs[4]
            except:
                '''
                '''
    tot = 0
    for i in xrange(len(omega)): tot += omega[i]
    for i in xrange(len(omega)): omega[i] = omega[i]/tot

    n = 0
    f_out = TFile(path_out[0], 'RECREATE')
    t_out = TTree('save', 'save')
    if sample == 'raw': m_rawm_D = array('d', [999.])
    if sample == 'raw': t_out.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
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
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/' + str(ecms) + '/sys_err/D1_2420_shape/sigMC_D1_2420_' + str(ecms) + '_raw.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/D1_2420_shape/sigMC_mixed_width_' + str(ecms) + '_raw.root')
        mode.append('D1_2420')
        mode.append('psipp')
        mode.append('DDPIPI')
        mix(path_in, path_out, mode, ecms, patch, sample)

if __name__ == '__main__':
    main()
