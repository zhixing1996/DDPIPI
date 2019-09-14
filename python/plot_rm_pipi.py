#!/usr/bin/env python
"""
Plot recoiling mass of selected piplus and piminus
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-11 Wed 19:35]"

import ROOT
from ROOT import TCanvas, gStyle, TTree
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def set_legend(legend, h1, h2, h3, h4, title):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'data: RM(D^{+}#pi^{+}#pi^{-}) sideband')
    legend.AddEntry(h3, 'D_{1}(2420)D')
    legend.AddEntry(h4, '#psi(3770)#pi^{+}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_pipi_fill(t1, t2, t3, t4, h1, h2, h3, h4):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        if t1.m_m_pipi > 0.28:
            h1.Fill(t1.m_rm_pipi)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        if t2.m_m_pipi > 0.28 and t2.m_rm_pipi > 3.75:
            h2.Fill(t2.m_rm_pipi)
    for ientry3 in xrange(t3.GetEntries()):
        t3.GetEntry(ientry3)
        if t3.m_m_pipi > 0.28:
            h3.Fill(t3.m_rm_pipi)
    for ientry4 in xrange(t4.GetEntries()):
        t4.GetEntry(ientry4)
        if t4.m_m_pipi > 0.28:
            h4.Fill(t4.m_rm_pipi)

def set_histo_style(h1, h2, h3, h4, xtitle, ytitle):
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
    h1.GetYaxis().SetTitleOffset(1.2)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetXaxis().CenterTitle()
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetYaxis().CenterTitle()
    h1.SetLineColor(1)
    h2.SetLineColor(2)
    h3.SetLineColor(3)
    h4.SetLineColor(4)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data_path, data_sideband_path, sigMC1_path, sigMC2_path, leg_title, ecms, scale, scale1, scale2, xmax):
    try:
        f_data = TFile(data_path)
        f_data_sideband = TFile(data_sideband_path)
        f_sigMC1 = TFile(sigMC1_path)
        f_sigMC2 = TFile(sigMC2_path)
        t_data = f_data.Get('save')
        t_data_sideband = f_data_sideband.Get('save')
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        entries_data = t_data.GetEntries()
        entries_data_sideband = t_data_sideband.GetEntries()
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('data sideband entries :'+str(entries_data_sideband))
        logging.info('signal MC(D1(2420)) entries :'+str(entries_sigMC1))
        logging.info('signal MC(psi(3770)) entries :'+str(entries_sigMC2))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 3.7
    xbins = 40
    ytitle = 'Events'
    xtitle = 'RM(#pi^{+}#pi^{-})(GeV/c^{2})'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_data_sideband = TH1F('data_sideband', 'data sideband', xbins, xmin, float(xmax))
    h_sigMC1 = TH1F('sigMC1', 'signal MC: D1(2420)', xbins, xmin, float(xmax))
    h_sigMC2 = TH1F('sigMC2', 'signal MC: psi(3770)', xbins, xmin, float(xmax))

    set_histo_style(h_data, h_data_sideband, h_sigMC1, h_sigMC2, xtitle, ytitle)
    rm_pipi_fill(t_data, t_data_sideband, t_sigMC1, t_sigMC2, h_data, h_data_sideband, h_sigMC1, h_sigMC2)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_data_sideband.Scale(scale)
    h_sigMC1.Scale(scale1)
    h_sigMC2.Scale(scale2)
    h_data.Draw('ep')
    h_data_sideband.Draw('samee')
    h_sigMC1.Draw('samee')
    h_sigMC2.Draw('samee')

    legend = TLegend(0.5, 0.6, 0.75, 0.85)
    set_legend(legend, h_data, h_data_sideband, h_sigMC1, h_sigMC2, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_pipi_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4360/data_4360_signal.root'
    data_sideband_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4360/data_4360_sideband.root'
    sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_signal.root'
    sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_signal.root'
    leg_title = '(a)'
    ecms = 4360
    scale = 0.5
    scale1 = 0.00625
    scale2 = 0.00625
    xmax = 4.1
    plot(data_path, data_sideband_path, sigMC1_path, sigMC2_path, leg_title, ecms, scale, scale1, scale2, xmax)

    data_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4420/data_4420_signal.root'
    data_sideband_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4420/data_4420_sideband.root'
    sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_signal.root'
    sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_signal.root'
    leg_title = '(b)'
    ecms = 4420
    scale = 0.5
    scale1 = 0.00625
    scale2 = 0.00625
    xmax = 4.1
    plot(data_path, data_sideband_path, sigMC1_path, sigMC2_path, leg_title, ecms, scale, scale1, scale2, xmax)

    data_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4600/data_4600_signal.root'
    data_sideband_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4600/data_4600_sideband.root'
    sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_signal.root'
    sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_signal.root'
    leg_title = '(c)'
    ecms = 4600
    scale = 0.5
    scale1 = 0.00625
    scale2 = 0.00325
    xmax = 4.35
    plot(data_path, data_sideband_path, sigMC1_path, sigMC2_path, leg_title, ecms, scale, scale1, scale2, xmax)
