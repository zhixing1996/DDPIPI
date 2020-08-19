#!/usr/bin/env python
"""
Plot recoiling mass of tagged D and selected piplus piminus
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-05 Tue 19:12]"

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
    plot_rm_Dpipi_sideband.py

SYNOPSIS
    ./plot_rm_Dpipi_sideband.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h, title):
    legend.AddEntry(h, 'data: sideband region of M(K^{-}#pi^{+}#pi^{+})')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_Dpipi_fill(t, h, runNolow, runNoup, ecms):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if fabs(t.m_runNo) >= runNolow and fabs(t.m_runNo) <= runNoup:
            h.Fill(t.m_rm_Dpipi)

def set_histo_style(h, xtitle, ytitle, ymax):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetTitleOffset(1.3)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.5)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.GetYaxis().SetRangeUser(0, ymax)
    h.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup, ymax):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    
    set_histo_style(h_data, xtitle, ytitle, ymax)
    rm_Dpipi_fill(t_data, h_data, runNolow, runNoup, ecms)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_data.Draw('E1')

    legend = TLegend(0.55, 0.7, 0.8, 0.85)
    set_legend(legend, h_data, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_Dpipi_'+str(ecms)+'_sideband.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = args[0]

    path = []
    if int(ecms) == 4360:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_raw_sideband_before.root')
        leg_title = '(a)'
        xmin = 1.75
        xmax = 1.95
        xbins = 80
        ymax = 500
        runNolow = 30616
        runNoup = 31279
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup, ymax)

    path = []
    if int(ecms) == 4420:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_raw_sideband_before.root')
        leg_title = '(b)'
        xmin = 1.75
        xmax = 1.95
        xbins = 80
        ymax = 1200
        runNolow = 36773
        runNoup = 38140
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup, ymax)

    path = []
    if int(ecms) == 4600:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_raw_sideband_before.root')
        leg_title = '(c)'
        xmin = 1.75
        xmax = 1.95
        xbins = 50
        ymax = 700
        runNolow = 35227
        runNoup = 35743
        plot(path, leg_title, ecms, xmin, xmax, xbins, runNolow, runNoup, ymax)
