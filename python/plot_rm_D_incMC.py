#!/usr/bin/env python
"""
Plot recoiling mass of tagged D of inclusive MC
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-25 Sun 08:21]"

import ROOT
from ROOT import TCanvas, gStyle, TTree
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def set_legend(legend, h1, h2, ecms, title):
    legend.AddEntry(h1, str(ecms)+' MeV: signal region')
    legend.AddEntry(h2, str(ecms)+' MeV: sideband region')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_Dpipi_fill(t1, t2, h1, h2):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        h1.Fill(t1.m_rm_D)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        h2.Fill(t2.m_rm_D)

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

def plot(signal_path, sideband_path, title, ecms, scale, xmax, ymax, mode):
    try:
        f_signal = TFile(signal_path)
        f_sideband = TFile(sideband_path)
        t_signal = f_signal.Get('save')
        t_sideband = f_sideband.Get('save')
        entries_signal = t_signal.GetEntries()
        entries_sideband = t_sideband.GetEntries()
        logging.info('signal region entries :'+str(entries_signal))
        logging.info('sideband region entries :'+str(entries_sideband))
    except:
        logging.error(signal_path+' or '+sideband_path+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 2.1
    xbins = 25
    ytitle = 'Events'
    xtitle = 'RM(D^{+}) (GeV/c^{2})'
    h_signal = TH1F('signal', 'signal', xbins, xmin, float(xmax))
    h_sideband = TH1F('sideband', 'sideband', xbins, xmin, float(xmax))

    set_histo_style(h_signal, h_sideband, xtitle, ytitle, ymax)
    rm_Dpipi_fill(t_signal, t_sideband, h_signal, h_sideband)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sideband.Scale(float(scale))
    h_signal.Draw('ep')
    h_sideband.Draw('samee')

    legend = TLegend(0.25, 0.6, 0.42, 0.4)
    set_legend(legend, h_signal, h_sideband, ecms, title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_D_'+str(ecms)+'_incMC'+mode+'.pdf')

if __name__ == '__main__':
    incqq_signal_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4360/incMC_qq_4360_selected_signal.root'
    incqq_sideband_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4360/incMC_qq_4360_selected_sideband.root'
    title_incqq_4360 = '(a)'
    ecms_4360 = 4360
    scale_4360 = 0.25
    xmax_4360 = 2.5
    ymax_incqq_4360 = 90
    mode = 'qq'
    plot(incqq_signal_4360, incqq_sideband_4360, title_incqq_4360, ecms_4360, scale_4360, xmax_4360, ymax_incqq_4360, mode)

    incqq_signal_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4420/incMC_qq_4420_selected_signal.root'
    incqq_sideband_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4420/incMC_qq_4420_selected_sideband.root'
    title_incqq_4420 = '(b)'
    ecms_4420 = 4420
    scale_4420 = 0.25
    xmax_4420 = 2.6
    ymax_incqq_4420 = 500
    mode = 'qq'
    plot(incqq_signal_4420, incqq_sideband_4420, title_incqq_4420, ecms_4420, scale_4420, xmax_4420, ymax_incqq_4420, mode)

    incqq_signal_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4600/incMC_qq_4600_selected_signal.root'
    incqq_sideband_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4600/incMC_qq_4600_selected_sideband.root'
    title_incqq_4600 = '(c)'
    ecms_4600 = 4600
    scale_4600 = 0.25
    xmax_4600 = 2.75
    ymax_incqq_4600 = 70
    mode = 'qq'
    plot(incqq_signal_4600, incqq_sideband_4600, title_incqq_4600, ecms_4600, scale_4600, xmax_4600, ymax_incqq_4600, mode)

    incDD_signal_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4360/incMC_DD_4360_selected_signal.root'
    incDD_sideband_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4360/incMC_DD_4360_selected_sideband.root'
    title_incDD_4360 = '(d)'
    ecms_4360 = 4360
    scale_4360 = 0.25
    xmax_4360 = 2.5
    ymax_incDD_4360 = 50
    mode = 'DD'
    plot(incDD_signal_4360, incDD_sideband_4360, title_incDD_4360, ecms_4360, scale_4360, xmax_4360, ymax_incDD_4360, mode)

    incDD_signal_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4420/incMC_DD_4420_selected_signal.root'
    incDD_sideband_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4420/incMC_DD_4420_selected_sideband.root'
    title_incDD_4420 = '(e)'
    ecms_4420 = 4420
    scale_4420 = 0.25
    xmax_4420 = 2.6
    ymax_incDD_4420 = 2600
    mode = 'DD'
    plot(incDD_signal_4420, incDD_sideband_4420, title_incDD_4420, ecms_4420, scale_4420, xmax_4420, ymax_incDD_4420, mode)

    incDD_signal_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4600/incMC_DD_4600_selected_signal.root'
    incDD_sideband_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4600/incMC_DD_4600_selected_sideband.root'
    title_incDD_4600 = '(f)'
    ecms_4600 = 4600
    scale_4600 = 0.25
    xmax_4600 = 2.75
    ymax_incDD_4600 = 900
    mode = 'DD'
    plot(incDD_signal_4600, incDD_sideband_4600, title_incDD_4600, ecms_4600, scale_4600, xmax_4600, ymax_incDD_4600, mode)

    incLL_signal_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/LL/4600/incMC_LL_4600_selected_signal.root'
    incLL_sideband_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/LL/4600/incMC_LL_4600_selected_sideband.root'
    title_incLL_4600 = '(g)'
    ecms_4600 = 4600
    scale_4600 = 0.25
    xmax_4600 = 2.75
    ymax_incLL_4600 = 30
    mode = 'LL'
    plot(incLL_signal_4600, incLL_sideband_4600, title_incLL_4600, ecms_4600, scale_4600, xmax_4600, ymax_incLL_4600, mode)
