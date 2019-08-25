#!/usr/bin/env python
"""
Plot recoiling mass of tagged D vs mass of Dpipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-25 Sun 22:36]"

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

def fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h.Fill(t.m_rm_D, t.m_m_Dpipi)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().CenterTitle()

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(signal, leg_title, ecms, max):
    try:
        f_signal = TFile(signal)
        t_signal = f_signal.Get('save')
        entries_signal = t_signal.GetEntries()
        logging.info('signal entries :'+str(entries_signal))
    except:
        logging.error(signal+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    min = 2.1
    bins = 40
    xtitle = 'RM(D^{+})(GeV/c^{2})'
    ytitle = 'M(D^{+}#pi^{+}#pi^{-})(GeV/c^{2})'
    h_rm_D_vs_m_Dpipi = TH2F('rm_D_vs_m_Dpipi', 'recoliling mass of D vs mass of Dpipi', bins, min, float(max), bins, min, float(max))

    set_histo_style(h_rm_D_vs_m_Dpipi, xtitle, ytitle)
    fill(t_signal, h_rm_D_vs_m_Dpipi)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_rm_D_vs_m_Dpipi.Draw()

    legend = TLegend(0.25, 0.2, 0.2, 0.45)
    set_legend(legend, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_D_vs_m_Dpipi_'+str(ecms)+'_sigMC.pdf')

if __name__ == '__main__':
    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected_signal.root'
    leg_title = '(c)'
    ecms = 4360
    max = 2.55
    plot(signal, leg_title, ecms, max)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected_signal.root'
    leg_title = '(c)'
    ecms = 4420
    max = 2.6
    plot(signal, leg_title, ecms, max)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected_signal.root'
    leg_title = '(c)'
    ecms = 4600
    max = 2.8
    plot(signal, leg_title, ecms, max)
