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
from tools import width
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_rm_Dpipi.py

SYNOPSIS
    ./plot_rm_Dpipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h_data, title):
    legend.AddEntry(h_data, 'data')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.06)

def rm_Dpipi_fill(t, h, ecms, mode):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if abs(t.m_rawm_D - 1.86965) < width(ecms)/2.:
            if mode == 'bkg':
                if t.m_n_p == 0 and t.m_n_pbar == 0:
                    continue
            if mode == 'after':
                if not (t.m_n_p == 0 and t.m_n_pbar == 0):
                    continue
            h.Fill(t.m_rm_Dpipi)

def set_histo_style(h, xtitle, ytitle, color, fill_style, ymax):
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
    # h.GetYaxis().SetRangeUser(0, ymax)
    h.SetLineColor(color)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, ecms, xmin, xmax, ymax, mode):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' path is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = 100
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Eentries/%.1f MeV'%content
    xtitle = 'RM(D^{+}#pi_{0}^{+}#pi_{0}^{-})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    set_histo_style(h_data, xtitle, ytitle, 1, -1, ymax)
    rm_Dpipi_fill(t_data, h_data, ecms, mode)
    
    h_data.Draw('E1')

    legend = TLegend(0.2, 0.72, 0.5, 0.85)
    if ecms == 4230: leg_title = '(a)'
    if ecms == 4420: leg_title = '(b)'
    set_legend(legend, h_data, leg_title)
    legend.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    mbc.SaveAs('./figs/rm_Dpipi_'+str(ecms)+'_'+mode+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = int(args[0])
    mode = args[1]

    path = []
    path.append('/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_signal.root')
    xmin = 1.75
    xmax = 1.95
    ymax = 100
    plot(path, ecms, xmin, xmax, ymax, mode)
