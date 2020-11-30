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
from tools import width
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_rm_Dpipi.py

SYNOPSIS
    ./plot_rm_Dpipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h_data, title):
    legend.AddEntry(h_data, 'data')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.06)

def rm_Dpipi_fill(t, h, mode):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if abs(t.m_rawm_D - 1.86965) < width(ecms)/2. and t.m_n_p == 0 and t.m_n_pbar == 0:
            if not (t.m_n_othertrks <= 3 and t.m_n_othershws <= 6):
                continue
            discarded = False
            for iTrk in range(3):
                if abs(t.m_Vxy_Dtrks[iTrk]) > 0.55:
                    discarded = True
                if abs(t.m_Vz_Dtrks[iTrk]) > 3.0:
                    discarded = True
                if abs(t.m_cos_theta_Dtrks[iTrk]) > 0.93:
                    discarded = True
            if abs(t.m_Vxy_pip) > 0.55: discarded = True
            if abs(t.m_Vxy_pim) > 0.55: discarded = True
            if abs(t.m_Vz_pip) > 3.: discarded = True
            if abs(t.m_Vz_pim) > 3.: discarded = True
            if abs(t.m_cos_theta_pip) > 0.93: discarded = True
            if abs(t.m_cos_theta_pim) > 0.93: discarded = True
            if mode == 'bkg':
                # if (t.m_m_pipi > 0.491036 and t.m_m_pipi < 0.503471 and t.m_ctau_svf > 0.2) and not discarded: h.Fill(t.m_rm_Dpipi)
                if (t.m_m_pipi > 0.491036 and t.m_m_pipi < 0.503471 and abs(t.m_L_svf/t.m_Lerr_svf) > 2) and not discarded: h.Fill(t.m_rm_Dpipi)
            if mode == 'after':
                # if not (t.m_m_pipi > 0.491036 and t.m_m_pipi < 0.503471 and t.m_ctau_svf > 0.2) and not discarded: h.Fill(t.m_rm_Dpipi)
                if not (t.m_m_pipi > 0.491036 and t.m_m_pipi < 0.503471 and abs(t.m_L_svf/t.m_Lerr_svf) > 2) and not discarded: h.Fill(t.m_rm_Dpipi)

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

def plot(path, ecms, xmin, xmax, mode):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' path is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = 100
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Eentries/%.1f MeV'%content
    xtitle = 'RM(D^{+}#pi_{0}^{+}#pi_{0}^{-})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    set_histo_style(h_data, xtitle, ytitle, 1, -1)
    rm_Dpipi_fill(t_data, h_data, mode)
    
    h_data.Draw('E1')

    if mode == 'after': legend = TLegend(0.2, 0.72, 0.5, 0.85)
    if mode == 'bkg': legend = TLegend(0.2, 0.2, 0.5, 0.33)
    leg_title = str(ecms) + ' MeV'
    set_legend(legend, h_data, leg_title)
    legend.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
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
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_signal.root')
    xmin = 1.75
    xmax = 1.95
    plot(path, ecms, xmin, xmax, mode)
