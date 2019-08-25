#!/usr/bin/env python
"""
Plot recoiling mass of tagged D and mass of Dpipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-25 Sun 21:43]"

import ROOT
from ROOT import TCanvas, gStyle, TTree
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def set_legend(legend, h1, h2, title, ecms):
    legend.AddEntry(h1, str(ecms)+' MeV: RM(D)')
    legend.AddEntry(h2, str(ecms)+' MeV: M(D^{+}#pi^{+}#pi^{-})')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def fill(t1, h1, h2):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        h1.Fill(t1.m_rm_D)
        h2.Fill(t1.m_m_Dpipi)

def set_histo_style(h1, h2, ytitle, ymax):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitleOffset(1.0)
    h1.GetXaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetTitleOffset(1.0)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetYaxis().CenterTitle()
    h1.GetYaxis().SetRangeUser(0, int(ymax))
    h1.SetLineColor(1)
    h2.SetLineColor(2)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(signal, leg_title, ecms, ymax, xmax):
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
    xmin = 2.1
    xbins = 40
    ytitle = 'Events'
    h_rm_D = TH1F('rm_D', 'recoliling mass of D', xbins, xmin, float(xmax))
    h_m_Dpipi = TH1F('m_Dpipi', 'mass of Dpipi', xbins, xmin, float(xmax))

    set_histo_style(h_rm_D, h_m_Dpipi, ytitle, ymax)
    fill(t_signal, h_rm_D, h_m_Dpipi)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_rm_D.Draw('e')
    h_m_Dpipi.Draw('same')

    legend = TLegend(0.25, 0.6, 0.42, 0.4)
    set_legend(legend, h_rm_D, h_m_Dpipi, leg_title, ecms)
    legend.Draw()

    mbc.SaveAs('./figs/rm_D_or_m_Dpipi_'+str(ecms)+'_sigMC.pdf')

if __name__ == '__main__':
    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected_signal.root'
    leg_title = '(b)'
    ecms = 4360
    xmax = 2.5
    ymax = 60000
    plot(signal, leg_title, ecms, ymax, xmax)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected_signal.root'
    leg_title = '(b)'
    ecms = 4420
    xmax = 2.6
    ymax = 60000
    plot(signal, leg_title, ecms, ymax, xmax)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected_signal.root'
    leg_title = '(b)'
    ecms = 4600
    xmax = 2.75
    ymax = 57000
    plot(signal, leg_title, ecms, ymax, xmax)
