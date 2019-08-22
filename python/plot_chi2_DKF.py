#!/usr/bin/env python
"""
Plot chi2 of D kinematic fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-20 Tue 15:37]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TArrow
from tools import set_root_style
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def set_arrow(arrow):
    arrow.SetLineWidth(0)
    arrow.SetLineColor(2)
    arrow.SetFillColor(2)

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'signal MC')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def chi2_KF_fill(t1, t2, entries1, entries2, h1, h2):
    for ientry1 in xrange(entries1):
        t1.GetEntry(ientry1)
        h1.Fill(t1.chi2_kf)
    for ientry2 in xrange(entries2):
        t2.GetEntry(ientry2)
        h2.Fill(t2.chi2_kf)

def set_histo_style(h1, h2, xtitle, ytitle):
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

def plot(data_path, sigMC_path, leg_title, ecms, arrow_bottom, arrow_top):
    try:
        f_data = TFile(data_path)
        f_sigMC = TFile(sigMC_path)
        t_data = f_data.Get('STD')
        t_sigMC = f_sigMC.Get('STD')
        entries_data = t_data.GetEntries()
        entries_sigMC = t_sigMC.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('signal MC entries :'+str(entries_sigMC))
    except:
        logging.error(data_path+' or '+sigMC_path+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 0
    xmax = 100
    xbins = 100
    ytitle = "Events"
    xtitle = "#chi^{2}(K^{-}#pi^{+}#pi^{+})"
    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    h_sigMC = TH1F('sigMC', 'sigMC', xbins, xmin, xmax)

    set_histo_style(h_data, h_sigMC, xtitle, ytitle)
    chi2_KF_fill(t_data, t_sigMC, entries_data, entries_sigMC, h_data, h_sigMC)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sigMC.Scale(h_data.GetEntries()/h_sigMC.GetEntries())
    h_data.Draw('ep')
    h_sigMC.Draw('samee')

    legend = TLegend(0.65, 0.6, 0.82, 0.8)
    set_legend(legend, h_data, h_sigMC, leg_title)
    legend.Draw()

    arrow = TArrow(20, arrow_bottom, 20, arrow_top, 0.02,'<|')
    set_arrow(arrow)
    arrow.Draw()

    mbc.SaveAs('./figs/chi2_KF_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path_4360 = '/scratchfs/bes/jingmq/bes/DDPIPI/v0.1/data/4360/data_4360.root'
    sigMC_path_4360 = '/scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/D1_2420/4360/rootfile/sigMC_D1_2420_4360.root'
    leg_title_4360 = '(a)'
    ecms_4360 = 4360
    arrow_bottom_4360 = 2500
    arrow_top_4360 = 20000
    plot(data_path_4360, sigMC_path_4360, leg_title_4360, ecms_4360, arrow_bottom_4360, arrow_top_4360)

    data_path_4420 = '/scratchfs/bes/jingmq/bes/DDPIPI/v0.1/data/4420/data_4420.root'
    sigMC_path_4420 = '/scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/D1_2420/4420/rootfile/sigMC_D1_2420_4420.root'
    leg_title_4420 = '(b)'
    ecms_4420 = 4420
    arrow_bottom_4420 = 5000
    arrow_top_4420 = 50000
    plot(data_path_4420, sigMC_path_4420, leg_title_4420, ecms_4420, arrow_bottom_4420, arrow_top_4420)

    data_path_4600 = '/scratchfs/bes/jingmq/bes/DDPIPI/v0.1/data/4600/data_4600.root'
    sigMC_path_4600 = '/scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/D1_2420/4600/rootfile/sigMC_D1_2420_4600.root'
    leg_title_4600 = '(c)'
    ecms_4600 = 4600
    arrow_bottom_4600 = 2500
    arrow_top_4600 = 20000
    plot(data_path_4600, sigMC_path_4600, leg_title_4600, ecms_4600, arrow_bottom_4600, arrow_top_4600)
