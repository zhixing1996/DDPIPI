#!/usr/bin/env python
"""
Get useful info from raw root files
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-03 Tue 05:41]"

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
    get_info.py

SYNOPSIS
    ./get_info.py [infile_path] [outfile_path] [Ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    August 2019
\n''')

def save_missing(f_in, cms, t, MODE):
    if MODE == 'signal' or MODE == 'sidebandlow' or MODE == 'sidebandup':
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
    if MODE == 'signal':
        t_in = f_in.Get('STD_signal')
    if MODE == 'sidebandlow':
        t_in = f_in.Get('STD_sidebandlow')
    if MODE == 'sidebandup':
        t_in = f_in.Get('STD_sidebandup')
    if MODE == 'signal' or 'sidebandlow' or 'sidebandup':
        nentries = t_in.GetEntries()
        for ientry in range(nentries):
            t_in.GetEntry(ientry)
            if t_in.mode != 200:
                continue
            pD_raw = TLorentzVector(0, 0, 0, 0)
            pD = TLorentzVector(0, 0, 0, 0)
            for iTrk in range(t_in.n_trkD):
                ptrack_raw = TLorentzVector(0, 0, 0, 0)
                ptrack = TLorentzVector(0, 0, 0, 0)
                ptrack_raw.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*4+0], t_in.rawp4_Dtrk[iTrk*4+1], t_in.rawp4_Dtrk[iTrk*4+2], t_in.rawp4_Dtrk[iTrk*4+3])
                ptrack.SetPxPyPzE(t_in.p4_Dtrk[iTrk*4+0], t_in.p4_Dtrk[iTrk*4+1], t_in.p4_Dtrk[iTrk*4+2], t_in.p4_Dtrk[iTrk*4+3])
                pD_raw += ptrack_raw
                pD += ptrack
            pPip = TLorentzVector(0,0,0,0)
            pPim = TLorentzVector(0,0,0,0)
            pPi0 = TLorentzVector(0, 0, 0, 0)
            pPip.SetPxPyPzE(t_in.p4_piplus[0], t_in.p4_piplus[1], t_in.p4_piplus[2], t_in.p4_piplus[3])
            pPim.SetPxPyPzE(t_in.p4_piminus[0], t_in.p4_piminus[1], t_in.p4_piminus[2], t_in.p4_piminus[3])
            pPi0.SetPxPyPzE(t_in.p4_pi0_save[0], t_in.p4_pi0_save[1], t_in.p4_pi0_save[2], t_in.p4_pi0_save[3])
            m_runNo[0] = t_in.runNo
            m_evtNo[0] = t_in.evtNo
            m_mode[0] = t_in.mode
            m_charm[0] = t_in.charm
            m_rawm_D[0] = pD_raw.M()
            m_m_D[0] = pD.M()
            m_rm_D[0] = (cms-pD).M()
            m_rm_pipi[0] = (cms-pPip-pPim).M()
            m_m_pipi[0] = (pPip+pPim).M()
            if t_in.charm > 0:
                m_m_Dpi[0] = (pD+pPim).M()
            elif t_in.charm < 0:
                m_m_Dpi[0] = (pD+pPip).M()
            m_m_Dpipi[0] = (pD+pPip+pPim).M()
            m_rm_Dpipi[0] = (cms-pD-pPip-pPim).M()
            m_chi2_vf[0] = t_in.chi2_vf
            m_chi2_kf[0] = t_in.chi2_kf
            m_charge_left[0] = t_in.charge_left
            m_chi2_pi0[0] = t_in.chi2_pi0_save
            m_m_Dpi0[0] = (pD+pPi0).M()
            m_m_pi0[0] = pPi0.M()
            m_n_pi0[0] = t_in.n_pi0
            if t_in.charm == 1:
                pothers = TLorentzVector(0, 0, 0, 0)
                pD0_cand = TLorentzVector(0, 0, 0, 0)
                for iTrk in range(t_in.n_othertrks):
                    pKpi = TLorentzVector(0, 0, 0, 0)
                    pKpi.SetPxPyPzE(t_in.rawp4_otherMdcKaltrk[iTrk*6+0], t_in.rawp4_otherMdcKaltrk[iTrk*6+1], t_in.rawp4_otherMdcKaltrk[iTrk*6+2], t_in.rawp4_otherMdcKaltrk[iTrk*6+3])
                    pothers += pKpi
                pD0_cand = pothers + pPip
                m_D0_back = pD0_cand.M()
                delta_M = 999.
                m_D0 = 0.
                for iPi0 in range(t_in.n_pi0):
                    pPi0_cand1 = TLorentzVector(0, 0, 0, 0)
                    pPi0_cand1.SetPxPyPzE(t_in.p4_pi0[iPi0*4+0], t_in.p4_pi0[iPi0*4+1], t_in.p4_pi0[iPi0*4+2], t_in.p4_pi0[iPi0*4+3])
                    if pPi0_cand1.M() != pPi0.M() and pPi0_cand1.M() > 0:
                        pD01 = TLorentzVector(0, 0, 0, 0)
                        pD01 = pD0_cand + pPi0_cand1
                        if math.fabs(pD01.M() - 1.86483) < delta_M:
                            delta_M = pD01.M() - 1.86483
                            m_D0 = pD01.M()
                            for jPi0 in range(t_in.n_pi0):
                                pPi0_cand2 = TLorentzVector(0, 0, 0, 0)
                                pPi0_cand2.SetPxPyPzE(t_in.p4_pi0[jPi0*4+0], t_in.p4_pi0[jPi0*4+1], t_in.p4_pi0[jPi0*4+2], t_in.p4_pi0[jPi0*4+3])
                                if pPi0_cand2.M() != pPi0.M() and pPi0_cand2.M() != pPi0_cand1.M() and pPi0_cand2.M() > 0:
                                    pD02 = TLorentzVector(0, 0, 0, 0)
                                    pD02 = pD01 + pPi0_cand2
                                    if math.fabs(pD02.M() - 1.86483) < delta_M:
                                        delta_M = pD02.M() - 1.86483
                                        m_D0 = pD02.M()
                if (m_D0 - 1.86483) <= (m_D0_back - 1.86483):
                    m_m_D0[0] = m_D0
                else:
                    m_m_D0[0] = m_D0_back
            if t_in.charm == -1:
                pothers = TLorentzVector(0, 0, 0, 0)
                pD0_cand = TLorentzVector(0, 0, 0, 0)
                for iTrk in range(t_in.n_othertrks):
                    pKpi = TLorentzVector(0, 0, 0, 0)
                    pKpi.SetPxPyPzE(t_in.rawp4_otherMdcKaltrk[iTrk*6+0], t_in.rawp4_otherMdcKaltrk[iTrk*6+1], t_in.rawp4_otherMdcKaltrk[iTrk*6+2], t_in.rawp4_otherMdcKaltrk[iTrk*6+3])
                    pothers += pKpi
                pD0_cand = pothers + pPim
                m_D0_back = pD0_cand.M()
                delta_M = 999.
                m_D0 = 0.
                for iPi0 in range(t_in.n_pi0):
                    pPi0_cand1 = TLorentzVector(0, 0, 0, 0)
                    pPi0_cand1.SetPxPyPzE(t_in.p4_pi0[iPi0*4+0], t_in.p4_pi0[iPi0*4+1], t_in.p4_pi0[iPi0*4+2], t_in.p4_pi0[iPi0*4+3])
                    if pPi0_cand1.M() != pPi0.M() and pPi0_cand1.M() > 0:
                        pD01 = TLorentzVector(0, 0, 0, 0)
                        pD01 = pD0_cand + pPi0_cand1
                        if math.fabs(pD01.M() - 1.86483) < delta_M:
                            delta_M = pD01.M() - 1.86483
                            m_D0 = pD01.M()
                            for jPi0 in range(t_in.n_pi0):
                                pPi0_cand2 = TLorentzVector(0, 0, 0, 0)
                                pPi0_cand2.SetPxPyPzE(t_in.p4_pi0[jPi0*4+0], t_in.p4_pi0[jPi0*4+1], t_in.p4_pi0[jPi0*4+2], t_in.p4_pi0[jPi0*4+3])
                                if pPi0_cand2.M() != pPi0.M() and pPi0_cand2.M() != pPi0_cand2.M() and pPi0_cand2.M() > 0:
                                    pD02 = TLorentzVector(0, 0, 0, 0)
                                    pD02 = pD01 + pPi0_cand2
                                    if math.fabs(pD02.M() - 1.86483) < delta_M:
                                        delta_M = pD02.M() - 1.86483
                                        m_D0 = pD02.M()
                if (m_D0 - 1.86483) <= (m_D0_back - 1.86483):
                    m_m_D0[0] = m_D0
                else:
                    m_m_D0[0] = m_D0_back
            t.Fill()

def save_raw(f_in, cms, t, MODE):
    if MODE == 'raw':
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
        t_std = f_in.Get('STD')
        t_otherTrk = f_in.Get('otherTrk')
        nentries = t_std.GetEntries()
        for ientry in range(nentries):
            t_std.GetEntry(ientry)
            if t_std.mode != 200:
                continue
            pD_raw = TLorentzVector(0, 0, 0, 0)
            pD = TLorentzVector(0, 0, 0, 0)
            for iTrk in range(t_std.n_trkD):
                ptrack_raw = TLorentzVector(0, 0, 0, 0)
                ptrack = TLorentzVector(0, 0, 0, 0)
                ptrack_raw.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*4+0], t_std.rawp4_Dtrk[iTrk*4+1], t_std.rawp4_Dtrk[iTrk*4+2], t_std.rawp4_Dtrk[iTrk*4+3])
                ptrack.SetPxPyPzE(t_std.p4_Dtrk[iTrk*4+0], t_std.p4_Dtrk[iTrk*4+1], t_std.p4_Dtrk[iTrk*4+2], t_std.p4_Dtrk[iTrk*4+3])
                pD_raw += ptrack_raw
                pD += ptrack
            pPip = TLorentzVector(0,0,0,0)
            pPim = TLorentzVector(0,0,0,0)
            t_otherTrk.GetEntry(ientry)
            for iTrk1 in range(t_otherTrk.n_othertrks):
                if t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*6+4] != 1:
                    continue
                if t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*6+5] != 2:
                    continue
                pPip.SetPxPyPzE(t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*6+0], t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*6+1], t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*6+2], t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*6+3])
                for iTrk2 in range(t_otherTrk.n_othertrks):
                    if t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+4] != -1:
                        continue
                    if t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+5] != 2:
                        continue
                    pPim.SetPxPyPzE(t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+0], t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+1], t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+2], t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+3])
                    m_runNo[0] = t_std.runNo
                    m_evtNo[0] = t_std.evtNo
                    m_mode[0] = t_std.mode
                    m_charm[0] = t_std.charm
                    m_rawm_D[0] = pD_raw.M()
                    m_m_D[0] = pD.M()
                    m_rm_D[0] = (cms-pD).M()
                    m_rm_pipi[0] = (cms-pPip-pPim).M()
                    m_m_pipi[0] = (pPip+pPim).M()
                    if t_std.charm > 0 and t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+4] == -1:
                        m_m_Dpi[0] = (pD+pPim).M()
                    elif t_std.charm < 0 and t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+4] == 1:
                        m_m_Dpi[0] = (pD+pPip).M()
                    m_m_Dpipi[0] = (pD+pPip+pPim).M()
                    m_rm_Dpipi[0] = (cms-pD-pPip-pPim).M()
                    m_chi2_vf[0] = t_std.chi2_vf
                    m_chi2_kf[0] = t_std.chi2_kf
                    t.Fill()

def save_truth(f_in, cms, t, MODE, chi2_kf_cut):
    if MODE == 'truth':
        m_runNo = array('i', [0])
        m_evtNo = array('i', [0])
        m_m_pipi = array('d', [999.])
        m_chi2_kf = array('d', [999.])
        m_rm_Dpipi = array('d', [999.])
        m_indexmc = array('i', [0])
        m_motheridx = array('i', 100*[0])
        m_pdgid = array('i', 100*[0])
        m_n_othershws = array('i', [0])
        m_n_othertrks = array('i', [0])
        m_charge_left = array('i', [0])
        m_chi2_pi0 = array('d', [999.])
        m_m_Dpi0 = array('d', [999.])
        m_m_pi0 = array('d', [999.])
        m_n_pi0 = array('i', [0])
        m_m_D0 = array('d', [999.])
        t.Branch('runNo', m_runNo, 'm_runNo/I')
        t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
        t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
        t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')
        t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
        t.Branch('indexmc', m_indexmc, 'indexmc/I')
        t.Branch('motheridx', m_motheridx, 'motheridx[100]/I')
        t.Branch('pdgid', m_pdgid, 'pdgid[100]/I')
        t.Branch('n_othershws', m_n_othershws, 'm_n_othershws/I')
        t.Branch('n_othertrks', m_n_othertrks, 'm_n_othertrks/I')
        t.Branch('charge_left', m_charge_left, 'm_charge_left/I')
        t.Branch('chi2_pi0', m_chi2_pi0, 'm_chi2_pi0/D')
        t.Branch('m_Dpi0', m_m_Dpi0, 'm_m_Dpi0/D')
        t.Branch('m_pi0', m_m_pi0, 'm_m_pi0/D')
        t.Branch('n_pi0', m_n_pi0, 'm_n_pi0/I')
        t.Branch('m_D0', m_m_D0, 'm_m_D0/D')
        t_in = f_in.Get('STD_signal')
        t_shw = f_in.Get('otherShw')
        nentries = t_in.GetEntries()
        for ientry in range(nentries):
            t_in.GetEntry(ientry)
            if t_in.mode != 200:
                continue
            pD_raw = TLorentzVector(0, 0, 0, 0)
            pD = TLorentzVector(0, 0, 0, 0)
            for iTrk in range(t_in.n_trkD):
                ptrack_raw = TLorentzVector(0, 0, 0, 0)
                ptrack = TLorentzVector(0, 0, 0, 0)
                ptrack_raw.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*4+0], t_in.rawp4_Dtrk[iTrk*4+1], t_in.rawp4_Dtrk[iTrk*4+2], t_in.rawp4_Dtrk[iTrk*4+3])
                ptrack.SetPxPyPzE(t_in.p4_Dtrk[iTrk*4+0], t_in.p4_Dtrk[iTrk*4+1], t_in.p4_Dtrk[iTrk*4+2], t_in.p4_Dtrk[iTrk*4+3])
                pD_raw += ptrack_raw
                pD += ptrack
            pPip = TLorentzVector(0,0,0,0)
            pPim = TLorentzVector(0,0,0,0)
            pPi0 = TLorentzVector(0, 0, 0, 0)
            pPip.SetPxPyPzE(t_in.p4_piplus[0], t_in.p4_piplus[1], t_in.p4_piplus[2], t_in.p4_piplus[3])
            pPim.SetPxPyPzE(t_in.p4_piminus[0], t_in.p4_piminus[1], t_in.p4_piminus[2], t_in.p4_piminus[3])
            pPi0.SetPxPyPzE(t_in.p4_pi0_save[0], t_in.p4_pi0_save[1], t_in.p4_pi0_save[2], t_in.p4_pi0_save[3])
            rm_Dpipi = (cms-pD-pPip-pPim).M()
            m_runNo[0] = t_in.runNo
            m_evtNo[0] = t_in.evtNo
            m_m_pipi[0] = (pPip+pPim).M()
            m_chi2_kf[0] = t_in.chi2_kf
            m_rm_Dpipi[0] = rm_Dpipi
            m_indexmc[0] = t_in.indexmc
            m_n_othershws[0] = t_in.n_othershws
            m_n_othertrks[0] = t_in.n_othertrks
            m_charge_left[0] = t_in.charge_left
            m_chi2_pi0[0] = t_in.chi2_pi0_save
            m_m_Dpi0[0] = (pD+pPi0).M()
            m_m_pi0[0] = pPi0.M()
            m_n_pi0[0] = t_in.n_pi0
            for i in range(t_in.indexmc):
                m_motheridx[i] = t_in.motheridx[i]
                m_pdgid[i] = t_in.pdgid[i]
            if t_in.charm == 1:
                pothers = TLorentzVector(0, 0, 0, 0)
                pD0 = TLorentzVector(0, 0, 0, 0)
                for iTrk in range(t_in.n_othertrks):
                    pKpi = TLorentzVector(0, 0, 0, 0)
                    pKpi.SetPxPyPzE(t_in.rawp4_otherMdcKaltrk[iTrk*6+0], t_in.rawp4_otherMdcKaltrk[iTrk*6+1], t_in.rawp4_otherMdcKaltrk[iTrk*6+2], t_in.rawp4_otherMdcKaltrk[iTrk*6+3])
                    pothers += pKpi
                pD0 = pothers + pPip
                m_m_D0[0] = pD0.M()
            if t_in.charm == -1:
                pothers = TLorentzVector(0, 0, 0, 0)
                pD0 = TLorentzVector(0, 0, 0, 0)
                for iTrk in range(t_in.n_othertrks):
                    pKpi = TLorentzVector(0, 0, 0, 0)
                    pKpi.SetPxPyPzE(t_in.rawp4_otherMdcKaltrk[iTrk*6+0], t_in.rawp4_otherMdcKaltrk[iTrk*6+1], t_in.rawp4_otherMdcKaltrk[iTrk*6+2], t_in.rawp4_otherMdcKaltrk[iTrk*6+3])
                    pothers += pKpi
                pD0 = pothers + pPim
                m_m_D0[0] = pD0.M()
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
        chi2_kf_cut = 45
    if ecms == 4.415:
        chi2_kf_cut = 46
    if ecms == 4.600:
        chi2_kf_cut = 25
    if MODE == 'raw':
        save_raw(f_in, cms, t_out, MODE)
    if MODE == 'truth':
        save_truth(f_in, cms, t_out, MODE, chi2_kf_cut)
    if MODE == 'signal' or MODE == 'sidebandlow' or MODE == 'sidebandup':
        save_missing(f_in, cms, t_out, MODE)

    f_out.cd()
    t_out.Write()
    f_out.Close()

if __name__ == '__main__':
    main()
