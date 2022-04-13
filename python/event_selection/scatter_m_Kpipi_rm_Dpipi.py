#!/usr/bin/env python
"""
Plot scatter plot of M(Kpipi) and RM(Dpipi)
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-12-24 Thu 11:18]"

from ROOT import *
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    scatter_m_Kpipi_rm_Dpipi.py

SYNOPSIS
    ./scatter_m_Kpipi_rm_Dpipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2020
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h.Fill(t.m_rawm_D, t.m_rm_Dpipi)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.06)
    h.GetXaxis().SetTitleOffset(1.)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetLabelSize(0.05)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(0.9)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().CenterTitle()
    h.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, leg_title, ecms, xmin, xmax, ymin, ymax, bins):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xtitle = 'M(K^{-}#pi^{+}#pi^{+}) (GeV)'
    ytitle = 'RM(D^{+}#pi_{0}^{+}#pi_{0}^{-}) (GeV)'

    h_data = TH2F('scatter_data', 'scatter plot of M(Kpipi) and Rm(Dpipi)', bins, xmin, xmax, bins, ymin, ymax)
    set_histo_style(h_data, xtitle, ytitle)
    fill(t_data, h_data)
    if ecms == 4230: h_data.Draw('scat=2')
    elif ecms == 4420: h_data.Draw('scat=0.2')
    else: h_data.Draw('COLZ')

    pt = TPaveText(0.75, 0.75, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(leg_title)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/scatter_m_Kpipi_rm_Dpipi_'+str(ecms)+'.pdf')

    raw_input('Press <Enter> to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw.root')
    leg_title = str(ecms) + ' MeV'
    if ecms == 4230: leg_title = '(a)'
    if ecms == 4420: leg_title = '(b)'
    # xmin = 1.84
    # xmax = 1.89
    # ymin = 1.84
    # ymax = 1.89
    # ymin = 0.8
    # ymax = 2.2
    xmin = 1.81
    xmax = 1.94
    ymin = 1.81
    ymax = 1.94
    bins = 80
    plot(path, leg_title, ecms, xmin, xmax, ymin, ymax, bins)
