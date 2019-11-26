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
    ./get_info.py [infile_path] [outfile_path] [Ecms] [MODE]

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
        m_m_Dold = array('d', [999.])
        m_rrawm_D = array('d', [999.])
        m_m_D = array('d', [999.])
        m_p_D = array('d', [999.])
        m_E_D = array('d', [999.])
        m_rm_D = array('d', [999.])
        m_rm_D_old = array('d', [999.])
        m_rm_Dmiss = array('d', [999.])
        m_rm_DDmisspip = array('d', [999.])
        m_rm_DDmisspim = array('d', [999.])
        m_rm_pipi = array('d', [999.])
        m_m_pipi = array('d', [999.])
        m_p_pipi = array('d', [999.])
        m_E_pipi = array('d', [999.])
        m_m_Dpi = array('d', [999.])
        m_m_DDmiss = array('d', [999.])
        m_m_Dmisspi = array('d', [999.])
        m_rm_Dmisspi = array('d', [999.])
        m_rm_Dpi = array('d', [999.])
        m_m_Dpip = array('d', [999.])
        m_m_Dpim = array('d', [999.])
        m_m2_Kpip = array('d', [999.])
        m_m_Kpip = array('d', [999.])
        m_rm_Kpip = array('d', [999.])
        m_m2_Kpim = array('d', [999.])
        m_m_Kpim = array('d', [999.])
        m_rm_Kpim = array('d', [999.])
        m_m_Dpipi = array('d', [999.])
        m_rm_Dpipi = array('d', [999.])
        m_chi2_vf = array('d', [999.])
        m_chi2_kf = array('d', [999.])
        m_chi2_svf = array('d', [999.])
        m_ctau_svf = array('d', [999.])
        m_L_svf = array('d', [999.])
        m_Lerr_svf = array('d', [999.])
        m_n_othershws = array('i', [0])
        m_n_othertrks = array('i', [0])
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
        if MODE == 'signal':
            m_matched_D = array('i', [0])
            m_matched_pi = array('i', [0])
            m_matched_piplus = array('i', [0])
            m_matched_piminus = array('i', [0])
        t.Branch('runNo', m_runNo, 'm_runNo/I')
        t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
        t.Branch('mode', m_mode, 'm_mode/I')
        t.Branch('charm', m_charm, 'm_charm/I')
        t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
        t.Branch('m_Dold', m_m_Dold, 'm_m_Dold/D')
        t.Branch('rrawm_D', m_rrawm_D, 'm_rrawm_D/D')
        t.Branch('m_D', m_m_D, 'm_m_D/D')
        t.Branch('p_D', m_p_D, 'm_p_D/D')
        t.Branch('E_D', m_E_D, 'm_E_D/D')
        t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
        t.Branch('rm_D_old', m_rm_D_old, 'm_rm_D_old/D')
        t.Branch('rm_Dmiss', m_rm_Dmiss, 'm_rm_Dmiss/D')
        t.Branch('rm_DDmisspip', m_rm_DDmisspip, 'm_rm_DDmisspip/D')
        t.Branch('rm_DDmisspim', m_rm_DDmisspim, 'm_rm_DDmisspim/D')
        t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
        t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
        t.Branch('p_pipi', m_p_pipi, 'm_p_pipi/D')
        t.Branch('E_pipi', m_E_pipi, 'm_E_pipi/D')
        t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
        t.Branch('m_DDmiss', m_m_DDmiss, 'm_m_DDmiss/D')
        t.Branch('m_Dmisspi', m_m_Dmisspi, 'm_m_Dmisspi/D')
        t.Branch('rm_Dmisspi', m_rm_Dmisspi, 'm_rm_Dmisspi/D')
        t.Branch('rm_Dpi', m_rm_Dpi, 'm_rm_Dpi/D')
        t.Branch('m_Dpip', m_m_Dpip, 'm_m_Dpip/D')
        t.Branch('m_Dpim', m_m_Dpim, 'm_m_Dpim/D')
        t.Branch('m2_Kpip', m_m2_Kpip, 'm_m2_Kpip/D')
        t.Branch('m_Kpip', m_m_Kpip, 'm_m_Kpip/D')
        t.Branch('rm_Kpip', m_rm_Kpip, 'm_rm_Kpip/D')
        t.Branch('m2_Kpim', m_m2_Kpim, 'm_m2_Kpim/D')
        t.Branch('m_Kpim', m_m_Kpim, 'm_m_Kpim/D')
        t.Branch('rm_Kpim', m_rm_Kpim, 'm_rm_Kpim/D')
        t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
        t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
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
        if MODE == 'signal':
            t.Branch('matched_D', m_matched_D, 'm_matched_D/I')
            t.Branch('matched_pi', m_matched_pi, 'm_matched_pi/I')
            t.Branch('matched_piplus', m_matched_piplus, 'm_matched_piplus/I')
            t.Branch('matched_piminus', m_matched_piminus, 'm_matched_piminus/I')
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
            pD_old = TLorentzVector(0, 0, 0, 0)
            pD = TLorentzVector(0, 0, 0, 0)
            pKpip = TLorentzVector(0, 0, 0, 0)
            pKpim = TLorentzVector(0, 0, 0, 0)
            for iTrk in range(t_in.n_trkD):
                ptrack_raw = TLorentzVector(0, 0, 0, 0)
                ptrack_old = TLorentzVector(0, 0, 0, 0)
                ptrack_Kpip = TLorentzVector(0, 0, 0, 0)
                ptrack_Kpim = TLorentzVector(0, 0, 0, 0)
                ptrack = TLorentzVector(0, 0, 0, 0)
                ptrack_raw.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                ptrack_old.SetPxPyPzE(t_in.p4_Dtrkold[iTrk*4+0], t_in.p4_Dtrkold[iTrk*4+1], t_in.p4_Dtrkold[iTrk*4+2], t_in.p4_Dtrkold[iTrk*4+3])
                ptrack.SetPxPyPzE(t_in.p4_Dtrk[iTrk*4+0], t_in.p4_Dtrk[iTrk*4+1], t_in.p4_Dtrk[iTrk*4+2], t_in.p4_Dtrk[iTrk*4+3])
                pD_raw += ptrack_raw
                pD_old += ptrack_old
                pD += ptrack
                if t_in.rawp4_Dtrk[iTrk*6+5] == 3:
                    ptrack_Kpip.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                    ptrack_Kpim.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                    pKpip += ptrack_Kpip
                    pKpim += ptrack_Kpim
                if t_in.rawp4_Dtrk[iTrk*6+4] == 1 and t_in.rawp4_Dtrk[iTrk*6+5] == 2:
                    ptrack_Kpip.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                    pKpip += ptrack_Kpip
                if t_in.rawp4_Dtrk[iTrk*6+4] == -1 and t_in.rawp4_Dtrk[iTrk*6+5] == 2:
                    ptrack_Kpim.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                    pKpim += ptrack_Kpim
            for iShw in range(t_in.n_shwD):
                pshower_raw = TLorentzVector(0, 0, 0, 0)
                pshower_old = TLorentzVector(0, 0, 0, 0)
                pshower = TLorentzVector(0, 0, 0, 0)
                pshower_raw.SetPxPyPzE(t_in.rawp4_Dshw[iShw*4+0], t_in.rawp4_Dshw[iShw*4+1], t_in.rawp4_Dshw[iShw*4+2], t_in.rawp4_Dshw[iShw*4+3])
                pshower_old.SetPxPyPzE(t_in.p4_Dshwold[iShw*4+0], t_in.p4_Dshwold[iShw*4+1], t_in.p4_Dshwold[iShw*4+2], t_in.p4_Dshwold[iShw*4+3])
                pshower.SetPxPyPzE(t_in.p4_Dshw[iShw*4+0], t_in.p4_Dshw[iShw*4+1], t_in.p4_Dshw[iShw*4+2], t_in.p4_Dshw[iShw*4+3])
                pD_raw += pshower_raw
                pD_old += pshower_old
                pD += pshower
            pPip = TLorentzVector(0, 0, 0, 0)
            pPim = TLorentzVector(0, 0, 0, 0)
            pDmiss = TLorentzVector(0, 0, 0, 0)
            rawpPip = TLorentzVector(0, 0, 0, 0)
            rawpPim = TLorentzVector(0, 0, 0, 0)
            pPi0 = TLorentzVector(0, 0, 0, 0)
            pPip.SetPxPyPzE(t_in.p4_piplus[0], t_in.p4_piplus[1], t_in.p4_piplus[2], t_in.p4_piplus[3])
            pPim.SetPxPyPzE(t_in.p4_piminus[0], t_in.p4_piminus[1], t_in.p4_piminus[2], t_in.p4_piminus[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss[0], t_in.p4_Dmiss[1], t_in.p4_Dmiss[2], t_in.p4_Dmiss[3])
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
            m_m_D[0] = pD.M()
            m_p_D[0] = pD.P()
            m_E_D[0] = pD.E()
            m_rm_D[0] = (cms-pD).M()
            m_rm_D_old[0] = (cms-pD_old).M()
            m_rm_Dmiss[0] = (cms-pDmiss).M()
            m_rm_pipi[0] = (cms-pPip-pPim).M()
            m_m_pipi[0] = (pPip+pPim).M()
            m_p_pipi[0] = (rawpPip+rawpPim).P()
            m_E_pipi[0] = (rawpPip+rawpPim).E()
            m_m_Dpim[0] = (pD+pPim).M()
            m_m_Dpip[0] = (pD+pPip).M()
            if t_in.charm > 0:
                m_m_Dmisspi[0] = (pDmiss+pPip).M()
                m_rm_Dmisspi[0] = (cms-pDmiss-pPip).M()
                m_m_Dpi[0] = (pD_old+rawpPim).M()
                m_rm_Dpi[0] = (cms-pD_old-rawpPim).M()
            elif t_in.charm < 0:
                m_m_Dmisspi[0] = (pDmiss+pPim).M()
                m_rm_Dmisspi[0] = (cms-pDmiss-pPim).M()
                m_m_Dpi[0] = (pD_old+rawpPip).M()
                m_rm_Dpi[0] = (cms-pD_old-rawpPip).M()
            m_m_DDmiss[0] = (pDmiss+pD).M()
            m_rm_DDmisspip[0] = (cms-pDmiss-pD-pPip).M()
            m_rm_DDmisspim[0] = (cms-pDmiss-pD-pPim).M()
            m_m2_Kpip[0] = pKpip.M2()
            m_m_Kpip[0] = pKpip.M()
            m_rm_Kpip[0] = (cms-pKpip).M()
            m_m2_Kpim[0] = pKpim.M2()
            m_m_Kpim[0] = pKpim.M()
            m_rm_Kpim[0] = (cms-pKpim).M()
            m_m_Dpipi[0] = (pD+pPip+pPim).M()
            m_rm_Dpipi[0] = t_in.rm_Dpipi
            m_chi2_vf[0] = t_in.chi2_vf
            m_chi2_kf[0] = t_in.chi2_kf
            m_chi2_svf[0] = t_in.chi2_svf
            m_ctau_svf[0] = t_in.ctau_svf
            m_L_svf[0] = t_in.L_svf
            m_Lerr_svf[0] = t_in.Lerr_svf
            m_n_othershws[0] = t_in.n_othershws
            m_n_othertrks[0] = t_in.n_othertrks
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
            for iPi0 in range(t_in.n_pi0):
                ppi0 = TLorentzVector(0, 0, 0, 0)
                ppi0.SetPxPyPzE(t_in.p4_pi0[iPi0*4+0], t_in.p4_pi0[iPi0*4+1], t_in.p4_pi0[iPi0*4+2], t_in.p4_pi0[iPi0*4+3])
                if (fabs((pDmiss + ppi0).M() - 2.000685) < deltaM):
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
            if MODE == 'signal':
                m_matched_D[0] = t_in.matched_D
                m_matched_pi[0] = t_in.matched_pi
                m_matched_piplus[0] = t_in.matched_piplus
                m_matched_piminus[0] = t_in.matched_piminus
            t.Fill()

def save_raw(f_in, cms, t, MODE):
    if MODE == 'raw':
        m_runNo = array('i', [0])
        m_evtNo = array('i', [0])
        m_mode = array('i', [0])
        m_charm = array('i', [0])
        m_rrawm_Dpipi = array('d', [999.])
        m_rawm_D = array('d', [999.])
        m_m_D = array('d', [999.])
        m_p_D = array('d', [999.])
        m_E_D = array('d', [999.])
        m_rm_D = array('d', [999.])
        m_rm_pipi = array('d', [999.])
        m_m_pipi = array('d', [999.])
        m_p_pipi = array('d', [999.])
        m_E_pipi = array('d', [999.])
        m_m_Dpi = array('d', [999.])
        m_rm_Dpi = array('d', [999.])
        m_m_Dpip = array('d', [999.])
        m_m_Dpim = array('d', [999.])
        m_m2_Kpip = array('d', [999.])
        m_m2_Kpim = array('d', [999.])
        m_m_Dpipi = array('d', [999.])
        m_rm_Dpipi = array('d', [999.])
        m_chi2_vf = array('d', [999.])
        m_chi2_kf = array('d', [999.])
        m_n_othershws = array('i', [0])
        m_n_othertrks = array('i', [0])
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
        t.Branch('runNo', m_runNo, 'm_runNo/I')
        t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
        t.Branch('mode', m_mode, 'm_mode/I')
        t.Branch('charm', m_charm, 'm_charm/I')
        t.Branch('rrawm_Dpipi', m_rrawm_Dpipi, 'm_rrawm_Dpipi/D')
        t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
        t.Branch('m_D', m_m_D, 'm_m_D/D')
        t.Branch('p_D', m_p_D, 'm_p_D/D')
        t.Branch('E_D', m_E_D, 'm_E_D/D')
        t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
        t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
        t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
        t.Branch('p_pipi', m_p_pipi, 'm_p_pipi/D')
        t.Branch('E_pipi', m_E_pipi, 'm_E_pipi/D')
        t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
        t.Branch('rm_Dpi', m_rm_Dpi, 'm_rm_Dpi/D')
        t.Branch('m_Dpip', m_m_Dpip, 'm_m_Dpip/D')
        t.Branch('m_Dpim', m_m_Dpim, 'm_m_Dpim/D')
        t.Branch('m2_Kpip', m_m2_Kpip, 'm_m2_Kpip/D')
        t.Branch('m2_Kpim', m_m2_Kpim, 'm_m2_Kpim/D')
        t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
        t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
        t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
        t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')
        t.Branch('n_othertrks', m_n_othertrks, 'm_n_othertrks/I')
        t.Branch('n_othershws', m_n_othershws, 'm_n_othershws/I')
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
        t_std = f_in.Get('STD')
        t_otherTrk = f_in.Get('otherTrk')
        t_otherShw = f_in.Get('otherShw')
        nentries = t_std.GetEntries()
        for ientry in range(nentries):
            t_std.GetEntry(ientry)
            if t_std.mode != 200:
                continue
            pD_raw = TLorentzVector(0, 0, 0, 0)
            pD = TLorentzVector(0, 0, 0, 0)
            pKpip = TLorentzVector(0, 0, 0, 0)
            pKpim = TLorentzVector(0, 0, 0, 0)
            for iTrk in range(t_std.n_trkD):
                ptrack_raw = TLorentzVector(0, 0, 0, 0)
                ptrack_Kpip = TLorentzVector(0, 0, 0, 0)
                ptrack_Kpim = TLorentzVector(0, 0, 0, 0)
                ptrack = TLorentzVector(0, 0, 0, 0)
                ptrack_raw.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*6+0], t_std.rawp4_Dtrk[iTrk*6+1], t_std.rawp4_Dtrk[iTrk*6+2], t_std.rawp4_Dtrk[iTrk*6+3])
                ptrack.SetPxPyPzE(t_std.p4_Dtrk[iTrk*4+0], t_std.p4_Dtrk[iTrk*4+1], t_std.p4_Dtrk[iTrk*4+2], t_std.p4_Dtrk[iTrk*4+3])
                pD_raw += ptrack_raw
                pD += ptrack
                if t_std.rawp4_Dtrk[iTrk*6+5] == 3:
                    ptrack_Kpip.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*6+0], t_std.rawp4_Dtrk[iTrk*6+1], t_std.rawp4_Dtrk[iTrk*6+2], t_std.rawp4_Dtrk[iTrk*6+3])
                    ptrack_Kpim.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*6+0], t_std.rawp4_Dtrk[iTrk*6+1], t_std.rawp4_Dtrk[iTrk*6+2], t_std.rawp4_Dtrk[iTrk*6+3])
                    pKpip += ptrack_Kpip
                    pKpim += ptrack_Kpim
                if t_std.rawp4_Dtrk[iTrk*6+4] == 1 and t_std.rawp4_Dtrk[iTrk*6+5] == 2:
                    ptrack_Kpip.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*6+0], t_std.rawp4_Dtrk[iTrk*6+1], t_std.rawp4_Dtrk[iTrk*6+2], t_std.rawp4_Dtrk[iTrk*6+3])
                    pKpip += ptrack_Kpip
                if t_std.rawp4_Dtrk[iTrk*6+4] == -1 and t_std.rawp4_Dtrk[iTrk*6+5] == 2:
                    ptrack_Kpim.SetPxPyPzE(t_std.rawp4_Dtrk[iTrk*6+0], t_std.rawp4_Dtrk[iTrk*6+1], t_std.rawp4_Dtrk[iTrk*6+2], t_std.rawp4_Dtrk[iTrk*6+3])
                    pKpim += ptrack_Kpim
            for iShw in range(t_std.n_shwD):
                pshower_raw = TLorentzVector(0, 0, 0, 0)
                pshower = TLorentzVector(0, 0, 0, 0)
                pshower_raw.SetPxPyPzE(t_std.rawp4_Dshw[iShw*4+0], t_std.rawp4_Dshw[iShw*4+1], t_std.rawp4_Dshw[iShw*4+2], t_std.rawp4_Dshw[iShw*4+3])
                pshower.SetPxPyPzE(t_std.p4_Dshw[iShw*4+0], t_std.p4_Dshw[iShw*4+1], t_std.p4_Dshw[iShw*4+2], t_std.p4_Dshw[iShw*4+3])
                pD_raw += pshower_raw
                pD += pshower
            pPip = TLorentzVector(0,0,0,0)
            pPim = TLorentzVector(0,0,0,0)
            t_otherTrk.GetEntry(ientry)
            t_otherShw.GetEntry(ientry)
            count = 0;
            for iTrk1 in range(t_otherTrk.n_othertrks):
                if t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*7+4] != 1:
                    continue
                if t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*7+5] != 2:
                    continue
                pPip.SetPxPyPzE(t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*7+0], t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*7+1], t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*7+2], t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*7+3])
                for iTrk2 in range(t_otherTrk.n_othertrks):
                    if t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+4] != -1:
                        continue
                    if t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+5] != 2:
                        continue
                    pPim.SetPxPyPzE(t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+0], t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+1], t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+2], t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+3])
                    m_runNo[0] = t_std.runNo
                    m_evtNo[0] = t_std.evtNo
                    m_mode[0] = t_std.mode
                    m_charm[0] = t_std.charm
                    m_rrawm_Dpipi[0] = (cms-pD_raw-pPip-pPim).M()
                    m_rawm_D[0] = pD_raw.M()
                    m_m_D[0] = pD.M()
                    m_p_D[0] = pD.P()
                    m_E_D[0] = pD.E()
                    m_rm_D[0] = (cms-pD).M()
                    m_rm_pipi[0] = (cms-pPip-pPim).M()
                    m_m_pipi[0] = (pPip+pPim).M()
                    m_p_pipi[0] = (pPip+pPim).P()
                    m_E_pipi[0] = (pPip+pPim).E()
                    m_m_Dpim[0] = (pD+pPim).M()
                    m_m_Dpip[0] = (pD+pPip).M()
                    if t_std.charm > 0 and t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+4] == -1:
                        m_m_Dpi[0] = (pD+pPim).M()
                        m_rm_Dpi[0] = (cms-pD-pPim).M()
                    elif t_std.charm < 0 and t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+4] == 1:
                        m_m_Dpi[0] = (pD+pPip).M()
                        m_rm_Dpi[0] = (cms-pD-pPip).M()
                    m_m2_Kpip[0] = pKpip.M2()
                    m_m2_Kpim[0] = pKpim.M2()
                    m_m_Dpipi[0] = (pD+pPip+pPim).M()
                    m_rm_Dpipi[0] = (cms-pD-pPip-pPim).M()
                    m_chi2_vf[0] = t_std.chi2_vf
                    m_chi2_kf[0] = t_std.chi2_kf
                    m_n_othershws[0] = t_otherShw.n_othershws
                    m_n_othertrks[0] = t_otherTrk.n_othertrks
                    charge_left = 0
                    for i in range(t_otherTrk.n_othertrks):
                        if i != iTrk1 and i != iTrk2:
                            charge_left += t_otherTrk.rawp4_otherMdcKaltrk[i*7+4]
                    m_charge_left[0] = int(charge_left)
                    m_m_piplus0[0] = pPip.M()
                    m_m_piminus0[0] = pPim.M()
                    m_p_piplus0[0] = pPip.P()
                    m_p_piminus0[0] = pPim.P()
                    m_E_piplus0[0] = pPip.E()
                    m_E_piminus0[0] = pPim.E()
                    m_chi2_pi0[0] = t_otherShw.chi2_pi0_save
                    m_Dpi0 = pD.M()
                    pPi0 = TLorentzVector(0, 0, 0, 0)
                    pPi0.SetPxPyPzE(t_otherShw.p4_pi0_save[0], t_otherShw.p4_pi0_save[1], t_otherShw.p4_pi0_save[2], t_otherShw.p4_pi0_save[3])
                    if pPi0.M() > 0:
                        m_Dpi0 = (pD + pPi0).M()
                    m_m_Dpi0[0] = m_Dpi0
                    m_m_pi0[0] = pPi0.M()
                    m_p_pi0[0] = pPi0.P()
                    m_E_pi0[0] = pPi0.E()
                    m_n_pi0[0] = t_otherShw.n_pi0
                    m_matched_D[0] = t_std.matched_D
                    if t_otherTrk.rawp4_otherMdcKaltrk[iTrk1*7+6] == 1 and t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*7+6] == 1:
                        m_matched_pi[0] = 1
                    else:
                        m_matched_pi[0] = 0
                    t.Fill()

