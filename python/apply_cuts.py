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
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    apply_cuts.py

SYNOPSIS
    ./apply_cuts.py [infile_path] [outfile_path] [ecms] [MODE]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    October 2019
\n''')

def save_before(f_in, t, chi2_kf_cut, width):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_mode = array('i', [0])
    m_charm = array('i', [0])
    m_rawm_D = array('d', [999.])
    m_m_D = array('d', [999.])
    m_p_D = array('d', [999.])
    m_E_D = array('d', [999.])
    m_rm_D = array('d', [999.])
    m_rm_pipi = array('d', [999.])
    m_m_pipi = array('d', [999.])
    m_p_pipi = array('d', [999.])
    m_rm_Dpi = array('d', [999.])
    m_m_Dpi = array('d', [999.])
    m_m_Dmisspi = array('d', [999.])
    m_rm_Dmisspi = array('d', [999.])
    m_m_Dpipi = array('d', [999.])
    m_m2_Kpip = array('d', [999.])
    m_m2_Kpim = array('d', [999.])
    m_rm_Dpipi = array('d', [999.])
    m_chi2_vf = array('d', [999.])
    m_chi2_kf = array('d', [999.])
    m_chi2_svf = array('d', [999.])
    m_ctau_svf = array('d', [999.])
    m_L_svf = array('d', [999.])
    m_Lerr_svf = array('d', [999.])
    m_n_othertrks = array('i', [0])
    m_n_othershws = array('i', [0])
    m_charge_left = array('i', [0])
    m_m_piplus0 = array('d', [999.])
    m_m_piminus0 = array('d', [999.])
    m_p_piplus0 = array('d', [999.])
    m_p_piminus0 = array('d', [999.])
    m_chi2_pi0 = array('d', [999.])
    m_m_Dpi0 = array('d', [999.])
    m_rm_Dpi0 = array('d', [999.])
    m_m_Dmisspi0 = array('d', [999.])
    m_rm_Dmisspi0 = array('d', [999.])
    m_m_pi0 = array('d', [999.])
    m_n_pi0 = array('i', [0])
    m_matched_D = array('i', [0])
    m_matched_pi = array('i', [0])
    t.Branch('runNo', m_runNo, 'm_runNo/I')
    t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
    t.Branch('mode', m_mode, 'm_mode/I')
    t.Branch('charm', m_charm, 'm_charm/I')
    t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
    t.Branch('m_D', m_m_D, 'm_m_D/D')
    t.Branch('p_D', m_p_D, 'm_p_D/D')
    t.Branch('E_D', m_E_D, 'm_E_D/D')
    t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
    t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
    t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
    t.Branch('p_pipi', m_p_pipi, 'm_p_pipi/D')
    t.Branch('rm_Dpi', m_rm_Dpi, 'm_rm_Dpi/D')
    t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
    t.Branch('m_Dmisspi', m_m_Dmisspi, 'm_m_Dmisspi/D')
    t.Branch('rm_Dmisspi', m_rm_Dmisspi, 'm_rm_Dmisspi/D')
    t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
    t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    t.Branch('m2_Kpip', m_m2_Kpip, 'm_m2_Kpip/D')
    t.Branch('m2_Kpim', m_m2_Kpim, 'm_m2_Kpim/D')
    t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
    t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')
    t.Branch('chi2_svf', m_chi2_svf, 'm_chi2_svf/D')
    t.Branch('ctau_svf', m_ctau_svf, 'm_ctau_svf/D')
    t.Branch('L_svf', m_L_svf, 'm_L_svf/D')
    t.Branch('Lerr_svf', m_Lerr_svf, 'm_Lerr_svf/D')
    t.Branch('n_othertrks', m_n_othertrks, 'm_n_othertrks/I')
    t.Branch('n_othershws', m_n_othershws, 'm_n_othershws/I')
    t.Branch('charge_left', m_charge_left, 'm_charge_left/I')
    t.Branch('m_piplus0', m_m_piplus0, 'm_m_piplus0/D')
    t.Branch('m_piminus0', m_m_piminus0, 'm_m_piminus0/D')
    t.Branch('p_piplus0', m_p_piplus0, 'm_p_piplus0/D')
    t.Branch('p_piminus0', m_p_piminus0, 'm_p_piminus0/D')
    t.Branch('chi2_pi0', m_chi2_pi0, 'm_chi2_pi0/D')
    t.Branch('m_Dpi0', m_m_Dpi0, 'm_m_Dpi0/D')
    t.Branch('rm_Dpi0', m_rm_Dpi0, 'm_rm_Dpi0/D')
    t.Branch('m_Dmisspi0', m_m_Dmisspi0, 'm_m_Dmisspi0/D')
    t.Branch('rm_Dmisspi0', m_rm_Dmisspi0, 'm_rm_Dmisspi0/D')
    t.Branch('m_pi0', m_m_pi0, 'm_m_pi0/D')
    t.Branch('n_pi0', m_n_pi0, 'm_n_pi0/I')
    t.Branch('matched_D', m_matched_D, 'm_matched_D/I')
    t.Branch('matched_pi', m_matched_pi, 'm_matched_pi/I')
    t_in = f_in.Get('save')
    nentries = t_in.GetEntries()
    for ientry in range(nentries):
        t_in.GetEntry(ientry)
        if t_in.m_chi2_kf < chi2_kf_cut and fabs(t_in.m_rawm_D - 1.86965) < width/2.:
            m_runNo[0] = t_in.m_runNo
            m_evtNo[0] = t_in.m_evtNo
            m_mode[0] = t_in.m_mode
            m_charm[0] = t_in.m_charm
            m_rawm_D[0] = t_in.m_rawm_D
            m_m_D[0] = t_in.m_m_D
            m_p_D[0] = t_in.m_p_D
            m_E_D[0] = t_in.m_E_D
            m_rm_D[0] = t_in.m_rm_D
            m_rm_pipi[0] = t_in.m_rm_pipi
            m_m_pipi[0] = t_in.m_m_pipi
            m_p_pipi[0] = t_in.m_p_pipi
            m_rm_Dpi[0] = t_in.m_rm_Dpi
            m_m_Dpi[0] = t_in.m_m_Dpi
            m_m_Dmisspi[0] = t_in.m_m_Dmisspi
            m_rm_Dmisspi[0] = t_in.m_rm_Dmisspi
            m_m_Dpipi[0] = t_in.m_m_Dpipi
            m_rm_Dpipi[0] = t_in.m_rm_Dpipi
            m_m2_Kpip[0] = t_in.m_m2_Kpip
            m_m2_Kpim[0] = t_in.m_m2_Kpim
            m_chi2_vf[0] = t_in.m_chi2_vf
            m_chi2_kf[0] = t_in.m_chi2_kf
            m_chi2_svf[0] = t_in.m_chi2_svf
            m_ctau_svf[0] = t_in.m_ctau_svf
            m_L_svf[0] = t_in.m_L_svf
            m_Lerr_svf[0] = t_in.m_Lerr_svf
            m_n_othertrks[0] = t_in.m_n_othertrks
            m_n_othershws[0] = t_in.m_n_othershws
            m_charge_left[0] = t_in.m_charge_left
            m_m_piplus0[0] = t_in.m_m_piplus0
            m_m_piminus0[0] = t_in.m_m_piminus0
            m_p_piplus0[0] = t_in.m_p_piplus0
            m_p_piminus0[0] = t_in.m_p_piminus0
            m_chi2_pi0[0] = t_in.m_chi2_pi0
            m_m_Dpi0[0] = t_in.m_m_Dpi0
            m_rm_Dpi0[0] = t_in.m_rm_Dpi0
            m_m_Dmisspi0[0] = t_in.m_m_Dmisspi0
            m_rm_Dmisspi0[0] = t_in.m_rm_Dmisspi0
            m_m_pi0[0] = t_in.m_m_pi0
            m_n_pi0[0] = t_in.m_n_pi0
            m_matched_D[0] = t_in.m_matched_D
            m_matched_pi[0] = t_in.m_matched_pi
            t.Fill()

def save_after(f_in, t, chi2_kf_cut, width):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_mode = array('i', [0])
    m_charm = array('i', [0])
    m_rawm_D = array('d', [999.])
    m_m_D = array('d', [999.])
    m_p_D = array('d', [999.])
    m_E_D = array('d', [999.])
    m_rm_D = array('d', [999.])
    m_rm_pipi = array('d', [999.])
    m_m_pipi = array('d', [999.])
    m_p_pipi = array('d', [999.])
    m_rm_Dpi = array('d', [999.])
    m_m_Dpi = array('d', [999.])
    m_m_Dmisspi = array('d', [999.])
    m_rm_Dmisspi = array('d', [999.])
    m_m_Dpipi = array('d', [999.])
    m_rm_Dpipi = array('d', [999.])
    m_m2_Kpip = array('d', [999.])
    m_m2_Kpim = array('d', [999.])
    m_chi2_vf = array('d', [999.])
    m_chi2_kf = array('d', [999.])
    m_chi2_svf = array('d', [999.])
    m_ctau_svf = array('d', [999.])
    m_L_svf = array('d', [999.])
    m_Lerr_svf = array('d', [999.])
    m_n_othertrks = array('i', [0])
    m_n_othershws = array('i', [0])
    m_charge_left = array('i', [0])
    m_m_piplus0 = array('d', [999.])
    m_m_piminus0 = array('d', [999.])
    m_p_piplus0 = array('d', [999.])
    m_p_piminus0 = array('d', [999.])
    m_chi2_pi0 = array('d', [999.])
    m_m_Dpi0 = array('d', [999.])
    m_m_Dmisspi0 = array('d', [999.])
    m_m_pi0 = array('d', [999.])
    m_n_pi0 = array('i', [0])
    m_matched_D = array('i', [0])
    m_matched_pi = array('i', [0])
    t.Branch('runNo', m_runNo, 'm_runNo/I')
    t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
    t.Branch('mode', m_mode, 'm_mode/I')
    t.Branch('charm', m_charm, 'm_charm/I')
    t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
    t.Branch('m_D', m_m_D, 'm_m_D/D')
    t.Branch('p_D', m_p_D, 'm_p_D/D')
    t.Branch('E_D', m_E_D, 'm_E_D/D')
    t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
    t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
    t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
    t.Branch('p_pipi', m_p_pipi, 'm_p_pipi/D')
    t.Branch('rm_Dpi', m_rm_Dpi, 'm_rm_Dpi/D')
    t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
    t.Branch('m_Dmisspi', m_m_Dmisspi, 'm_m_Dmisspi/D')
    t.Branch('rm_Dmisspi', m_rm_Dmisspi, 'm_rm_Dmisspi/D')
    t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
    t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    t.Branch('m2_Kpip', m_m2_Kpip, 'm_m2_Kpip/D')
    t.Branch('m2_Kpim', m_m2_Kpim, 'm_m2_Kpim/D')
    t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
    t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')
    t.Branch('chi2_svf', m_chi2_svf, 'm_chi2_svf/D')
    t.Branch('ctau_svf', m_ctau_svf, 'm_ctau_svf/D')
    t.Branch('L_svf', m_L_svf, 'm_L_svf/D')
    t.Branch('Lerr_svf', m_Lerr_svf, 'm_Lerr_svf/D')
    t.Branch('n_othertrks', m_n_othertrks, 'm_n_othertrks/I')
    t.Branch('n_othershws', m_n_othershws, 'm_n_othershws/I')
    t.Branch('charge_left', m_charge_left, 'm_charge_left/I')
    t.Branch('m_piplus0', m_m_piplus0, 'm_m_piplus0/D')
    t.Branch('m_piminus0', m_m_piminus0, 'm_m_piminus0/D')
    t.Branch('p_piplus0', m_p_piplus0, 'm_p_piplus0/D')
    t.Branch('p_piminus0', m_p_piminus0, 'm_p_piminus0/D')
    t.Branch('chi2_pi0', m_chi2_pi0, 'm_chi2_pi0/D')
    t.Branch('m_Dpi0', m_m_Dpi0, 'm_m_Dpi0/D')
    t.Branch('m_Dmisspi0', m_m_Dmisspi0, 'm_m_Dmisspi0/D')
    t.Branch('m_pi0', m_m_pi0, 'm_m_pi0/D')
    t.Branch('n_pi0', m_n_pi0, 'm_n_pi0/I')
    t.Branch('matched_D', m_matched_D, 'm_matched_D/I')
    t.Branch('matched_pi', m_matched_pi, 'm_matched_pi/I')
    t_in = f_in.Get('save')
    nentries = t_in.GetEntries()
    for ientry in range(nentries):
        t_in.GetEntry(ientry)
        if not ((t_in.m_m_pipi > 0.491036 and t_in.m_m_pipi < 0.503471) and t_in.m_ctau_svf > 0.5):
            if (t_in.m_m_Dpi0 < 2.0082 or t_in.m_m_Dpi0 > 2.01269) and t_in.m_chi2_kf < chi2_kf_cut and fabs(t_in.m_rawm_D - 1.86965) < width/2.:
                m_runNo[0] = t_in.m_runNo
                m_evtNo[0] = t_in.m_evtNo
                m_mode[0] = t_in.m_mode
                m_charm[0] = t_in.m_charm
                m_rawm_D[0] = t_in.m_rawm_D
                m_m_D[0] = t_in.m_m_D
                m_p_D[0] = t_in.m_p_D
                m_E_D[0] = t_in.m_E_D
                m_rm_D[0] = t_in.m_rm_D
                m_rm_pipi[0] = t_in.m_rm_pipi
                m_m_pipi[0] = t_in.m_m_pipi
                m_p_pipi[0] = t_in.m_p_pipi
                m_rm_Dpi[0] = t_in.m_rm_Dpi
                m_m_Dpi[0] = t_in.m_m_Dpi
                m_m_Dmisspi[0] = t_in.m_m_Dmisspi
                m_rm_Dmisspi[0] = t_in.m_rm_Dmisspi
                m_m_Dpipi[0] = t_in.m_m_Dpipi
                m_rm_Dpipi[0] = t_in.m_rm_Dpipi
                m_m2_Kpip[0] = t_in.m_m2_Kpip
                m_m2_Kpim[0] = t_in.m_m2_Kpim
                m_chi2_vf[0] = t_in.m_chi2_vf
                m_chi2_kf[0] = t_in.m_chi2_kf
                m_chi2_svf[0] = t_in.m_chi2_svf
                m_ctau_svf[0] = t_in.m_ctau_svf
                m_L_svf[0] = t_in.m_L_svf
                m_Lerr_svf[0] = t_in.m_Lerr_svf
                m_n_othertrks[0] = t_in.m_n_othertrks
                m_n_othershws[0] = t_in.m_n_othershws
                m_charge_left[0] = t_in.m_charge_left
                m_m_piplus0[0] = t_in.m_m_piplus0
                m_m_piminus0[0] = t_in.m_m_piminus0
                m_p_piplus0[0] = t_in.m_p_piplus0
                m_p_piminus0[0] = t_in.m_p_piminus0
                m_chi2_pi0[0] = t_in.m_chi2_pi0
                m_m_Dpi0[0] = t_in.m_m_Dpi0
                m_m_Dmisspi0[0] = t_in.m_m_Dmisspi0
                m_m_pi0[0] = t_in.m_m_pi0
                m_n_pi0[0] = t_in.m_n_pi0
                m_matched_D[0] = t_in.m_matched_D
                m_matched_pi[0] = t_in.m_matched_pi
                t.Fill()

def main():
    args = sys.argv[1:]
    if len(args)<4:
        return usage()

    file_in = args[0]
    file_out = args[1]
    ecms = float(args[2])
    MODE = args[3]

    f_in = TFile(file_in)
    f_out = TFile(file_out, 'recreate')
    t_out = TTree('save', 'save')

    chi2_kf_cut_before = 999
    chi2_kf_cut_after = 999
    if ecms == 4.358:
        chi2_kf_cut = 999
        width = 0.02063
    if ecms == 4.416:
        chi2_kf_cut = 15
        width = 0.02063
    if ecms == 4.600:
        chi2_kf_cut = 999
        width = 0.02063
    if MODE == 'before':
        save_before(f_in, t_out, chi2_kf_cut, width)
    if MODE == 'after':
        save_after(f_in, t_out, chi2_kf_cut, width)

    f_out.cd()
    t_out.Write()
    f_out.Close()

if __name__ == '__main__':
    main()
