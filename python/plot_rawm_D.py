#!/usr/bin/env python
"""
Plot invariant mass of tagged D without kinematic fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-06 Tue 09:14]"

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

def rawm_D_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if t.m_mode == 200:
            h.Fill(t.m_rawm_D)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
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
    h.SetFillColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data_path, leg_title, ecms):
    try:
        f_data = TFile(data_path)
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 1.8593
    xmax = 1.88
    xbins = 75
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'M(D^{+})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    
    set_histo_style(h_data, xtitle, ytitle)
    rawm_D_fill(t_data, h_data)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_data.Draw('E1')

    mbc.SaveAs('./figs/rawm_D_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_raw.root'
    leg_title = '(b)'
    ecms = 4360
    plot(data_path, leg_title, ecms)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_raw.root'
    leg_title = '(b)'
    ecms = 4420
    plot(data_path, leg_title, ecms)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_raw.root'
    leg_title = '(b)'
    ecms = 4600
    plot(data_path, leg_title, ecms)
