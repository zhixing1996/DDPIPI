#!/usr/bin/env python
"""
Plot Vz of tracks
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-09-09 Thr 20:12]"

import ROOT
from ROOT import TCanvas, gStyle, TTree, THStack
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
from math import *
from tools import width, set_pub_style, set_prelim_style, name_axis, format_data_hist, set_arrow, set_pavetext, position_convert, set_legend, format_mc_hist
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    plot_Vz_trks.py

SYNOPSIS
    ./plot_Vz_trks.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    September 2019
\n''')

def set_legend(legend, h_data, h_sideband, title):
    legend.AddEntry(h_data, 'S sample')
    legend.AddEntry(h_sideband, 'B sample')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.07)

def Vz_trks_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if not (t.m_n_p == 0 and t.m_n_pbar == 0):
            continue
        if (abs(t.m_m_Kpipipi1-1.86483) < 0.01 or abs(t.m_m_Kpipipi2-1.86483) < 0.01): continue
        if (t.m_m_pipi > 0.491036 and t.m_m_pipi < 0.503471) and abs(t.m_L_svf/t.m_Lerr_svf) > 2.: continue
        for iTrk in range(3):
            h.Fill(t.m_Vz_Dtrks[iTrk])
        h.Fill(t.m_Vz_pip)
        h.Fill(t.m_Vz_pim)

def plot(path, ecms, xmin, xmax):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' path is invalid!')
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

    set_pub_style()
    set_prelim_style()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    mbc.SetLogy()
    xbins = 200
    content = (xmax - xmin)/xbins
    ytitle = 'Eentries/%.2f (cm)'%content
    xtitle = '|V_{z}| (cm)'

    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    format_data_hist(h_data)
    name_axis(h_data, xtitle, ytitle)
    Vz_trks_fill(t_data, h_data)
    
    h_side1 = TH1F('side1', 'side1', xbins, xmin, xmax)
    format_mc_hist(h_side1, 3)
    Vz_trks_fill(t_side1, h_side1)
    
    h_side2 = TH1F('side2', 'side2', xbins, xmin, xmax)
    format_mc_hist(h_side2, 3)
    Vz_trks_fill(t_side2, h_side2)
    
    h_side3 = TH1F('side3', 'side3', xbins, xmin, xmax)
    format_mc_hist(h_side3, 3)
    Vz_trks_fill(t_side3, h_side3)
    
    h_side4 = TH1F('side4', 'side4', xbins, xmin, xmax)
    format_mc_hist(h_side4, 3)
    Vz_trks_fill(t_side4, h_side4)
    
    h_side1.Add(h_side2)
    h_side1.Scale(0.5)
    h_side3.Add(h_side4)
    h_side3.Scale(0.25)
    h_side1.Add(h_side3, -1)
    h_data.Draw('E1')
    hs = THStack('hs', 'Stacked')
    hs.Add(h_side1)
    hs.Draw('same')
    h_data.Draw('sameE1')

    legend = TLegend(0.55, 0.6, 0.8, 0.85)
    if ecms == 4230: leg_title = '(b)'
    if ecms == 4420: leg_title = '(d)'
    if ecms == 4680: leg_title = '(f)'
    set_legend(legend, h_data, h_side1, leg_title)
    legend.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    mbc.SaveAs('./figs/Vz_trks_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_before.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side1_before.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side2_before.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side3_before.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side4_before.root')
    xmin = 0.
    xmax = 10.
    plot(path, ecms, xmin, xmax)
