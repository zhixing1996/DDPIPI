#!/usr/bin/env python
"""
Calculate significance and efficiency
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-10-13 Thu 00:14]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TPaveText
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def cal(t1, t2, t3, t4, ecms, MODE, runNolow, runNoup):
    N1 = 0
    for ientry in xrange(t1.GetEntries()):
        t1.GetEntry(ientry)
        if fabs(t1.m_runNo) < runNolow or fabs(t1.m_runNo) > runNoup:
            continue
        if MODE == 'raw':
            N1 += 1
        if MODE == 'cut1':
            if t1.m_m_Dpi0 < 2.0082 or t1.m_m_Dpi0 > 2.01269:
                N1 += 1
        if MODE == 'cut2':
            if t1.m_m_Dpi0 < 2.0082 or t1.m_m_Dpi0 > 2.01269 and (t1.m_m_pipi < 0.491036 or t1.m_m_pipi > 0.503471):
                N1 += 1
        if MODE == 'cut3':
            if t1.m_m_Dpi0 < 2.0082 or t1.m_m_Dpi0 > 2.01269 and (t1.m_m_pipi < 0.491036 or t1.m_m_pipi > 0.503471) and t1.m_chi2_vf < 20:
                N1 += 1
    N2 = 0
    for ientry in xrange(t2.GetEntries()):
        t2.GetEntry(ientry)
        if fabs(t2.m_runNo) < runNolow or fabs(t2.m_runNo) > runNoup:
            continue
        if MODE == 'raw':
            N2 += 1
        if MODE == 'cut1':
            if t2.m_m_Dpi0 < 2.0082 or t2.m_m_Dpi0 > 2.01269:
                N2 += 1
        if MODE == 'cut2':
            if t2.m_m_Dpi0 < 2.0082 or t2.m_m_Dpi0 > 2.01269 and (t2.m_m_pipi < 0.491036 or t2.m_m_pipi > 0.503471):
                N2 += 1
        if MODE == 'cut3':
            if t2.m_m_Dpi0 < 2.0082 or t2.m_m_Dpi0 > 2.01269 and (t2.m_m_pipi < 0.491036 or t2.m_m_pipi > 0.503471) and t2.m_chi2_vf < 20:
                N2 += 1
    N3 = 0
    for ientry in xrange(t3.GetEntries()):
        t3.GetEntry(ientry)
        if fabs(t3.m_runNo) < runNolow or fabs(t3.m_runNo) > runNoup:
            continue
        if MODE == 'raw':
            N3 += 1
        if MODE == 'cut1':
            if t3.m_m_Dpi0 < 2.0082 or t3.m_m_Dpi0 > 2.01269:
                N3 += 1
        if MODE == 'cut2':
            if t3.m_m_Dpi0 < 2.0082 or t3.m_m_Dpi0 > 2.01269 and (t3.m_m_pipi < 0.491036 or t3.m_m_pipi > 0.503471):
                N3 += 1
        if MODE == 'cut3':
            if t3.m_m_Dpi0 < 2.0082 or t3.m_m_Dpi0 > 2.01269 and (t3.m_m_pipi < 0.491036 or t3.m_m_pipi > 0.503471) and t3.m_chi2_vf < 20:
                N3 += 1
    N4 = 0
    for ientry in xrange(t4.GetEntries()):
        t4.GetEntry(ientry)
        if fabs(t4.m_runNo) < runNolow or fabs(t4.m_runNo) > runNoup:
            continue
        if MODE == 'raw':
            N4 += 1
        if MODE == 'cut1':
            if t4.m_m_Dpi0 < 2.0082 or t4.m_m_Dpi0 > 2.01269:
                N4 += 1
        if MODE == 'cut2':
            if t4.m_m_Dpi0 < 2.0082 or t4.m_m_Dpi0 > 2.01269 and (t4.m_m_pipi < 0.491036 or t4.m_m_pipi > 0.503471):
                N4 += 1
        if MODE == 'cut3':
            if t4.m_m_Dpi0 < 2.0082 or t4.m_m_Dpi0 > 2.01269 and (t4.m_m_pipi < 0.491036 or t4.m_m_pipi > 0.503471) and t4.m_chi2_vf < 20:
                N4 += 1
    if int(ecms) == 4420:
        NDD = 40300000.
        Nqq = 14000000.
        scale1 = 1073.56*65.4*0.0938/(500000*0.0938/(0.0938+0.00993+0.00304+0.00254+0.00174))
        scale2 = 1073.56*23.8*0.0938/(500000*0.0938/(0.0938+0.00993+0.00304+0.00254+0.00174))
        scale3 = 10494678.0/40300000.0
        scale4 = 7202230.0/14000000.0
    significance = (N1*scale1 + N2*scale2)/sqrt(N1*scale1+ N2*scale2 + N3*scale3 + N4*scale4)
    print 'sigificance of ' + MODE + ': ' + str(significance)
    eff1 = N1/500000./(0.0938/(0.0938+0.00993+0.00304+0.00254+0.00174)) 
    eff2 = N2/500000./(0.0938/(0.0938+0.00993+0.00304+0.00254+0.00174))
    eff3 = N3/NDD/0.0938 
    eff4 = N4/Nqq/0.0938
    print 'efficiency of D1(2420): ' + '(' + MODE + ')' + ': ' + str(eff1)
    print 'efficiency of psipp: ' + '(' + MODE + ')' + ': ' + str(eff2)
    print 'efficiency of open charm' + '(' + MODE + ')' + ': ' + str(eff3)
    print 'efficiency of qqbar: ' + '(' + MODE + ')' + ': ' + str(eff4)

def content(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, ecms, MODE, runNolow, runNoup):
    try:
        f_incMC1 = TFile(incMC1_path)
        f_incMC2 = TFile(incMC2_path)
        f_sigMC1 = TFile(sigMC1_path)
        f_sigMC2 = TFile(sigMC2_path)
        t_incMC1 = f_incMC1.Get('save')
        t_incMC2 = f_incMC2.Get('save')
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        entries_incMC1 = t_incMC1.GetEntries()
        entries_incMC2 = t_incMC2.GetEntries()
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('inclusive MC(open charm) entries :'+str(entries_incMC1))
        logging.info('inclusive MC(qqbar) entries :'+str(entries_incMC2))
        logging.info('signal MC(D1(2420)) entries :'+str(entries_sigMC1))
        logging.info('signal MC(psi(3770)) entries :'+str(entries_sigMC2))
    except:
        logging.error('File is invalid!')
        sys.exit()

    cal(t_sigMC1, t_sigMC2, t_incMC1, t_incMC2, ecms, MODE, runNolow, runNoup)
    
if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        MODE = args[0]
    except:
        logging.error('python plot_stat_match.py [MODE]: MODE = raw or cut')
        sys.exit()

    incMC1_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_before.root'
    incMC2_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_before.root'
    sigMC1_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_before.root'
    sigMC2_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_before.root'
    ecms = 4360
    runNolow = 30616
    runNoup = 30279
    content(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, ecms, MODE, runNolow, runNoup)

    incMC1_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_before.root'
    incMC2_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_before.root'
    sigMC1_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_before.root'
    sigMC2_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_before.root'
    ecms = 4420
    runNolow = 36773
    runNoup = 38140
    content(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, ecms, MODE, runNolow, runNoup)

    incMC1_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_before.root'
    incMC2_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_before.root'
    sigMC1_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_before.root'
    sigMC2_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_before.root'
    ecms = 4600
    runNolow = 35227
    runNoup = 36213
    content(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, ecms, MODE, runNolow, runNoup)
