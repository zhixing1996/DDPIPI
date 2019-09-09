#!/usr/bin/env python
"""
Plot chi2 of D kinematic fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-5 Thu 00:04]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'inclusive MC')
    legend.AddEntry(h2, 'signal MC')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def chi2_KF_fill(t1, t2, entries1, entries2, h1, h2):
    for ientry1 in xrange(entries1):
        t1.GetEntry(ientry1)
        h1.Fill(t1.m_chi2_kf)
    for ientry2 in xrange(entries2):
        t2.GetEntry(ientry2)
        h2.Fill(t2.m_chi2_kf)

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

def plot(incMC_path, sigMC_path, leg_title, ecms):
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
    xmin = 0
    xmax = 100
    xbins = 100
    ytitle = "Events"
    xtitle = "#chi^{2}(K^{-}#pi^{+}#pi^{+})"
    h_incMC = TH1F('incMC', 'incMC', xbins, xmin, xmax)
    h_sigMC = TH1F('sigMC', 'sigMC', xbins, xmin, xmax)

    set_histo_style(h_incMC, h_sigMC, xtitle, ytitle)
    chi2_KF_fill(t_incMC, t_sigMC, entries_incMC, entries_sigMC, h_incMC, h_sigMC)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sigMC.Scale(h_incMC.GetEntries()/h_sigMC.GetEntries())
    h_incMC.Draw('ep')
    h_sigMC.Draw('samee')

    legend = TLegend(0.65, 0.6, 0.82, 0.8)
    set_legend(legend, h_incMC, h_sigMC, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/chi2_KF_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4360/incMC_hadrons_4360_raw.root'
    sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/signal/4360/sigMC_4360_raw.root'
    leg_title = '(a)'
    ecms = 4360
    plot(incMC_path, sigMC_path, leg_title, ecms)

    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4420/incMC_hadrons_4420_raw.root'
    sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/signal/4420/sigMC_4420_raw.root'
    leg_title = '(b)'
    ecms = 4420
    plot(incMC_path, sigMC_path, leg_title, ecms)

    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4600/incMC_hadrons_4600_raw.root'
    sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/signal/4600/sigMC_4600_raw.root'
    leg_title = '(c)'
    ecms = 4600
    plot(incMC_path, sigMC_path, leg_title, ecms)
