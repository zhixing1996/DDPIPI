#!/usr/bin/env python
"""
Plot recoiling mass of tagged D
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-22 Thu 15:32]"

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
    legend.AddEntry(h2, 'data: RM(D#pi#pi) sideband')
    legend.AddEntry(h3, 'PHSP')
    legend.AddEntry(h4, 'signal MC')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_Dpipi_fill(t1, t2, t3, t4, h1, h2, h3, h4):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        h1.Fill(t1.m_rm_D)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        h2.Fill(t2.m_rm_D)
    for ientry3 in xrange(t3.GetEntries()):
        t3.GetEntry(ientry3)
        h3.Fill(t3.m_rm_D)
    for ientry4 in xrange(t4.GetEntries()):
        t4.GetEntry(ientry4)
        h4.Fill(t4.m_rm_D)

def set_histo_style(h1, h2, h3, h4, xtitle, ytitle, ymax):
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
    h1.GetYaxis().SetRangeUser(0, int(ymax))
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

def plot(data_path, data_sideband_path, bkgMC_path, sigMC_path, leg_title, ecms, scale1, scale2, scale3, ymax, xmax):
    try:
        f_data = TFile(data_path)
        f_data_sideband = TFile(data_sideband_path)
        f_bkgMC = TFile(bkgMC_path)
        f_sigMC = TFile(sigMC_path)
        t_data = f_data.Get('save')
        t_data_sideband = f_data_sideband.Get('save')
        t_bkgMC = f_bkgMC.Get('save')
        t_sigMC = f_sigMC.Get('save')
        entries_data = t_data.GetEntries()
        entries_data_sideband = t_data_sideband.GetEntries()
        entries_bkgMC = t_bkgMC.GetEntries()
        entries_sigMC = t_sigMC.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('data sideband entries :'+str(entries_data_sideband))
        logging.info('background MC entries :'+str(entries_bkgMC))
        logging.info('signal MC entries :'+str(entries_sigMC))
    except:
        logging.error(data_path+' or '+sigMC_path+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 2.1
    xbins = 25
    ytitle = 'Events'
    xtitle = 'RM(D^{+}) (GeV/c^{2})'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_data_sideband = TH1F('data_sideband', 'data sideband', xbins, xmin, float(xmax))
    h_bkgMC = TH1F('bkgMC', 'background MC', xbins, xmin, float(xmax))
    h_sigMC = TH1F('sigMC', 'signal MC', xbins, xmin, float(xmax))

    set_histo_style(h_data, h_data_sideband, h_bkgMC, h_sigMC, xtitle, ytitle, ymax)
    rm_Dpipi_fill(t_data, t_data_sideband, t_bkgMC, t_sigMC, h_data, h_data_sideband, h_bkgMC, h_sigMC)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_data_sideband.Scale(float(scale1))
    h_bkgMC.Scale(float(scale2))
    h_sigMC.Scale(float(scale3))
    h_data.Draw('ep')
    h_data_sideband.Draw('samee')
    h_bkgMC.Draw('samee')
    h_sigMC.Draw('samee')

    legend = TLegend(0.25, 0.6, 0.42, 0.4)
    set_legend(legend, h_data, h_data_sideband, h_bkgMC, h_sigMC, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_D_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected_signal.root'
    data_sideband_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected_sideband.root'
    bkgMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/PHSP/4360/bkgMC_PHSP_4360_selected.root'
    sigMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected.root'
    leg_title = '(a)'
    ecms = 4360
    scale1 = 0.25
    scale2 = 0.0014
    scale3 = 0.00035
    xmax = 2.5
    ymax = 500
    plot(data_path, data_sideband_path, bkgMC_path, sigMC_path, leg_title, ecms, scale1, scale2, scale3, ymax, xmax)

    data_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected_signal.root'
    data_sideband_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected_sideband.root'
    bkgMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/PHSP/4420/bkgMC_PHSP_4420_selected.root'
    sigMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected.root'
    leg_title = '(b)'
    ecms = 4420
    scale1 = 0.25
    scale2 = 0.0014
    scale3 = 0.00035
    xmax = 2.6
    ymax = 1700
    plot(data_path, data_sideband_path, bkgMC_path, sigMC_path, leg_title, ecms, scale1, scale2, scale3, ymax, xmax)

    data_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected_signal.root'
    data_sideband_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected_sideband.root'
    bkgMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/PHSP/4600/bkgMC_PHSP_4600_selected.root'
    sigMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected.root'
    leg_title = '(c)'
    ecms = 4600
    scale1 = 0.25
    scale2 = 0.0014
    scale3 = 0.00035
    xmax = 2.75
    ymax = 600
    plot(data_path, data_sideband_path, bkgMC_path, sigMC_path, leg_title, ecms, scale1, scale2, scale3, ymax, xmax)
