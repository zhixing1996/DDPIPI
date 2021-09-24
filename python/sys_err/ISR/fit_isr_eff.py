#!/usr/bin/env python
"""
Plot invariant mass of tagged D without kinematic fit
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
from tools import pull_range
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_m_Kpipi.py

SYNOPSIS
    ./plot_m_Kpipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.04)

def pull_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h.Fill(t.pull)

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
    h.GetXaxis().SetLabelSize(0.04)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(1.1)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetLabelSize(0.04)
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

def plot(path, pt_title, ecms, xmin, xmax, xbins):
    try:
        f = TFile(path[0])
        t = f.Get('save')
        entries = t.GetEntries()
        logging.info('Sampled entries :'+str(entries))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    ytitle = 'Entries'
    xtitle = '#epsilon*(1+#delta)^{ISR}'
    h = TH1F('h', 'h', xbins, xmin, xmax)
    
    set_histo_style(h, xtitle, ytitle)
    pull_fill(t, h)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h.Draw()
    h.Fit('gaus')
    Gaus = h.GetFunction('gaus')
    mean = Gaus.GetParameter(1)
    mean_err = Gaus.GetParError(1)
    sigma = Gaus.GetParameter(2)
    sigma_err = Gaus.GetParError(2)

    pt = TPaveText(0.15, 0.6, 0.5, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)
    pt.AddText('#mu: ' + str(round(mean, 5)) + '#pm' + str(round(mean_err, 5)))
    pt.AddText('#sigma: ' + str(round(sigma, 5)) + '#pm' + str(round(sigma_err, 5)))
    pt.AddText('#sigma/#mu: ' + str(round(sigma/mean*100, 1)) + '%')
    if ecms == 4380: pt.AddText('old #epsilon*(1+#delta)^{ISR}: ' + str(round(0.197740875666, 5)))
    if ecms == 4390: pt.AddText('old #epsilon*(1+#delta)^{ISR}: ' + str(round(0.209832870851, 5)))
    if ecms == 4400: pt.AddText('old #epsilon*(1+#delta)^{ISR}: ' + str(round(0.199480295161, 5)))
    if ecms == 4420: pt.AddText('old #epsilon*(1+#delta)^{ISR}: ' + str(round(0.216992692342, 5)))
    if ecms == 4440: pt.AddText('old #epsilon*(1+#delta)^{ISR}: ' + str(round(0.214240073899, 5)))
    if ecms == 4575: pt.AddText('old #epsilon*(1+#delta)^{ISR}: ' + str(round(0.233814323177, 5)))

    mbc.SaveAs('./figs/isr_eff_'+str(ecms)+'.pdf')

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    with open('./txts/isr_eff_'+str(ecms)+'.txt', 'w') as f:
        f.write(str(round(round(sigma/mean*100, 1))) + '\n')

    # raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/sys_err/ISR/' + str(ecms) + '/isr_eff_' + str(ecms) + '.root')
    pt_title = str(ecms) + ' MeV'
    xbins, xmin, xmax = pull_range(ecms)
    plot(path, pt_title, ecms, xmin, xmax, xbins)