def save_truth(f_in, cms, t, MODE):
    if MODE == 'truth':
        m_runNo = array('i', [0])
        m_evtNo = array('i', [0])
        m_mode = array('i', [0])
        m_charm = array('i', [0])
        m_rawm_D = array('d', [999.])
        m_rm_D = array('d', [999.])
        m_rm_D_old = array('d', [999.])
        m_rm_Dmiss = array('d', [999.])
        m_m_D = array('d', [999.])
        m_rawm_D = array('d', [999.])
        m_p_D = array('d', [999.])
        m_E_D = array('d', [999.])
        m_p_pipi = array('d', [999.])
        m_m_pipi = array('d', [999.])
        m_E_pipi = array('d', [999.])
        m_rm_pipi = array('d', [999.])
        m_chi2_vf = array('d', [999.])
        m_chi2_kf = array('d', [999.])
        m_m_DDmiss = array('d', [999.])
        m_m_Dmisspi = array('d', [999.])
        m_rm_Dmisspi = array('d', [999.])
        m_m_Dpi = array('d', [999.])
        m_rm_Dpi = array('d', [999.])
        m_m_Dpip = array('d', [999.])
        m_m_Dpim = array('d', [999.])
        m_m2_Kpip = array('d', [999.])
        m_m2_Kpim = array('d', [999.])
        m_m_Dpipi = array('d', [999.])
        m_rm_Dpipi = array('d', [999.])
        m_indexmc = array('i', [0])
        m_motheridx = array('i', 100*[0])
        m_pdgid = array('i', 100*[0])
        m_n_othershws = array('i', [0])
        m_n_othertrks = array('i', [0])
        m_charge_left = array('i', [0])
        m_m_piplus0 = array('d', [999.])
        m_m_piminus0 = array('d', [999.])
        m_p_piplus0 = array('d', [999.])
        m_p_piminus0 = array('d', [999.])
        m_E_piplus0 = array('d', [999.])
        m_E_piminus0 = array('d', [999.])
        m_chi2_pi0 = array('d', [999.])
        m_m_Dmisspi0 = array('d', [999.])
        m_rm_Dmisspi0 = array('d', [999.])
        m_m_Dpi0 = array('d', [999.])
        m_rm_Dpi0 = array('d', [999.])
        m_m_pi0 = array('d', [999.])
        m_p_pi0 = array('d', [999.])
        m_E_pi0 = array('d', [999.])
        m_n_pi0 = array('i', [0])
        m_matched_D = array('i', [0])
        m_matched_pi = array('i', [0])
        m_matched_piplus = array('i', [0])
        m_matched_piminus = array('i', [0])
        t.Branch('runNo', m_runNo, 'm_runNo/I')
        t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
        t.Branch('mode', m_mode, 'm_mode/I')
        t.Branch('charm', m_charm, 'm_charm/I')
        t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
        t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
        t.Branch('rm_D_old', m_rm_D_old, 'm_rm_D_old/D')
        t.Branch('rm_Dmiss', m_rm_Dmiss, 'm_rm_Dmiss/D')
        t.Branch('m_D', m_m_D, 'm_m_D/D')
        t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
        t.Branch('p_D', m_p_D, 'm_p_D/D')
        t.Branch('E_D', m_E_D, 'm_E_D/D')
        t.Branch('p_pipi', m_p_pipi, 'm_p_pipi/D')
        t.Branch('m_pipi', m_m_pipi, 'm_m_pipi/D')
        t.Branch('E_pipi', m_E_pipi, 'm_E_pipi/D')
        t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
        t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
        t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')
        t.Branch('m_DDmiss', m_m_DDmiss, 'm_m_DDmiss/D')
        t.Branch('m_Dmisspi', m_m_Dmisspi, 'm_m_Dmisspi/D')
        t.Branch('rm_Dmisspi', m_rm_Dmisspi, 'm_rm_Dmisspi/D')
        t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
        t.Branch('rm_Dpi', m_rm_Dpi, 'm_rm_Dpi/D')
        t.Branch('m_Dpip', m_m_Dpip, 'm_m_Dpip/D')
        t.Branch('m_Dpim', m_m_Dpim, 'm_m_Dpim/D')
        t.Branch('m2_Kpip', m_m2_Kpip, 'm_m2_Kpip/D')
        t.Branch('m2_Kpim', m_m2_Kpim, 'm_m2_Kpim/D')
        t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
        t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
        t.Branch('indexmc', m_indexmc, 'indexmc/I')
        t.Branch('motheridx', m_motheridx, 'motheridx[100]/I')
        t.Branch('pdgid', m_pdgid, 'pdgid[100]/I')
        t.Branch('n_othershws', m_n_othershws, 'm_n_othershws/I')
        t.Branch('n_othertrks', m_n_othertrks, 'm_n_othertrks/I')
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
        t.Branch('matched_D', m_matched_D, 'm_matched_D/I')
        t.Branch('matched_pi', m_matched_pi, 'm_matched_pi/I')
        t.Branch('matched_piplus', m_matched_piplus, 'm_matched_piplus/I')
        t.Branch('matched_piminus', m_matched_piminus, 'm_matched_piminus/I')
        t_in = f_in.Get('STD_signal')
        nentries = t_in.GetEntries()
        for ientry in range(nentries):
            t_in.GetEntry(ientry)
            if t_in.mode != 200:
                continue
            pD_raw = TLorentzVector(0, 0, 0, 0)
            pD_old = TLorentzVector(0, 0, 0, 0)
            pKpip = TLorentzVector(0, 0, 0, 0)
            pKpim = TLorentzVector(0, 0, 0, 0)
            pD = TLorentzVector(0, 0, 0, 0)
            for iTrk in range(t_in.n_trkD):
                ptrack_raw = TLorentzVector(0, 0, 0, 0)
                ptrack_old = TLorentzVector(0, 0, 0, 0)
                ptrack_Kpip = TLorentzVector(0, 0, 0, 0)
                ptrack_Kpim = TLorentzVector(0, 0, 0, 0)
                ptrack = TLorentzVector(0, 0, 0, 0)
                ptrack_raw.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                ptrack_old.SetPxPyPzE(t_in.p4_Dtrkold[iTrk*4+0], t_in.p4_Dtrkold[iTrk*4+1], t_in.p4_Dtrkold[iTrk*4+2], t_in.p4_Dtrkold[iTrk*4+3])
                ptrack.SetPxPyPzE(t_in.p4_Dtrk[iTrk*4+0], t_in.p4_Dtrk[iTrk*4+1], t_in.p4_Dtrk[iTrk*4+2], t_in.p4_Dtrk[iTrk*4+3])
                pD_raw += ptrack_raw
                pD_old += ptrack_old
                pD += ptrack
                if t_in.rawp4_Dtrk[iTrk*6+5] == 3:
                    ptrack_Kpip.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                    ptrack_Kpim.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                    pKpip += ptrack_Kpip
                    pKpim += ptrack_Kpim
                if t_in.rawp4_Dtrk[iTrk*6+4] == 1 and t_in.rawp4_Dtrk[iTrk*6+5] == 2:
                    ptrack_Kpip.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                    pKpip += ptrack_Kpip
                if t_in.rawp4_Dtrk[iTrk*6+4] == -1 and t_in.rawp4_Dtrk[iTrk*6+5] == 2:
                    ptrack_Kpim.SetPxPyPzE(t_in.rawp4_Dtrk[iTrk*6+0], t_in.rawp4_Dtrk[iTrk*6+1], t_in.rawp4_Dtrk[iTrk*6+2], t_in.rawp4_Dtrk[iTrk*6+3])
                    pKpim += ptrack_Kpim
            for iShw in range(t_in.n_shwD):
                pshower_raw = TLorentzVector(0, 0, 0, 0)
                pshower_old = TLorentzVector(0, 0, 0, 0)
                pshower = TLorentzVector(0, 0, 0, 0)
                pshower_raw.SetPxPyPzE(t_in.rawp4_Dshw[iShw*4+0], t_in.rawp4_Dshw[iShw*4+1], t_in.rawp4_Dshw[iShw*4+2], t_in.rawp4_Dshw[iShw*4+3])
                pshower_old.SetPxPyPzE(t_in.p4_Dshwold[iShw*4+0], t_in.p4_Dshwold[iShw*4+1], t_in.p4_Dshwold[iShw*4+2], t_in.p4_Dshwold[iShw*4+3])
                pshower.SetPxPyPzE(t_in.p4_Dshw[iShw*4+0], t_in.p4_Dshw[iShw*4+1], t_in.p4_Dshw[iShw*4+2], t_in.p4_Dshw[iShw*4+3])
                pD_raw += pshower_raw
                pD_old += pshower_old
                pD += pshower
            pPip = TLorentzVector(0,0,0,0)
            pPim = TLorentzVector(0,0,0,0)
            pDmiss = TLorentzVector(0,0,0,0)
            rawpPip = TLorentzVector(0,0,0,0)
            rawpPim = TLorentzVector(0,0,0,0)
            pPi0 = TLorentzVector(0, 0, 0, 0)
            pPip.SetPxPyPzE(t_in.p4_piplus[0], t_in.p4_piplus[1], t_in.p4_piplus[2], t_in.p4_piplus[3])
            pPim.SetPxPyPzE(t_in.p4_piminus[0], t_in.p4_piminus[1], t_in.p4_piminus[2], t_in.p4_piminus[3])
            pDmiss.SetPxPyPzE(t_in.p4_Dmiss[0], t_in.p4_Dmiss[1], t_in.p4_Dmiss[2], t_in.p4_Dmiss[3])
            rawpPip.SetPxPyPzE(t_in.rawp4_tagPiplus[0], t_in.rawp4_tagPiplus[1], t_in.rawp4_tagPiplus[2], t_in.rawp4_tagPiplus[3])
            rawpPim.SetPxPyPzE(t_in.rawp4_tagPiminus[0], t_in.rawp4_tagPiminus[1], t_in.rawp4_tagPiminus[2], t_in.rawp4_tagPiminus[3])
            pPi0.SetPxPyPzE(t_in.p4_pi0_save[0], t_in.p4_pi0_save[1], t_in.p4_pi0_save[2], t_in.p4_pi0_save[3])
            m_runNo[0] = t_in.runNo
            m_evtNo[0] = t_in.evtNo
            m_mode[0] = t_in.mode
            m_charm[0] = t_in.charm
            m_p_D = pD.P()
            m_rm_D[0] = (cms-pD).M()
            m_rm_D_old[0] = (cms-pD_old).M()
            m_rm_Dmiss[0] = (cms-pDmiss).M()
            m_m_D = pD.M()
            m_rawm_D = pD_raw.M()
            m_E_D = pD.E()
            m_p_pipi[0] = (rawpPip+rawpPim).P()
            m_E_pipi[0] = (rawpPip+rawpPim).E()
            m_m_pipi[0] = (pPip+pPim).M()
            m_rm_pipi[0] = (cms-pPip-pPim).M()
            m_chi2_vf[0] = t_in.chi2_vf
            m_chi2_kf[0] = t_in.chi2_kf
            m_m2_Kpip[0] = pKpip.M2()
            m_m2_Kpim[0] = pKpim.M2()
            m_m_Dpipi[0] = (pD+pPip+pPim).M()
            m_rm_Dpipi[0] = t_in.rm_Dpipi
            m_m_Dpim[0] = (pD+pPim).M()
            m_m_Dpip[0] = (pD+pPim).M()
            if t_in.charm > 0:
                m_m_Dmisspi[0] = (pDmiss+pPip).M()
                m_rm_Dmisspi[0] = (cms-pDmiss-pPip).M()
                m_m_Dpi[0] = (pD_old+rawpPim).M()
                m_rm_Dpi[0] = (cms-pD_old-rawpPim).M()
            elif t_in.charm < 0:
                m_m_Dmisspi[0] = (pDmiss+pPim).M()
                m_rm_Dmisspi[0] = (cms-pDmiss-pPim).M()
                m_m_Dpi[0] = (pD_old+rawpPip).M()
                m_rm_Dpi[0] = (cms-pD_old-rawpPip).M()
            m_indexmc[0] = t_in.indexmc
            m_m_DDmiss[0] = (pDmiss+pD).M()
            m_n_othershws[0] = t_in.n_othershws
            m_n_othertrks[0] = t_in.n_othertrks
            m_charge_left[0] = t_in.charge_left
            m_m_piplus0[0] = rawpPip.M()
            m_m_piminus0[0] = rawpPim.M()
            m_p_piplus0[0] = rawpPip.P()
            m_p_piminus0[0] = rawpPim.P()
            m_E_piplus0[0] = rawpPip.E()
            m_E_piminus0[0] = rawpPim.E()
            m_chi2_pi0[0] = t_in.chi2_pi0_save
            m_m_Dpi0[0] = (pD+pPi0).M()
            m_rm_Dpi0[0] = (cms-pD-pPi0).M()
            deltaM = 999.
            m_Dmisspi0 = pDmiss.M()
            rm_Dmisspi0 = (cms-pDmiss).M()
            for iPi0 in range(t_in.n_pi0):
                ppi0 = TLorentzVector(0, 0, 0, 0)
                ppi0.SetPxPyPzE(t_in.p4_pi0[iPi0*4+0], t_in.p4_pi0[iPi0*4+1], t_in.p4_pi0[iPi0*4+2], t_in.p4_pi0[iPi0*4+3])
                if (fabs((pDmiss + ppi0).M() - 2.01026) < deltaM):
                    deltaM = fabs((pDmiss + ppi0).M() - 2.01026)
                    m_Dmisspi0 = (pDmiss + ppi0).M()
                    rm_Dmisspi0 = (cms - pDmiss - ppi0).M()
            m_m_Dmisspi0 = m_Dmisspi0
            m_m_pi0[0] = pPi0.M()
            m_p_pi0[0] = pPi0.P()
            m_E_pi0[0] = pPi0.E()
            m_n_pi0[0] = t_in.n_pi0
            for i in range(t_in.indexmc):
                m_motheridx[i] = t_in.motheridx[i]
                m_pdgid[i] = t_in.pdgid[i]
            m_matched_D[0] = t_in.matched_D
            m_matched_pi[0] = t_in.matched_pi
            m_matched_piplus[0] = t_in.matched_piplus
            m_matched_piminus[0] = t_in.matched_piminus
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
    if MODE == 'raw':
        save_raw(f_in, cms, t_out, MODE)
    if MODE == 'truth':
        save_truth(f_in, cms, t_out, MODE)
    if MODE == 'signal' or MODE == 'sidebandlow' or MODE == 'sidebandup':
        save_missing(f_in, cms, t_out, MODE)

    f_out.cd()
    t_out.Write()
    f_out.Close()

if __name__ == '__main__':
    main()
