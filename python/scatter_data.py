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

def set_legend(legend, title):
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def fill(t, h, cut_chi2):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if t.m_m_pipi > 0.28 and t.m_chi2_kf < chi2_cut and t.m_rm_Dpipi > 1.855 and t.m_rm_Dpipi < 1.885:
            h.Fill(t.m_rm_D, t.m_rm_pipi)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetTitleOffset(1.3)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.3)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().CenterTitle()
    h.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data, leg_title, ecms, x_min, x_max, y_min, y_max, chi2_cut):
    try:
        f_data = TFile(data)
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    bins = 40
    xtitle = 'RM(D^{+})(GeV/c^{2})'
    ytitle = 'RM(#pi^{+}#pi^{-})(GeV/c^{2})'
    h_data = TH2F('h_sigMC1', 'recoliling mass of D vs recoiling mass of pipi', bins, x_min, x_max, bins, y_min, y_max)

    set_histo_style(h_data, xtitle, ytitle)
    fill(t_data, h_data, chi2_cut)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_data.Draw()

    legend = TLegend(0.55, 0.7, 0.8, 0.75)
    set_legend(legend, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/scatter_data_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_signal.root'
    leg_title = '(a)'
    ecms = 4360
    x_min = 2.1
    x_max = 2.55
    y_min = 3.7
    y_max = 4.1
    chi2_cut = 999
    plot(data, leg_title, ecms, x_min, x_max, y_min, y_max, chi2_cut)

    data = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_signal.root'
    leg_title = '(b)'
    ecms = 4420
    x_min = 2.1
    x_max = 2.6
    y_min = 3.7
    y_max = 4.2
    chi2_cut = 47
    plot(data, leg_title, ecms, x_min, x_max, y_min, y_max, chi2_cut)

    data = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_signal.root'
    leg_title = '(c)'
    ecms = 4600
    x_min = 2.1
    x_max = 2.8
    y_min = 3.7
    y_max = 4.35
    chi2_cut = 999
    plot(data, leg_title, ecms, x_min, x_max, y_min, y_max, chi2_cut)
