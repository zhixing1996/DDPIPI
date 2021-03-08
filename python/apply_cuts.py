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
m_D0 = 1.86483
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
    width_low = 1.86965 - width(ecms)/2.
    width_up = 1.86965 + width(ecms)/2.
    window_low = 1.86965 - window(ecms)/2.
    window_up = 1.86965 + window(ecms)/2.
    width_side_low_up = width_low - (width_up - width_low)
    width_side_low_low = width_side_low_up - (width_up - width_low)
    width_side_up_low = width_up + (width_up - width_low)
    width_side_up_up = width_side_up_low + (width_up - width_low)
    window_side_low_up = window_low - (window_up - window_low)
    window_side_low_low = window_side_low_up - (window_up - window_low)
    window_side_up_low = window_up + (window_up - window_low)
    window_side_up_up = window_side_up_low + (window_up - window_low)

    if region == 'raw_signal':
        cut_base = '(m_rawm_D > ' + str(width_low) + ' && m_rawm_D < ' + str(width_up) + ')'
        cut = cut_base 

    if region == 'raw_sidebandlow':
        cut_base = '(m_rawm_D > ' + str(width_side_low_low) + '&& m_rawm_D < ' + str(width_side_low_up) + ')'
        cut = cut_base 

    if region == 'raw_sidebandup':
        cut_base = '(m_rawm_D > ' + str(width_side_up_low) + '&& m_rawm_D < ' + str(width_side_up_up) + ')'
        cut = cut_base 

    if region == 'STDDmiss_signal':
        cut_base = '(m_rawm_D > ' + str(width_low) + ' && m_rawm_D < ' + str(width_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + ' && m_rm_Dpipi < ' + str(window_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_side1_low':
        cut_base = '(m_rawm_D > ' + str(width_low) + ' && m_rawm_D < ' + str(width_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_low_low) + '&& m_rm_Dpipi < ' + str(window_side_low_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_side1_up':
        cut_base = '(m_rawm_D > ' + str(width_low) + ' && m_rawm_D < ' + str(width_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_up_low) + '&& m_rm_Dpipi < ' + str(window_side_up_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_side2_low':
        cut_base = '(m_rawm_D > ' + str(width_side_low_low) + ' && m_rawm_D < ' + str(width_side_low_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + '&& m_rm_Dpipi < ' + str(window_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_side2_up':
        cut_base = '(m_rawm_D > ' + str(width_side_up_low) + ' && m_rawm_D < ' + str(width_side_up_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + '&& m_rm_Dpipi < ' + str(window_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_side3_low':
        cut_base = '(m_rawm_D > ' + str(width_side_low_low) + ' && m_rawm_D < ' + str(width_side_low_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_low_low) + '&& m_rm_Dpipi < ' + str(window_side_low_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_side3_up':
        cut_base = '(m_rawm_D > ' + str(width_side_low_low) + ' && m_rawm_D < ' + str(width_side_low_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_up_low) + '&& m_rm_Dpipi < ' + str(window_side_up_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_side4_low':
        cut_base = '(m_rawm_D > ' + str(width_side_up_low) + ' && m_rawm_D < ' + str(width_side_up_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_low_low) + '&& m_rm_Dpipi < ' + str(window_side_low_up) + ')'
        cut = cut_base + ' && ' + cut_window

    if region == 'STDDmiss_side4_up':
        cut_base = '(m_rawm_D > ' + str(width_side_up_low) + ' && m_rawm_D < ' + str(width_side_up_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_up_low) + '&& m_rm_Dpipi < ' + str(window_side_up_up) + ')'
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
    width_low = 1.86965 - width(ecms)/2.
    width_up = 1.86965 + width(ecms)/2.
    window_low = 1.86965 - window(ecms)/2.
    window_up = 1.86965 + window(ecms)/2.
    width_side_low_up = width_low - (width_up - width_low)
    width_side_low_low = width_side_low_up - (width_up - width_low)
    width_side_up_low = width_up + (width_up - width_low)
    width_side_up_up = width_side_up_low + (width_up - width_low)
    window_side_low_up = window_low - (window_up - window_low)
    window_side_low_low = window_side_low_up - (window_up - window_low)
    window_side_up_low = window_up + (window_up - window_low)
    window_side_up_up = window_side_up_low + (window_up - window_low)

    if region == 'STDDmiss_signal':
        cut_base = '(m_rawm_D > ' + str(width_low) + ' && m_rawm_D < ' + str(width_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + ' && m_rm_Dpipi < ' + str(window_up) + ')'

    if region == 'STDDmiss_side1_low':
        cut_base = '(m_rawm_D > ' + str(width_low) + ' && m_rawm_D < ' + str(width_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_low_low) + '&& m_rm_Dpipi < ' + str(window_side_low_up) + ')'

    if region == 'STDDmiss_side1_up':
        cut_base = '(m_rawm_D > ' + str(width_low) + ' && m_rawm_D < ' + str(width_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_up_low) + '&& m_rm_Dpipi < ' + str(window_side_up_up) + ')'

    if region == 'STDDmiss_side2_low':
        cut_base = '(m_rawm_D > ' + str(width_side_low_low) + ' && m_rawm_D < ' + str(width_side_low_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + '&& m_rm_Dpipi < ' + str(window_up) + ')'

    if region == 'STDDmiss_side2_up':
        cut_base = '(m_rawm_D > ' + str(width_side_up_low) + ' && m_rawm_D < ' + str(width_side_up_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + '&& m_rm_Dpipi < ' + str(window_up) + ')'

    if region == 'STDDmiss_side3_low':
        cut_base = '(m_rawm_D > ' + str(width_side_low_low) + ' && m_rawm_D < ' + str(width_side_low_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_low_low) + '&& m_rm_Dpipi < ' + str(window_side_low_up) + ')'

    if region == 'STDDmiss_side3_up':
        cut_base = '(m_rawm_D > ' + str(width_side_low_low) + ' && m_rawm_D < ' + str(width_side_low_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_up_low) + '&& m_rm_Dpipi < ' + str(window_side_up_up) + ')'

    if region == 'STDDmiss_side4_low':
        cut_base = '(m_rawm_D > ' + str(width_side_up_low) + ' && m_rawm_D < ' + str(width_side_up_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_low_low) + '&& m_rm_Dpipi < ' + str(window_side_low_up) + ')'

    if region == 'STDDmiss_side4_up':
        cut_base = '(m_rawm_D > ' + str(width_side_up_low) + ' && m_rawm_D < ' + str(width_side_up_up) + ')'
        cut_window = '(m_rm_Dpipi > ' + str(window_side_up_low) + '&& m_rm_Dpipi < ' + str(window_side_up_up) + ')'

    cut_DDPI = '(abs(m_Kpipipi1-1.86483) > 0.01 && abs(m_Kpipipi2-1.86483) > 0.01)'
    if not (region == 'raw_signal' or region == 'raw_sidebandlow' or region == 'raw_sidebandup' or region == 'rm_Dpipi_signal'):
        cut_num = '(m_n_p == 0 && m_n_pbar == 0)'
        cut_KS = '(!((m_m_pipi > 0.491036 && m_m_pipi < 0.503471) && abs(m_L_svf/m_Lerr_svf) > 2))'
        cut_Vxy = '(m_Vxy_Dtrks[0] <= 0.55 && m_Vxy_Dtrks[1] <= 0.55 && m_Vxy_Dtrks[2] <= 0.55 && m_Vxy_pip <= 0.55 && m_Vxy_pim <= 0.55)'
        cut_Vz = '(m_Vz_Dtrks[0] <= 3 && m_Vz_Dtrks[1] <= 3 && m_Vz_Dtrks[2] <= 3 && m_Vz_pip <= 3 && m_Vz_pim <= 3)'
        cut = cut_base + ' && ' + cut_window + ' && ' + cut_num + ' && ' + cut_KS + ' && ' + cut_Vxy + ' && ' + cut_Vz + ' && ' + cut_DDPI

    if region == 'rm_Dpipi_signal':
        cut_window = '(m_rm_Dpipi > ' + str(window_low) + ' && m_rm_Dpipi < ' + str(window_up) + ')'
        cut = cut_window + ' && ' + cut_DDPI

    if region == 'raw_signal':
        cut_base = '(m_rawm_D > ' + str(width_low) + ' && m_rawm_D < ' + str(width_up) + ')'
        cut = cut_base + ' && ' + cut_DDPI

    if region == 'raw_sidebandlow':
        cut_base = '(m_rawm_D > ' + str(width_side_low_low) + '&& m_rawm_D < ' + str(width_side_low_up) + ')'
        cut = cut_base + ' && ' + cut_DDPI

    if region == 'raw_sidebandup':
        cut_base = '(m_rawm_D > ' + str(width_side_up_low) + '&& m_rawm_D < ' + str(width_side_up_up) + ')'
        cut = cut_base + ' && ' + cut_DDPI

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
