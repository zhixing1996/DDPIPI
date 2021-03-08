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
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_rm_Dpipi.py

SYNOPSIS
    ./plot_rm_Dpipi.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def rm_Dpipi_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h.Fill(t.m_rm_Dpipi)

def set_histo_style(h, xtitle, ytitle):
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
    h.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data_path, pt_title, ecms, xmin, xmax, xbins, mode):
    try:
        f_MC = TFile(data_path)
        t_MC = f_MC.Get('save')
        entries_MC = t_MC.GetEntries()
        logging.info('data entries :'+str(entries_MC))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'RM(D^{+}#pi_{0}^{+}#pi_{0}^{-})(GeV)'
    h_MC = TH1F('MC', 'MC', xbins, xmin, float(xmax))
    
    set_histo_style(h_MC, xtitle, ytitle)
    rm_Dpipi_fill(t_MC, h_MC)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_MC.Draw()

    pt = TPaveText(0.2, 0.62, 0.35, 0.75, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)
    if mode == 'D1_2420': process = 'e^{+}e^{-}#rightarrow D_{1}(2420)^{+}D^{-}'
    if mode == 'DDPIPI': process = 'e^{+}e^{-}#rightarrow #pi^{+}#pi^{-}D^{+}D^{-}(PHSP)'
    if mode == 'psipp': process = 'e^{+}e^{-}#rightarrow #pi^{+}#pi^{-}#psi(3770)'
    pt.AddText(process)

    mbc.SaveAs('./figs/rm_Dpipi_'+str(ecms)+'_'+mode+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = int(args[0])
    mode = args[1]

    if not mode == 'DDPIPI':
        data_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/'+mode+'/'+str(ecms)+'/sigMC_'+mode+'_'+str(ecms)+'_raw_sideband_before.root'
    if mode == 'DDPIPI':
        data_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/'+mode+'/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_raw_sideband_before.root'
    pt_title = str(ecms) + ' MeV'
    xmin = 1.75
    xmax = 1.95
    xbins = 100
    plot(data_path, pt_title, ecms, xmin, xmax, xbins, mode)
