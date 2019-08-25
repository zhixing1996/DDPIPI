#!/usr/bin/env python
"""
Plot recoiling mass of tagged D
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-25 Sun 20:03]"

import ROOT
from ROOT import TCanvas, gStyle, TTree
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def set_legend(legend, h1, h2, h3, title, ecms):
    legend.AddEntry(h1, str(ecms)+' MeV: signal region')
    legend.AddEntry(h2, str(ecms)+' MeV: sideband region')
    legend.AddEntry(h3, str(ecms)+' MeV: signal shape')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_D_fill(t1, t2, h1, h2, h3, xbins):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        h1.Fill(t1.m_rm_D)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        h2.Fill(t2.m_rm_D)
    for ientry3 in xrange(xbins):
        sig_bin = h1.GetBinContent(ientry3)
        side_bin = h2.GetBinContent(ientry3)
        shape_bin = sig_bin - side_bin/4
        h3.SetBinContent(ientry3, shape_bin)

def set_histo_style(h1, h2, h3, xtitle, ytitle, ymax):
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

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(signal, sideband, leg_title, ecms, scale, ymax, xmax, mode):
    try:
        f_signal = TFile(signal)
        f_sideband = TFile(sideband)
        t_signal = f_signal.Get('save')
        t_sideband = f_sideband.Get('save')
        entries_signal = t_signal.GetEntries()
        entries_sideband = t_sideband.GetEntries()
        logging.info('signal entries :'+str(entries_signal))
        logging.info('sideband entries :'+str(entries_sideband))
    except:
        logging.error(signal+' or '+sideband+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 2.1
    xbins = 40
    ytitle = 'Events'
    xtitle = 'RM(D^{+}) (GeV/c^{2})'
    h_signal = TH1F('signal', 'signal', xbins, xmin, float(xmax))
    h_sideband = TH1F('sideband', 'sideband', xbins, xmin, float(xmax))
    h_subtract = TH1F('subtract', 'subtract', xbins, xmin, float(xmax))

    set_histo_style(h_signal, h_sideband, h_subtract, xtitle, ytitle, ymax)
    rm_D_fill(t_signal, t_sideband, h_signal, h_sideband, h_subtract, xbins)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sideband.Scale(float(scale))
    h_signal.Draw('ep')
    h_sideband.Draw('samee')
    h_subtract.Draw('samee')

    legend = TLegend(0.25, 0.6, 0.42, 0.4)
    set_legend(legend, h_signal, h_sideband, h_subtract, leg_title, ecms)
    legend.Draw()

    mbc.SaveAs('./figs/rm_D_'+str(ecms)+'_sigMC_'+mode+'.pdf')

if __name__ == '__main__':
    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected_signal.root'
    sideband = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected_sideband.root'
    leg_title = '(a)'
    ecms = 4360
    scale = 0.25
    xmax = 2.5
    ymax = 60000
    mode = 'D1_2420'
    plot(signal, sideband, leg_title, ecms, scale, ymax, xmax, mode)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected_signal.root'
    sideband = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected_sideband.root'
    leg_title = '(a)'
    ecms = 4420
    scale = 0.25
    xmax = 2.6
    ymax = 60000
    mode = 'D1_2420'
    plot(signal, sideband, leg_title, ecms, scale, ymax, xmax, mode)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected_signal.root'
    sideband = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected_sideband.root'
    leg_title = '(a)'
    ecms = 4600
    scale = 0.25
    xmax = 2.75
    ymax = 57000
    mode = 'D1_2420'
    plot(signal, sideband, leg_title, ecms, scale, ymax, xmax, mode)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4360/sigMC_psi_3770_4360_selected_signal.root'
    sideband = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4360/sigMC_psi_3770_4360_selected_sideband.root'
    leg_title = '(a)'
    ecms = 4360
    scale = 0.25
    xmax = 2.6
    ymax = 60000
    mode = 'psi_3770'
    plot(signal, sideband, leg_title, ecms, scale, ymax, xmax, mode)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4420/sigMC_psi_3770_4420_selected_signal.root'
    sideband = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4420/sigMC_psi_3770_4420_selected_sideband.root'
    leg_title = '(a)'
    ecms = 4420
    scale = 0.25
    xmax = 2.6
    ymax = 60000
    mode = 'psi_3770'
    plot(signal, sideband, leg_title, ecms, scale, ymax, xmax, mode)

    signal = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4600/sigMC_psi_3770_4600_selected_signal.root'
    sideband = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4600/sigMC_psi_3770_4600_selected_sideband.root'
    leg_title = '(a)'
    ecms = 4600
    scale = 0.25
    xmax = 2.8
    ymax = 60000
    mode = 'psi_3770'
    plot(signal, sideband, leg_title, ecms, scale, ymax, xmax, mode)
