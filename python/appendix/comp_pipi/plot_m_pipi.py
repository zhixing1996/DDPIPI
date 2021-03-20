#!/usr/bin/env python
"""
Plot invariant mass of tagged pi+ and pi-
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
    plot_m_pipi.py

SYNOPSIS
    ./plot_m_pipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h1, h2):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'PHSP MC')
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.06)

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def m_pipi_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h.Fill(t.m_m_pipi)

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

def plot(data_path, phsp_path, pt_title, ecms, xmin, xmax, xbins):
    try:
        f_data = TFile(data_path)
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(data_path + ' is invalid!')
        sys.exit()
    try:
        f_phsp = TFile(phsp_path)
        t_phsp = f_phsp.Get('save')
        entries_phsp = t_phsp.GetEntries()
        logging.info('PHSP MC entries :'+str(entries_phsp))
    except:
        logging.error(phsp_path + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    content = int((xmax - xmin)/xbins * 1000)
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'M(#pi_{0}^{+}#pi_{0}^{-})(GeV)'
    
    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    set_histo_style(h_data, xtitle, ytitle, 1, -1)
    m_pipi_fill(t_data, h_data)
    
    h_phsp = TH1F('PHSP', 'PHSP', xbins, xmin, xmax)
    set_histo_style(h_phsp, xtitle, ytitle, 2, 3004)
    m_pipi_fill(t_phsp, h_phsp)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    scale = h_data.Integral()/h_phsp.Integral()*0.2
    h_phsp.Scale(scale)
    h_data.Draw('E1')
    h_phsp.Draw('same')
    h_data.Draw('sameE1')

    pt = TPaveText(0.6, 0.7, 0.75, 0.75, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)

    legend = TLegend(0.6, 0.55, 0.75, 0.7)
    set_legend(legend, h_data, h_phsp)
    legend.Draw()

    mbc.SaveAs('./figs/m_pipi_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    data_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_after.root'
    phsp_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_after.root'
    pt_title = str(ecms) + ' MeV'
    xmin = 0.25
    if ecms > 4440:
        xmax = 1.15
    elif ecms > 4340:
        xmax = 0.85
    elif ecms > 4230:
        xmax = 0.7
    elif ecms >= 4190:
        xmax = 0.6
    xbins = int((xmax - xmin)/0.005)
    plot(data_path, phsp_path, pt_title, ecms, xmin, xmax, xbins)
