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
    ./apply_cuts.py [infile_path] [outfile_path] [ecms] [MODE] [region]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    October 2019
\n''')

def save_before(path_in, path_out, cms, region):
    try:
        chain = TChain('save')
        chain.Add(path_in)
    except:
        logging.error(path_in + ' is invalid!')
        sys.exit()

    cut = ''
    if region == 'raw_signal':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'raw_sidebandlow':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        sidebandlow_up = signal_low - (signal_up - signal_low)
        sidebandlow_low = sidebandlow_up - (signal_up - signal_low)
        cut_base = '(m_rawm_D > ' + str(sidebandlow_low) + '&& m_rawm_D < ' + str(sidebandlow_up) + ' && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'raw_sidebandup':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        sidebandup_low = signal_up + (signal_up - signal_low)
        sidebandup_up = sidebandup_low + (signal_up - signal_low)
        cut_base = '(m_rawm_D > ' + str(sidebandup_low) + '&& m_rawm_D < ' + str(sidebandup_up) + ' && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'STDDmiss_signal':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        window_low = 1.86965 - window(cms)/2.
        window_up = 1.86965 + window(cms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < ' + str(chi2_kf(cms)) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + ' && m_rm_Dpipi < ' + str(window_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_sidebandlow':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        window_low = 1.86965 - window(cms)/2.
        window_up = 1.86965 + window(cms)/2.
        windowlow_up = window_low - (window_up - window_low)
        windowlow_low = windowlow_up - (window_up - window_low)
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < ' + str(chi2_kf(cms)) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(windowlow_low) + '&& m_rm_Dpipi < ' + str(windowlow_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_sidebandup':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        window_low = 1.86965 - window(cms)/2.
        window_up = 1.86965 + window(cms)/2.
        windowup_low = window_up + (window_up - window_low)
        windowup_up = windowup_low + (window_up - window_low)
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < ' + str(chi2_kf(cms)) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(windowup_low) + '&& m_rm_Dpipi < ' + str(windowup_up) + ')'
        cut = cut_base + ' && ' + cut_window

    t = chain.CopyTree(cut)
    t.SaveAs(path_out)

def save_after(path_in, path_out, cms, region):
    try:
        chain = TChain('save')
        chain.Add(path_in)
    except:
        logging.error(path_in + ' is invalid!')
        sys.exit()

    cut = ''
    if region == 'STDDmiss_signal':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        window_low = 1.86965 - window(cms)/2.
        window_up = 1.86965 + window(cms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < ' + str(chi2_kf(cms)) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + ' && m_rm_Dpipi < ' + str(window_up) + ')'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471 && m_ctau_svf < 0.5)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_window + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'STDDmiss_sidebandlow':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        window_low = 1.86965 - window(cms)/2.
        window_up = 1.86965 + window(cms)/2.
        windowlow_up = window_low - (window_up - window_low)
        windowlow_low = windowlow_up - (window_up - window_low)
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < ' + str(chi2_kf(cms)) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(windowlow_low) + '&& m_rm_Dpipi < ' + str(windowlow_up) + ')'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471 && m_ctau_svf < 0.5)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_window + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'STDDmiss_sidebandup':
        signal_low = 1.86965 - width(cms)/2.
        signal_up = 1.86965 + width(cms)/2.
        window_low = 1.86965 - window(cms)/2.
        window_up = 1.86965 + window(cms)/2.
        windowup_low = window_up + (window_up - window_low)
        windowup_up = windowup_low + (window_up - window_low)
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < ' + str(chi2_kf(cms)) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(windowup_low) + '&& m_rm_Dpipi < ' + str(windowup_up) + ')'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471 && m_ctau_svf < 0.5)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_window + ' && ' + cut_KS + ' && ' + cut_Dst

    t = chain.CopyTree(cut)
    t.SaveAs(path_out)

def main():
    args = sys.argv[1:]
    if len(args)<4:
        return usage()

    path_in = args[0]
    path_out = args[1]
    cms = int(args[2])
    MODE = args[3]
    region = args[4]

    print '--> Begin to process file: ' + path_in
    if MODE == 'before':
        save_before(path_in, path_out, cms, region)
    if MODE == 'after':
        save_after(path_in, path_out, cms, region)
    print '--> End of processing file: ' + path_out

if __name__ == '__main__':
    main()
