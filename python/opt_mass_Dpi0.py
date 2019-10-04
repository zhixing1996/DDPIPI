#!/usr/bin/env python
"""
Optiomize mass window of tagged D and pi0
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-30 Mon 09:05]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH2F, TPaveText, TArrow
import sys, os
import logging
import math
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
    h.GetYaxis().SetTitleOffset(1.6)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetMarkerStyle(8)
    h.SetMarkerSize(0.65)
    h.SetLineColor(1)

def cal_significance(t1, t2, t3, entries1, entries2, entries3, N, step, ratio1, ratio2, chi2_cut):
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
            if t1.m_m_Dpi0 > (2.0 + step + i*step) and t1.m_m_pipi > 0.28 and t1.m_rm_Dpipi > 1.857 and t1.m_rm_Dpipi < 1.882 and t1.m_chi2_kf < chi2_cut:
                S1 = S1 + 1
        S1_list.append(S1)
    print 'Start of sigMC2...'
    for i in xrange(N):
        S2 = 0
        for j in xrange(int(entries2*ratio2)):
            t2.GetEntry(j)
            if t2.m_m_Dpi0 > (2.0 + step + i*step) and t2.m_m_pipi > 0.28 and t2.m_rm_Dpipi > 1.857 and t2.m_rm_Dpipi < 1.882 and t2.m_chi2_kf < chi2_cut:
                S2 = S2 + 1
        S2_list.append(S2)
    for i in xrange(N):
        S_list.append(S1_list[i]+S2_list[i])
    B_list = []
    print 'Start of incMC...'
    for i in xrange(N):
        B = 0
        for j in xrange(entries3/5):
            t3.GetEntry(j)
            if t3.m_m_Dpi0 > (2.0 + step + i*step) and t3.m_m_pipi > 0.28 and t3.m_rm_Dpipi > 1.857 and t3.m_rm_Dpipi < 1.882 and t3.m_chi2_kf < chi2_cut:
                B = B + 1
        B_list.append(B)
    Ratio_list = []
    for i in xrange(N):
        if B_list[i] == 0:
            significance = 0
        else:
            significance = S_list[i]/math.sqrt(B_list[i])
        Ratio_list.append(significance)
        if significance > ymax:
            ymax = significance
            NEntry = i
    xmin = 2.0 + step
    xmax = 2.0 + step + N*step
    xtitle = 'M(D_{tag}#pi^{0})'
    ytitle = '#frac{S}{#sqrt{S+B}}'
    h_FOM = TH2F('h_FOM', 'FOM', N, xmin, xmax, N, 0, ymax + 40)
    set_histo_style(h_FOM, xtitle, ytitle)
    for i in xrange(N):
        h_FOM.Fill(2.0 + step + i*step, Ratio_list[i])
    return h_FOM, NEntry, ymax

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(incMC_path, sigMC1_path, sigMC2_path, pt_title, ecms, lum, XS1, XS2, GenNum, chi2_cut):
    try:
        f_incMC = TFile(incMC_path)
        f_sigMC1 = TFile(sigMC1_path)
        f_sigMC2 = TFile(sigMC2_path)
        t_incMC = f_incMC.Get('save')
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        entries_incMC = t_incMC.GetEntries()
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('inclusive MC entries :'+str(entries_incMC))
        logging.info('D1(2420) signal MC entries :'+str(entries_sigMC1))
        logging.info('psi(3770) signal MC entries :'+str(entries_sigMC2))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = 100
    step = 0.5/xbins
    ratio1 = lum*XS1/GenNum
    ratio2 = lum*XS2/GenNum

    h_FOM, ientry, arrow_top = cal_significance(t_sigMC1, t_sigMC2, t_incMC, entries_sigMC1, entries_sigMC2, entries_incMC, xbins, step, ratio1, ratio2, chi2_cut)
    h_FOM.Draw()
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    arrow_left = 2.0 + ientry*step + step
    arrow_right = 2.0 + ientry*step + step
    arrow_bottom = 0.0
    arrow = TArrow(arrow_left, arrow_bottom, arrow_right, arrow_top, 0.01,'>')
    set_arrow(arrow)
    arrow.Draw()

    pt = TPaveText(0.6, 0.8, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)

    range = 'invariant mass of D^{tag}#pi^{0} should be larger than ' + str(arrow_right)
    print range

    mbc.Update()
    mbc.SaveAs('./figs/opt_mass_Dpi0_'+str(ecms)+'.pdf')

def main():
    args = sys.argv[1:]
    energy = args[0]

    if int(energy) == 4360:
        incMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/hadrons/4360/incMC_hadrons_4360_signal.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_signal.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_signal.root'
        pt_title = '(a)'
        ecms = 4360
        lum = 539.84
        XS1 = 41.8
        XS2 = 17.3
        GenNum = 500000
        chi2_cut = 46
        plot(incMC_path, sigMC1_path, sigMC2_path, pt_title, ecms, lum, XS1, XS2, GenNum, chi2_cut)

    if int(energy) == 4420:
        incMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/hadrons/4420/incMC_hadrons_4420_signal.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_signal.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_signal.root'
        pt_title = '(b)'
        ecms = 4420
        lum = 1073.56
        XS1 = 65.4
        XS2 = 23.8
        GenNum = 500000
        chi2_cut = 42
        plot(incMC_path, sigMC1_path, sigMC2_path, pt_title, ecms, lum, XS1, XS2, GenNum, chi2_cut)

    if int(energy) == 4600:
        incMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/hadrons/4600/incMC_hadrons_4600_signal.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_signal.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_signal.root'
        pt_title = '(c)'
        ecms = 4600
        lum = 566.93
        XS1 = 27.7
        XS2 = 7.2
        GenNum = 500000
        chi2_cut = 25
        plot(incMC_path, sigMC1_path, sigMC2_path, pt_title, ecms, lum, XS1, XS2, GenNum, chi2_cut)

if __name__ == '__main__':
    main()
