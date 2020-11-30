#!/usr/bin/env python
"""
Plot recoiling mass of tagged D
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-08 Fri 19:52]"

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
    plot_rm_D.py

SYNOPSIS
    ./plot_rm_D.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, ecms, h_list, title):
    legend.AddEntry(h_list[0], 'Open Charm')
    legend.AddEntry(h_list[1], 'q#bar{q}')
    legend.AddEntry(h_list[2], 'bhabha')
    legend.AddEntry(h_list[3], 'digamma')
    legend.AddEntry(h_list[4], 'dimu')
    legend.AddEntry(h_list[5], 'ditau')
    if ecms > 4316: legend.AddEntry(h_list[6], 'D_{1}(2420)D')
    legend.AddEntry(h_list[7], '#psi(3770)#pi^{+}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.06)

def rm_D_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h.Fill(t.m_rm_D)

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

def plot(incMC, sigMC, leg_title, ecms, scale, xmin, xmax, ymax):
    try:
        f_incMC1 = TFile(incMC[0])
        t_incMC1 = f_incMC1.Get('save')
        entries_incMC1 = t_incMC1.GetEntries()
        logging.info('inclusive MC(open charm) entries :'+str(entries_incMC1))

        if not ecms == 4600:
            f_incMC2 = TFile(incMC[1])
            t_incMC2 = f_incMC2.Get('save')
            entries_incMC2 = t_incMC2.GetEntries()
            logging.info('inclusive MC(qqbar) entries :'+str(entries_incMC2))

        if ecms > 4316:
            f_sigMC1 = TFile(sigMC[0])
            t_sigMC1 = f_sigMC1.Get('save')
            entries_sigMC1 = t_sigMC1.GetEntries()
            logging.info('signal MC(D1(2420)) entries :'+str(entries_sigMC1))

        f_sigMC2 = TFile(sigMC[1])
        t_sigMC2 = f_sigMC2.Get('save')
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('signal MC(psi(3770)) entries :'+str(entries_sigMC2))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = int((xmax - xmin)/0.005)
    content = int((xmax - xmin)/xbins * 1000)
    ytitle = 'Entries/%.1f MeV'%content
    xtitle = 'RM(D^{+})(GeV)'
    h_incMC1 = TH1F('incMC1', 'inclusive MC: open charm', xbins, xmin, float(xmax))
    h_incMC2 = TH1F('incMC2', 'inclusive MC: qqbar', xbins, xmin, float(xmax))
    h_incMC3 = TH1F('incMC3', 'inclusive MC: bhabha', xbins, xmin, float(xmax))
    h_incMC4 = TH1F('incMC4', 'inclusive MC: digamma', xbins, xmin, float(xmax))
    h_incMC5 = TH1F('incMC5', 'inclusive MC: dimu', xbins, xmin, float(xmax))
    h_incMC6 = TH1F('incMC6', 'inclusive MC: ditau', xbins, xmin, float(xmax))
    if ecms > 4316: h_sigMC1 = TH1F('sigMC1', 'signal MC: D1(2420)', xbins, xmin, float(xmax))
    h_sigMC2 = TH1F('sigMC2', 'signal MC: psi(3770)', xbins, xmin, float(xmax))
    
    set_histo_style(h_incMC1, xtitle, ytitle, ymax, 2, -1)
    set_histo_style(h_incMC2, xtitle, ytitle, ymax, 3, -1)
    set_histo_style(h_incMC3, xtitle, ytitle, ymax, 5, -1)
    set_histo_style(h_incMC4, xtitle, ytitle, ymax, 7, -1)
    set_histo_style(h_incMC5, xtitle, ytitle, ymax, 8, -1)
    set_histo_style(h_incMC6, xtitle, ytitle, ymax, 9, -1)
    if ecms > 4316: set_histo_style(h_sigMC1, xtitle, ytitle, ymax, 4, -1)
    set_histo_style(h_sigMC2, xtitle, ytitle, ymax, 6, -1)

    rm_D_fill(t_incMC1, h_incMC1)
    if not ecms == 4600: rm_D_fill(t_incMC2, h_incMC2)
    if ecms > 4316: rm_D_fill(t_sigMC1, h_sigMC1)
    rm_D_fill(t_sigMC2, h_sigMC2)
    
    h_incMC1.Scale(scale[0])
    h_incMC2.Scale(scale[1])
    if ecms > 4316: h_sigMC1.Scale(scale[2])
    h_sigMC2.Scale(scale[3])
    h_incMC1.GetYaxis().SetRangeUser(0, ymax)
    h_incMC1.Draw()
    hs = THStack('hs', 'Stacked')
    hs.Add(h_incMC2)
    hs.Add(h_incMC1)
    if ecms > 4316: hs.Add(h_sigMC1)
    hs.Add(h_sigMC2)
    hs.Draw('same')

    if ecms > 4316: h_list = [h_incMC1, h_incMC2, h_incMC3, h_incMC4, h_incMC5, h_incMC6, h_sigMC1, h_sigMC2]
    else: h_list = [h_incMC1, h_incMC2, h_incMC3, h_incMC4, h_incMC5, h_incMC6, '', h_sigMC2]
    legend = TLegend(0.2, 0.3, 0.35, 0.85)
    set_legend(legend, ecms, h_list, leg_title)
    legend.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    mbc.SaveAs('./figs/rm_D_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    incMC = []
    sigMC = []
    scale = []

    if ecms == 4230:
        incMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4230/incMC_DD_4230_before.root')
        incMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4230/incMC_qq_4230_before.root')
        sigMC.append('')
        sigMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4230/sigMC_psipp_4230_before.root')
        leg_title = str(ecms) + ' MeV'
        scale.append(scale_factor(ecms, 'DD'))
        scale.append(scale_factor(ecms, 'qq'))
        scale.append(0.)
        scale.append(scale_factor(ecms, 'psipp'))
        xmin = 2.15
        xmax = 2.36
        ymax = 30
        plot(incMC, sigMC, leg_title, ecms, scale, xmin, xmax, ymax)

    if ecms == 4360:
        incMC.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_before.root')
        incMC.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_before.root')
        sigMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_before.root')
        sigMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_before.root')
        leg_title = str(ecms) + ' MeV'
        scale.append(scale_factor(ecms, 'DD'))
        scale.append(scale_factor(ecms, 'qq'))
        scale.append(scale_factor(ecms, 'D1_2420'))
        scale.append(scale_factor(ecms, 'psipp'))
        xmin = 2.15
        xmax = 2.5
        ymax = 80
        plot(incMC, sigMC, leg_title, ecms, scale, xmin, xmax, ymax)

    if ecms == 4420:
        incMC.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_before.root')
        incMC.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_before.root')
        sigMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_before.root')
        sigMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_before.root')
        leg_title = str(ecms) + ' MeV'
        scale.append(scale_factor(ecms, 'DD'))
        scale.append(scale_factor(ecms, 'qq'))
        scale.append(scale_factor(ecms, 'D1_2420'))
        scale.append(scale_factor(ecms, 'psipp'))
        xmin = 2.15
        xmax = 2.55
        ymax = 250
        plot(incMC, sigMC, leg_title, ecms, scale, xmin, xmax, ymax)

    if ecms == 4600:
        incMC.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_before.root')
        sigMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_before.root')
        sigMC.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_before.root')
        leg_title = str(ecms) + ' MeV'
        scale.append(scale_factor(ecms, 'DD'))
        scale.append(scale_factor(ecms, 'qq'))
        scale.append(scale_factor(ecms, 'D1_2420'))
        scale.append(scale_factor(ecms, 'psipp'))
        xmin = 2.05
        xmax = 2.75
        ymax = 70
        plot(incMC, sigMC, leg_title, ecms, scale, xmin, xmax, ymax)
