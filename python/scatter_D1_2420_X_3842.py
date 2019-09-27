#!/usr/bin/env python
"""
Plot recoiling mass of tagged D vs recoiling mass of pipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-25 Wed 09:39]"

import ROOT
from ROOT import TCanvas, gStyle, TTree
from ROOT import TFile, TH2F, TLegend, TArrow
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'D_{1}(2420)D')
    legend.AddEntry(h2, 'X(3842)#pi^{+}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def fill(t1, t2, h1, h2, cut_chi2):
    for ientry1 in xrange(int(t1.GetEntries()/2)):
        t1.GetEntry(ientry1)
        if t1.m_m_pipi > 0.28 and t1.m_chi2_kf < chi2_cut and t1.m_rm_Dpipi > 1.857 and t1.m_rm_Dpipi < 1.882:
            h1.Fill(t1.m_rm_D, t1.m_rm_pipi)
    for ientry2 in xrange(int(t2.GetEntries()/4)):
        t2.GetEntry(ientry2)
        if t2.m_m_pipi > 0.28 and t2.m_chi2_kf < chi2_cut and t2.m_rm_Dpipi > 1.857 and t2.m_rm_Dpipi < 1.882:
            h2.Fill(t2.m_rm_D, t2.m_rm_pipi)

def set_histo_style(h1, h2, xtitle, ytitle):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitleOffset(1.3)
    h1.GetXaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetTitleOffset(1.3)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetXaxis().CenterTitle()
    h1.GetYaxis().CenterTitle()
    h1.SetLineColor(1)
    h2.SetLineColor(2)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(sigMC1, sigMC2, leg_title, ecms, x_min, x_max, y_min, y_max, chi2_cut):
    try:
        f_sigMC1 = TFile(sigMC1)
        f_sigMC2 = TFile(sigMC2)
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('sigMC1 entries :'+str(entries_sigMC1))
        logging.info('sigMC2 entries :'+str(entries_sigMC2))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    bins = 40
    xtitle = 'RM(D^{+})(GeV/c^{2})'
    ytitle = 'RM(#pi^{+}#pi^{-})(GeV/c^{2})'
    h_sigMC1 = TH2F('h_sigMC1', 'recoliling mass of D vs recoiling mass of pipi', bins, x_min, x_max, bins, y_min, y_max)
    h_sigMC2 = TH2F('h_sigMC2', 'recoliling mass of D vs recoiling mass of pipi', bins, x_min, x_max, bins, y_min, y_max)

    set_histo_style(h_sigMC1, h_sigMC2, xtitle, ytitle)
    fill(t_sigMC1, t_sigMC2, h_sigMC1, h_sigMC2, chi2_cut)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sigMC1.Draw('box')
    h_sigMC2.Draw('box same')

    legend = TLegend(0.55, 0.7, 0.8, 0.85)
    set_legend(legend, h_sigMC1, h_sigMC2, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/scatter_D1_2420_X_3842_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    sigMC1 = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_signal.root'
    sigMC2 = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/sigMC_X_3842_4360_signal.root'
    leg_title = '(a)'
    ecms = 4360
    x_min = 2.1
    x_max = 2.55
    y_min = 3.7
    y_max = 4.1
    chi2_cut = 45
    plot(sigMC1, sigMC2, leg_title, ecms, x_min, x_max, y_min, y_max, chi2_cut)

    sigMC1 = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_signal.root'
    sigMC2 = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/sigMC_X_3842_4420_signal.root'
    leg_title = '(b)'
    ecms = 4420
    x_min = 2.1
    x_max = 2.6
    y_min = 3.7
    y_max = 4.2
    chi2_cut = 46
    plot(sigMC1, sigMC2, leg_title, ecms, x_min, x_max, y_min, y_max, chi2_cut)

    sigMC1 = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_signal.root'
    sigMC2 = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/sigMC_X_3842_4600_signal.root'
    leg_title = '(c)'
    ecms = 4600
    x_min = 2.1
    x_max = 2.8
    y_min = 3.7
    y_max = 4.35
    chi2_cut = 25
    plot(sigMC1, sigMC2, leg_title, ecms, x_min, x_max, y_min, y_max, chi2_cut)
