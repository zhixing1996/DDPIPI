#!/usr/bin/env python
"""
Plot chi2 of D kinematic fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-05 Thu 00:04]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'X(3842)#pi^{+}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def chi2_KF_fill(t1, t2, entries1, entries2, h1, h2):
    for ientry1 in xrange(entries1):
        t1.GetEntry(ientry1)
        if t1.m_m_pipi > 0.28 and t1.m_rm_Dpipi > 1.8593 and t1.m_rm_Dpipi < 1.8800:
            h1.Fill(t1.m_chi2_kf)
    for ientry2 in xrange(entries2):
        t2.GetEntry(ientry2)
        if t2.m_m_pipi > 0.28 and t2.m_rm_Dpipi > 1.8593 and t2.m_rm_Dpipi < 1.8800:
            h2.Fill(t2.m_chi2_kf)

def set_histo_style(h1, h2, xtitle, ytitle, ymax):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitleOffset(1.4)
    h1.GetXaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetTitleOffset(1.5)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetXaxis().CenterTitle()
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetYaxis().CenterTitle()
    # h1.GetYaxis().SetRangeUser(0, int(ymax))
    h1.SetLineColor(1)
    h2.SetLineColor(2)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data_path, sigMC_path, leg_title, ecms, ymax):
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
        logging.error(data_path+' or '+sigMC_path+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 0
    xmax = 200
    xbins = 200
    ytitle = "Events"
    xtitle = "#chi^{2}(D^{+}D_{missing}#pi^{+}_{0}#pi^{-}_{0})"
    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    h_sigMC = TH1F('sigMC', 'sigMC', xbins, xmin, xmax)

    set_histo_style(h_data, h_sigMC, xtitle, ytitle, ymax)
    chi2_KF_fill(t_data, t_sigMC, entries_data, entries_sigMC, h_data, h_sigMC)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sigMC.Scale(h_data.GetEntries()/h_sigMC.GetEntries()/2)
    h_data.Draw('ep')
    h_sigMC.Draw('same')

    legend = TLegend(0.65, 0.6, 0.82, 0.8)
    set_legend(legend, h_data, h_sigMC, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/chi2_kf_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_signal.root'
    sigMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/sigMC_X_3842_4360_signal.root'
    leg_title = '(a)'
    ecms = 4360
    ymax = 1200
    plot(data_path, sigMC_path, leg_title, ecms, ymax)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_signal.root'
    sigMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/sigMC_X_3842_4420_signal.root'
    leg_title = '(b)'
    ecms = 4420
    ymax = 2200
    ymax = 1500
    plot(data_path, sigMC_path, leg_title, ecms, ymax)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_signal.root'
    sigMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/sigMC_X_3842_4600_signal.root'
    leg_title = '(c)'
    ecms = 4600
    ymax = 3000
    plot(data_path, sigMC_path, leg_title, ecms, ymax)
