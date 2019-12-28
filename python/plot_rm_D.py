#!/usr/bin/env python
"""
Plot recoiling mass of tagged D and missed D
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-28 Thu 00:33]"

import ROOT
from ROOT import *
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
    plot_rm_D.py

SYNOPSIS
    ./plot_rm_D.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'data: signal region of RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})')
    legend.AddEntry(h2, 'data: sideband region of RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_Dpipi_fill(t1, t2, h1, h2, runNolow, runNoup, ecms):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        if fabs(t1.m_runNo) >= runNolow and fabs(t1.m_runNo) <= runNoup:
            h1.Fill(t1.m_rm_D)
            h1.Fill(t1.m_rm_Dmiss)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        if fabs(t2.m_runNo) >= runNolow and fabs(t2.m_runNo) <= runNoup:
            h2.Fill(t2.m_rm_D)
            h2.Fill(t2.m_rm_Dmiss)

def set_histo_style(h1, h2, xtitle, ytitle):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitleOffset(1.3)
    h1.GetXaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetTitleOffset(1.5)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetXaxis().CenterTitle()
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetYaxis().CenterTitle()
    h1.SetFillColor(1)
    h2.SetFillColor(kGreen)
    h2.SetLineColor(kGreen)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup):
    try:
        f_data = TFile(path[0])
        f_sideband = TFile(path[1])
        t_data = f_data.Get('save')
        t_sideband = f_sideband.Get('save')
        entries_data = t_data.GetEntries()
        entries_sideband = t_sideband.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('sideband entries :'+str(entries_sideband))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'RM(D^{+}) and RM(D^{-}_{miss})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_sideband = TH1F('sideband', 'sideband', xbins, xmin, float(xmax))
    
    set_histo_style(h_data, h_sideband, xtitle, ytitle)
    rm_Dpipi_fill(t_data, t_sideband, h_data, h_sideband, runNolow, runNoup, ecms)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sideband.Scale(0.5)
    h_data.Draw('E1')
    h_sideband.Draw('same')

    legend = TLegend(0.2, 0.7, 0.4, 0.85)
    set_legend(legend, h_data, h_sideband, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_D_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = args[0]

    path = []
    if int(ecms) == 4360:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_after.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_sideband.root')
        leg_title = '(a)'
        xmin = 2.14
        xmax = 2.49
        xbins = 140
        runNolow = 30616
        runNoup = 31279
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup)

    path = []
    if int(ecms) == 4420:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_after.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_sideband.root')
        leg_title = '(b)'
        xmin = 2.14
        xmax = 2.55
        xbins = 164
        runNolow = -99999
        runNoup = 99999
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup)

    path = []
    if int(ecms) == 4600:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_after.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_sideband.root')
        leg_title = '(c)'
        xmin = 2.14
        xmax = 2.72
        xbins = 232
        runNolow = 35227
        runNoup = 35743
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup)
