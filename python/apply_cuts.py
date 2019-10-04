#!/usr/bin/env python
"""
Apply cuts on root files
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-10-03 Tue 17:06]"

import math
from array import array
import ROOT
from ROOT import TCanvas, gStyle, TLorentzVector, TTree
from ROOT import TFile, TH1F, TLegend, TArrow, TChain, TVector3
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    apply_cuts.py

SYNOPSIS
    ./apply_cuts.py [infile_path] [outfile_path] [Ecms] [MODE]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    October 2019
\n''')

def save(f_in, cms, t, MODE, chi2_kf_cut):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_mode = array('i', [0])
    m_charm = array('i', [0])
    m_rawm_D = array('d', [999.])
    m_m_D = array('d', [999.])
    m_rm_D = array('d', [999.])
    m_rm_pipi = array('d', [999.])
    m_m_pipi = array('d', [999.])
    m_m_Dpi = array('d', [999.])
    m_m_Dpipi = array('d', [999.])
    m_rm_Dpipi = array('d', [999.])
    m_chi2_vf = array('d', [999.])
    m_chi2_kf = array('d', [999.])
    m_charge_left = array('i', [0])
    m_chi2_pi0 = array('d', [999.])
    m_m_Dpi0 = array('d', [999.])
    m_m_pi0 = array('d', [999.])
    m_n_pi0 = array('i', [0])
    m_m_D0 = array('d', [999.])
    t.Branch('runNo', m_runNo, 'm_runNo/I')
    t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
    t.Branch('mode', m_mode, 'm_mode/I')
    t.Branch('charm', m_charm, 'm_charm/I')
    t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
    t.Branch('m_D', m_m_D, 'm_m_D/D')
    t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
    t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
    t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
    t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
    t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
    t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
    t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')
    t.Branch('charge_left', m_charge_left, 'm_charge_left/I')
    t.Branch('chi2_pi0', m_chi2_pi0, 'm_chi2_pi0/D')
    t.Branch('m_Dpi0', m_m_Dpi0, 'm_m_Dpi0/D')
    t.Branch('m_pi0', m_m_pi0, 'm_m_pi0/D')
    t.Branch('n_pi0', m_n_pi0, 'm_n_pi0/I')
    t.Branch('m_D0', m_m_D0, 'm_m_D0/D')
    t_in = f_in.Get('save')
    nentries = t_in.GetEntries()
    for ientry in range(nentries):
        t_in.GetEntry(ientry)
        if MODE == 'signal' and t_in.m_m_pipi > 0.28 and t_in.m_chi2_kf < chi2_kf_cut and t_in.m_rm_Dpipi > 1.857 and t_in.m_rm_Dpipi < 1.882:
            m_runNo[0] = t_in.m_runNo
            m_evtNo[0] = t_in.m_evtNo
            m_mode[0] = t_in.m_mode
            m_charm[0] = t_in.m_charm
            m_rawm_D[0] = t_in.m_rawm_D
            m_m_D[0] = t_in.m_m_D
            m_rm_D[0] = t_in.m_rm_D
            m_rm_pipi[0] = t_in.m_rm_pipi
            m_m_pipi[0] = t_in.m_m_pipi
            m_m_Dpi[0] = t_in.m_m_Dpi
            m_m_Dpipi[0] = t_in.m_m_Dpipi
            m_rm_Dpipi[0] = t_in.m_rm_Dpipi
            m_chi2_vf[0] = t_in.m_chi2_vf
            m_chi2_kf[0] = t_in.m_chi2_kf
            m_charge_left[0] = t_in.m_charge_left
            m_chi2_pi0[0] = t_in.m_chi2_pi0
            m_m_Dpi0[0] = t_in.m_m_Dpi0
            m_m_pi0[0] = t_in.m_m_pi0
            m_n_pi0[0] = t_in.m_n_pi0
            m_m_D0[0] = t_in.m_m_D0
            t.Fill()
        if MODE == 'sideband' and t_in.m_m_pipi > 0.28 and t_in.m_chi2_kf < chi2_kf_cut and ((t_in.m_rm_Dpipi > 1.806 and t_in.m_rm_Dpipi < 1.832) or (t_in.m_rm_Dpipi > 1.906 and t_in.m_rm_Dpipi < 1.933)):
            m_runNo[0] = t_in.m_runNo
            m_evtNo[0] = t_in.m_evtNo
            m_mode[0] = t_in.m_mode
            m_charm[0] = t_in.m_charm
            m_rawm_D[0] = t_in.m_rawm_D
            m_m_D[0] = t_in.m_m_D
            m_rm_D[0] = t_in.m_rm_D
            m_rm_pipi[0] = t_in.m_rm_pipi
            m_m_pipi[0] = t_in.m_m_pipi
            m_m_Dpi[0] = t_in.m_m_Dpi
            m_m_Dpipi[0] = t_in.m_m_Dpipi
            m_rm_Dpipi[0] = t_in.m_rm_Dpipi
            m_chi2_vf[0] = t_in.m_chi2_vf
            m_chi2_kf[0] = t_in.m_chi2_kf
            m_charge_left[0] = t_in.m_charge_left
            m_chi2_pi0[0] = t_in.m_chi2_pi0
            m_m_Dpi0[0] = t_in.m_m_Dpi0
            m_m_pi0[0] = t_in.m_m_pi0
            m_n_pi0[0] = t_in.m_n_pi0
            m_m_D0[0] = t_in.m_m_D0
            t.Fill()

def main():
    args = sys.argv[1:]
    if len(args)<3:
        return usage()
    
    file_in = args[0]
    file_out = args[1]
    ecms = float(args[2])
    MODE = args[3]

    f_in = TFile(file_in)
    f_out = TFile(file_out, 'recreate')
    t_out = TTree('save', 'save')

    cms = TLorentzVector(0.011*ecms, 0, 0, ecms)
    chi2_kf_cut = 999
    if ecms == 4.358:
        chi2_kf_cut = 46
    if ecms == 4.415:
        chi2_kf_cut = 42
    if ecms == 4.600:
        chi2_kf_cut = 25
    save(f_in, cms, t_out, MODE, chi2_kf_cut)

    f_out.cd()
    t_out.Write()
    f_out.Close()

if __name__ == '__main__':
    main()
