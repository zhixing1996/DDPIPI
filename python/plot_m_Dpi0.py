#!/usr/bin/env python
"""
Plot invariant mass of tagged D and pi0
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-30 Mon 08:35]"

import ROOT
from ROOT import TCanvas, gStyle, TTree
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
import math
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'X(3842)#pi^{+}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def m_Dpi0_fill(t1, t2, h1, h2, chi2_cut):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        if t1.m_m_pipi > 0.28 and t1.m_chi2_kf < chi2_cut and t1.m_rm_Dpipi > 1.855 and t1.m_rm_Dpipi < 1.885:
            h1.Fill(t1.m_m_Dpi0)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        if t2.m_m_pipi > 0.28 and t2.m_chi2_kf < chi2_cut and t2.m_rm_Dpipi > 1.855 and t2.m_rm_Dpipi < 1.885:
            h2.Fill(t2.m_m_Dpi0)

def set_histo_style(h1, h2, xtitle, ytitle):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitleOffset(1.3)
    h1.GetXaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetTitleOffset(1.5)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetXaxis().CenterTitle()
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetYaxis().CenterTitle()
    h1.SetLineColor(1)
    h2.SetLineColor(2)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data_path, sigMC_path, leg_title, ecms, scale, xmax, chi2_cut):
    try:
        f_data = TFile(data_path)
        f_sigMC = TFile(sigMC_path)
        t_data = f_data.Get('save')
        t_sigMC = f_sigMC.Get('save')
        entries_data = t_data.GetEntries()
        entries_sigMC = t_sigMC.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('signal MC(X(3842)) entries :'+str(entries_sigMC))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 2.0
    xbins = 100
    ytitle = 'Events'
    xtitle = 'M(D_{tag}#pi^{0})(GeV/c^{2})'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_sigMC = TH1F('sigMC', 'signal MC: X(3842)', xbins, xmin, float(xmax))

    set_histo_style(h_data, h_sigMC, xtitle, ytitle)
    m_Dpi0_fill(t_data, t_sigMC, h_data, h_sigMC, chi2_cut)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sigMC.Scale(h_data.GetEntries()/h_sigMC.GetEntries()/1.4)
    h_data.Draw('ep')
    h_sigMC.Draw('samee')

    legend = TLegend(0.55, 0.6, 0.8, 0.75)
    set_legend(legend, h_data, h_sigMC, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/m_Dpi0_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_signal.root'
    sigMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/sigMC_X_3842_4360_signal.root'
    leg_title = '(a)'
    ecms = 4360
    scale = 0.00065
    xmax = 3.
    chi2_cut = 46
    plot(data_path, sigMC_path, leg_title, ecms, scale, xmax, chi2_cut)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_signal.root'
    sigMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/sigMC_X_3842_4420_signal.root'
    leg_title = '(b)'
    ecms = 4420
    scale = 0.0015
    xmax = 3.
    chi2_cut = 42
    plot(data_path, sigMC_path, leg_title, ecms, scale, xmax, chi2_cut)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_signal.root'
    sigMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/sigMC_X_3842_4600_signal.root'
    leg_title = '(c)'
    ecms = 4600
    scale = 0.0009
    xmax = 3.
    chi2_cut = 25
    plot(data_path, sigMC_path, leg_title, ecms, scale, xmax, chi2_cut)
