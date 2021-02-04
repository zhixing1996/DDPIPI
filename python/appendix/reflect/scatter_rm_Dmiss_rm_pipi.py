#!/usr/bin/env python
"""
Plot invariant mass of D0pip vs invariant mass of Dmpip
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-09-29 Tue 14:05]"

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
    scatter_rm_Dmiss_rm_pipi.py

SYNOPSIS
    ./scatter_rm_Dmiss_rm_pipi.py [ecms] [charm]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    September 2020
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def fill(t, h, charm):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if t.m_rm_pipi < 3.79 and t.m_charm != charm:
            continue
        h.Fill(t.m_rm_Dmiss, t.m_rm_pipi)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.06)
    h.GetXaxis().SetTitleOffset(1.)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(1.)
    h.GetYaxis().SetLabelOffset(0.01)
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

def plot(path, leg_title, ecms, xmin, xmax, ymin, ymax, bins, charm):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()
    try:
        f_side1 = TFile(path[1])
        t_side1 = f_side1.Get('save')
        entries_side1 = t_side1.GetEntries()
        logging.info('data(side1) entries :'+str(entries_side1))
    except:
        logging.error(path[1] + ' is invalid!')
        sys.exit()
    try:
        f_side2 = TFile(path[2])
        t_side2 = f_side2.Get('save')
        entries_side2 = t_side2.GetEntries()
        logging.info('data(side2) entries :'+str(entries_side2))
    except:
        logging.error(path[2] + ' is invalid!')
        sys.exit()
    try:
        f_side3 = TFile(path[3])
        t_side3 = f_side3.Get('save')
        entries_side3 = t_side3.GetEntries()
        logging.info('data(side3) entries :'+str(entries_side3))
    except:
        logging.error(path[3] + ' is invalid!')
        sys.exit()
    try:
        f_side4 = TFile(path[4])
        t_side4 = f_side4.Get('save')
        entries_side4 = t_side4.GetEntries()
        logging.info('data(side4) entries :'+str(entries_side4))
    except:
        logging.error(path[4] + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xtitle = 'RM(D_{miss}^{-}) (GeV)'
    ytitle = 'RM(#pi_{0}^{+}#pi_{0}^{-}) (GeV)'

    h_data = TH2F('scatter_data', 'scatter plot of M(Dpi) and M(Dmisspi)', bins, xmin, xmax, bins, ymin, ymax)
    set_histo_style(h_data, xtitle, ytitle)
    fill(t_data, h_data, charm)
    h_side1 = TH2F('scatter_side1', 'scatter plot of M(Dpi) and M(Dmisspi)', bins, xmin, xmax, bins, ymin, ymax)
    set_histo_style(h_side1, xtitle, ytitle)
    fill(t_side1, h_side1, charm)
    h_side2 = TH2F('scatter_side2', 'scatter plot of M(Dpi) and M(Dmisspi)', bins, xmin, xmax, bins, ymin, ymax)
    set_histo_style(h_side2, xtitle, ytitle)
    fill(t_side2, h_side2, charm)
    h_side3 = TH2F('scatter_side3', 'scatter plot of M(Dpi) and M(Dmisspi)', bins, xmin, xmax, bins, ymin, ymax)
    set_histo_style(h_side3, xtitle, ytitle)
    fill(t_side3, h_side3, charm)
    h_side4 = TH2F('scatter_side4', 'scatter plot of M(Dpi) and M(Dmisspi)', bins, xmin, xmax, bins, ymin, ymax)
    set_histo_style(h_side4, xtitle, ytitle)
    fill(t_side4, h_side4, charm)
    h_side1.Add(h_side2)
    h_side1.Scale(0.5)
    h_side3.Add(h_side4)
    h_side3.Scale(0.25)
    h_side1.Add(h_side3, -1)
    h_data.Add(h_side1, -1)
    h_data.Draw('COLZ')

    pt = TPaveText(0.55, 0.7, 0.75, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(leg_title)
    if charm == 1: pt.AddText('D_{tag}^{+}')
    if charm == -1: pt.AddText('D_{tag}^{-}')

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/scatter_rm_Dmiss_rm_pipi_'+str(ecms)+'_'+str(charm)+'.pdf')

    raw_input('Press <Enter> to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = int(args[0])
    charm = int(args[1])

    path = []
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_after.root')
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side1_after.root')
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side2_after.root')
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side3_after.root')
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side4_after.root')
    leg_title = str(ecms) + ' MeV'
    xmin = 2.2
    xmax = 2.6
    ymin = 3.79
    ymax = 4.12
    bins = 50
    plot(path, leg_title, ecms, xmin, xmax, ymin, ymax, bins, charm)
