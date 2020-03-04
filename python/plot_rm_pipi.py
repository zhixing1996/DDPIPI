#!/usr/bin/env python
"""
Plot invariant mass of tagged D and selected pi0
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-05 Tue 16:27]"

import ROOT
from ROOT import TCanvas, gStyle, TTree, THStack
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
from math import *
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_rm_pipi.py

SYNOPSIS
    ./plot_rm_pipi.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h1, h2, h3, h4, h5, title):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'inclusive MC: open charm')
    legend.AddEntry(h3, 'inclusive MC: q#bar{q}')
    legend.AddEntry(h4, 'D_{1}(2420)D')
    legend.AddEntry(h5, '#psi(3770)#pi^{+}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_pipi_fill(t1, t2, t3, t4, t5, h1, h2, h3, h4, h5, runNolow, runNoup):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        if fabs(t1.m_runNo) >= runNolow and fabs(t1.m_runNo) <= runNoup:
            h1.Fill(t1.m_rm_pipi)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        if fabs(t2.m_runNo) >= runNolow and fabs(t2.m_runNo) <= runNoup:
            h2.Fill(t2.m_rm_pipi)
    for ientry3 in xrange(t3.GetEntries()):
        t3.GetEntry(ientry3)
        if fabs(t3.m_runNo) >= runNolow and fabs(t3.m_runNo) <= runNoup:
            h3.Fill(t3.m_rm_pipi)
    for ientry4 in xrange(t4.GetEntries()):
        t4.GetEntry(ientry4)
        if fabs(t4.m_runNo) >= runNolow and fabs(t4.m_runNo) <= runNoup:
            h4.Fill(t4.m_rm_pipi)
    for ientry5 in xrange(t5.GetEntries()):
        t5.GetEntry(ientry5)
        if fabs(t5.m_runNo) >= runNolow and fabs(t5.m_runNo) <= runNoup:
            h5.Fill(t5.m_rm_pipi)

def set_histo_style(h1, h2, h3, h4, h5, xtitle, ytitle, ymax):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.06)
    h1.GetXaxis().SetTitleOffset(1.15)
    h1.GetXaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitleSize(0.06)
    h1.GetYaxis().SetTitleOffset(1.15)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetXaxis().CenterTitle()
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetYaxis().CenterTitle()
    h1.GetYaxis().SetRangeUser(0, ymax)
    h1.SetFillColor(1)
    h2.SetFillColor(2)
    h3.SetFillColor(3)
    h4.SetFillColor(4)
    h5.SetFillColor(6)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup, ymax, mode):
    try:
        f_data = TFile(path[0])
        f_incMC1 = TFile(path[1])
        f_incMC2 = TFile(path[2])
        f_sigMC1 = TFile(path[3])
        f_sigMC2 = TFile(path[4])
        t_data = f_data.Get('save')
        t_incMC1 = f_incMC1.Get('save')
        t_incMC2 = f_incMC2.Get('save')
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        entries_data = t_data.GetEntries()
        entries_incMC1 = t_incMC1.GetEntries()
        entries_incMC2 = t_incMC2.GetEntries()
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('inclusive MC(open charm) entries :'+str(entries_incMC1))
        logging.info('inclusive MC(qqbar) entries :'+str(entries_incMC2))
        logging.info('signal MC(D1(2420)) entries :'+str(entries_sigMC1))
        logging.info('signal MC(psi(3770)) entries :'+str(entries_sigMC2))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'RM(#pi^{+}_{0}#pi^{-}_{0})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_incMC1 = TH1F('incMC1', 'inclusive MC: open charm', xbins, xmin, float(xmax))
    h_incMC2 = TH1F('incMC2', 'inclusive MC: qqbar', xbins, xmin, float(xmax))
    h_sigMC1 = TH1F('sigMC1', 'signal MC: D1(2420)', xbins, xmin, float(xmax))
    h_sigMC2 = TH1F('sigMC2', 'signal MC: psi(3770)', xbins, xmin, float(xmax))
    
    set_histo_style(h_data, h_incMC1, h_incMC2, h_sigMC1, h_sigMC2, xtitle, ytitle, ymax)
    rm_pipi_fill(t_data, t_incMC1, t_incMC2, t_sigMC1, t_sigMC2, h_data, h_incMC1, h_incMC2, h_sigMC1, h_sigMC2, runNolow, runNoup)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sigMC1.Scale(scale_factor(ecms, 'D1_2420'))
    h_sigMC2.Scale(scale_factor(ecms, 'psipp'))
    h_incMC1.Scale(scale_factor(ecms, 'DD'))
    h_incMC2.Scale(scale_factor(ecms, 'qq'))
    h_data.Draw('E1')
    h_incMC1.SetFillColor(ROOT.kBlue)
    h_incMC2.SetFillColor(ROOT.kYellow)
    h_sigMC1.SetFillColor(ROOT.kGreen)
    h_sigMC2.SetFillColor(ROOT.kRed)
    hs = THStack('hs', 'Stacked')
    hs.Add(h_incMC2)
    hs.Add(h_incMC1)
    hs.Add(h_sigMC1)
    hs.Add(h_sigMC2)
    hs.Draw('same')
    h_data.Draw('sameE1')

    legend = TLegend(0.55, 0.6, 0.8, 0.75)
    set_legend(legend, h_data, h_incMC1, h_incMC2, h_sigMC1, h_sigMC2, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_pipi_'+str(ecms)+'_'+mode+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = args[0]
    mode = args[1]

    path = []
    if int(ecms) == 4360:
        if mode == 'before':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_before.root')
            ymax = 70
            xmin = 3.7
            xmax = 4.1
            xbins = 200
        if mode == 'after':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_after.root')
            ymax = 70
            xmin = 3.7
            xmax = 4.1
            xbins = 200
        if mode == 'X_3842':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_after.root')
            ymax = 60
            xmin = 3.8
            xmax = 3.9
            xbins = 40
        leg_title = '(a)'
        runNolow = 30616
        runNoup = 31279
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup, ymax, mode)

    if int(ecms) == 4420:
        if mode == 'before':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_before.root')
            ymax = 130
            xmin = 3.7
            xmax = 4.1
            xbins = 200
        if mode == 'after':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_after.root')
            ymax = 130
            xmin = 3.7
            xmax = 4.1
            xbins = 200
        if mode == 'X_3842':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_after.root')
            ymax = 170
            xmin = 3.8
            xmax = 3.9
            xbins = 40
        leg_title = '(b)'
        runNolow = -999999
        runNoup = 999999
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup, ymax, mode)

    if int(ecms) == 4600:
        if mode == 'before':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_before.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_before.root')
            ymax = 30
            xmin = 3.7
            xmax = 4.3
            xbins = 300
        if mode == 'after':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_after.root')
            ymax = 30
            xmin = 3.7
            xmax = 4.3
            xbins = 300
        if mode == 'X_3842':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_after.root')
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_after.root')
            ymax = 40
            xmin = 3.8
            xmax = 3.9
            xbins = 50
        leg_title = '(c)'
        runNolow = 35227
        runNoup = 35743
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup, ymax, mode)
