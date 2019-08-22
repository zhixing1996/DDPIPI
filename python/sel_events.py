#!/usr/bin/env python
"""
Select events using cuts
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-21 Wed 14:41]"

from array import array
# import numpy as np
import ROOT
from ROOT import TCanvas, gStyle, TLorentzVector, TTree
from ROOT import TFile, TH1F, TLegend, TArrow, TChain
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    sel_events.py

SYNOPSIS
    ./sel_events.py [infile_path] [outfile_path] [Ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    August 2019
\n''')

def apply_cuts(t_std, t_otherTrk, cms, t):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_mode = array('i', [0])
    m_charm = array('i', [0])
    m_rawm_D = array('d', [999.])
    m_rm_D = array('d', [999.])
    m_rm_pipi = array('d', [999.])
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
    t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
    t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
    t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
    t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
    t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
    t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')

    nentries = t_std.GetEntries()
    for ientry in range(nentries):
        t_std.GetEntry(ientry)
        if t_std.mode != 200:
            continue
        if t_std.chi2_vf > 100:
            continue
        if t_std.chi2_kf > 20:
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
                m_rm_D[0] = (cms-pD).M()
                m_rm_pipi[0] = (cms-pPip-pPim).M()
                if t_std.charm > 0 and t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+4] == -1:
                    m_m_Dpi[0] = (pD+pPim).M()
                elif t_std.charm < 0 and t_otherTrk.rawp4_otherMdcKaltrk[iTrk2*6+4] == 1:
                    m_m_Dpi[0] = (pD+pPip).M()
                m_m_Dpipi[0] = (pD+pPip+pPim).M()
                m_rm_Dpipi[0] = (cms-pD-pPip-pPim).M()
                m_chi2_vf[0] = t_std.chi2_vf
                m_chi2_kf[0] = t_std.chi2_kf
                t.Fill()

def main():
    args = sys.argv[1:]
    if len(args)<3:
        return usage()

    file_in = args[0]
    file_out = args[1]
    ecms = float(args[2])

    f_in = TFile(file_in)
    t_std = f_in.Get('STD')
    t_otherTrk = f_in.Get('otherTrk')

    f_out = TFile(file_out, 'recreate')
    t_out = TTree('save', 'save')

    cms = TLorentzVector(0.011*ecms, 0, 0, ecms)
    apply_cuts(t_std, t_otherTrk, cms, t_out)

    f_out.cd()
    t_out.Write()
    f_out.Close()

if __name__ == '__main__':
    main()
