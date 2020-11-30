#!/usr/bin/env python
"""
Plot invariant mass of tagged piplus and selected piplus piminus
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-09-09 Thr 20:12]"

import ROOT
from ROOT import TCanvas, gStyle, TTree, THStack
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_m_pipi.py

SYNOPSIS
    ./plot_m_pipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    September 2019
\n''')

def set_legend(legend, h_data, h_sideband, title):
    legend.AddEntry(h_data, 'data')
    legend.AddEntry(h_sideband, 'sideband')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.06)

def m_pipi_fill(t, h, mode):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if not (t.m_n_p == 0 and t.m_n_pbar == 0):
            continue
        if not (t.m_n_othertrks <= 3 and t.m_n_othershws <= 6):
            continue
        discarded = False
        for iTrk in range(3):
            if abs(t.m_Vxy_Dtrks[iTrk]) > 0.55:
                discarded = True
            if abs(t.m_Vz_Dtrks[iTrk]) > 3.0:
                discarded = True
            if abs(t.m_cos_theta_Dtrks[iTrk]) > 0.93:
                discarded = True
        if abs(t.m_Vxy_pip) > 0.55: discarded = True
        if abs(t.m_Vxy_pim) > 0.55: discarded = True
        if abs(t.m_Vz_pip) > 3.: discarded = True
        if abs(t.m_Vz_pim) > 3.: discarded = True
        if abs(t.m_cos_theta_pip) > 0.93: discarded = True
        if abs(t.m_cos_theta_pim) > 0.93: discarded = True
        if mode == 'before':
            if not discarded: h.Fill(t.m_m_pipi)
        if mode == 'after':
            if not (t.m_m_pipi > 0.491036 and t.m_m_pipi < 0.503471 and abs(t.m_L_svf/t.m_Lerr_svf) > 2) and not discarded: h.Fill(t.m_m_pipi)

def set_histo_style(h, xtitle, ytitle, color, fill_style):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.SetStats(0)
    if not fill_style == -1:
        h.SetFillStyle(fill_style) 
        h.SetFillColor(color)
    h.GetXaxis().SetTitleSize(0.06)
    h.GetXaxis().SetTitleOffset(1.)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(1.)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetLineColor(color)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, ecms, xmin, xmax, mode):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' path is invalid!')
        sys.exit()
    try:
        f_sideband = TFile(path[1])
        t_sideband = f_sideband.Get('save')
        entries_sideband = t_sideband.GetEntries()
        logging.info('data entries :'+str(entries_sideband))
    except:
        logging.error(path[1] + ' path is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = 140
    content = int((xmax - xmin)/xbins * 1000)
    ytitle = 'Eentries/%.1f MeV'%content
    xtitle = 'M(#pi_{0}^{+}#pi_{0}^{-}) (GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    set_histo_style(h_data, xtitle, ytitle, 1, -1)
    m_pipi_fill(t_data, h_data, mode)
    
    h_sideband = TH1F('sideband', 'sideband', xbins, xmin, xmax)
    set_histo_style(h_sideband, xtitle, ytitle, 3, 3004)
    m_pipi_fill(t_sideband, h_sideband, mode)
    
    h_sideband.Scale(0.5)
    h_data.Draw('E1')
    h_sideband.Draw('same')
    h_data.Draw('sameE1')

    legend = TLegend(0.55, 0.65, 0.8, 0.85)
    leg_title = str(ecms) + ' MeV'
    set_legend(legend, h_data, h_sideband, leg_title)
    legend.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    mbc.SaveAs('./figs/m_pipi_'+str(ecms)+'_'+mode+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = int(args[0])
    mode = args[1]

    path = []
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_before.root')
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_sideband_before.root')
    xmin = 0.25
    xmax = 0.95
    plot(path, ecms, xmin, xmax, mode)
