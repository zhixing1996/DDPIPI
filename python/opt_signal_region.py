#!/usr/bin/env python
"""
Optiomize signal region of recoiling mass of DPIPI
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-03 Tue 05:30]"

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
    h.GetXaxis().SetTitleOffset(1.3)
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

def cal_significance(t1, t2, entries1, entries2, M_D, N, step):
    ymax = 0
    NEntry = 0
    S_list = []
    print 'Start of sigMC...'
    for i in xrange(N):
        S = 0
        for j in xrange(int(entries1/100)):
            t1.GetEntry(j)
            if t1.m_chi2_kf > 10:
                continue
            if abs(t1.m_rm_Dpipi - M_D) < (step + i*step):
                S = S + 1
        S_list.append(S)
    B_list = []
    print 'Start of incMC...'
    for i in xrange(N):
        B = 0
        for j in xrange(entries2/150):
            t2.GetEntry(j)
            if t2.m_chi2_kf > 10:
                continue
            if abs(t2.m_rm_Dpipi - M_D) < (step + i*step):
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
    xmin = step
    xmax = N*step
    xtitle = "|RM(D^{+}#pi^{+}#pi^{-})-m_{D}|(GeV/c^{2})"
    ytitle = "#frac{S}{#sqrt{B}}"
    h_FOM = TH2F('h_FOM', 'FOM', N, xmin, xmax, N, 0, ymax + 70)
    set_histo_style(h_FOM, xtitle, ytitle)
    for i in xrange(N):
        h_FOM.Fill(step + i*step, Ratio_list[i])
    return h_FOM, NEntry, ymax

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(incMC_path, sigMC_path, pt_title, ecms):
    try:
        f_incMC = TFile(incMC_path)
        f_sigMC = TFile(sigMC_path)
        t_incMC = f_incMC.Get('save')
        t_sigMC = f_sigMC.Get('save')
        entries_incMC = t_incMC.GetEntries()
        entries_sigMC = t_sigMC.GetEntries()
        logging.info('inclusive MC entries :'+str(entries_incMC))
        logging.info('signal MC entries :'+str(entries_sigMC))
    except:
        logging.error(incMC_path+' or '+sigMC_path+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = 100
    M_Dplus = 1.86965
    step = (1.9 - M_Dplus)/xbins

    h_FOM, ientry, arrow_top = cal_significance(t_sigMC, t_incMC, entries_sigMC, entries_incMC, M_Dplus, xbins, step)
    h_FOM.Draw()
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    arrow_left = ientry*step + step
    arrow_right = ientry*step + step
    arrow_bottom = 0.0
    arrow = TArrow(arrow_left, arrow_bottom, arrow_right, arrow_top, 0.01,'>')
    set_arrow(arrow)
    arrow.Draw()

    pt = TPaveText(0.6, 0.8, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)

    mass_low = str(M_Dplus - (step + step*ientry))
    mass_up = str(M_Dplus + (step + step*ientry))
    range = 'Signal region of RM(D^{+}#pi^{+}#pi^{-}): [' + mass_low + ', ' + mass_up + '] GeV/c2'
    print range

    mbc.Update()
    mbc.SaveAs('./figs/opt_signal_region_'+str(ecms)+'.pdf')

def main():
    args = sys.argv[1:]
    energy = args[0]

    if int(energy) == 4360:
        incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4360/incMC_hadrons_4360_raw.root'
        sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/signal/4360/sigMC_4360_raw.root'
        pt_title = '(a)'
        ecms = 4360
        plot(incMC_path, sigMC_path, pt_title, ecms)

    if int(energy) == 4420:
        incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4420/incMC_hadrons_4420_raw.root'
        sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/signal/4420/sigMC_4420_raw.root'
        pt_title = '(b)'
        ecms = 4420
        plot(incMC_path, sigMC_path, pt_title, ecms)

    if int(energy) == 4600:
        incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4600/incMC_hadrons_4600_raw.root'
        sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/signal/4600/sigMC_4600_raw.root'
        pt_title = '(c)'
        ecms = 4600
        plot(incMC_path, sigMC_path, pt_title, ecms)

if __name__ == '__main__':
    main()
