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
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    apply_cuts.py

SYNOPSIS
    ./apply_cuts.py [file_in] [file_out] [ecms] [mode] [region]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    October 2019
\n''')

def save_before(file_in, file_out, ecms, region):
    try:
        chain = TChain('save')
        chain.Add(file_in)
    except:
        logging.error(file_in + ' is invalid!')
        sys.exit()

    cut = ''
    if region == 'raw_signal':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ')'
        cut = cut_base 

    if region == 'raw_sidebandlow':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        sidebandlow_up = signal_low - (signal_up - signal_low)
        sidebandlow_low = sidebandlow_up - (signal_up - signal_low)
        cut_base = '(m_rawm_D > ' + str(sidebandlow_low) + '&& m_rawm_D < ' + str(sidebandlow_up) + ')'
        cut = cut_base 

    if region == 'raw_sidebandup':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        sidebandup_low = signal_up + (signal_up - signal_low)
        sidebandup_up = sidebandup_low + (signal_up - signal_low)
        cut_base = '(m_rawm_D > ' + str(sidebandup_low) + '&& m_rawm_D < ' + str(sidebandup_up) + ')'
        cut = cut_base 

    if region == 'STDDmiss_signal':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        window_low = 1.86965 - window(ecms)/2.
        window_up = 1.86965 + window(ecms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + ' && m_rm_Dpipi < ' + str(window_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_sidebandlow':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        window_low = 1.86965 - window(ecms)/2.
        window_up = 1.86965 + window(ecms)/2.
        windowlow_up = window_low - (window_up - window_low)
        windowlow_low = windowlow_up - (window_up - window_low)
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(windowlow_low) + '&& m_rm_Dpipi < ' + str(windowlow_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_sidebandup':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        window_low = 1.86965 - window(ecms)/2.
        window_up = 1.86965 + window(ecms)/2.
        windowup_low = window_up + (window_up - window_low)
        windowup_up = windowup_low + (window_up - window_low)
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(windowup_low) + '&& m_rm_Dpipi < ' + str(windowup_up) + ')'
        cut = cut_base + ' && ' + cut_window

    t = chain.CopyTree(cut)
    t.SaveAs(file_out)

def save_after(file_in, file_out, ecms, region):
    try:
        chain = TChain('save')
        chain.Add(file_in)
    except:
        logging.error(file_in + ' is invalid!')
        sys.exit()

    cut = ''
    if region == 'STDDmiss_signal':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        window_low = 1.86965 - window(ecms)/2.
        window_up = 1.86965 + window(ecms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + ' && m_rm_Dpipi < ' + str(window_up) + ')'
        # cut_num = '(m_n_othertrks <= 3 && m_n_othershws <= 6 && m_n_p == 0 && m_n_pbar == 0)'
        cut_num = '(m_n_p == 0 && m_n_pbar == 0)'
        cut_KS = '(!((m_m_pipi > 0.491036 && m_m_pipi < 0.503471) && abs(m_L_svf/m_Lerr_svf) > 2))'
        cut_Vxy = '(m_Vxy_Dtrks[0] <= 0.55 && m_Vxy_Dtrks[1] <= 0.55 && m_Vxy_Dtrks[2] <= 0.55 && m_Vxy_pip <= 0.55 && m_Vxy_pim <= 0.55)'
        cut_Vz = '(m_Vz_Dtrks[0] <= 3 && m_Vz_Dtrks[1] <= 3 && m_Vz_Dtrks[2] <= 3 && m_Vz_pip <= 3 && m_Vz_pim <= 3)'
        cut = cut_base + ' && ' + cut_window + ' && ' + cut_num + ' && ' + cut_KS + ' && ' + cut_Vxy + ' && ' + cut_Vz

    if region == 'STDDmiss_sidebandlow':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        window_low = 1.86965 - window(ecms)/2.
        window_up = 1.86965 + window(ecms)/2.
        windowlow_up = window_low - (window_up - window_low)
        windowlow_low = windowlow_up - (window_up - window_low)
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(windowlow_low) + '&& m_rm_Dpipi < ' + str(windowlow_up) + ')'
        # cut_num = '(m_n_othertrks <= 3 && m_n_othershws <= 6 && m_n_p == 0 && m_n_pbar == 0)'
        cut_num = '(m_n_p == 0 && m_n_pbar == 0)'
        cut_KS = '(!((m_m_pipi > 0.491036 && m_m_pipi < 0.503471) && abs(m_L_svf/m_Lerr_svf) > 2))'
        cut_Vxy = '(m_Vxy_Dtrks[0] <= 0.55 && m_Vxy_Dtrks[1] <= 0.55 && m_Vxy_Dtrks[2] <= 0.55 && m_Vxy_pip <= 0.55 && m_Vxy_pim <= 0.55)'
        cut_Vz = '(m_Vz_Dtrks[0] <= 3 && m_Vz_Dtrks[1] <= 3 && m_Vz_Dtrks[2] <= 3 && m_Vz_pip <= 3 && m_Vz_pim <= 3)'
        cut = cut_base + ' && ' + cut_window + ' && ' + cut_num + ' && ' + cut_KS + ' && ' + cut_Vxy + ' && ' + cut_Vz

    if region == 'STDDmiss_sidebandup':
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        window_low = 1.86965 - window(ecms)/2.
        window_up = 1.86965 + window(ecms)/2.
        windowup_low = window_up + (window_up - window_low)
        windowup_up = windowup_low + (window_up - window_low)
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(windowup_low) + '&& m_rm_Dpipi < ' + str(windowup_up) + ')'
        # cut_num = '(m_n_othertrks <= 3 && m_n_othershws <= 6 && m_n_p == 0 && m_n_pbar == 0)'
        cut_num = '(m_n_p == 0 && m_n_pbar == 0)'
        cut_KS = '(!((m_m_pipi > 0.491036 && m_m_pipi < 0.503471) && abs(m_L_svf/m_Lerr_svf) > 2))'
        cut_Vxy = '(m_Vxy_Dtrks[0] <= 0.55 && m_Vxy_Dtrks[1] <= 0.55 && m_Vxy_Dtrks[2] <= 0.55 && m_Vxy_pip <= 0.55 && m_Vxy_pim <= 0.55)'
        cut_Vz = '(m_Vz_Dtrks[0] <= 3 && m_Vz_Dtrks[1] <= 3 && m_Vz_Dtrks[2] <= 3 && m_Vz_pip <= 3 && m_Vz_pim <= 3)'
        cut = cut_base + ' && ' + cut_window + ' && ' + cut_num + ' && ' + cut_KS + ' && ' + cut_Vxy + ' && ' + cut_Vz

    t = chain.CopyTree(cut)
    t.SaveAs(file_out)

def main():
    args = sys.argv[1:]
    if len(args)<4:
        return usage()
    file_in = args[0]
    file_out = args[1]
    ecms = int(args[2])
    mode = args[3]
    region = args[4]

    print '--> Begin to process file: ' + file_in
    if mode == 'before':
        save_before(file_in, file_out, ecms, region)
    if mode == 'after':
        save_after(file_in, file_out, ecms, region)
    print '--> End of processing file: ' + file_out

if __name__ == '__main__':
    main()
