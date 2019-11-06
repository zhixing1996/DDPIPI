#!/usr/bin/env python
"""
Plot mathced chi2 of vertex fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-10-14 Mon 22:32]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def set_arrow(arrow):
    arrow.SetLineWidth(0)
    arrow.SetLineColor(2)
    arrow.SetFillColor(2)

def set_legend(legend, h1, h2, h3, h4, title):
    legend.AddEntry(h1, 'open charm: not D')
    legend.AddEntry(h2, 'open charm: D')
    legend.AddEntry(h3, '#psi(3770)#pi^{+}#pi^{-}: not D')
    legend.AddEntry(h4, '#psi(3770)#pi^{+}#pi^{-}: D')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def chi2_KF_fill(t1, t2, h1, h2, h3, h4, runNolow, runNoup):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        if fabs(t1.m_runNo) < runNolow or fabs(t1.m_runNo) > runNoup:
            continue
        if (t1.m_m_Dpi0 < 2.0082 or t1.m_m_Dpi0 > 2.01269) and (t1.m_m_pipi < 0.491036 or t1.m_m_pipi > 0.503471):
            if t1.m_matched_D == 0:
                h1.Fill(t1.m_chi2_vf)
            if t1.m_matched_D == 1:
                h2.Fill(t1.m_chi2_vf)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        if fabs(t2.m_runNo) < runNolow or fabs(t2.m_runNo) > runNoup:
            continue
        if (t2.m_m_Dpi0 < 2.0082 or t2.m_m_Dpi0 > 2.01269) and (t2.m_m_pipi < 0.491036 or t2.m_m_pipi > 0.503471):
            if t2.m_matched_D == 0:
                h3.Fill(t2.m_chi2_vf)
            if t2.m_matched_D == 1:
                h4.Fill(t2.m_chi2_vf)

def set_histo_style(h1, h2, h3, h4, xtitle, ytitle):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h3.SetLineWidth(2)
    h4.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h3.SetStats(0)
    h4.SetStats(0)
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

def plot(incMC_path, sigMC_path, leg_title, ecms, xmax, runNolow, runNoup):
    try:
        f_incMC = TFile(incMC_path)
        f_sigMC = TFile(sigMC_path)
        t_incMC = f_incMC.Get('save')
        t_sigMC = f_sigMC.Get('save')
        entries_incMC = t_incMC.GetEntries()
        entries_sigMC = t_sigMC.GetEntries()
        logging.info('inclusive MC(open charm) entries :'+str(entries_incMC))
        logging.info('inclusive MC(psi(3770)) entries :'+str(entries_sigMC))
    except:
        logging.error('File is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 0
    xbins = xmax
    ytitle = "Events"
    xtitle = "#chi^{2}_{vertex}"
    h_unDincMC = TH1F('unDincMC', 'unDincMC', xbins, xmin, xmax)
    h_DincMC = TH1F('DincMC', 'DincMC', xbins, xmin, xmax)
    h_unDsigMC = TH1F('unDsigMC', 'unDsigMC', xbins, xmin, xmax)
    h_DsigMC = TH1F('DsigMC', 'DsigMC', xbins, xmin, xmax)

    set_histo_style(h_unDincMC, h_DincMC, h_unDsigMC, h_DsigMC, xtitle, ytitle)
    chi2_KF_fill(t_incMC, t_sigMC, h_unDincMC, h_DincMC, h_unDsigMC, h_DsigMC, runNolow, runNoup)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_DincMC.Scale(h_unDincMC.GetEntries()/h_DincMC.GetEntries()/2)
    h_unDsigMC.Scale(h_unDincMC.GetEntries()/h_unDsigMC.GetEntries()/2)
    h_DsigMC.Scale(h_unDincMC.GetEntries()/h_DsigMC.GetEntries()/2)
    h_unDincMC.Draw()
    h_DincMC.Draw('same')
    h_unDsigMC.Draw('same')
    h_DsigMC.Draw('same')

    arrow = TArrow(20, 0, 20, 300, 0.01, '<')
    set_arrow(arrow)
    arrow.Draw()

    legend = TLegend(0.45, 0.6, 0.82, 0.8)
    set_legend(legend, h_unDincMC, h_DincMC, h_unDsigMC, h_DsigMC, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/matched_chi2_vf_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_before.root'
    sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_before.root'
    leg_title = '(b)'
    ecms = 4360
    xmax = 100
    runNolow = 30616
    runNoup = 31279
    plot(incMC_path, sigMC_path, leg_title, ecms, xmax, runNolow, runNoup)

    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_before.root'
    sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_before.root'
    leg_title = '(b)'
    ecms = 4420
    xmax = 100
    runNolow = 36773
    runNoup = 38140
    plot(incMC_path, sigMC_path, leg_title, ecms, xmax, runNolow, runNoup)

    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_before.root'
    sigMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_before.root'
    leg_title = '(b)'
    ecms = 4600
    xmax = 100
    runNolow = 35227
    runNoup = 36213
    plot(incMC_path, sigMC_path, leg_title, ecms, xmax, runNolow, runNoup)
