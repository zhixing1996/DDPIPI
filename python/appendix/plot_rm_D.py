#!/usr/bin/env python
"""
Plot recoiling mass of tagged D and missed D
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-28 Thu 00:33]"

import ROOT
from ROOT import *
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

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'signal: RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})')
    legend.AddEntry(h2, 'sideband: RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.06)

def rm_Dpipi_fill(t1, t2, h1, h2, ecms):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        discarded = False
        for iTrk in range(3):
            if t1.m_Vxy_Dtrks[iTrk] > 0.4:
                discarded = True
            if t1.m_Vz_Dtrks[iTrk] > 3.0:
                discarded = True
            if t1.m_cos_theta_Dtrks[iTrk] > 0.93:
                discarded = True
        if not discarded: h1.Fill(t1.m_rm_D)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        discarded = False
        for iTrk in range(3):
            if t2.m_Vxy_Dtrks[iTrk] > 0.4:
                discarded = True
            if t2.m_Vz_Dtrks[iTrk] > 3.0:
                discarded = True
            if t2.m_cos_theta_Dtrks[iTrk] > 0.93:
                discarded = True
        if not discarded: h2.Fill(t2.m_rm_D)

def set_histo_style(h1, h2, xtitle, ytitle):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.06)
    h1.GetXaxis().SetTitleOffset(1.1)
    h1.GetXaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitleSize(0.06)
    h1.GetYaxis().SetTitleOffset(1.1)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetXaxis().CenterTitle()
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetYaxis().CenterTitle()
    h1.SetLineColor(1)
    h2.SetFillColor(kGreen)
    h2.SetLineColor(kGreen)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, leg_title, ecms, xmin, xmax, xbins):
    try:
        f_data = TFile(path[0])
        f_sideband = TFile(path[1])
        t_data = f_data.Get('save')
        t_sideband = f_sideband.Get('save')
        entries_data = t_data.GetEntries()
        entries_sideband = t_sideband.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('sideband entries :'+str(entries_sideband))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Entries/%.1f MeV'%content
    xtitle = 'RM(D^{+}) (GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_sideband = TH1F('sideband', 'sideband', xbins, xmin, float(xmax))
    
    set_histo_style(h_data, h_sideband, xtitle, ytitle)
    rm_Dpipi_fill(t_data, t_sideband, h_data, h_sideband, ecms)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sideband.Scale(0.5)
    h_data.Draw('E1')
    h_sideband.Draw('same')
    h_data.Draw('sameE1')

    legend = TLegend(0.17, 0.65, 0.37, 0.85)
    set_legend(legend, h_data, h_sideband, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_D_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = args[0]

    path = []
    if int(ecms) == 4360:
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_after.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_sideband.root')
        leg_title = '(a)'
        xmin = 2.14
        xmax = 2.49
        xbins = 140
        plot(path, leg_title, ecms, xmin, xmax, xbins)
    elif int(ecms) == 4420:
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_after.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_sideband.root')
        leg_title = '(b)'
        xmin = 2.14
        xmax = 2.55
        xbins = 164
        plot(path, leg_title, ecms, xmin, xmax, xbins)
    elif int(ecms) == 4600:
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_after.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_sideband.root')
        leg_title = '(c)'
        xmin = 2.14
        xmax = 2.72
        xbins = 232
        plot(path, leg_title, ecms, xmin, xmax, xbins)
    else:
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + ecms + '/data_' + ecms + '_after.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + ecms + '/data_' + ecms + '_sideband.root')
        leg_title = ecms + ' MeV'
        xmin = 2.14
        xmax = 2.82
        xbins = int((xmax - xmin)/0.005)
        plot(path, leg_title, ecms, xmin, xmax, xbins)
