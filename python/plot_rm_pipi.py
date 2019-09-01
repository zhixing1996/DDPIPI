#!/usr/bin/env python
"""
Plot recoiling mass of selected pipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-01 Thu 23:14]"

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
    legend.AddEntry(h2, 'inclusive MC: DD')
    legend.AddEntry(h3, 'signal MC: psi(3770)#pi^{+}#pi^{-}')
    legend.AddEntry(h4, 'signal MC: DD1(2420)')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_D_fill(t1, t2, t3, t4, h1, h2, h3, h4):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        h1.Fill(t1.m_rm_pipi)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        h2.Fill(t2.m_rm_pipi)
    for ientry3 in xrange(t3.GetEntries()):
        t3.GetEntry(ientry3)
        h3.Fill(t3.m_rm_pipi)
    for ientry4 in xrange(t4.GetEntries()):
        t4.GetEntry(ientry4)
        h4.Fill(t4.m_rm_pipi)

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

def plot(data_path, incMC_path, sigMC1_path, sigMC2_path, leg_title, ecms, scale1, scale2, scale3, ymax, xmax):
    try:
        f_data = TFile(data_path)
        f_incMC = TFile(incMC_path)
        f_sigMC1 = TFile(sigMC1_path)
        f_sigMC2 = TFile(sigMC2_path)
        t_data = f_data.Get('save')
        t_incMC = f_incMC.Get('save')
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        entries_data = t_data.GetEntries()
        entries_incMC = t_incMC.GetEntries()
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('inclusive MC DD entries :'+str(entries_incMC))
        logging.info('signal MC psi(3770) entries :'+str(entries_sigMC1))
        logging.info('signal MC DD1(2420) entries :'+str(entries_sigMC2))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 3.7
    xbins = 40
    ytitle = 'Events'
    xtitle = 'RM(#pi^{+}#pi^{-}) (GeV/c^{2})'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_incMC = TH1F('inc_MC', 'inclusive MC: DD', xbins, xmin, float(xmax))
    h_sigMC1 = TH1F('sigMC1', 'signal MC: psi(3770)', xbins, xmin, float(xmax))
    h_sigMC2 = TH1F('sigMC2', 'signal MC: DD1(2420)', xbins, xmin, float(xmax))

    set_histo_style(h_data, h_incMC, h_sigMC1, h_sigMC2, xtitle, ytitle, ymax)
    rm_D_fill(t_data, t_incMC, t_sigMC1, t_sigMC2, h_data, h_incMC, h_sigMC1, h_sigMC2)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_incMC.Scale(float(scale1))
    h_sigMC1.Scale(float(scale2)/h_sigMC1.GetEntries())
    h_sigMC2.Scale(float(scale3)/h_sigMC2.GetEntries())
    h_data.Draw('ep')
    h_incMC.Draw('samee')
    h_sigMC1.Draw('samee')
    h_sigMC2.Draw('samee')

    legend = TLegend(0.55, 0.65, 0.76, 0.82)
    set_legend(legend, h_data, h_incMC, h_sigMC1, h_sigMC2, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_pipi_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected_signal.root'
    incMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4360/incMC_DD_4360_selected_signal.root'
    sigMC1_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4360/sigMC_psi_3770_4360_selected_signal.root'
    sigMC2_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected.root'
    leg_title = '(a)'
    ecms = 4360
    scale1 = 7
    scale2 = 342
    scale3 = 1009
    xmax = 4.1
    ymax = 400
    plot(data_path, incMC_path, sigMC1_path, sigMC2_path, leg_title, ecms, scale1, scale2, scale3, ymax, xmax)

    data_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected_signal.root'
    incMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4420/incMC_DD_4420_selected_signal.root'
    sigMC1_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4420/sigMC_psi_3770_4420_selected_signal.root'
    sigMC2_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected.root'
    leg_title = '(b)'
    ecms = 4420
    scale1 = 0.25
    scale2 = 938
    scale3 = 2667
    xmax = 4.1
    ymax = 900
    plot(data_path, incMC_path, sigMC1_path, sigMC2_path, leg_title, ecms, scale1, scale2, scale3, ymax, xmax)

    data_path = '/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected_signal.root'
    incMC_path = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4600/incMC_DD_4600_selected_signal.root'
    sigMC1_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4600/sigMC_psi_3770_4600_selected_signal.root'
    sigMC2_path = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected.root'
    leg_title = '(c)'
    ecms = 4600
    scale1 = 0.5
    scale2 = 187
    scale3 = 650
    xmax = 4.2
    ymax = 300
    plot(data_path, incMC_path, sigMC1_path, sigMC2_path, leg_title, ecms, scale1, scale2, scale3, ymax, xmax)
