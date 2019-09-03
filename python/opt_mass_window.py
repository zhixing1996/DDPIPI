#!/usr/bin/env python
"""
Optiomize mass window of recoiling mass of DPIPI
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
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetMarkerStyle(8)
    h.SetMarkerSize(0.65)
    h.SetLineColor(1)

def cal_significance(t1, t2, entries1, entries2, h, M_D, N, step):
    ymax = 0
    S_list = []
    for i in xrange(entries1):
        t1.GetEntry(i)
        S = 0
        for j in xrange(N):
            if abs(t1.m_rm_Dpipi - M_D) < (step + j*step):
                S = S + 1
        S_list.append(S)
    SB_list = []
    for i in xrange(entries2):
        t2.GetEntry(i)
        SB = 0
        for j in xrange(N):
            if abs(t2.m_rm_Dpipi - M_D) < (step + j*step):
                SB = SB + 1
        SB_list.append(SB)
    for i in xrange(N):
        if SB_list[i] == 0:
            significance = 0
        else:
            significance = S_list[i]/math.sqrt(SB_list[i])
            Ratio_list.append(significance)
        if significance > ymax:
            ymax = significance
            NEntry = i
    xmin = step
    xmax = N*step
    xtitle = "Mass Window of RM(D^{-}#pi^{+}#pi^{-})"
    ytitle = "frac{S}{#sqrt{S+B}}"
    h_FOM = TH2F('h_FOM', 'FOM', N, xmin, xmax, N, 0, ymax + 100)
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

def plot(data_path, sigMC_path, leg_title, ecms, arrow_bottom, arrow_top):
    try:
        f_data = TFile(data_path)
        f_sigMC = TFile(sigMC_path)
        t_data = f_data.Get('save')
        t_sigMC = f_sigMC.Get('save')
        entries_data = t_data.GetEntries()
        entries_sigMC = t_sigMC.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('signal MC entries :'+str(entries_sigMC))
    except:
        logging.error(data_path+' or '+sigMC_path+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = 100
    M_Dplus = 1.8696
    step = (1.9 - M_Dplus)/xbins

    h_FOM, NEntry, arrow_top = cal_significance(t_data, t_sigMC, entries_data, entries_sigMC, M_Dplus, xbins, step)
    h_FOM.Draw()
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    arrow_left = NEntry*step + step
    arrow_right = NEntry*step + step
    arrow_bottom = 0.0
    arrow = TArrow(arrow_left, arrow_bottom, arrow_right, arrow_top, 0.01,'>')
    set_arrow(arrow)
    arrow.Draw()

    pt = TPaveText(0.6, 0.8, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()

    mass_low = str(M_Dplus - (step + step*NEntry))
    mass_up = str(M_Dplus + (step + step*NEntry))
    range = 'Mass window of RM(D^{+}#pi^{+}#pi^{-}): [' + mass_low + ', ' + mass_up + ']'
    pt.AddText(range)

    mbc.Update()
    mbc.SaveAs('./figs/opt_mass_window_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = ''
    sigMC_path = ''
    leg_title = '(a)'
    ecms = 4360
    plot(data_path, sigMC_path, leg_title, ecms)

    data_path = ''
    sigMC_path = ''
    leg_title = '(b)'
    ecms = 4420
    plot(data_path, sigMC_path, leg_title, ecms)

    data_path = ''
    sigMC_path = ''
    leg_title = '(c)'
    ecms = 4600
    plot(data_path, sigMC_path, leg_title, ecms)