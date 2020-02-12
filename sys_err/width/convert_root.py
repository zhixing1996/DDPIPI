#!/usr/bin/env python
"""
Extract tagged D an missed D distribution and put them into one variable
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
    convert_root.py

SYNOPSIS
    ./convert_root.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def convert(path_in, path_out, mode, ecms):
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
        f_out = TFile(path_out[i], 'RECREATE')
        t_out = TTree('save', 'save')

        m_rm_D = array('d', [999.])
        t_out.Branch('rm_D', m_rm_D, 'm_rm_D/D')

        low, up, temp = param_rm_D(ecms)
        nentries = t_in.GetEntries()
        for ientry in xrange(nentries):
            t_in.GetEntry(ientry)
            if t_in.m_rm_D < low or t_in.m_rm_D > up:
                continue
            if t_in.m_rm_Dmiss < low or t_in.m_rm_Dmiss > up:
                continue
            m_rm_D[0] = t_in.m_rm_D
            t_out.Fill()
            m_rm_D[0] = t_in.m_rm_Dmiss
            t_out.Fill()

        f_out.cd()
        t_out.Write()
        f_out.Close()
        print '--> End of processing file: ' + path_out[i]

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = int(args[0])

    path_in = []
    path_out = []
    mode = []
    if ecms >= 4290:
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/sys_err/width/data_' + str(ecms) + '_after.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/sys_err/width/data_' + str(ecms) + '_sideband.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/' + str(ecms) + '/sys_err/width/sigMC_D1_2420_' + str(ecms) + '_after.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sys_err/width/sigMC_psipp_' + str(ecms) + '_after.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sys_err/width/sigMC_D_D_PI_PI_' + str(ecms) + '_after.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/sys_err/width/data_' + str(ecms) + '_fit.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/sys_err/width/data_' + str(ecms) + '_sideband_fit.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/' + str(ecms) + '/sys_err/width/sigMC_D1_2420_' + str(ecms) + '_fit.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sys_err/width/sigMC_psipp_' + str(ecms) + '_fit.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sys_err/width/sigMC_D_D_PI_PI_' + str(ecms) + '_fit.root')
        mode.append('data')
        mode.append('sideband')
        mode.append('D1_2420')
        mode.append('psipp')
        mode.append('DDPIPI')
        convert(path_in, path_out, mode, ecms)

    if ecms < 4290:
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/sys_err/width/data_' + str(ecms) + '_after.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/sys_err/width/data_' + str(ecms) + '_sideband.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sys_err/width/sigMC_psipp_' + str(ecms) + '_after.root')
        path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sys_err/width/sigMC_D_D_PI_PI_' + str(ecms) + '_after.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/sys_err/width/data_' + str(ecms) + '_fit.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/sys_err/width/data_' + str(ecms) + '_sideband_fit.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sys_err/width/sigMC_psipp_' + str(ecms) + '_fit.root')
        path_out.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sys_err/width/sigMC_D_D_PI_PI_' + str(ecms) + '_fit.root')
        mode.append('data')
        mode.append('sideband')
        mode.append('psipp')
        mode.append('DDPIPI')
        convert(path_in, path_out, mode, ecms)

if __name__ == '__main__':
    main()
