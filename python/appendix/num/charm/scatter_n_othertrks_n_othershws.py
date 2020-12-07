#!/usr/bin/env python
"""
Plot N(othertrks) vs N(othershws)
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
    scatter_n_othertrks_n_othershws.py

SYNOPSIS
    ./scatter_n_othertrks_n_othershws.py [ecms] [sample] [num_charm]

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
            h.Fill(t.m_n_othertrks, t.m_n_othershws)

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
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('Entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xtitle = 'N(OtherTrks)'
    ytitle = 'N(OtherShws)'
    h_data = TH2F('scatter_data', 'scatter plot of N(othertrks) and N(othershws)', xbins, xmin, xmax, ybins, ymin, ymax)

    set_histo_style(h_data, xtitle, ytitle)
    fill(t_data, h_data, num_charm)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    if sample == 'sideband':
        h_data.Scale(0.5)
    h_data.Draw('COLZ')

    pt = TPaveText(0.65, 0.7, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(leg_title)
    pt.AddText(sample)

    mbc.SaveAs('./figs/scatter_n_othertrks_n_othershws_'+str(ecms)+'_'+sample+'_'+str(num_charm)+'.pdf')

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
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_before.root')
    if sample == 'sideband':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_sideband_before.root')
    leg_title = str(ecms) + ' MeV'
    xmin = 0
    xmax = 7
    xbins = 7
    ymin = 0
    ymax = 13
    ybins = 13
    plot(path, leg_title, ecms, xmin, xmax, xbins, ymin, ymax, ybins, sample, num_charm)
