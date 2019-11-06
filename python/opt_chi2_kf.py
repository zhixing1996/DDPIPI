#!/usr/bin/env python
"""
Optiomize chi2 of Kiniematic fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-04 Tue 06:13]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH2F, TPaveText, TArrow
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetPaperSize(20,30)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadRightMargin(0.08)
gStyle.SetPadBottomMargin(0.18)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.04)

def set_arrow(arrow):
    arrow.SetLineWidth(0)
    arrow.SetLineColor(2)
    arrow.SetFillColor(2)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetTitleOffset(1.4)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.5)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetMarkerStyle(8)
    h.SetMarkerSize(0.65)
    h.SetLineColor(1)

def cal_significance(t1, t2, t3, t4, entries1, entries2, entries3, entries4, N, step, ratio1, ratio2, ratio3, ratio4, runNolow, runNoup):
    ymax = 0
    NEntry = 0
    S1_list = []
    S2_list = []
    S_list = []
    print 'Start of sigMC1...'
    for i in xrange(N):
        S1 = 0
        for j in xrange(int(entries1*ratio1)):
            t1.GetEntry(j)
            if t1.m_chi2_kf < (step + i*step) and t1.m_mode == 200 and fabs(t1.m_runNo) > runNolow and fabs(t1.m_runNo) < runNoup:
                S1 = S1 + 1
        S1_list.append(S1)
    print 'Start of sigMC2...'
    for i in xrange(N):
        S2 = 0
        for j in xrange(int(entries2*ratio2)):
            t2.GetEntry(j)
            if t2.m_chi2_kf < (step + i*step) and t2.m_mode == 200 and fabs(t2.m_runNo) > runNolow and fabs(t2.m_runNo) < runNoup:
                S2 = S2 + 1
        S2_list.append(S2)
    for i in xrange(N):
        S_list.append(S1_list[i]+S2_list[i])
    B1_list = []
    B2_list = []
    B_list = []
    print 'Start of incMC1...'
    for i in xrange(N):
        B1 = 0
        for j in xrange(int(entries3*ratio3)):
            t3.GetEntry(j)
            if t3.m_chi2_kf < (step + i*step) and t3.m_mode == 200 and fabs(t3.m_runNo) > runNolow and fabs(t3.m_runNo) < runNoup:
                B1 = B1 + 1
        B1_list.append(B1)
    print 'Start of incMC2...'
    for i in xrange(N):
        B2 = 0
        for j in xrange(int(entries4*ratio4)):
            t4.GetEntry(j)
            if t4.m_chi2_kf < (step + i*step) and t4.m_mode == 200 and fabs(t4.m_runNo) > runNolow and fabs(t4.m_runNo) < runNoup:
                B2 = B2 + 1
        B2_list.append(B2)
    for i in xrange(N):
        B_list.append(B1_list[i]+B2_list[i])
    Ratio_list = []
    for i in xrange(N):
        if B_list[i] == 0:
            significance = 0
        else:
            significance = S_list[i]/sqrt(S_list[i] + B_list[i])
        Ratio_list.append(significance)
        if significance > ymax:
            ymax = significance
            NEntry = i
    xmin = step
    xmax = N*step
    xtitle = '#chi^{2}(D^{+}D_{missing}#pi^{+}_{0}#pi^{-}_{0})'
    ytitle = '#frac{S}{#sqrt{S+B}}'
    h_FOM = TH2F('h_FOM', 'FOM', N, xmin, xmax, N, 0, ymax + 5)
    set_histo_style(h_FOM, xtitle, ytitle)
    for i in xrange(N):
        h_FOM.Fill(step + i*step, Ratio_list[i])
    return h_FOM, NEntry

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, pt_title, ecms, ratio1, ratio2, ratio3, ratio4, runNolow, runNoup, arrow_left, arrow_bottom, arrow_right, arrow_top):
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
        logging.info('inclusive MC (open charm) entries :'+str(entries_incMC1))
        logging.info('inclusive MC (qqbar) entries :'+str(entries_incMC2))
        logging.info('D1(2420) signal MC entries :'+str(entries_sigMC1))
        logging.info('psi(3770) signal MC entries :'+str(entries_sigMC2))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = 100
    step = 100/xbins

    h_FOM, ientry= cal_significance(t_sigMC1, t_sigMC2, t_incMC1, t_incMC2, entries_sigMC1, entries_sigMC2, entries_incMC1, entries_incMC2, xbins, step, ratio1, ratio2, ratio3, ratio4, runNolow, runNoup)
    h_FOM.Draw()
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    arrow = TArrow(arrow_left, arrow_bottom, arrow_right, arrow_top, 0.01,'>')
    set_arrow(arrow)
    arrow.Draw()

    pt = TPaveText(0.6, 0.8, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)

    range = 'chi2 of kinematic fit of K^{-}#pi^{+}#pi^{+}: ' + str(arrow_right)
    print range

    mbc.Update()
    mbc.SaveAs('./figs/opt_chi2_kf_'+str(ecms)+'.pdf')

def main():
    args = sys.argv[1:]
    energy = args[0]

    if int(energy) == 4360:
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_signal.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_signal.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_signal.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_signal.root'
        pt_title = '(a)'
        ecms = 4360
        lum = 539.84
        XS1 = 41.8
        XS2 = 17.3
        XS3 = 17500.0
        XS4 = 1000.0
        runNolow = 30616
        runNoup = 31279
        GenNum = 500000
        GenNum1 = 9400000
        GenNum2 = 500000
        ratio1 = lum*XS1*(0.0938+0.00993+0.00304+0.00254+0.00174)/GenNum
        ratio2 = lum*XS2*(0.0938+0.00993+0.00304+0.00254+0.00174)/GenNum
        ratio3 = lum*XS3/GenNum1
        ratio4 = lum*XS4/GenNum2
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 22
        plot(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, pt_title, ecms, ratio1, ratio2, ratio3, ratio4, runNolow, runNoup, arrow_left, arrow_bottom, arrow_right, arrow_top)

    if int(energy) == 4420:
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_signal.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_signal.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_signal.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_signal.root'
        pt_title = '(b)'
        ecms = 4420
        lum = 1073.56
        XS1 = 65.4
        XS2 = 23.8
        XS3 = 7000.0
        XS4 = 10200.0
        runNolow = 36773
        runNoup = 38140
        GenNum = 500000
        GenNum1 = 14000000
        GenNum2 = 40300000
        ratio1 = lum*XS1*(0.0938+0.00993+0.00304+0.00254+0.00174)/GenNum
        ratio2 = lum*XS2*(0.0938+0.00993+0.00304+0.00254+0.00174)/GenNum
        ratio3 = lum*XS3/GenNum1
        ratio4 = lum*XS4/GenNum2
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 25
        plot(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, pt_title, ecms, ratio1, ratio2, ratio3, ratio4, runNolow, runNoup, arrow_left, arrow_bottom, arrow_right, arrow_top)

    if int(energy) == 4600:
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_signal.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_signal.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_signal.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_signal.root'
        pt_title = '(c)'
        ecms = 4600
        lum = 566.93
        XS1 = 27.7
        XS2 = 7.2
        XS3 = 6000.0
        XS4 = 7800.0
        runNolow = 35227
        runNoup = 35743
        GenNum = 500000
        GenNum1 = 2800000
        GenNum2 = 3100000
        ratio1 = lum*XS1*(0.0938+0.00993+0.00304+0.00254+0.00174)/GenNum
        ratio2 = lum*XS2*(0.0938+0.00993+0.00304+0.00254+0.00174)/GenNum
        ratio3 = lum*XS3/GenNum1
        ratio4 = lum*XS4/GenNum2
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 22
        plot(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, pt_title, ecms, ratio1, ratio2, ratio3, ratio4, runNolow, runNoup, arrow_left, arrow_bottom, arrow_right, arrow_top)

if __name__ == '__main__':
    main()
