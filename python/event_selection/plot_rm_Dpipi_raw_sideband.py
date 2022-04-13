#!/usr/bin/env python
"""
Plot recoiling mass of tagged D, pi+, and pi- in sideband region
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-06 Tue 09:14]"

import ROOT
from ROOT import TCanvas, gStyle, TTree, THStack
from ROOT import TFile, TH1F, TLegend, TArrow, TPaveText
import sys, os
import logging
from math import *
from tools import luminosity
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_rm_Dpipi_raw_sideband.py

SYNOPSIS
    ./plot_rm_Dpipi_raw_sideband.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h1, h2, h3, title, ecms):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'e^{+}e^{-}#rightarrow #pi^{+}#pi^{-}D^{+}D^{-}')
    legend.AddEntry(h3, 'e^{+}e^{-}#rightarrow D^{+}#bar{D^{0}}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    if ecms > 4320: legend.SetTextSize(0.055)
    if ecms < 4320: legend.SetTextSize(0.05)

def scale(ecms, mode):
    lum = luminosity(ecms)
    with open('../fit_xs/txts/xs_total_round2_plot.txt', 'r') as f:
        for line in f.readlines():
            fargs3 = map(float, line.strip().split())
            if ecms == int(fargs3[0]*1000):
                xs = fargs3[1]
    if mode == 'DDPI':
        if ecms == 4230:
            xs = 31.79
        if ecms == 4420:
            xs = 670.75
        if ecms == 4600:
            xs = 131.56
        if ecms == 4840:
            xs = 52.
    N = 50000
    if not mode == 'DDPI':
        if ecms == 4420 or ecms == 4230:
            N = 100000
    if mode == 'DDPI':
        if ecms == 4420 or ecms == 4230:
            N = 500000
        if ecms == 4600:
            N = 250000
    return lum*xs/N

def rm_Dpipi_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h.Fill(t.m_rm_Dpipi)

def set_histo_style(h, xtitle, ytitle, color, is_fill):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.06)
    h.GetXaxis().SetTitleOffset(1.)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetLabelSize(0.06)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(1.)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetLabelSize(0.06)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetLineColor(color)
    if is_fill: h.SetFillColor(color)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, pt_title, ecms, xmin, xmax, xbins, ymax):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()
    try:
        f_DDPIPI = TFile(path[1])
        t_DDPIPI = f_DDPIPI.Get('save')
        entries_DDPIPI = t_DDPIPI.GetEntries()
        logging.info('DDPIPI entries :'+str(entries_DDPIPI))
    except:
        logging.error(path[1] + ' is invalid!')
        sys.exit()
    try:
        f_DDPI = TFile(path[2])
        t_DDPI = f_DDPI.Get('save')
        entries_DDPI = t_DDPI.GetEntries()
        logging.info('DDPI entries :'+str(entries_DDPI))
    except:
        logging.error(path[2] + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'RM(D^{+}#pi_{0}^{+}#pi_{0}^{-})(GeV)'

    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    set_histo_style(h_data, xtitle, ytitle, 1, False)
    rm_Dpipi_fill(t_data, h_data)
    
    h_DDPIPI = TH1F('DDPIPI', 'DDPIPI', xbins, xmin, float(xmax))
    set_histo_style(h_DDPIPI, xtitle, ytitle, 2, True)
    rm_Dpipi_fill(t_DDPIPI, h_DDPIPI)
    
    h_DDPI = TH1F('DDPI', 'DDPI', xbins, xmin, float(xmax))
    set_histo_style(h_DDPI, xtitle, ytitle, 3, True)
    rm_Dpipi_fill(t_DDPI, h_DDPI)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    F_DDPIPI = scale(ecms, 'DDPIPI')
    F_DDPI = scale(ecms, 'DDPI')
    h_DDPIPI.Scale(F_DDPIPI)
    h_DDPI.Scale(F_DDPI)
    h_data.GetYaxis().SetRangeUser(0, ymax)
    h_data.Draw('E1')
    hs = THStack('hs', 'Stacked')
    hs.Add(h_DDPIPI)
    hs.Add(h_DDPI)
    hs.Draw('same')
    h_data.Draw('sameE1')

    if ecms > 4320: legend = TLegend(0.2, 0.25, 0.5, 0.55)
    if ecms < 4320: legend = TLegend(0.2, 0.2, 0.55, 0.4)
    set_legend(legend, h_data, h_DDPIPI, h_DDPI, pt_title, ecms)
    legend.Draw()

    mbc.SaveAs('./figs/rm_Dpipi_'+str(ecms)+'_raw_sideband.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_sideband_before.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPIinc/'+str(ecms)+'/sigMC_D_D_PI_PI_inc_'+str(ecms)+'_raw_sideband_before.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPI/'+str(ecms)+'/sigMC_D_D_PI_'+str(ecms)+'_raw_sideband_before.root')
    pt_title = str(ecms) + ' MeV'
    xmin = 1.75
    xmax = 1.95
    xbins = 100
    if ecms == 4840: ymax = 550
    if ecms == 4420: ymax = 900
    if ecms == 4600: ymax = 550
    if ecms == 4230: ymax = 320
    plot(path, pt_title, ecms, xmin, xmax, xbins, ymax)
