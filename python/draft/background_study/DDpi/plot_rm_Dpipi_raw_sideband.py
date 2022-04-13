#!/usr/bin/env python
"""
Plot recoiling mass of tagged D, pi+, and pi- in sideband region
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
from tools import luminosity
from tools import width, set_pub_style, set_prelim_style, name_axis, format_data_hist, set_arrow, set_pavetext, position_convert, set_legend, format_mc_hist
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    plot_rm_Dpipi_raw_sideband.py

SYNOPSIS
    ./plot_rm_Dpipi_raw_sideband.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_legend(legend, h1, h2, h3, title, ecms):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'e^{+}e^{-}#rightarrow #pi^{+}#pi^{-}D^{+}D^{-}')
    legend.AddEntry(h3, 'e^{+}e^{-}#rightarrow D^{0}D^{-}#pi^{+}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    if ecms > 4320: legend.SetTextSize(0.07)
    if ecms < 4320: legend.SetTextSize(0.07)

def scale(ecms, mode):
    lum = luminosity(ecms)
    with open('../../../fit_xs/txts/xs_total_round2_plot.txt', 'r') as f:
        for line in f.readlines():
            fargs3 = map(float, line.strip().split())
            if ecms == int(fargs3[0]*1000):
                xs = fargs3[1]
    if mode == 'DDPI':
        if ecms == 4230:
            xs = 31.79
        if ecms == 4420:
            xs = 670.75
        if ecms == 4600:
            xs = 131.56
        if ecms == 4840:
            xs = 52.
    N = 50000
    if not mode == 'DDPI':
        if ecms == 4420 or ecms == 4230:
            N = 100000
    if mode == 'DDPI':
        if ecms == 4420 or ecms == 4230:
            N = 500000
        if ecms == 4600:
            N = 250000
    return lum*xs/N

def rm_Dpipi_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
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
        if not discarded: h.Fill(t.m_rm_Dpipi)

def plot(path, pt_title, ecms, xmin, xmax, xbins, ymax, mode):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()
    try:
        f_DDPIPI = TFile(path[1])
        t_DDPIPI = f_DDPIPI.Get('save')
        entries_DDPIPI = t_DDPIPI.GetEntries()
        logging.info('DDPIPI entries :'+str(entries_DDPIPI))
    except:
        logging.error(path[1] + ' is invalid!')
        sys.exit()
    try:
        f_DDPI = TFile(path[2])
        t_DDPI = f_DDPI.Get('save')
        entries_DDPI = t_DDPI.GetEntries()
        logging.info('DDPI entries :'+str(entries_DDPI))
    except:
        logging.error(path[2] + ' is invalid!')
        sys.exit()

    set_pub_style()
    set_prelim_style()
    mbc = TCanvas('mbc', 'mbc', 800, 600)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV/c^{2}'%content
    xtitle = 'RM(D^{+}#pi_{d}^{+}#pi_{d}^{-}) (GeV/c^{2})'

    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    format_data_hist(h_data)
    name_axis(h_data, xtitle, ytitle)
    rm_Dpipi_fill(t_data, h_data)
    
    h_DDPIPI = TH1F('DDPIPI', 'DDPIPI', xbins, xmin, float(xmax))
    format_mc_hist(h_DDPIPI, 2)
    rm_Dpipi_fill(t_DDPIPI, h_DDPIPI)
    
    h_DDPI = TH1F('DDPI', 'DDPI', xbins, xmin, float(xmax))
    format_mc_hist(h_DDPI, 3)
    rm_Dpipi_fill(t_DDPI, h_DDPI)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    F_DDPIPI = scale(ecms, 'DDPIPI')
    F_DDPI = scale(ecms, 'DDPI')
    h_DDPIPI.Scale(F_DDPIPI)
    h_DDPI.Scale(F_DDPI)
    h_data.GetYaxis().SetRangeUser(0, ymax)
    h_data.Draw('E1')
    hs = THStack('hs', 'Stacked')
    hs.Add(h_DDPIPI)
    hs.Add(h_DDPI)
    hs.Draw('same')
    h_data.Draw('sameE1')

    if ecms > 4320 and mode == 'before': legend = TLegend(0.2, 0.25, 0.5, 0.55)
    elif ecms > 4320 and mode == 'after': legend = TLegend(0.2, 0.22, 0.5, 0.52)
    elif ecms > 4320: legend = TLegend(0.2, 0.25, 0.5, 0.55)
    elif ecms < 4320: legend = TLegend(0.2, 0.2, 0.55, 0.4)
    set_legend(legend, h_data, h_DDPIPI, h_DDPI, pt_title, ecms)
    legend.Draw()

    mbc.SaveAs('./figs/rm_Dpipi_'+str(ecms)+'_raw_sideband_' + mode + '.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = int(args[0])
    mode = args[1]

    path = []
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_sideband_' + mode + '.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPIinc/'+str(ecms)+'/sigMC_D_D_PI_PI_inc_'+str(ecms)+'_raw_sideband_' + mode + '.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPI/'+str(ecms)+'/sigMC_D_D_PI_'+str(ecms)+'_raw_sideband_' + mode + '.root')
    if ecms == 4420 and mode == 'before': pt_title = '(a)'
    elif ecms == 4420 and mode == 'after': pt_title = '(c)'
    else: pt_title = str(ecms) + ' MeV'
    xmin = 1.75
    xmax = 1.95
    xbins = 100
    if ecms == 4840: ymax = 550
    if ecms == 4420: ymax = 700
    if ecms == 4600: ymax = 550
    if ecms == 4230: ymax = 320
    plot(path, pt_title, ecms, xmin, xmax, xbins, ymax, mode)
