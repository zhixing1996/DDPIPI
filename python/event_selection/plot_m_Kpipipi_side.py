#!/usr/bin/env python
"""
Plot invariant mass of Kpipipi without kinematic fit
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
from tools import window
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_m_Kpipipi.py

SYNOPSIS
    ./plot_m_Kpipipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.05)

def m_Kpipipi_fill(t, h, type):
    window_low = 1.86965 - window(ecms)/2.
    window_up = 1.86965 + window(ecms)/2.
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if not (t.m_rm_Dpipi > window_low and t.m_rm_Dpipi < window_up):
            continue
        if type == 'Kpipipi1': h.Fill(t.m_m_Kpipipi1)
        if type == 'Kpipipi2': h.Fill(t.m_m_Kpipipi2)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.06)
    h.GetXaxis().SetTitleOffset(1.1)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(1.1)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data_path, pt_title, ecms, xmin, xmax, xbins):
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
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'M(K^{-}#pi_{0}^{+}#pi_{0}^{-}#pi_{1}^{+})/M(K^{-}#pi_{0}^{+}#pi_{0}^{-}#pi_{2}^{+})(GeV)'
    h_Kpipipi1 = TH1F('Kpipipi1', 'Kpipipi1', xbins, xmin, float(xmax))
    set_histo_style(h_Kpipipi1, xtitle, ytitle)
    m_Kpipipi_fill(t_data, h_Kpipipi1, 'Kpipipi1')
    
    h_Kpipipi2 = TH1F('Kpipipi2', 'Kpipipi2', xbins, xmin, float(xmax))
    set_histo_style(h_Kpipipi2, xtitle, ytitle)
    m_Kpipipi_fill(t_data, h_Kpipipi2, 'Kpipipi2')
    
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    set_histo_style(h_data, xtitle, ytitle)
    h_data.Add(h_Kpipipi1)
    h_data.Add(h_Kpipipi2)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_data.Draw('E1')

    pt = TPaveText(0.2, 0.75, 0.35, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText('M(K^{-}#pi^{+}#pi^(+)) in sideband region')
    pt.AddText(pt_title)

    mbc.SaveAs('./figs/m_Kpipipi_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    data_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw_sideband_before.root'
    pt_title = str(ecms) + ' MeV'
    xmin = 1.75
    xmax = 1.95
    xbins = 100
    plot(data_path, pt_title, ecms, xmin, xmax, xbins)
