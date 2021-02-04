#!/usr/bin/env python
"""
Plot VrVz of selected tracks
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

TGaxis.SetMaxDigits(2)

def usage():
    sys.stdout.write('''
NAME
    plot_Vr_Vz.py

SYNOPSIS
    ./plot_Vr_Vz.py [ecms]

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

def Vr_Vz_count(t, h_Vr, h_Vz):
    count = 0
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        h_Vr.Fill(t.m_Vr_pionp)
        h_Vr.Fill(t.m_Vr_pionm)
        h_Vr.Fill(t.m_Vr_lepp)
        h_Vr.Fill(t.m_Vr_lepm)
        h_Vz.Fill(t.m_Vz_pionp)
        h_Vz.Fill(t.m_Vz_pionm)
        h_Vz.Fill(t.m_Vz_lepp)
        h_Vz.Fill(t.m_Vz_lepm)
        if (t.m_Vr_pionp > 0.55 and t.m_Vr_pionm > 0.55 and t.m_Vr_lepp > 0.55 and t.m_Vr_lepm > 0.55):
            continue
        if (t.m_Vz_pionp > 3 and t.m_Vz_pionm > 3 and t.m_Vz_lepp > 3 and t.m_Vz_lepm > 3):
            continue
        count += 1
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
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetTitleOffset(0.8)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleOffset(0.8)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetLineColor(color)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.1)
    mbc.SetRightMargin(0.1)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.1)

def plot(path, leg_title, ecms):
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

    mbc = TCanvas('mbc', 'mbc', 1200, 600)
    set_canvas_style(mbc)
    mbc.Divide(2, 1)
    ytitle = 'Entries'
    xtitle_Vr = 'V_{xy} (cm)'
    xtitle_Vz = 'V_{z} (cm)'
    h_data_Vr = TH1F('data_Vr', 'data_Vr', 140, 0, 1)
    h_data_Vz = TH1F('data_Vz', 'data_Vz', 200, 0, 10)
    h_JPIPI_Vr = TH1F('JPIPI_Vr', 'JPIPI_Vr', 140, 0, 1)
    h_JPIPI_Vz = TH1F('JPIPI_Vz', 'JPIPI_Vz', 200, 0, 10)
    
    set_histo_style(h_data_Vr, xtitle_Vr, ytitle, 1, -1)
    set_histo_style(h_data_Vz, xtitle_Vz, ytitle, 1, -1)
    N_data = Vr_Vz_count(t_data, h_data_Vr, h_data_Vz)

    set_histo_style(h_JPIPI_Vr, xtitle_Vr, ytitle, 2, 3004)
    set_histo_style(h_JPIPI_Vz, xtitle_Vz, ytitle, 2, 3004)
    N_JPIPI = Vr_Vz_count(t_JPIPI, h_JPIPI_Vr, h_JPIPI_Vz)
    
    mbc.cd(1)
    h_JPIPI_Vr.Scale(0.008)
    h_data_Vr.Draw('E1')
    h_JPIPI_Vr.Draw('same')
    h_data_Vr.Draw('sameE1')

    legend_Vr = TLegend(0.17, 0.65, 0.37, 0.85)
    set_legend(legend_Vr, h_data_Vr, h_JPIPI_Vr, leg_title)
    legend_Vr.Draw()

    mbc.cd(2)
    h_JPIPI_Vz.Scale(0.008)
    h_data_Vz.Draw('E1')
    h_JPIPI_Vz.Draw('same')
    h_data_Vz.Draw('sameE1')

    legend_Vz = TLegend(0.17, 0.65, 0.37, 0.85)
    set_legend(legend_Vz, h_data_Vz, h_JPIPI_Vz, leg_title)
    legend_Vz.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    mbc.SaveAs('./figs/VrVz_'+str(ecms)+'.pdf')

    eff_data = float(N_data)/entries_data
    eff_JPIPI = float(N_JPIPI)/entries_JPIPI
    eff_data_err = sqrt(eff_data*(1 - eff_data)/entries_data)
    eff_JPIPI_err = sqrt(eff_JPIPI*(1 - eff_JPIPI)/entries_JPIPI)
    f = eff_data/eff_JPIPI
    f_err = sqrt(f**2*(eff_data_err**2/eff_data**2 + eff_JPIPI_err**2/eff_JPIPI**2))
    sys_err = abs(1 - f) + f_err
    print 'factor VrVz: ' + str(f) + ', Delta_f/sigma_f: ' + str(abs(1 - f)/f_err)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    with open('./txts/f_VrVz.txt', 'w') as f_out:
        f_out.write(str(f) + '\n')
    
    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700]
    with open('./txts/sys_err_VrVz.txt', 'w') as f_out:
        for ecm in ecms:
            out = str(ecm/1000.) + '\t' + str(round(sys_err*100, 2)) + '\n'
            f_out.write(out)

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/groups/cal/dedx/$USER/bes/PipiJpsi/run/pipi_jpsi/anaroot/data/' + str(ecms) + '/data_' + str(ecms) + '_signal.root')
    path.append('/besfs5/groups/cal/dedx/$USER/bes/PipiJpsi/run/pipi_jpsi/anaroot/mc/JPIPI/' + str(ecms) + '/mc_JPIPI_' + str(ecms) + '_signal.root')
    leg_title = str(ecms) + ' MeV'
    plot(path, leg_title, ecms)
