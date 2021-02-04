#!/usr/bin/env python
"""
Plot P(othertrks) vs P(othershws)
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-09-09 Thr 21:17]"

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
    scatter_p_othertrks_p_othershws.py

SYNOPSIS
    ./scatter_p_othertrks_p_othershws.py [ecms] [sample] [num_charm]

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

def fill(t, h, num_charm):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if t.m_n_p == 0 and t.m_n_pbar == 0 and t.m_charm == num_charm:
            h.Fill(t.m_p_othertrk, t.m_p_othershw)

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

def plot(path, leg_title, ecms, xmin, xmax, xbins, ymin, ymax, ybins, sample, num_charm):
    if sample == 'data':
        try:
            f_data = TFile(path[0])
            t_data = f_data.Get('save')
            entries_data = t_data.GetEntries()
            logging.info('data entries :'+str(entries_data))
        except:
            logging.error(path[0] + ' is invalid!')
            sys.exit()
    if sample == 'side':
        try:
            f_side1 = TFile(path[0])
            t_side1 = f_side1.Get('save')
            entries_side1 = t_side1.GetEntries()
            logging.info('data(side1) entries :'+str(entries_side1))
        except:
            logging.error(path[0] + ' is invalid!')
            sys.exit()
        try:
            f_side2 = TFile(path[1])
            t_side2 = f_side2.Get('save')
            entries_side2 = t_side2.GetEntries()
            logging.info('data(side2) entries :'+str(entries_side2))
        except:
            logging.error(path[1] + ' is invalid!')
            sys.exit()
        try:
            f_side3 = TFile(path[2])
            t_side3 = f_side3.Get('save')
            entries_side3 = t_side3.GetEntries()
            logging.info('data(side3) entries :'+str(entries_side3))
        except:
            logging.error(path[2] + ' is invalid!')
            sys.exit()
        try:
            f_side4 = TFile(path[3])
            t_side4 = f_side4.Get('save')
            entries_side4 = t_side4.GetEntries()
            logging.info('data(side4) entries :'+str(entries_side4))
        except:
            logging.error(path[3] + ' is invalid!')
            sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xtitle = 'P(OtherTrks) (GeV)'
    ytitle = 'P(OtherShws) (GeV)'

    if sample == 'data':
        h_data = TH2F('scatter_data', 'scatter plot of P(othertrks) and P(othershws)', xbins, xmin, xmax, ybins, ymin, ymax)
        set_histo_style(h_data, xtitle, ytitle)
        fill(t_data, h_data, num_charm)
        h_data.Draw('COLZ')
    if sample == 'sideband':
        h_side1 = TH2F('scatter_side1', 'scatter plot of P(othertrks) and P(othershws)', xbins, xmin, xmax, ybins, ymin, ymax)
        set_histo_style(h_side1, xtitle, ytitle)
        fill(t_side1, h_side1, num_charm)
        h_side2 = TH2F('scatter_side2', 'scatter plot of P(othertrks) and P(othershws)', xbins, xmin, xmax, ybins, ymin, ymax)
        set_histo_style(h_side2, xtitle, ytitle)
        fill(t_side2, h_side2, num_charm)
        h_side3 = TH2F('scatter_side3', 'scatter plot of P(othertrks) and P(othershws)', xbins, xmin, xmax, ybins, ymin, ymax)
        set_histo_style(h_side3, xtitle, ytitle)
        fill(t_side3, h_side3, num_charm)
        h_side4 = TH2F('scatter_side4', 'scatter plot of P(othertrks) and P(othershws)', xbins, xmin, xmax, ybins, ymin, ymax)
        set_histo_style(h_side4, xtitle, ytitle)
        fill(t_side4, h_side4, num_charm)
        h_side1.Add(h_side2)
        h_side1.Scale(0.5)
        h_side3.Add(h_side4)
        h_side3.Scale(0.25)
        h_side1.Add(h_side3, -1)
        h_side1.Draw('COLZ')
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    pt = TPaveText(0.65, 0.7, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(leg_title)
    pt.AddText(sample)

    mbc.SaveAs('./figs/scatter_p_othertrks_p_othershws_'+str(ecms)+'_'+sample+'_'+str(num_charm)+'.pdf')

    raw_input('Press <Enter> to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<3:
        usage()
        sys.exit()
    ecms = int(args[0])
    sample = args[1]
    num_charm = int(args[2])

    path = []
    if sample == 'data':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_after.root')
    if sample == 'sideband':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side1_after.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side2_after.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side3_after.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side4_after.root')
    leg_title = str(ecms) + ' MeV'
    xmin = 0
    xmax = 3
    xbins = 25
    ymin = 0
    ymax = 1.5
    ybins = 25
    plot(path, leg_title, ecms, xmin, xmax, xbins, ymin, ymax, ybins, sample, num_charm)
