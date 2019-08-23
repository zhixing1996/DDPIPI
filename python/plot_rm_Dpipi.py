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

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'signal MC')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_Dpipi_fill(t1, t2, entries1, entries2, h1, h2):
    for ientry1 in xrange(entries1):
        t1.GetEntry(ientry1)
        h1.Fill(t1.m_rm_Dpipi)
    for ientry2 in xrange(entries2):
        t2.GetEntry(ientry2)
        h2.Fill(t2.m_rm_Dpipi)

def set_histo_style(h1, h2, xtitle, ytitle, ymax):
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

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data_path, sigMC_path, leg_title, ecms, scale, ymax):
    try:
        f_data = TFile(data_path)
        f_sigMC = TFile(sigMC_path)
        t_data = f_data.Get('save')
        t_sigMC = f_sigMC.Get('save')
        entries_data = t_data.GetEntries()
        entries_sigMC = t_sigMC.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('signal MC entries :'+str(entries_sigMC))
    except:
        logging.error(data_path+' or '+sigMC_path+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 1.7
    xmax = 2.2
    xbins = 100
    ytitle = 'Events'
    xtitle = 'RM(D^{+}#pi^{+}#pi^{-}) (GeV/c^{2})'
    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    h_sigMC = TH1F('sigMC', 'sigMC', xbins, xmin, xmax)

    set_histo_style(h_data, h_sigMC, xtitle, ytitle, ymax)
    rm_Dpipi_fill(t_data, t_sigMC, entries_data, entries_sigMC, h_data, h_sigMC)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sigMC.Scale(float(scale))
    h_data.Draw('ep')
    h_sigMC.Draw('samee')

    legend = TLegend(0.65, 0.6, 0.82, 0.8)
    set_legend(legend, h_data, h_sigMC, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_Dpipi_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected.root'
    sigMC_path_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected.root'
    leg_title_4360 = '(a)'
    ecms_4360 = 4360
    scale_4360 = 0.003
    ymax_4360 = 1100
    plot(data_path_4360, sigMC_path_4360, leg_title_4360, ecms_4360, scale_4360, ymax_4360)

    data_path_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected.root'
    sigMC_path_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected.root'
    leg_title_4420 = '(b)'
    ecms_4420 = 4420
    scale_4420 = 0.005
    ymax_4420 = 2600
    plot(data_path_4420, sigMC_path_4420, leg_title_4420, ecms_4420, scale_4420, ymax_4420)

    data_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected.root'
    sigMC_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected.root'
    leg_title_4600 = '(c)'
    ecms_4600 = 4600
    scale_4600 = 0.0035
    ymax_4600 = 1500
    plot(data_path_4600, sigMC_path_4600, leg_title_4600, ecms_4600, scale_4600, ymax_4600)
