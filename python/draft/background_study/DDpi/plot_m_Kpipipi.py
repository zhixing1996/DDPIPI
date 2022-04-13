#!/usr/bin/env python
"""
Plot invariant mass of Kpipipi without kinematic fit
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
from tools import window
from tools import width, set_pub_style, set_prelim_style, name_axis, format_data_hist, set_arrow, set_pavetext, position_convert, set_legend, format_mc_hist
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    plot_m_Kpipipi.py

SYNOPSIS
    ./plot_m_Kpipipi.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def m_Kpipipi_fill(t, h, type):
    window_low = 1.86965 - window(ecms)/2.
    window_up = 1.86965 + window(ecms)/2.
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if not (t.m_rm_Dpipi > window_low and t.m_rm_Dpipi < window_up):
            continue
        if not (t.m_n_p == 0 and t.m_n_pbar == 0):
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
        if (t.m_m_pipi > 0.491036 and t.m_m_pipi < 0.503471) and abs(t.m_L_svf/t.m_Lerr_svf) > 2.: discarded = True
        if discarded: continue
        if type == 'Kpipipi1': h.Fill(t.m_m_Kpipipi1)
        if type == 'Kpipipi2': h.Fill(t.m_m_Kpipipi2)

def plot(data_path, pt_title, ecms, xmin, xmax, xbins, mode):
    try:
        f_data = TFile(data_path)
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    set_pub_style()
    set_prelim_style()
    mbc = TCanvas('mbc', 'mbc', 800, 600)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV/c^{2}'%content
    xtitle = 'M(K^{-}#pi_{d}^{+}#pi_{d}^{-}#pi^{+}) (GeV/c^{2})'
    h_Kpipipi1 = TH1F('Kpipipi1', 'Kpipipi1', xbins, xmin, float(xmax))
    format_data_hist(h_Kpipipi1)
    name_axis(h_Kpipipi1, xtitle, ytitle)
    m_Kpipipi_fill(t_data, h_Kpipipi1, 'Kpipipi1')
    
    h_Kpipipi2 = TH1F('Kpipipi2', 'Kpipipi2', xbins, xmin, float(xmax))
    format_data_hist(h_Kpipipi2)
    name_axis(h_Kpipipi2, xtitle, ytitle)
    m_Kpipipi_fill(t_data, h_Kpipipi2, 'Kpipipi2')
   
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    format_data_hist(h_data)
    name_axis(h_data, xtitle, ytitle)
    h_data.Add(h_Kpipipi1)
    h_data.Add(h_Kpipipi2)
    if mode == 'raw':
        ymax = 100
        h_data.GetYaxis().SetRangeUser(20, ymax)
    if mode == 'side_low':
        ymax = 100
        h_data.GetYaxis().SetRangeUser(0, ymax)
    if mode == 'side_up':
        ymax = 60
        h_data.GetYaxis().SetRangeUser(0, ymax)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_data.Draw('E1')

    leg = TLegend(0.65, 0.65, 0.8, 0.8)
    set_legend(leg, h_data, 'Data', pt_title)
    leg.Draw()

    mbc.SaveAs('./figs/m_Kpipipi_'+str(ecms)+'_'+mode+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = int(args[0])
    mode = args[1]

    if mode == 'raw':
        data_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw_before.root'
    if mode == 'side_low':
        data_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw_sidebandlow_before.root'
    if mode == 'side_up':
        data_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw_sidebandup_before.root'
    if mode == 'raw': pt_title = '(b)'
    if mode == 'side_low': pt_title = '(c)'
    if mode == 'side_up': pt_title = '(d)'
    xmin = 1.75
    xmax = 1.95
    xbins = 100
    plot(data_path, pt_title, ecms, xmin, xmax, xbins, mode)
