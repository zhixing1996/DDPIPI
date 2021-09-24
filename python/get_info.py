#!/usr/bin/env python
"""
Get useful info from raw root files
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-03 Tue 05:41]"

from math import *
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
    get_info.py

SYNOPSIS
    ./get_info.py [file_in] [file_out] [ecms] [region]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    August 2019
\n''')

def save_missing(f_in, cms, t, region):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_mode = array('i', [0])
    m_charm = array('i', [0])
    m_rawm_D = array('d', [999.])
    m_m_Dold = array('d', [999.])
    m_rrawm_D = array('d', [999.])
    m_rm_D = array('d', [999.])
    m_rm_D_old = array('d', [999.])
    m_rm_Dmiss = array('d', [999.])
    m_rm_DDmisspim = array('d', [999.])
    m_m_DDmisspim = array('d', [999.])
    m_rm_DDmisspip = array('d', [999.])
    m_m_DDmisspip = array('d', [999.])
    m_rm_pipi = array('d', [999.])
    m_m_pipi = array('d', [999.])
    m_m_Dpi = array('d', [999.])
    m_m_DDmiss = array('d', [999.])
    m_rm_DDmiss = array('d', [999.])
    m_m_Dmisspi = array('d', [999.])
    m_rm_Dmisspi = array('d', [999.])
    m_rm_Dmisspipi = array('d', [999.])
    m_m_Dmisspipi = array('d', [999.])
    m_rm_Dpi = array('d', [999.])
    m_m_Dpip = array('d', [999.])
    m_m_Dpim = array('d', [999.])
    m_m_Kpi1 = array('d', [999.])
    m_rm_Kpi1 = array('d', [999.])
    m_m_Kpi2 = array('d', [999.])
    m_rm_Kpi2 = array('d', [999.])
    m_m_Dpipi = array('d', [999.])
    m_rm_Dpipi = array('d', [999.])
    m_m_Dmiss = array('d', [999.])
    m_chi2_vf = array('d', [999.])
    m_chi2_kf = array('d', [999.])
    m_chi2_svf = array('d', [999.])
    m_ctau_svf = array('d', [999.])
    m_L_svf = array('d', [999.])
    m_Lerr_svf = array('d', [999.])
    m_n_othershws = array('i', [0])
    m_n_othertrks = array('i', [0])
    m_n_p = array('i', [0])
    m_n_pbar = array('i', [0])
    m_n_Kp = array('i', [0])
    m_n_Km = array('i', [0])
    m_charge_left = array('i', [0])
    m_m_piplus0 = array('d', [999.])
    m_m_piminus0 = array('d', [999.])
    m_p_piplus0 = array('d', [999.])
    m_p_piminus0 = array('d', [999.])
    m_E_piplus0 = array('d', [999.])
    m_E_piminus0 = array('d', [999.])
    m_chi2_pi0 = array('d', [999.])
    m_m_Dpi0 = array('d', [999.])
    m_rm_Dpi0 = array('d', [999.])
    m_m_Dmisspi0 = array('d', [999.])
    m_rm_Dmisspi0 = array('d', [999.])
    m_m_pi0 = array('d', [999.])
    m_p_pi0 = array('d', [999.])
    m_E_pi0 = array('d', [999.])
    m_n_pi0 = array('i', [0])
    m_m_truthall = array('d', [0.])
    m_E_othertrks = array('d', [0.])
    m_E_othershws = array('d', [0.])
    m_p_otherall = array('d', [0.])
    m_cos_otherall = array('d', [0.])
    m_p_Dmiss = array('d', [0.])
    m_cos_other_Dmiss = array('d', [999.])
    m_has_badshws = array('i', [0])
    m_has_badtrks = array('i', [0])
    m_has_leps = array('i', [0])
    if region == 'STDDmiss_signal':
        m_matched_D = array('i', [0])
        m_matched_pi = array('i', [0])
        m_matched_piplus = array('i', [0])
        m_matched_piminus = array('i', [0])
    m_indexmc = array('i', [0])
    m_motheridx = array('i', 100*[0])
    m_pdgid = array('i', 100*[0])
    m_p_othertrk = array('d', [999.])
    m_p_othershw = array('d', [999.])
    m_cos_other_trk_shw = array('d', [999.])
    m_cos_other_trk = array('d', [999.])
    m_cos_other_shw = array('d', [999.])
    m_Vxy_trks = array('d', 100*[999.])
    m_Vz_trks = array('d', 100*[999.])
    m_cos_theta_trks = array('d', 100*[999.])
    m_mode_shws = array('d', 100*[999.])
    m_Emin_shws = array('d', 100*[999.])
    m_T_shws = array('d', 100*[999.])
    m_angle_shws = array('d', 100*[999.])
    m_Vxy_Dtrks = array('d', 3*[999.])
    m_Vz_Dtrks = array('d', 3*[999.])
    m_cos_theta_Dtrks = array('d', 3*[999.])
    m_Vxy_pip = array('d', [999.])
    m_Vz_pip = array('d', [999.])
    m_cos_theta_pip = array('d', [999.])
    m_Vxy_pim = array('d', [999.])
    m_Vz_pim = array('d', [999.])
    m_cos_theta_pim = array('d', [999.])
    m_m_Kpipipi1 = array('d', [0])
    m_m_Kpipipi2 = array('d', [0])
    m_cos_D = array('d', [999.])
    t.Branch('runNo', m_runNo, 'm_runNo/I')
    t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
    t.Branch('mode', m_mode, 'm_mode/I')
    t.Branch('charm', m_charm, 'm_charm/I')
    t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
    t.Branch('m_Dold', m_m_Dold, 'm_m_Dold/D')
    t.Branch('rrawm_D', m_rrawm_D, 'm_rrawm_D/D')
    t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
    t.Branch('rm_D_old', m_rm_D_old, 'm_rm_D_old/D')
    t.Branch('rm_Dmiss', m_rm_Dmiss, 'm_rm_Dmiss/D')
    t.Branch('rm_DDmisspim', m_rm_DDmisspim, 'm_rm_DDmisspim/D')
    t.Branch('m_DDmisspim', m_m_DDmisspim, 'm_m_DDmisspim/D')
    t.Branch('rm_DDmisspip', m_rm_DDmisspip, 'm_rm_DDmisspip/D')
    t.Branch('m_DDmisspip', m_m_DDmisspip, 'm_m_DDmisspip/D')
    t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
    t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
    t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
    t.Branch('m_DDmiss', m_m_DDmiss, 'm_m_DDmiss/D')
    t.Branch('rm_DDmiss', m_rm_DDmiss, 'm_rm_DDmiss/D')
    t.Branch('m_Dmisspi', m_m_Dmisspi, 'm_m_Dmisspi/D')
    t.Branch('rm_Dmisspi', m_rm_Dmisspi, 'm_rm_Dmisspi/D')
    t.Branch('rm_Dmisspipi', m_rm_Dmisspipi, 'm_rm_Dmisspipi/D')
    t.Branch('m_Dmisspipi', m_m_Dmisspipi, 'm_m_Dmisspipi/D')
    t.Branch('rm_Dpi', m_rm_Dpi, 'm_rm_Dpi/D')
    t.Branch('m_Dpip', m_m_Dpip, 'm_m_Dpip/D')
    t.Branch('m_Dpim', m_m_Dpim, 'm_m_Dpim/D')
    t.Branch('m_Kpi1', m_m_Kpi1, 'm_m_Kpi1/D')
    t.Branch('rm_Kpi1', m_rm_Kpi1, 'm_rm_Kpi1/D')
    t.Branch('m_Kpi2', m_m_Kpi2, 'm_m_Kpi2/D')
    t.Branch('rm_Kpi2', m_rm_Kpi2, 'm_rm_Kpi2/D')
    t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
    t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    t.Branch('m_Dmiss', m_m_Dmiss, 'm_m_Dmiss/D')
    t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
    t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')
    t.Branch('chi2_svf', m_chi2_svf, 'm_chi2_svf/D')
    t.Branch('ctau_svf', m_ctau_svf, 'm_ctau_svf/D')
    t.Branch('L_svf', m_L_svf, 'm_L_svf/D')
    t.Branch('Lerr_svf', m_Lerr_svf, 'm_Lerr_svf/D')
    t.Branch('n_othertrks', m_n_othertrks, 'm_n_othertrks/I')
    t.Branch('n_othershws', m_n_othershws, 'm_n_othershws/I')
    t.Branch('n_p', m_n_p, 'm_n_p/I')
    t.Branch('n_pbar', m_n_pbar, 'm_n_pbar/I')
    t.Branch('n_Kp', m_n_Kp, 'm_n_Kp/I')
    t.Branch('n_Km', m_n_Km, 'm_n_Km/I')
    t.Branch('charge_left', m_charge_left, 'm_charge_left/I')
    t.Branch('m_piplus0', m_m_piplus0, 'm_m_piplus0/D')
    t.Branch('m_piminus0', m_m_piminus0, 'm_m_piminus0/D')
    t.Branch('p_piplus0', m_p_piplus0, 'm_p_piplus0/D')
    t.Branch('p_piminus0', m_p_piminus0, 'm_p_piminus0/D')
    t.Branch('E_piplus0', m_E_piplus0, 'm_E_piplus0/D')
    t.Branch('E_piminus0', m_E_piminus0, 'm_E_piminus0/D')
    t.Branch('chi2_pi0', m_chi2_pi0, 'm_chi2_pi0/D')
    t.Branch('m_Dpi0', m_m_Dpi0, 'm_m_Dpi0/D')
    t.Branch('rm_Dpi0', m_rm_Dpi0, 'm_rm_Dpi0/D')
    t.Branch('m_Dmisspi0', m_m_Dmisspi0, 'm_m_Dmisspi0/D')
    t.Branch('rm_Dmisspi0', m_rm_Dmisspi0, 'm_rm_Dmisspi0/D')
    t.Branch('m_pi0', m_m_pi0, 'm_m_pi0/D')
    t.Branch('p_pi0', m_p_pi0, 'm_p_pi0/D')
    t.Branch('E_pi0', m_E_pi0, 'm_E_pi0/D')
    t.Branch('n_pi0', m_n_pi0, 'm_n_pi0/I')
    if region == 'STDDmiss_signal':
        t.Branch('matched_D', m_matched_D, 'm_matched_D/I')
        t.Branch('matched_pi', m_matched_pi, 'm_matched_pi/I')
        t.Branch('matched_piplus', m_matched_piplus, 'm_matched_piplus/I')
        t.Branch('matched_piminus', m_matched_piminus, 'm_matched_piminus/I')
    t.Branch('indexmc', m_indexmc, 'indexmc/I')
    t.Branch('motheridx', m_motheridx, 'motheridx[100]/I')
    t.Branch('pdgid', m_pdgid, 'pdgid[100]/I')
    t.Branch('m_truthall', m_m_truthall, 'm_m_truthall/D')
    t.Branch('E_othertrks', m_E_othertrks, 'm_E_othertrks/D')
    t.Branch('E_othershws', m_E_othershws, 'm_E_othershws/D')
    t.Branch('p_otherall', m_p_otherall, 'm_p_otherall/D')
    t.Branch('cos_otherall', m_cos_otherall, 'm_cos_otherall/D')
    t.Branch('p_Dmiss', m_p_Dmiss, 'm_p_Dmiss/D')
    t.Branch('cos_other_Dmiss', m_cos_other_Dmiss, 'm_cos_other_Dmiss/D')
    t.Branch('has_badtrks', m_has_badtrks, 'm_has_badtrks/I')
    t.Branch('has_badshws', m_has_badshws, 'm_has_badshws/I')
    t.Branch('has_leps', m_has_leps, 'm_has_leps/I')
    t.Branch('p_othertrk', m_p_othertrk, 'm_p_othertrk/D')
    t.Branch('p_othershw', m_p_othershw, 'm_p_othershw/D')
    t.Branch('cos_other_trk_shw', m_cos_other_trk_shw, 'm_cos_other_trk_shw/D')
    t.Branch('cos_other_trk', m_cos_other_trk, 'm_cos_other_trk/D')
    t.Branch('cos_other_shw', m_cos_other_shw, 'm_cos_other_shw/D')
    t.Branch('Vxy_trks', m_Vxy_trks, 'm_Vxy_trks[100]/D')
    t.Branch('Vz_trks', m_Vz_trks, 'm_Vz_trks[100]/D')
    t.Branch('cos_theta_trks', m_cos_theta_trks, 'm_cos_theta_trks[100]/D')
    t.Branch('mode_shws', m_mode_shws, 'm_mode_shws[100]/D')
    t.Branch('Emin_shws', m_Emin_shws, 'm_Emin_shws[100]/D')
    t.Branch('T_shws', m_T_shws, 'm_T_shws[100]/D')
    t.Branch('angle_shws', m_angle_shws, 'm_angle_shws[100]/D')
    t.Branch('Vxy_Dtrks', m_Vxy_Dtrks, 'm_Vxy_Dtrks[100]/D')
    t.Branch('Vz_Dtrks', m_Vz_Dtrks, 'm_Vz_Dtrks[100]/D')
    t.Branch('cos_theta_Dtrks', m_cos_theta_Dtrks, 'm_cos_theta_Dtrks[100]/D')
    t.Branch('Vxy_pip', m_Vxy_pip, 'm_Vxy_pip/D')
    t.Branch('Vz_pip', m_Vz_pip, 'm_Vz_pip/D')
    t.Branch('cos_theta_pip', m_cos_theta_pip, 'm_cos_theta_pip/D')
    t.Branch('Vxy_pim', m_Vxy_pim, 'm_Vxy_pim/D')
    t.Branch('Vz_pim', m_Vz_pim, 'm_Vz_pim/D')
    t.Branch('cos_theta_pim', m_cos_theta_pim, 'm_cos_theta_pim/D')
    t.Branch('m_Kpipipi1', m_m_Kpipipi1, 'm_m_Kpipipi1/D')
    t.Branch('m_Kpipipi2', m_m_Kpipipi2, 'm_m_Kpipipi2/D')
    t.Branch('cos_D', m_cos_D, 'm_cos_D/D')
    t_in = f_in.Get('STDDmiss')
    nentries = t_in.GetEntries()
    for ientry in range(nentries):
        t_in.GetEntry(ientry)
        if t_in.mode != 200:
            continue
        if abs(t_in.vtx_tagPiplus[0]) >= 1.0:
            continue
        if abs(t_in.vtx_tagPiplus[1]) >= 10.0:
            continue
        if abs(t_in.vtx_tagPiplus[2]) >= 0.93:
            continue
        if abs(t_in.vtx_tagPiminus[0]) >= 1.0:
            continue
        if abs(t_in.vtx_tagPiminus[1]) >= 10.0:
            continue
        if abs(t_in.vtx_tagPiminus[2]) >= 0.93:
            continue
        m_Vxy_pip[0] = abs(t_in.vtx_tagPiplus[0])
        m_Vz_pip[0] = abs(t_in.vtx_tagPiplus[1])
        m_cos_theta_pip[0] = abs(t_in.vtx_tagPiplus[2])
        m_Vxy_pim[0] = abs(t_in.vtx_tagPiminus[0])
        m_Vz_pim[0] = abs(t_in.vtx_tagPiminus[1])
        m_cos_theta_pim[0] = abs(t_in.vtx_tagPiminus[2])
        pD_raw = TLorentzVector(0, 0, 0, 0)
        pD_old = TLorentzVector(0, 0, 0, 0)
        pD = TLorentzVector(0, 0, 0, 0)
        pKpi1 = TLorentzVector(0, 0, 0, 0)
        pKpi2 = TLorentzVector(0, 0, 0, 0)
        ptrack_K = TLorentzVector(0, 0, 0, 0)
        ptrack_pi1 = TLorentzVector(0, 0, 0, 0)
        ptrack_pi2 = TLorentzVector(0, 0, 0, 0)
        for iTrk in xrange(t_in.n_trkD):
            ptrack_raw = TLorentzVector(0, 0, 0, 0)
            ptrack_old = TLorentzVector(0, 0, 0, 0)
            ptrack_Kpi1 = TLorentzVector(0, 0, 0, 0)
            ptrack_Kpi2 = TLorentzVector(0, 0, 0, 0)
            ptrack = TLorentzVector(0, 0, 0, 0)
            ptrack_raw.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*9+0], t_in.rawp4_Dtrk[iTrk*9+1], t_in.rawp4_Dtrk[iTrk*9+2], t_in.rawp4_Dtrk[iTrk*9+3])
            ptrack_old.SetPxPyPzE(t_in.p4_Dtrkold[iTrk*4+0], t_in.p4_Dtrkold[iTrk*4+1], t_in.p4_Dtrkold[iTrk*4+2], t_in.p4_Dtrkold[iTrk*4+3])
            if region == 'STDDmiss_signal':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk[iTrk*4+0], t_in.p4_Dtrk[iTrk*4+1], t_in.p4_Dtrk[iTrk*4+2], t_in.p4_Dtrk[iTrk*4+3])
            if region == 'STDDmiss_side1_low':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk_side1_low[iTrk*4+0], t_in.p4_Dtrk_side1_low[iTrk*4+1], t_in.p4_Dtrk_side1_low[iTrk*4+2], t_in.p4_Dtrk_side1_low[iTrk*4+3])
            if region == 'STDDmiss_side1_up':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk_side1_up[iTrk*4+0], t_in.p4_Dtrk_side1_up[iTrk*4+1], t_in.p4_Dtrk_side1_up[iTrk*4+2], t_in.p4_Dtrk_side1_up[iTrk*4+3])
            if region == 'STDDmiss_side2_low':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk_side2_low[iTrk*4+0], t_in.p4_Dtrk_side2_low[iTrk*4+1], t_in.p4_Dtrk_side2_low[iTrk*4+2], t_in.p4_Dtrk_side2_low[iTrk*4+3])
            if region == 'STDDmiss_side2_up':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk_side2_up[iTrk*4+0], t_in.p4_Dtrk_side2_up[iTrk*4+1], t_in.p4_Dtrk_side2_up[iTrk*4+2], t_in.p4_Dtrk_side2_up[iTrk*4+3])
            if region == 'STDDmiss_side3_low':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk_side3_low[iTrk*4+0], t_in.p4_Dtrk_side3_low[iTrk*4+1], t_in.p4_Dtrk_side3_low[iTrk*4+2], t_in.p4_Dtrk_side3_low[iTrk*4+3])
            if region == 'STDDmiss_side3_up':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk_side3_up[iTrk*4+0], t_in.p4_Dtrk_side3_up[iTrk*4+1], t_in.p4_Dtrk_side3_up[iTrk*4+2], t_in.p4_Dtrk_side3_up[iTrk*4+3])
            if region == 'STDDmiss_side4_low':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk_side4_low[iTrk*4+0], t_in.p4_Dtrk_side4_low[iTrk*4+1], t_in.p4_Dtrk_side4_low[iTrk*4+2], t_in.p4_Dtrk_side4_low[iTrk*4+3])
            if region == 'STDDmiss_side4_up':
                ptrack.SetPxPyPzE(t_in.p4_Dtrk_side4_up[iTrk*4+0], t_in.p4_Dtrk_side4_up[iTrk*4+1], t_in.p4_Dtrk_side4_up[iTrk*4+2], t_in.p4_Dtrk_side4_up[iTrk*4+3])
            pD_raw += ptrack_raw
            pD_old += ptrack_old
            pD += ptrack
            if t_in.rawp4_Dtrk[iTrk*9+5] == 3:
                ptrack_Kpi1.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*9+0], t_in.rawp4_Dtrk[iTrk*9+1], t_in.rawp4_Dtrk[iTrk*9+2], t_in.rawp4_Dtrk[iTrk*9+3])
                ptrack_Kpi2.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*9+0], t_in.rawp4_Dtrk[iTrk*9+1], t_in.rawp4_Dtrk[iTrk*9+2], t_in.rawp4_Dtrk[iTrk*9+3])
                ptrack_K.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*9+0], t_in.rawp4_Dtrk[iTrk*9+1], t_in.rawp4_Dtrk[iTrk*9+2], t_in.rawp4_Dtrk[iTrk*9+3])
                pKpi1 += ptrack_Kpi2
                pKpi2 += ptrack_Kpi2
            if t_in.rawp4_Dtrk[iTrk*9+5] == 2 and iTrk == 1:
                ptrack_Kpi1.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*9+0], t_in.rawp4_Dtrk[iTrk*9+1], t_in.rawp4_Dtrk[iTrk*9+2], t_in.rawp4_Dtrk[iTrk*9+3])
                ptrack_pi1.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*9+0], t_in.rawp4_Dtrk[iTrk*9+1], t_in.rawp4_Dtrk[iTrk*9+2], t_in.rawp4_Dtrk[iTrk*9+3])
                pKpi1 += ptrack_Kpi1
            if t_in.rawp4_Dtrk[iTrk*9+5] == 2 and iTrk == 2:
                ptrack_Kpi2.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*9+0], t_in.rawp4_Dtrk[iTrk*9+1], t_in.rawp4_Dtrk[iTrk*9+2], t_in.rawp4_Dtrk[iTrk*9+3])
                ptrack_pi2.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*9+0], t_in.rawp4_Dtrk[iTrk*9+1], t_in.rawp4_Dtrk[iTrk*9+2], t_in.rawp4_Dtrk[iTrk*9+3])
                pKpi2 += ptrack_Kpi2
            m_Vxy_Dtrks[iTrk] = abs(t_in.rawp4_Dtrk[iTrk*9+6])
            m_Vz_Dtrks[iTrk] = abs(t_in.rawp4_Dtrk[iTrk*9+7])
            m_cos_theta_Dtrks[iTrk] = abs(t_in.rawp4_Dtrk[iTrk*9+8])
        for iShw in xrange(t_in.n_shwD):
            pshower_raw = TLorentzVector(0, 0, 0, 0)
            pshower_old = TLorentzVector(0, 0, 0, 0)
            pshower = TLorentzVector(0, 0, 0, 0)
            pshower_raw.SetPxPyPzE(t_in.rawp4_Dshw[iShw*4+0], t_in.rawp4_Dshw[iShw*4+1], t_in.rawp4_Dshw[iShw*4+2], t_in.rawp4_Dshw[iShw*4+3])
            pshower_old.SetPxPyPzE(t_in.p4_Dshwold[iShw*4+0], t_in.p4_Dshwold[iShw*4+1], t_in.p4_Dshwold[iShw*4+2], t_in.p4_Dshwold[iShw*4+3])
            if region == 'STDDmiss_signal':
                pshower.SetPxPyPzE(t_in.p4_Dshw[iShw*4+0], t_in.p4_Dshw[iShw*4+1], t_in.p4_Dshw[iShw*4+2], t_in.p4_Dshw[iShw*4+3])
            if region == 'STDDmiss_side1_low':
                pshower.SetPxPyPzE(t_in.p4_Dshw_side1_low[iShw*4+0], t_in.p4_Dshw_side1_low[iShw*4+1], t_in.p4_Dshw_side1_low[iShw*4+2], t_in.p4_Dshw_side1_low[iShw*4+3])
            if region == 'STDDmiss_side1_up':
                pshower.SetPxPyPzE(t_in.p4_Dshw_side1_up[iShw*4+0], t_in.p4_Dshw_side1_up[iShw*4+1], t_in.p4_Dshw_side1_up[iShw*4+2], t_in.p4_Dshw_side1_up[iShw*4+3])
            if region == 'STDDmiss_side2_low':
                pshower.SetPxPyPzE(t_in.p4_Dshw_side2_low[iShw*4+0], t_in.p4_Dshw_side2_low[iShw*4+1], t_in.p4_Dshw_side2_low[iShw*4+2], t_in.p4_Dshw_side2_low[iShw*4+3])
            if region == 'STDDmiss_side2_up':
                pshower.SetPxPyPzE(t_in.p4_Dshw_side2_up[iShw*4+0], t_in.p4_Dshw_side2_up[iShw*4+1], t_in.p4_Dshw_side2_up[iShw*4+2], t_in.p4_Dshw_side2_up[iShw*4+3])
            if region == 'STDDmiss_side3_low':
                pshower.SetPxPyPzE(t_in.p4_Dshw_side3_low[iShw*4+0], t_in.p4_Dshw_side3_low[iShw*4+1], t_in.p4_Dshw_side3_low[iShw*4+2], t_in.p4_Dshw_side3_low[iShw*4+3])
            if region == 'STDDmiss_side3_up':
                pshower.SetPxPyPzE(t_in.p4_Dshw_side3_up[iShw*4+0], t_in.p4_Dshw_side3_up[iShw*4+1], t_in.p4_Dshw_side3_up[iShw*4+2], t_in.p4_Dshw_side3_up[iShw*4+3])
            if region == 'STDDmiss_side4_low':
                pshower.SetPxPyPzE(t_in.p4_Dshw_side4_low[iShw*4+0], t_in.p4_Dshw_side4_low[iShw*4+1], t_in.p4_Dshw_side4_low[iShw*4+2], t_in.p4_Dshw_side4_low[iShw*4+3])
            if region == 'STDDmiss_side4_up':
                pshower.SetPxPyPzE(t_in.p4_Dshw_side4_up[iShw*4+0], t_in.p4_Dshw_side4_up[iShw*4+1], t_in.p4_Dshw_side4_up[iShw*4+2], t_in.p4_Dshw_side4_up[iShw*4+3])
            pD_raw += pshower_raw
            pD_old += pshower_old
            pD += pshower
        pPip = TLorentzVector(0, 0, 0, 0)
        pPim = TLorentzVector(0, 0, 0, 0)
        pDmiss = TLorentzVector(0, 0, 0, 0)
        rawpPip = TLorentzVector(0, 0, 0, 0)
        rawpPim = TLorentzVector(0, 0, 0, 0)
        pPi0 = TLorentzVector(0, 0, 0, 0)
        if region == 'STDDmiss_signal':
            pPip.SetPxPyPzE(t_in.p4_piplus[0], t_in.p4_piplus[1], t_in.p4_piplus[2], t_in.p4_piplus[3])
            pPim.SetPxPyPzE(t_in.p4_piminus[0], t_in.p4_piminus[1], t_in.p4_piminus[2], t_in.p4_piminus[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss[0], t_in.p4_Dmiss[1], t_in.p4_Dmiss[2], t_in.p4_Dmiss[3])
        if region == 'STDDmiss_side1_low':
            pPip.SetPxPyPzE(t_in.p4_piplus_side1_low[0], t_in.p4_piplus_side1_low[1], t_in.p4_piplus_side1_low[2], t_in.p4_piplus_side1_low[3])
            pPim.SetPxPyPzE(t_in.p4_piminus_side1_low[0], t_in.p4_piminus_side1_low[1], t_in.p4_piminus_side1_low[2], t_in.p4_piminus_side1_low[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss_side1_low[0], t_in.p4_Dmiss_side1_low[1], t_in.p4_Dmiss_side1_low[2], t_in.p4_Dmiss_side1_low[3])
        if region == 'STDDmiss_side1_up':
            pPip.SetPxPyPzE(t_in.p4_piplus_side1_up[0], t_in.p4_piplus_side1_up[1], t_in.p4_piplus_side1_up[2], t_in.p4_piplus_side1_up[3])
            pPim.SetPxPyPzE(t_in.p4_piminus_side1_up[0], t_in.p4_piminus_side1_up[1], t_in.p4_piminus_side1_up[2], t_in.p4_piminus_side1_up[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss_side1_up[0], t_in.p4_Dmiss_side1_up[1], t_in.p4_Dmiss_side1_up[2], t_in.p4_Dmiss_side1_up[3])
        if region == 'STDDmiss_side2_low':
            pPip.SetPxPyPzE(t_in.p4_piplus_side2_low[0], t_in.p4_piplus_side2_low[1], t_in.p4_piplus_side2_low[2], t_in.p4_piplus_side2_low[3])
            pPim.SetPxPyPzE(t_in.p4_piminus_side2_low[0], t_in.p4_piminus_side2_low[1], t_in.p4_piminus_side2_low[2], t_in.p4_piminus_side2_low[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss_side2_low[0], t_in.p4_Dmiss_side2_low[1], t_in.p4_Dmiss_side2_low[2], t_in.p4_Dmiss_side2_low[3])
        if region == 'STDDmiss_side2_up':
            pPip.SetPxPyPzE(t_in.p4_piplus_side2_up[0], t_in.p4_piplus_side2_up[1], t_in.p4_piplus_side2_up[2], t_in.p4_piplus_side2_up[3])
            pPim.SetPxPyPzE(t_in.p4_piminus_side2_up[0], t_in.p4_piminus_side2_up[1], t_in.p4_piminus_side2_up[2], t_in.p4_piminus_side2_up[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss_side2_up[0], t_in.p4_Dmiss_side2_up[1], t_in.p4_Dmiss_side2_up[2], t_in.p4_Dmiss_side2_up[3])
        if region == 'STDDmiss_side3_low':
            pPip.SetPxPyPzE(t_in.p4_piplus_side3_low[0], t_in.p4_piplus_side3_low[1], t_in.p4_piplus_side3_low[2], t_in.p4_piplus_side3_low[3])
            pPim.SetPxPyPzE(t_in.p4_piminus_side3_low[0], t_in.p4_piminus_side3_low[1], t_in.p4_piminus_side3_low[2], t_in.p4_piminus_side3_low[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss_side3_low[0], t_in.p4_Dmiss_side3_low[1], t_in.p4_Dmiss_side3_low[2], t_in.p4_Dmiss_side3_low[3])
        if region == 'STDDmiss_side3_up':
            pPip.SetPxPyPzE(t_in.p4_piplus_side3_up[0], t_in.p4_piplus_side3_up[1], t_in.p4_piplus_side3_up[2], t_in.p4_piplus_side3_up[3])
            pPim.SetPxPyPzE(t_in.p4_piminus_side3_up[0], t_in.p4_piminus_side3_up[1], t_in.p4_piminus_side3_up[2], t_in.p4_piminus_side3_up[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss_side3_up[0], t_in.p4_Dmiss_side3_up[1], t_in.p4_Dmiss_side3_up[2], t_in.p4_Dmiss_side3_up[3])
        if region == 'STDDmiss_side4_low':
            pPip.SetPxPyPzE(t_in.p4_piplus_side4_low[0], t_in.p4_piplus_side4_low[1], t_in.p4_piplus_side4_low[2], t_in.p4_piplus_side4_low[3])
            pPim.SetPxPyPzE(t_in.p4_piminus_side4_low[0], t_in.p4_piminus_side4_low[1], t_in.p4_piminus_side4_low[2], t_in.p4_piminus_side4_low[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss_side4_low[0], t_in.p4_Dmiss_side4_low[1], t_in.p4_Dmiss_side4_low[2], t_in.p4_Dmiss_side4_low[3])
        if region == 'STDDmiss_side4_up':
            pPip.SetPxPyPzE(t_in.p4_piplus_side4_up[0], t_in.p4_piplus_side4_up[1], t_in.p4_piplus_side4_up[2], t_in.p4_piplus_side4_up[3])
            pPim.SetPxPyPzE(t_in.p4_piminus_side4_up[0], t_in.p4_piminus_side4_up[1], t_in.p4_piminus_side4_up[2], t_in.p4_piminus_side4_up[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss_side4_up[0], t_in.p4_Dmiss_side4_up[1], t_in.p4_Dmiss_side4_up[2], t_in.p4_Dmiss_side4_up[3])
        rawpPip.SetPxPyPzE(t_in.rawp4_tagPiplus[0], t_in.rawp4_tagPiplus[1], t_in.rawp4_tagPiplus[2], t_in.rawp4_tagPiplus[3])
        rawpPim.SetPxPyPzE(t_in.rawp4_tagPiminus[0], t_in.rawp4_tagPiminus[1], t_in.rawp4_tagPiminus[2], t_in.rawp4_tagPiminus[3])
        pPi0.SetPxPyPzE(t_in.p4_pi0_save[0], t_in.p4_pi0_save[1], t_in.p4_pi0_save[2], t_in.p4_pi0_save[3])
        m_runNo[0] = t_in.runNo
        m_evtNo[0] = t_in.evtNo
        m_mode[0] = t_in.mode
        m_charm[0] = t_in.charm
        m_rawm_D[0] = pD_raw.M()
        m_m_Dold[0] = pD_old.M()
        m_rrawm_D[0] = (cms-pD_raw).M()
        m_rm_D[0] = (cms-pD).M()
        m_rm_D_old[0] = (cms-pD_old).M()
        m_rm_Dmiss[0] = (cms-pDmiss).M()
        m_rm_pipi[0] = (cms-pPip-pPim).M()
        m_m_pipi[0] = (pPip+pPim).M()
        m_m_Dpim[0] = (pD+pPim).M()
        m_m_Dpip[0] = (pD+pPip).M()
        if t_in.charm > 0:
            m_m_Dmisspi[0] = (pDmiss+pPip).M()
            m_rm_Dmisspi[0] = (cms-pDmiss-pPip).M()
            m_m_Dpi[0] = (pD+pPim).M()
            m_rm_Dpi[0] = (cms-pD-pPim).M()
            m_rm_DDmisspim[0] = (cms-pDmiss-pD-pPim).M()
            m_m_DDmisspim[0] = (pDmiss+pD+pPim).M()
            m_rm_DDmisspip[0] = (cms-pDmiss-pD-pPip).M()
            m_m_DDmisspip[0] = (pDmiss+pD+pPip).M()
        elif t_in.charm < 0:
            m_m_Dmisspi[0] = (pDmiss+pPim).M()
            m_rm_Dmisspi[0] = (cms-pDmiss-pPim).M()
            m_m_Dpi[0] = (pD+pPip).M()
            m_rm_Dpi[0] = (cms-pD-pPip).M()
            m_rm_DDmisspim[0] = (cms-pDmiss-pD-pPip).M()
            m_m_DDmisspim[0] = (pDmiss+pD+pPip).M()
            m_rm_DDmisspip[0] = (cms-pDmiss-pD-pPim).M()
            m_m_DDmisspip[0] = (pDmiss+pD+pPim).M()
        m_m_DDmiss[0] = (pDmiss+pD).M()
        m_rm_DDmiss[0] = (cms-pDmiss).M() + (cms-pD).M()
        m_rm_Dmisspipi[0] = (cms-pDmiss-pPip-pPim).M()
        m_m_Kpi1[0] = pKpi1.M()
        m_rm_Kpi1[0] = (cms-pKpi1).M()
        m_m_Kpi2[0] = pKpi2.M()
        m_rm_Kpi2[0] = (cms-pKpi2).M()
        m_m_Dpipi[0] = (pD+pPip+pPim).M()
        m_m_Dmisspipi[0] = (pDmiss+pPip+pPim).M()
        m_m_Dmiss[0] = pDmiss.M()
        m_chi2_vf[0] = t_in.chi2_vf
        if region == 'STDDmiss_signal':
            m_chi2_kf[0] = t_in.chi2_kf
            m_rm_Dpipi[0] = t_in.rm_Dpipi
        if region == 'STDDmiss_side1_low':
            m_chi2_kf[0] = t_in.chi2_kf_side1_low
            m_rm_Dpipi[0] = t_in.rm_Dpipi_side1_low
        if region == 'STDDmiss_side1_up':
            m_chi2_kf[0] = t_in.chi2_kf_side1_up
            m_rm_Dpipi[0] = t_in.rm_Dpipi_side1_up
        if region == 'STDDmiss_side2_low':
            m_chi2_kf[0] = t_in.chi2_kf_side2_low
            m_rm_Dpipi[0] = t_in.rm_Dpipi_side2_low
        if region == 'STDDmiss_side2_up':
            m_chi2_kf[0] = t_in.chi2_kf_side2_up
            m_rm_Dpipi[0] = t_in.rm_Dpipi_side2_up
        if region == 'STDDmiss_side3_low':
            m_chi2_kf[0] = t_in.chi2_kf_side3_low
            m_rm_Dpipi[0] = t_in.rm_Dpipi_side3_low
        if region == 'STDDmiss_side3_up':
            m_chi2_kf[0] = t_in.chi2_kf_side3_up
            m_rm_Dpipi[0] = t_in.rm_Dpipi_side3_up
        if region == 'STDDmiss_side4_low':
            m_chi2_kf[0] = t_in.chi2_kf_side4_low
            m_rm_Dpipi[0] = t_in.rm_Dpipi_side4_low
        if region == 'STDDmiss_side4_up':
            m_chi2_kf[0] = t_in.chi2_kf_side4_up
            m_rm_Dpipi[0] = t_in.rm_Dpipi_side4_up
        m_chi2_svf[0] = t_in.chi2_svf
        m_ctau_svf[0] = t_in.ctau_svf
        m_L_svf[0] = t_in.L_svf
        m_Lerr_svf[0] = t_in.Lerr_svf
        m_n_p[0] = t_in.n_p 
        m_n_pbar[0] = t_in.n_pbar
        m_charge_left[0] = t_in.charge_left
        m_m_piplus0[0] = rawpPip.M()
        m_m_piminus0[0] = rawpPim.M()
        m_p_piplus0[0] = rawpPip.P()
        m_p_piminus0[0] = rawpPim.P()
        m_E_piplus0[0] = rawpPip.E()
        m_E_piminus0[0] = rawpPim.E()
        m_chi2_pi0[0] = t_in.chi2_pi0_save
        m_Dpi0 = pD.M()
        rm_Dpi0 = (cms - pD).M()
        if pPi0.M() > 0:
            m_Dpi0 = (pD + pPi0).M()
            rm_Dpi0 = (cms - pD - pPi0).M()
        deltaM = 999.
        m_Dmisspi0 = pDmiss.M()
        rm_Dmisspi0 = (cms - pDmiss).M()
        for iPi0 in xrange(t_in.n_pi0):
            ppi0 = TLorentzVector(0, 0, 0, 0)
            ppi0.SetPxPyPzE(t_in.p4_pi0[iPi0*4+0], t_in.p4_pi0[iPi0*4+1], t_in.p4_pi0[iPi0*4+2], t_in.p4_pi0[iPi0*4+3])
            if (fabs((pDmiss + ppi0).M() - 2.01026) < deltaM):
                deltaM = fabs((pDmiss + ppi0).M() - 2.01026)
                m_Dmisspi0 = (pDmiss + ppi0).M()
                rm_Dmisspi0 = (cms - pDmiss - ppi0).M()
        m_m_Dmisspi0[0] = m_Dmisspi0
        m_rm_Dmisspi0[0] = rm_Dmisspi0
        m_m_Dpi0[0] = m_Dpi0
        m_rm_Dpi0[0] = rm_Dpi0
        m_m_pi0[0] = pPi0.M()
        m_p_pi0[0] = pPi0.P()
        m_E_pi0[0] = pPi0.E()
        m_n_pi0[0] = t_in.n_pi0
        if region == 'STDDmiss_signal':
            m_matched_D[0] = t_in.matched_D
            m_matched_pi[0] = t_in.matched_pi
            m_matched_piplus[0] = t_in.matched_piplus
            m_matched_piminus[0] = t_in.matched_piminus
        mc_truth = TLorentzVector(0, 0, 0, 0)
        all_truth = TLorentzVector(0, 0, 0, 0)
        m_indexmc[0] = t_in.indexmc
        is_psi4260_gen = False
        is_gamma_star_gen = False
        for i in xrange(t_in.indexmc):
            if t_in.pdgid[i] == 9030443: is_psi4260_gen = True # for KKMC
            if t_in.pdgid[i] == 90022: is_gamma_star_gen = True # for ConExc
        tag_psi4260 = False
        for i in xrange(t_in.indexmc):
            m_motheridx[i] = t_in.motheridx[i]
            m_pdgid[i] = t_in.pdgid[i]
            if is_psi4260_gen == True:
                if t_in.pdgid[i] == 9030443:
                    tag_psi4260 = True
                    mc_truth.SetPxPyPzE(t_in.p4_mc_all[i*4 + 0], t_in.p4_mc_all[i*4 + 1], t_in.p4_mc_all[i*4 + 2], t_in.p4_mc_all[i*4 + 3])
                    all_truth += mc_truth
                if t_in.pdgid[i] == -22 and tag_psi4260 == False:
                    mc_truth.SetPxPyPzE(t_in.p4_mc_all[i*4 + 0], t_in.p4_mc_all[i*4 + 1], t_in.p4_mc_all[i*4 + 2], t_in.p4_mc_all[i*4 + 3])
                    all_truth += mc_truth
            if is_gamma_star_gen == True:
                if t_in.pdgid[i] == 90022: mc_truth.SetPxPyPzE(t_in.p4_mc_all[i*4 + 0], t_in.p4_mc_all[i*4 + 1], t_in.p4_mc_all[i*4 + 2], t_in.p4_mc_all[i*4 + 3])
        m_m_truthall[0] = all_truth.M()
        ptrack = TLorentzVector(0, 0, 0, 0)
        p_othertrk = TLorentzVector(0, 0, 0, 0)
        p_othershw = TLorentzVector(0, 0, 0, 0)
        deltaM = 999.
        E_othertrks = 0.
        n_Kp = 0
        n_Km = 0
        n_othertrks = 0
        m_has_badtrks[0] = 0
        m_has_leps[0] = 0
        if not t_in.n_otherleps == 0: m_has_leps[0] = 1
        stat_othertrks = True
        for iTrk in xrange(t_in.n_othertrks):
            m_Vxy_trks[iTrk] = abs(t_in.vtx_otherMdcKaltrk[iTrk*3+0])
            m_Vz_trks[iTrk] = abs(t_in.vtx_otherMdcKaltrk[iTrk*3+1])
            m_cos_theta_trks[iTrk] = abs(t_in.vtx_otherMdcKaltrk[iTrk*3+2])
            if abs(t_in.vtx_otherMdcKaltrk[iTrk*3+0]) >= 1.0:
                stat_othertrks = False
                continue
            if abs(t_in.vtx_otherMdcKaltrk[iTrk*3+1]) >= 10.0:
                stat_othertrks = False
                continue
            if abs(t_in.vtx_otherMdcKaltrk[iTrk*3+2]) >= 0.93:
                stat_othertrks = False
                continue
            if t_in.rawp4_otherMdcKaltrk[iTrk*6+5] == 3:
                if t_in.rawp4_otherMdcKaltrk[iTrk*6+4] == 1:
                    n_Kp += 1
                if t_in.rawp4_otherMdcKaltrk[iTrk*6+4] == -1:
                    n_Km += 1
            n_othertrks += 1
            ptrack.SetPxPyPzE(t_in.rawp4_otherMdcKaltrk[iTrk*6+0], t_in.rawp4_otherMdcKaltrk[iTrk*6+1], t_in.rawp4_otherMdcKaltrk[iTrk*6+2], t_in.rawp4_otherMdcKaltrk[iTrk*6+3])
            ptrack += ptrack
            p_othertrk += ptrack
            E_othertrks += t_in.rawp4_otherMdcKaltrk[iTrk*6+3]
        if not stat_othertrks:
            m_has_badtrks[0] = 1
        m_p_Dmiss[0] = pDmiss.P()
        m_E_othertrks[0] = E_othertrks
        if t_in.charm == 1:
            m_n_Km[0] = n_Km + 1
            m_n_Kp[0] = n_Kp 
        if t_in.charm == -1:
            m_n_Km[0] = n_Km
            m_n_Kp[0] = n_Kp + 1
        m_n_othertrks[0] = n_othertrks
        E_othershws = 0.
        n_othershws = 0
        m_has_badshws[0] = 0
        stat_othershws = True
        for iShw in xrange(t_in.n_othershws):
            m_Emin_shws[iShw] = t_in.vtx_othershw[iShw*6+0]
            m_angle_shws[iShw] = t_in.vtx_othershw[iShw*6+3]
            m_mode_shws[iShw] = t_in.vtx_othershw[iShw*6+4]
            m_T_shws[iShw] = t_in.vtx_othershw[iShw*6+5]
            if abs(t_in.vtx_othershw[iShw*6+3]) < 10.:
                stat_othershws = False
                continue
            if t_in.vtx_othershw[iShw*6+5] < 0. or t_in.vtx_othershw[iShw*6+5] > 14:
                stat_othershws = False
                continue
            if t_in.vtx_othershw[iShw*6+4] == 1 and t_in.vtx_othershw[iShw*6+0] < 0.025:
                stat_othershws = False
                continue
            if (t_in.vtx_othershw[iShw*6+4] == 0 or t_in.vtx_othershw[iShw*6+4] == 2) and t_in.vtx_othershw[iShw*6+0] < 0.05:
                stat_othershws = False
                continue
            pshower = TLorentzVector(0, 0, 0, 0)
            pshower.SetPxPyPzE(t_in.rawp4_othershw[iShw*4+0], t_in.rawp4_othershw[iShw*4+1], t_in.rawp4_othershw[iShw*4+2], t_in.rawp4_othershw[iShw*4+3])
            ptrack += pshower
            p_othershw += pshower
            E_othershws += t_in.rawp4_othershw[iShw*4+3]
            n_othershws += 1
        if not stat_othershws:
            m_has_badshws[0] = 1
        m_E_othershws[0] = E_othershws
        m_n_othershws[0] = n_othershws
        m_p_otherall[0] = ptrack.P()
        m_cos_otherall[0] = ptrack.CosTheta()
        m_cos_other_Dmiss[0] = cos(ptrack.Vect().Angle(pDmiss.Vect()))
        m_p_othertrk[0] = p_othertrk.P()
        m_p_othershw[0] = p_othershw.P()
        m_cos_other_trk_shw[0] = cos(p_othertrk.Vect().Angle(p_othershw.Vect()))
        m_cos_other_trk[0] = p_othertrk.CosTheta()
        m_cos_other_shw[0] = p_othershw.CosTheta()
        m_m_Kpipipi1[0] = (ptrack_K + rawpPip + rawpPim + ptrack_pi1).M()
        m_m_Kpipipi2[0] = (ptrack_K + rawpPip + rawpPim + ptrack_pi2).M()
        m_cos_D[0] = pD_raw.CosTheta()
        t.Fill()

def save_raw(f_in, cms, t, region):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_mode = array('i', [0])
    m_charm = array('i', [0])
    m_rrawm_Dpipi = array('d', [999.])
    m_rawm_D = array('d', [999.])
    m_rm_D = array('d', [999.])
    m_rm_pipi = array('d', [999.])
    m_rm_pip = array('d', [999.])
    m_rm_pim = array('d', [999.])
    m_m_pipi = array('d', [999.])
    m_m_Dpi = array('d', [999.])
    m_rm_Dpi = array('d', [999.])
    m_m_Dpip = array('d', [999.])
    m_m_Dpim = array('d', [999.])
    m_m_Dpipi = array('d', [999.])
    m_rm_Dpipi = array('d', [999.])
    m_chi2_vf = array('d', [999.])
    m_chi2_kf = array('d', [999.])
    m_n_othershws = array('i', [0])
    m_n_othertrks = array('i', [0])
    m_n_p = array('i', [0])
    m_n_pbar = array('i', [0])
    m_n_Kp = array('i', [0])
    m_n_Km = array('i', [0])
    m_m_truthall = array('d', [0.])
    m_charge_left = array('i', [0])
    m_m_piplus0 = array('d', [999.])
    m_m_piminus0 = array('d', [999.])
    m_p_piplus0 = array('d', [999.])
    m_p_piminus0 = array('d', [999.])
    m_E_piplus0 = array('d', [999.])
    m_E_piminus0 = array('d', [999.])
    m_chi2_pi0 = array('d', [999.])
    m_m_Dpi0 = array('d', [999.])
    m_m_pi0 = array('d', [999.])
    m_p_pi0 = array('d', [999.])
    m_E_pi0 = array('d', [999.])
    m_n_pi0 = array('i', [0])
    m_matched_D = array('i', [0])
    m_matched_pi = array('i', [0])
    m_indexmc = array('i', [0])
    m_motheridx = array('i', 100*[0])
    m_pdgid = array('i', 100*[0])
    m_E_othertrks = array('d', [0.])
    m_E_othershws = array('d', [0.])
    m_p_otherall = array('d', [0.])
    m_cos_otherall = array('d', [0.])
    m_has_badshws = array('i', [0])
    m_has_badtrks = array('i', [0])
    m_has_leps = array('i', [0])
    m_m_Kpipipi1 = array('d', [0])
    m_m_Kpipipi2 = array('d', [0])
    m_Vxy_Dtrks = array('d', 3*[999.])
    m_Vz_Dtrks = array('d', 3*[999.])
    m_cos_theta_Dtrks = array('d', 3*[999.])
    m_Vxy_pip = array('d', [999.])
    m_Vz_pip = array('d', [999.])
    m_cos_theta_pip = array('d', [999.])
    m_Vxy_pim = array('d', [999.])
    m_Vz_pim = array('d', [999.])
    m_cos_theta_pim = array('d', [999.])
    m_chi2_svf = array('d', [999.])
    m_ctau_svf = array('d', [999.])
    m_L_svf = array('d', [999.])
    m_Lerr_svf = array('d', [999.])
    m_n_count = array('i', [0])
    t.Branch('runNo', m_runNo, 'm_runNo/I')
    t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
    t.Branch('mode', m_mode, 'm_mode/I')
    t.Branch('charm', m_charm, 'm_charm/I')
    t.Branch('rrawm_Dpipi', m_rrawm_Dpipi, 'm_rrawm_Dpipi/D')
    t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
    t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
    t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
    t.Branch('rm_pip', m_rm_pip, 'm_rm_pip/D')
    t.Branch('rm_pim', m_rm_pim, 'm_rm_pim/D')
    t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
    t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
    t.Branch('rm_Dpi', m_rm_Dpi, 'm_rm_Dpi/D')
    t.Branch('m_Dpip', m_m_Dpip, 'm_m_Dpip/D')
    t.Branch('m_Dpim', m_m_Dpim, 'm_m_Dpim/D')
    t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
    t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
    t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')
    t.Branch('n_othertrks', m_n_othertrks, 'm_n_othertrks/I')
    t.Branch('n_othershws', m_n_othershws, 'm_n_othershws/I')
    t.Branch('n_p', m_n_p, 'm_n_p/I')
    t.Branch('n_pbar', m_n_pbar, 'm_n_pbar/I')
    t.Branch('n_Kp', m_n_Kp, 'm_n_Kp/I')
    t.Branch('n_Km', m_n_Km, 'm_n_Km/I')
    t.Branch('m_truthall', m_m_truthall, 'm_m_truthall/D')
    t.Branch('charge_left', m_charge_left, 'm_charge_left/I')
    t.Branch('m_piplus0', m_m_piplus0, 'm_m_piplus0/D')
    t.Branch('m_piminus0', m_m_piminus0, 'm_m_piminus0/D')
    t.Branch('p_piplus0', m_p_piplus0, 'm_p_piplus0/D')
    t.Branch('p_piminus0', m_p_piminus0, 'm_p_piminus0/D')
    t.Branch('E_piplus0', m_E_piplus0, 'm_E_piplus0/D')
    t.Branch('E_piminus0', m_E_piminus0, 'm_E_piminus0/D')
    t.Branch('chi2_pi0', m_chi2_pi0, 'm_chi2_pi0/D')
    t.Branch('m_Dpi0', m_m_Dpi0, 'm_m_Dpi0/D')
    t.Branch('m_pi0', m_m_pi0, 'm_m_pi0/D')
    t.Branch('p_pi0', m_p_pi0, 'm_p_pi0/D')
    t.Branch('E_pi0', m_E_pi0, 'm_E_pi0/D')
    t.Branch('n_pi0', m_n_pi0, 'm_n_pi0/I')
    t.Branch('matched_D', m_matched_D, 'm_matched_D/I')
    t.Branch('matched_pi', m_matched_pi, 'm_matched_pi/I')
    t.Branch('indexmc', m_indexmc, 'indexmc/I')
    t.Branch('motheridx', m_motheridx, 'motheridx[100]/I')
    t.Branch('pdgid', m_pdgid, 'pdgid[100]/I')
    t.Branch('E_othertrks', m_E_othertrks, 'm_E_othertrks/D')
    t.Branch('E_othershws', m_E_othershws, 'm_E_othershws/D')
    t.Branch('p_otherall', m_p_otherall, 'm_p_otherall/D')
    t.Branch('cos_otherall', m_cos_otherall, 'm_cos_otherall/D')
    t.Branch('has_badtrks', m_has_badtrks, 'm_has_badtrks/I')
    t.Branch('has_badshws', m_has_badshws, 'm_has_badshws/I')
    t.Branch('has_leps', m_has_leps, 'm_has_leps/I')
    t.Branch('m_Kpipipi1', m_m_Kpipipi1, 'm_m_Kpipipi1/D')
    t.Branch('m_Kpipipi2', m_m_Kpipipi2, 'm_m_Kpipipi2/D')
    t.Branch('Vxy_Dtrks', m_Vxy_Dtrks, 'm_Vxy_Dtrks[100]/D')
    t.Branch('Vz_Dtrks', m_Vz_Dtrks, 'm_Vz_Dtrks[100]/D')
    t.Branch('cos_theta_Dtrks', m_cos_theta_Dtrks, 'm_cos_theta_Dtrks[100]/D')
    t.Branch('Vxy_pip', m_Vxy_pip, 'm_Vxy_pip/D')
    t.Branch('Vz_pip', m_Vz_pip, 'm_Vz_pip/D')
    t.Branch('cos_theta_pip', m_cos_theta_pip, 'm_cos_theta_pip/D')
    t.Branch('Vxy_pim', m_Vxy_pim, 'm_Vxy_pim/D')
    t.Branch('Vz_pim', m_Vz_pim, 'm_Vz_pim/D')
    t.Branch('cos_theta_pim', m_cos_theta_pim, 'm_cos_theta_pim/D')
    t.Branch('chi2_svf', m_chi2_svf, 'm_chi2_svf/D')
    t.Branch('ctau_svf', m_ctau_svf, 'm_ctau_svf/D')
    t.Branch('L_svf', m_L_svf, 'm_L_svf/D')
    t.Branch('Lerr_svf', m_Lerr_svf, 'm_Lerr_svf/D')
    t.Branch('n_count', m_n_count, 'm_n_count/I')
    t_std = f_in.Get('STD')
    nentries = t_std.GetEntries()
    for ientry in xrange(nentries):
        t_std.GetEntry(ientry)
        if t_std.mode != 200:
            continue
        pD_raw = TLorentzVector(0, 0, 0, 0)
        pD = TLorentzVector(0, 0, 0, 0)
        pKpi1 = TLorentzVector(0, 0, 0, 0)
        pKpi2 = TLorentzVector(0, 0, 0, 0)
        ptrack_K = TLorentzVector(0, 0, 0, 0)
        ptrack_pi1 = TLorentzVector(0, 0, 0, 0)
        ptrack_pi2 = TLorentzVector(0, 0, 0, 0)
        for iTrk in xrange(t_std.n_trkD):
            ptrack_raw = TLorentzVector(0, 0, 0, 0)
            ptrack_Kpi1 = TLorentzVector(0, 0, 0, 0)
            ptrack_Kpi2 = TLorentzVector(0, 0, 0, 0)
            ptrack = TLorentzVector(0, 0, 0, 0)
            ptrack_raw.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*9+0], t_std.rawp4_Dtrk[iTrk*9+1], t_std.rawp4_Dtrk[iTrk*9+2], t_std.rawp4_Dtrk[iTrk*9+3])
            if region == 'raw_signal':
                ptrack.SetPxPyPzE(t_std.p4_Dtrk[iTrk*4+0], t_std.p4_Dtrk[iTrk*4+1], t_std.p4_Dtrk[iTrk*4+2], t_std.p4_Dtrk[iTrk*4+3])
            if region == 'raw_sidebandlow':
                ptrack.SetPxPyPzE(t_std.p4_Dlowtrk[iTrk*4+0], t_std.p4_Dlowtrk[iTrk*4+1], t_std.p4_Dlowtrk[iTrk*4+2], t_std.p4_Dlowtrk[iTrk*4+3])
            if region == 'raw_sidebandup':
                ptrack.SetPxPyPzE(t_std.p4_Duptrk[iTrk*4+0], t_std.p4_Duptrk[iTrk*4+1], t_std.p4_Duptrk[iTrk*4+2], t_std.p4_Duptrk[iTrk*4+3])
            pD_raw += ptrack_raw
            pD += ptrack
            if t_std.rawp4_Dtrk[iTrk*9+5] == 3:
                ptrack_Kpi1.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*9+0], t_std.rawp4_Dtrk[iTrk*9+1], t_std.rawp4_Dtrk[iTrk*9+2], t_std.rawp4_Dtrk[iTrk*9+3])
                ptrack_Kpi2.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*9+0], t_std.rawp4_Dtrk[iTrk*9+1], t_std.rawp4_Dtrk[iTrk*9+2], t_std.rawp4_Dtrk[iTrk*9+3])
                ptrack_K.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*9+0], t_std.rawp4_Dtrk[iTrk*9+1], t_std.rawp4_Dtrk[iTrk*9+2], t_std.rawp4_Dtrk[iTrk*9+3])
                pKpi1 += ptrack_Kpi1
                pKpi2 += ptrack_Kpi2
            if t_std.rawp4_Dtrk[iTrk*9+5] == 2 and iTrk == 1:
                ptrack_Kpi1.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*9+0], t_std.rawp4_Dtrk[iTrk*9+1], t_std.rawp4_Dtrk[iTrk*9+2], t_std.rawp4_Dtrk[iTrk*9+3])
                ptrack_pi1.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*9+0], t_std.rawp4_Dtrk[iTrk*9+1], t_std.rawp4_Dtrk[iTrk*9+2], t_std.rawp4_Dtrk[iTrk*9+3])
                pKpi1 += ptrack_Kpi1
            if t_std.rawp4_Dtrk[iTrk*9+5] == 2 and iTrk == 2:
                ptrack_Kpi2.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*9+0], t_std.rawp4_Dtrk[iTrk*9+1], t_std.rawp4_Dtrk[iTrk*9+2], t_std.rawp4_Dtrk[iTrk*9+3])
                ptrack_pi2.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*9+0], t_std.rawp4_Dtrk[iTrk*9+1], t_std.rawp4_Dtrk[iTrk*9+2], t_std.rawp4_Dtrk[iTrk*9+3])
                pKpi2 += ptrack_Kpi2
            m_Vxy_Dtrks[iTrk] = abs(t_std.rawp4_Dtrk[iTrk*9+6])
            m_Vz_Dtrks[iTrk] = abs(t_std.rawp4_Dtrk[iTrk*9+7])
            m_cos_theta_Dtrks[iTrk] = abs(t_std.rawp4_Dtrk[iTrk*9+8])
        for iShw in xrange(t_std.n_shwD):
            pshower_raw = TLorentzVector(0, 0, 0, 0)
            pshower = TLorentzVector(0, 0, 0, 0)
            pshower_raw.SetPxPyPzE(t_std.rawp4_Dshw[iShw*4+0], t_std.rawp4_Dshw[iShw*4+1], t_std.rawp4_Dshw[iShw*4+2], t_std.rawp4_Dshw[iShw*4+3])
            if region == 'raw_signal':
                pshower.SetPxPyPzE(t_std.p4_Dshw[iShw*4+0], t_std.p4_Dshw[iShw*4+1], t_std.p4_Dshw[iShw*4+2], t_std.p4_Dshw[iShw*4+3])
            if region == 'raw_sidebandlow':
                pshower.SetPxPyPzE(t_std.p4_Dlowshw[iShw*4+0], t_std.p4_Dlowshw[iShw*4+1], t_std.p4_Dlowshw[iShw*4+2], t_std.p4_Dlowshw[iShw*4+3])
            if region == 'raw_sidebandup':
                pshower.SetPxPyPzE(t_std.p4_Dupshw[iShw*4+0], t_std.p4_Dupshw[iShw*4+1], t_std.p4_Dupshw[iShw*4+2], t_std.p4_Dupshw[iShw*4+3])
            pD_raw += pshower_raw
            pD += pshower
        pPip = TLorentzVector(0,0,0,0)
        pPim = TLorentzVector(0,0,0,0)
        count_pip = 0
        count_pim = 0
        n_combination = 0
        for iTrk1 in xrange(t_std.n_othertrks):
            if t_std.rawp4_otherMdcKaltrk[iTrk1*7+4] != 1:
                continue
            if t_std.rawp4_otherMdcKaltrk[iTrk1*7+5] != 2:
                continue
            pPip.SetPxPyPzE(t_std.rawp4_otherMdcKaltrk[iTrk1*7+0], t_std.rawp4_otherMdcKaltrk[iTrk1*7+1], t_std.rawp4_otherMdcKaltrk[iTrk1*7+2], t_std.rawp4_otherMdcKaltrk[iTrk1*7+3])
            for iTrk2 in xrange(t_std.n_othertrks):
                if t_std.rawp4_otherMdcKaltrk[iTrk2*7+4] != -1:
                    continue
                if t_std.rawp4_otherMdcKaltrk[iTrk2*7+5] != 2:
                    continue
                pPim.SetPxPyPzE(t_std.rawp4_otherMdcKaltrk[iTrk2*7+0], t_std.rawp4_otherMdcKaltrk[iTrk2*7+1], t_std.rawp4_otherMdcKaltrk[iTrk2*7+2], t_std.rawp4_otherMdcKaltrk[iTrk2*7+3])
                m_runNo[0] = t_std.runNo
                m_evtNo[0] = t_std.evtNo
                m_mode[0] = t_std.mode
                m_charm[0] = t_std.charm
                m_rrawm_Dpipi[0] = (cms-pD_raw-pPip-pPim).M()
                m_rawm_D[0] = pD_raw.M()
                m_rm_D[0] = (cms-pD).M()
                m_rm_pipi[0] = (cms-pPip-pPim).M()
                m_rm_pip[0] = (cms-pPip).M()
                m_rm_pim[0] = (cms-pPim).M()
                m_m_pipi[0] = (pPip+pPim).M()
                m_m_Dpim[0] = (pD+pPim).M()
                m_m_Dpip[0] = (pD+pPip).M()
                if t_std.charm > 0:
                    m_m_Dpi[0] = (pD+pPim).M()
                    m_rm_Dpi[0] = (cms-pD-pPim).M()
                elif t_std.charm < 0:
                    m_m_Dpi[0] = (pD+pPip).M()
                    m_rm_Dpi[0] = (cms-pD-pPip).M()
                m_m_Dpipi[0] = (pD+pPip+pPim).M()
                m_rm_Dpipi[0] = (cms-pD-pPip-pPim).M()
                m_chi2_vf[0] = t_std.chi2_vf
                if region == 'raw_signal':
                    m_chi2_kf[0] = t_std.chi2_kf
                if region == 'raw_sidebandlow':
                    m_chi2_kf[0] = t_std.chi2_kf_low
                if region == 'raw_sidebandup':
                    m_chi2_kf[0] = t_std.chi2_kf_up
                m_n_p[0] = t_std.n_p 
                m_n_pbar[0] = t_std.n_pbar
                charge_left = 0
                for i in xrange(t_std.n_othertrks):
                    if i != iTrk1 and i != iTrk2:
                        charge_left += t_std.rawp4_otherMdcKaltrk[i*7+4]
                m_charge_left[0] = int(charge_left)
                m_m_piplus0[0] = pPip.M()
                m_m_piminus0[0] = pPim.M()
                m_p_piplus0[0] = pPip.P()
                m_p_piminus0[0] = pPim.P()
                m_E_piplus0[0] = pPip.E()
                m_E_piminus0[0] = pPim.E()
                m_chi2_pi0[0] = t_std.chi2_pi0_save
                m_Dpi0 = pD.M()
                pPi0 = TLorentzVector(0, 0, 0, 0)
                pPi0.SetPxPyPzE(t_std.p4_pi0_save[0], t_std.p4_pi0_save[1], t_std.p4_pi0_save[2], t_std.p4_pi0_save[3])
                if pPi0.M() > 0:
                    m_Dpi0 = (pD + pPi0).M()
                m_m_Dpi0[0] = m_Dpi0
                m_m_pi0[0] = pPi0.M()
                m_p_pi0[0] = pPi0.P()
                m_E_pi0[0] = pPi0.E()
                m_n_pi0[0] = t_std.n_pi0
                m_matched_D[0] = t_std.matched_D
                if t_std.rawp4_otherMdcKaltrk[iTrk1*7+6] == 1 and t_std.rawp4_otherMdcKaltrk[iTrk2*7+6] == 1:
                    m_matched_pi[0] = 1
                else:
                    m_matched_pi[0] = 0
                mc_truth = TLorentzVector(0, 0, 0, 0)
                all_truth = TLorentzVector(0, 0, 0, 0)
                m_indexmc[0] = t_std.indexmc
                is_psi4260_gen = False
                is_gamma_star_gen = False
                for i in xrange(t_std.indexmc):
                    if t_std.pdgid[i] == 9030443: is_psi4260_gen = True # for KKMC
                    if t_std.pdgid[i] == 90022: is_gamma_star_gen = True # for ConExc
                tag_psi4260 = False
                for i in xrange(t_std.indexmc):
                    m_motheridx[i] = t_std.motheridx[i]
                    m_pdgid[i] = t_std.pdgid[i]
                    if is_psi4260_gen == True:
                        if t_std.pdgid[i] == 9030443:
                            tag_psi4260 = True
                            mc_truth.SetPxPyPzE(t_std.p4_mc_all[i*4 + 0], t_std.p4_mc_all[i*4 + 1], t_std.p4_mc_all[i*4 + 2], t_std.p4_mc_all[i*4 + 3])
                            all_truth += mc_truth
                        if t_std.pdgid[i] == -22 and tag_psi4260 == False:
                            mc_truth.SetPxPyPzE(t_std.p4_mc_all[i*4 + 0], t_std.p4_mc_all[i*4 + 1], t_std.p4_mc_all[i*4 + 2], t_std.p4_mc_all[i*4 + 3])
                            all_truth += mc_truth
                    if is_gamma_star_gen == True:
                        if t_std.pdgid[i] == 90022: mc_truth.SetPxPyPzE(t_std.p4_mc_all[i*4 + 0], t_std.p4_mc_all[i*4 + 1], t_std.p4_mc_all[i*4 + 2], t_std.p4_mc_all[i*4 + 3])
                m_m_truthall[0] = all_truth.M()
                ptrack = TLorentzVector(0, 0, 0, 0)
                E_othertrks = 0.
                n_Kp = 0
                n_Km = 0
                n_othertrks = 0
                m_has_leps[0] = 0
                if (len(t_std.rawp4_otherlep) > 0): m_has_leps[0] = 1
                if not t_std.n_otherleps == 0: m_has_leps[0] = 1
                m_has_badtrks[0] = 0
                trk_status = True
                for iTrk in xrange(t_std.n_othertrks):
                    if (iTrk == iTrk1) or (iTrk == iTrk2):
                        continue
                    if abs(t_std.vtx_otherMdcKaltrk[iTrk*3+0]) >= 1.0:
                        trk_status = False
                        continue
                    if abs(t_std.vtx_otherMdcKaltrk[iTrk*3+1]) >= 10.0:
                        trk_status = False
                        continue
                    if abs(t_std.vtx_otherMdcKaltrk[iTrk*3+2]) >= 0.93:
                        trk_status = False
                        continue
                    if t_std.rawp4_otherMdcKaltrk[iTrk*6+5] == 3:
                        if t_std.rawp4_otherMdcKaltrk[iTrk*6+4] == 1:
                            n_Kp += 1
                        if t_std.rawp4_otherMdcKaltrk[iTrk*6+4] == -1:
                            n_Km += 1
                    n_othertrks += 1
                    ptrack.SetPxPyPzE(t_std.rawp4_otherMdcKaltrk[iTrk*6+0], t_std.rawp4_otherMdcKaltrk[iTrk*6+1], t_std.rawp4_otherMdcKaltrk[iTrk*6+2], t_std.rawp4_otherMdcKaltrk[iTrk*6+3])
                    ptrack += ptrack
                    E_othertrks += t_std.rawp4_otherMdcKaltrk[iTrk*6+3]
                if not trk_status:
                    m_has_badtrks[0] = 1
                if t_std.charm == 1:
                    m_n_Km[0] = n_Km + 1
                    m_n_Kp[0] = n_Kp 
                if t_std.charm == -1:
                    m_n_Km[0] = n_Km
                    m_n_Kp[0] = n_Kp + 1
                m_n_othertrks[0] = n_othertrks
                E_othershws = 0.
                n_othershws = 0
                m_has_badshws[0] = 0
                shw_status = True
                for iShw in xrange(t_std.n_othershws):
                    if abs(t_std.vtx_othershw[iShw*6+3]) < 10.:
                        shw_status = False
                        continue
                    if t_std.vtx_othershw[iShw*6+5] < 0. or t_std.vtx_othershw[iShw*6+5] > 14:
                        shw_status = False
                        continue
                    if t_std.vtx_othershw[iShw*6+4] == 1 and t_std.vtx_othershw[iShw*6+0] < 0.025:
                        shw_status = False
                        continue
                    if (t_std.vtx_othershw[iShw*6+4] == 0 or t_std.vtx_othershw[iShw*6+4] == 2) and t_std.vtx_othershw[iShw*6+0] < 0.05:
                        shw_status = False
                        continue
                    pshower = TLorentzVector(0, 0, 0, 0)
                    pshower.SetPxPyPzE(t_std.rawp4_othershw[iShw*4+0], t_std.rawp4_othershw[iShw*4+1], t_std.rawp4_othershw[iShw*4+2], t_std.rawp4_othershw[iShw*4+3])
                    ptrack += pshower
                    E_othershws += t_std.rawp4_othershw[iShw*4+3]
                    n_othershws += 1
                if not shw_status:
                    m_has_badshws[0] = 1
                m_n_othershws[0] = n_othershws
                m_p_otherall[0] = ptrack.P()
                m_cos_otherall[0] = ptrack.CosTheta()
                m_E_othertrks[0] = E_othertrks
                m_E_othershws[0] = E_othershws
                m_m_Kpipipi1[0] = (ptrack_K + pPip + pPim + ptrack_pi1).M()
                m_m_Kpipipi2[0] = (ptrack_K + pPip + pPim + ptrack_pi2).M()
                m_Vxy_pip[0] = abs(t_std.vtx_otherMdcKaltrk[iTrk1*3 + 0])
                m_Vz_pip[0] = abs(t_std.vtx_otherMdcKaltrk[iTrk1*3 + 1])
                m_cos_theta_pip[0] = abs(t_std.vtx_otherMdcKaltrk[iTrk1*3 + 2])
                m_Vxy_pim[0] = abs(t_std.vtx_otherMdcKaltrk[iTrk2*3 + 0])
                m_Vz_pim[0] = abs(t_std.vtx_otherMdcKaltrk[iTrk2*3 + 1])
                m_cos_theta_pim[0] = abs(t_std.vtx_otherMdcKaltrk[iTrk2*3 + 2])
                for i_pipi in xrange(t_std.n_pipi_combination):
                    if i_pipi == n_combination:
                        m_chi2_svf[0] = t_std.chi2_svf[i_pipi]
                        m_ctau_svf[0] = t_std.ctau_svf[i_pipi]
                        m_L_svf[0] = t_std.L_svf[i_pipi]
                        m_Lerr_svf[0] = t_std.Lerr_svf[i_pipi]
                n_combination += 1
                m_n_count[0] = t_std.n_count
                if m_rm_Dpipi[0] > 1.7 and m_rm_Dpipi[0] < 2.0:
                    t.Fill()

def save_truth(f_in, cms, t, region):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_indexmc = array('i', [0])
    m_motheridx = array('i', 100*[0])
    m_pdgid = array('i', 100*[0])
    m_m_truthall = array('d', [999.])
    t.Branch('runNo', m_runNo, 'm_runNo/I')
    t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
    t.Branch('indexmc', m_indexmc, 'indexmc/I')
    t.Branch('motheridx', m_motheridx, 'motheridx[100]/I')
    t.Branch('pdgid', m_pdgid, 'pdgid[100]/I')
    t.Branch('m_truthall', m_m_truthall, 'm_m_truthall/D')
    t_Truth = f_in.Get('Truth')
    nentries = t_Truth.GetEntries()
    for ientry in xrange(nentries):
        t_Truth.GetEntry(ientry)
        m_runNo[0] = t_Truth.runNo
        m_evtNo[0] = t_Truth.evtNo
        m_indexmc[0] = t_Truth.indexmc
        mc_truth = TLorentzVector(0, 0, 0, 0)
        all_truth = TLorentzVector(0, 0, 0, 0)
        is_psi4260_gen = False
        is_gamma_star_gen = False
        for i in xrange(t_Truth.indexmc):
            if t_Truth.pdgid[i] == 9030443: is_psi4260_gen = True # for KKMC
            if t_Truth.pdgid[i] == 90022: is_gamma_star_gen = True # for ConExc
        tag_psi4260 = False
        for i in xrange(t_Truth.indexmc):
            m_motheridx[i] = t_Truth.motheridx[i]
            m_pdgid[i] = t_Truth.pdgid[i]
            if is_psi4260_gen == True:
                if t_Truth.pdgid[i] == 9030443:
                    tag_psi4260 = True
                    mc_truth.SetPxPyPzE(t_Truth.p4_mc_all[i*4 + 0], t_Truth.p4_mc_all[i*4 + 1], t_Truth.p4_mc_all[i*4 + 2], t_Truth.p4_mc_all[i*4 + 3])
                    all_truth += mc_truth
                if t_Truth.pdgid[i] == -22 and tag_psi4260 == False:
                    mc_truth.SetPxPyPzE(t_Truth.p4_mc_all[i*4 + 0], t_Truth.p4_mc_all[i*4 + 1], t_Truth.p4_mc_all[i*4 + 2], t_Truth.p4_mc_all[i*4 + 3])
                    all_truth += mc_truth
            if is_gamma_star_gen == True:
                if t_Truth.pdgid[i] == 90022: mc_truth.SetPxPyPzE(t_Truth.p4_mc_all[i*4 + 0], t_Truth.p4_mc_all[i*4 + 1], t_Truth.p4_mc_all[i*4 + 2], t_Truth.p4_mc_all[i*4 + 3])
        m_m_truthall[0] = all_truth.M()
        t.Fill()

def main():
    args = sys.argv[1:]
    if len(args)<3:
        return usage()
    file_in = args[0]
    file_out = args[1]
    ecms = float(args[2])
    region = args[3]

    f_in = TFile(file_in)
    f_out = TFile(file_out, 'recreate')
    t_out = TTree('save', 'save')
    t_truth = TTree('truth', 'truth')
    cms = TLorentzVector(0.011*ecms, 0, 0, ecms)
    if region == 'raw_signal' or region == 'raw_sidebandlow' or region == 'raw_sidebandup':
        save_raw(f_in, cms, t_out, region)
    if region == 'STDDmiss_signal' or region == 'STDDmiss_side1_low' or region == 'STDDmiss_side1_up' or region == 'STDDmiss_side2_low' or region == 'STDDmiss_side2_up' or region == 'STDDmiss_side3_low' or region == 'STDDmiss_side3_up' or region == 'STDDmiss_side4_low' or region == 'STDDmiss_side4_up':
        save_missing(f_in, cms, t_out, region)
    if region == 'truth':
        save_truth(f_in, cms, t_truth, region)

    f_out.cd()
    if not region == 'truth':
        t_out.Write()
    if region == 'truth':
        t_truth.Write()
    f_out.Close()

if __name__ == '__main__':
    main()
