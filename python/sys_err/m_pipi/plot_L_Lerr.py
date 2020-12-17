#!/usr/bin/env python
"""
Plot L/Lerr of selected piplus and piminus after second vertex fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-10-21 Thr 00:03]"

import ROOT
from ROOT import *
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    plot_L_Lerr.py

SYNOPSIS
    ./plot_L_Lerr.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    October 2020
\n''')

def set_legend(legend, h1, h2, title):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'e^{+}e^{-}#rightarrow#pi^{+}#pi^{-}J/#psi')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.06)

def L_Lerr_fill(t, h):
    count = 0
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h.Fill(t.m_L_svf/t.m_Lerr_svf)
        if abs(t.m_L_svf/t.m_Lerr_svf) < 2: count += 1
    return count

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

def plot(path, leg_title, ecms, xmin, xmax, xbins):
    try:
        f_data = TFile(path[0])
        f_JPIPI = TFile(path[1])
        t_data = f_data.Get('track')
        t_JPIPI = f_JPIPI.Get('track')
        entries_data = t_data.GetEntries()
        entries_JPIPI = t_JPIPI.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('JPIPI entries :'+str(entries_JPIPI))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    ytitle = 'Entries'
    xtitle = 'L/#Delta_{L}'
    h_data = TH1F('data', 'data', xbins, xmin, xmax)
    h_JPIPI = TH1F('JPIPI', 'JPIPI', xbins, xmin, xmax)
    
    set_histo_style(h_data, xtitle, ytitle, 1, -1)
    N_data = L_Lerr_fill(t_data, h_data)

    set_histo_style(h_JPIPI, xtitle, ytitle, 2, 3004)
    N_JPIPI = L_Lerr_fill(t_JPIPI, h_JPIPI)
    
    h_JPIPI.Scale(0.025)
    h_data.Draw('E1')
    h_JPIPI.Draw('same')
    h_data.Draw('sameE1')

    legend = TLegend(0.17, 0.65, 0.37, 0.85)
    set_legend(legend, h_data, h_JPIPI, leg_title)
    legend.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    mbc.SaveAs('./figs/L_Lerr_'+str(ecms)+'.pdf')

    eff_data = float(N_data)/entries_data
    eff_JPIPI = float(N_JPIPI)/entries_JPIPI
    eff_data_err = sqrt(eff_data*(1 - eff_data)/entries_data)
    eff_JPIPI_err = sqrt(eff_JPIPI*(1 - eff_JPIPI)/entries_JPIPI)
    
    sys_err = sqrt(eff_data_err**2/eff_data**2 + eff_JPIPI_err**2/eff_JPIPI**2)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    
    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700]
    with open('./txts/sys_err_m_pipi.txt', 'w') as f:
        for ecm in ecms:
            out = str(ecm/1000.) + '\t' + str(round(sys_err*100, 2)) + '\n'
            f.write(out)

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs/groups/cal/dedx/$USER/bes/PipiJpsi/run/pipi_jpsi/anaroot/data/' + str(ecms) + '/data_' + str(ecms) + '_signal.root')
    path.append('/besfs/groups/cal/dedx/$USER/bes/PipiJpsi/run/pipi_jpsi/anaroot/mc/JPIPI/' + str(ecms) + '/mc_JPIPI_' + str(ecms) + '_signal.root')
    leg_title = str(ecms) + ' MeV'
    xmin, xmax, xbins = -5., 5., 200
    plot(path, leg_title, ecms, xmin, xmax, xbins)
