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
    plot_rm_Dpipi.py

SYNOPSIS
    ./plot_rm_Dpipi.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h1, h2, h3, h4, h5, title, ecms):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'open charm')
    legend.AddEntry(h3, 'q#bar{q}')
    if ecms > 4230: legend.AddEntry(h4, 'D_{1}(2420)D')
    legend.AddEntry(h5, '#psi(3770)#pi^{+}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.06)

def rm_Dpipi_fill(t, h, ecms, mode):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if mode == 'before' and fabs(t.m_rawm_D - 1.86965) < width(ecms)/2.:
            h.Fill(t.m_rm_Dpipi)

def set_histo_style(h, xtitle, ytitle, ymax, color, fill_style):
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
    if not ymax == -1: h.GetYaxis().SetRangeUser(0, ymax)
    h.SetLineColor(color)
    h.SetFillColor(color)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, leg_title, ecms, xmin, xmax, xbins, mode, ymax):
    try:
        f_data = TFile(path[0])
        f_incMC1 = TFile(path[1])
        f_incMC2 = TFile(path[2])
        if ecms > 4230:
            f_sigMC1 = TFile(path[3])
            f_sigMC2 = TFile(path[4])
        else:
            f_sigMC2 = TFile(path[3])
        t_data = f_data.Get('save')
        t_incMC1 = f_incMC1.Get('save')
        t_incMC2 = f_incMC2.Get('save')
        if ecms > 4230: t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        entries_data = t_data.GetEntries()
        entries_incMC1 = t_incMC1.GetEntries()
        entries_incMC2 = t_incMC2.GetEntries()
        if ecms > 4230: entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('inclusive MC(open charm) entries :'+str(entries_incMC1))
        logging.info('inclusive MC(qqbar) entries :'+str(entries_incMC2))
        if ecms > 4230: logging.info('signal MC(D1(2420)) entries :'+str(entries_sigMC1))
        logging.info('signal MC(psi(3770)) entries :'+str(entries_sigMC2))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_incMC1 = TH1F('incMC1', 'inclusive MC: open charm', xbins, xmin, float(xmax))
    h_incMC2 = TH1F('incMC2', 'inclusive MC: qqbar', xbins, xmin, float(xmax))
    h_sigMC1 = TH1F('sigMC1', 'signal MC: D1(2420)', xbins, xmin, float(xmax))
    h_sigMC2 = TH1F('sigMC2', 'signal MC: psi(3770)', xbins, xmin, float(xmax))
    
    rm_Dpipi_fill(t_data, h_data, ecms, mode)
    if not ecms == 4600: set_histo_style(h_data, xtitle, ytitle, -1, 1, -1)
    else: set_histo_style(h_data, xtitle, ytitle, ymax, 1, -1)

    rm_Dpipi_fill(t_incMC1, h_incMC1, ecms, mode)
    set_histo_style(h_incMC1, xtitle, ytitle, -1, 2, -1)
    
    rm_Dpipi_fill(t_incMC2, h_incMC2, ecms, mode)
    set_histo_style(h_incMC2, xtitle, ytitle, -1, 3, -1)
    
    if ecms > 4230:
        rm_Dpipi_fill(t_sigMC1, h_sigMC1, ecms, mode)
        set_histo_style(h_sigMC1, xtitle, ytitle, -1, 4, -1)
    
    rm_Dpipi_fill(t_sigMC2, h_sigMC2, ecms, mode)
    set_histo_style(h_sigMC2, xtitle, ytitle, -1, 6, -1)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_incMC1.Scale(scale_factor(ecms, 'DD'))
    h_incMC2.Scale(scale_factor(ecms, 'qq'))
    if ecms > 4230: h_sigMC1.Scale(scale_factor(ecms, 'D1_2420'))
    h_sigMC2.Scale(scale_factor(ecms, 'psipp'))
    h_data.Draw('E1')
    hs = THStack('hs', 'Stacked')
    hs.Add(h_incMC1)
    hs.Add(h_incMC2)
    if ecms > 4230: hs.Add(h_sigMC1)
    hs.Add(h_sigMC2)
    hs.Draw('same')
    h_data.Draw('sameE1')

    if mode == 'before':
        legend = TLegend(0.5, 0.5, 0.8, 0.85)
    set_legend(legend, h_data, h_incMC1, h_incMC2, h_sigMC1, h_sigMC2, leg_title, ecms)
    legend.Draw()

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
    if mode == 'before':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/incMC/DD/'+str(ecms)+'/incMC_DD_'+str(ecms)+'_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/incMC/qq/'+str(ecms)+'/incMC_qq_'+str(ecms)+'_raw.root')
        if ecms > 4230: path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_raw.root')
        leg_title = str(ecms) + ' MeV'
        xmin = 1.8
        xmax = 2.2
        if ecms <= 4230: xmin, xmax = 1.8, 2.05
        xbins = int((xmax - xmin)/0.002)
        ymax = 1000
    plot(path, leg_title, ecms, xmin, xmax, xbins, mode, ymax)
