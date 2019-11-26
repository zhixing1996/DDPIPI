#!/usr/bin/env python
"""
Divide samples into rm_Dpipi signal and sideband region
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-22 Thu 23:38]"

import ROOT
from ROOT import TCanvas, gStyle, TTree, TChain
from ROOT import TFile
import sys, os
import logging
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def sel(path, ecms, sample, mode, region):
    print '--> Begin to process file: ' + path
    try:
        chain = TChain('save')
        chain.Add(path)
    except:
        logging.error(path+' is invalid!')
        sys.exit()

    if region == 'signal' and int(ecms) == 4360:
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'sideband' and int(ecms) == 4360:
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        sidebandup_low = signal_up + (signal_up - signal_low)
        sidebandup_up = sidebandup_low + (signal_up - signal_low)
        sidebandlow_up = signal_low - (signal_up - signal_low)
        sidebandlow_low = sidebandlow_up - (signal_up - signal_low)
        cut_base = '(((m_rawm_D > ' + str(sidebandlow_low) + '&& m_rawm_D < ' + str(sidebandlow_up) + ') || (m_rawm_D > ' + str(sidebandup_low) + '&& m_rawm_D < ' + str(sidebandup_up) + ')) && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'signal' and int(ecms) == 4420:
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'sideband' and int(ecms) == 4420:
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        sidebandup_low = signal_up + (signal_up - signal_low)
        sidebandup_up = sidebandup_low + (signal_up - signal_low)
        sidebandlow_up = signal_low - (signal_up - signal_low)
        sidebandlow_low = sidebandlow_up - (signal_up - signal_low)
        cut_base = '(((m_rawm_D > ' + str(sidebandlow_low) + '&& m_rawm_D < ' + str(sidebandlow_up) + ') || (m_rawm_D > ' + str(sidebandup_low) + '&& m_rawm_D < ' + str(sidebandup_up) + ')) && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'signal' and int(ecms) == 4600:
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        cut_base = '(m_rawm_D > ' + str(signal_low) + ' && m_rawm_D < ' + str(signal_up) + ' && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    if region == 'sideband' and int(ecms) == 4600:
        signal_low = 1.86965 - width(ecms)/2.
        signal_up = 1.86965 + width(ecms)/2.
        sidebandup_low = signal_up + (signal_up - signal_low)
        sidebandup_up = sidebandup_low + (signal_up - signal_low)
        sidebandlow_up = signal_low - (signal_up - signal_low)
        sidebandlow_low = sidebandlow_up - (signal_up - signal_low)
        cut_base = '(((m_rawm_D > ' + str(sidebandlow_low) + '&& m_rawm_D < ' + str(sidebandlow_up) + ') || (m_rawm_D > ' + str(sidebandup_low) + '&& m_rawm_D < ' + str(sidebandup_up) + ')) && m_chi2_kf < 20)'
        cut_KS = '!(m_m_pipi > 0.491036 && m_m_pipi < 0.503471)'
        cut_Dst = '(m_m_Dpi0 < 2.0082 || m_m_Dpi0 > 2.01269)'
        cut = cut_base + ' && ' + cut_KS + ' && ' + cut_Dst

    t = chain.CopyTree(cut)

    path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/'+sample+'/'+mode+'/'+str(ecms)+'/'
    if sample == 'data':
        file_out = sample+'_'+str(ecms)+'_signal'+'_'+region+'.root'
    elif sample == 'bkgMC' and mode == 'DDPIPI':
        file_out = sample+'_D_D_PI_PI_'+str(ecms)+'_signal'+'_'+region+'.root'
    else:
        file_out = sample+'_'+mode+'_'+str(ecms)+'_signal'+'_'+region+'.root'
    t.SaveAs(path_out + file_out)
    print '--> End of processing file: ' + path

if __name__ == '__main__':
    args = sys.argv[1:]
    energy = args[0]

    if int(energy) == 4360:
        data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_raw.root'
        sigMC_X_3842_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/sigMC_X_3842_4360_raw.root'
        sigMC_D1_2420_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_raw.root'
        sigMC_D2_2460_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4360/sigMC_D2_2460_4360_raw.root'
        sigMC_psipp_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_raw.root'
        bkgMC_D_D_PI_PI_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/bkgMC/DDPIPI/4360/bkgMC_D_D_PI_PI_4360_raw.root'
        incMC_DD_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_raw.root'
        incMC_qq_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_raw.root'
        ecms = 4360
        sel(data_path, ecms, 'data', '', 'signal')
        sel(data_path, ecms, 'data', '', 'sideband')
        sel(sigMC_X_3842_path, ecms, 'sigMC', 'X_3842', 'signal')
        sel(sigMC_X_3842_path, ecms, 'sigMC', 'X_3842', 'sideband')
        sel(sigMC_D1_2420_path, ecms, 'sigMC', 'D1_2420', 'signal')
        sel(sigMC_D1_2420_path, ecms, 'sigMC', 'D1_2420', 'sideband')
        sel(sigMC_D2_2460_path, ecms, 'sigMC', 'D2_2460', 'signal')
        sel(sigMC_D2_2460_path, ecms, 'sigMC', 'D2_2460', 'sideband')
        sel(sigMC_psipp_path, ecms, 'sigMC', 'psipp', 'signal')
        sel(sigMC_psipp_path, ecms, 'sigMC', 'psipp', 'sideband')
        sel(bkgMC_D_D_PI_PI_path, ecms, 'bkgMC', 'DDPIPI', 'signal')
        sel(bkgMC_D_D_PI_PI_path, ecms, 'bkgMC', 'DDPIPI', 'sideband')
        sel(incMC_DD_path, ecms, 'incMC', 'DD', 'signal')
        sel(incMC_DD_path, ecms, 'incMC', 'DD', 'sideband')
        sel(incMC_qq_path, ecms, 'incMC', 'qq', 'signal')
        sel(incMC_qq_path, ecms, 'incMC', 'qq', 'sideband')

    if int(energy) == 4420:
        data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_raw.root'
        sigMC_X_3842_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/sigMC_X_3842_4420_raw.root'
        sigMC_D1_2420_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_raw.root'
        sigMC_D2_2460_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4420/sigMC_D2_2460_4420_raw.root'
        sigMC_psipp_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_raw.root'
        bkgMC_D_D_PI_PI_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/bkgMC/DDPIPI/4420/bkgMC_D_D_PI_PI_4420_raw.root'
        incMC_DD_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_raw.root'
        incMC_qq_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_raw.root'
        ecms = 4420
        sel(data_path, ecms, 'data', '', 'signal')
        sel(data_path, ecms, 'data', '', 'sideband')
        sel(sigMC_X_3842_path, ecms, 'sigMC', 'X_3842', 'signal')
        sel(sigMC_X_3842_path, ecms, 'sigMC', 'X_3842', 'sideband')
        sel(sigMC_D1_2420_path, ecms, 'sigMC', 'D1_2420', 'signal')
        sel(sigMC_D1_2420_path, ecms, 'sigMC', 'D1_2420', 'sideband')
        sel(sigMC_D2_2460_path, ecms, 'sigMC', 'D2_2460', 'signal')
        sel(sigMC_D2_2460_path, ecms, 'sigMC', 'D2_2460', 'sideband')
        sel(sigMC_psipp_path, ecms, 'sigMC', 'psipp', 'signal')
        sel(sigMC_psipp_path, ecms, 'sigMC', 'psipp', 'sideband')
        sel(bkgMC_D_D_PI_PI_path, ecms, 'bkgMC', 'DDPIPI', 'signal')
        sel(bkgMC_D_D_PI_PI_path, ecms, 'bkgMC', 'DDPIPI', 'sideband')
        sel(incMC_DD_path, ecms, 'incMC', 'DD', 'signal')
        sel(incMC_DD_path, ecms, 'incMC', 'DD', 'sideband')
        sel(incMC_qq_path, ecms, 'incMC', 'qq', 'signal')
        sel(incMC_qq_path, ecms, 'incMC', 'qq', 'sideband')

    if int(energy) == 4600:
        data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_raw.root'
        sigMC_X_3842_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/sigMC_X_3842_4600_raw.root'
        sigMC_D1_2420_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_raw.root'
        sigMC_D2_2460_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4600/sigMC_D2_2460_4600_raw.root'
        sigMC_psipp_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_raw.root'
        bkgMC_D_D_PI_PI_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/bkgMC/DDPIPI/4600/bkgMC_D_D_PI_PI_4600_raw.root'
        incMC_DD_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_raw.root'
        incMC_qq_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_raw.root'
        incMC_LL_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/LL/4600/incMC_LL_4600_raw.root'
        ecms = 4600
        sel(data_path, ecms, 'data', '', 'signal')
        sel(data_path, ecms, 'data', '', 'sideband')
        sel(sigMC_X_3842_path, ecms, 'sigMC', 'X_3842', 'signal')
        sel(sigMC_X_3842_path, ecms, 'sigMC', 'X_3842', 'sideband')
        sel(sigMC_D1_2420_path, ecms, 'sigMC', 'D1_2420', 'signal')
        sel(sigMC_D1_2420_path, ecms, 'sigMC', 'D1_2420', 'sideband')
        sel(sigMC_D2_2460_path, ecms, 'sigMC', 'D2_2460', 'signal')
        sel(sigMC_D2_2460_path, ecms, 'sigMC', 'D2_2460', 'sideband')
        sel(sigMC_psipp_path, ecms, 'sigMC', 'psipp', 'signal')
        sel(sigMC_psipp_path, ecms, 'sigMC', 'psipp', 'sideband')
        sel(bkgMC_D_D_PI_PI_path, ecms, 'bkgMC', 'DDPIPI', 'signal')
        sel(bkgMC_D_D_PI_PI_path, ecms, 'bkgMC', 'DDPIPI', 'sideband')
        sel(incMC_DD_path, ecms, 'incMC', 'DD', 'signal')
        sel(incMC_DD_path, ecms, 'incMC', 'DD', 'sideband')
        sel(incMC_qq_path, ecms, 'incMC', 'qq', 'signal')
        sel(incMC_qq_path, ecms, 'incMC', 'qq', 'sideband')
        sel(incMC_LL_path, ecms, 'incMC', 'LL', 'signal')
        sel(incMC_LL_path, ecms, 'incMC', 'LL', 'sideband')
