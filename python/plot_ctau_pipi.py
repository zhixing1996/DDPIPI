#!/usr/bin/env python
"""
Plot ctau of selected piplus and piminus after second vertex fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-11 Mon 23:37]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    plot_ctau_pipi.py

SYNOPSIS
    ./plot_ctau_pipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_arrow(arrow):
    arrow.SetLineWidth(0)
    arrow.SetLineColor(1)
    arrow.SetFillColor(1)

def set_legend(legend, h1, h2, h3, h4, title):
    legend.AddEntry(h1, 'D_{1}(2420)D')
    legend.AddEntry(h2, '#psi(3770)#pi^{+}#pi^{-}')
    legend.AddEntry(h3, 'open charm')
    legend.AddEntry(h4, 'q#bar{q}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def ctau_fill(t1, t2, t3, t4, h1, h2, h3, h4):
    for i in xrange(t1.GetEntries()):
        t1.GetEntry(i)
        if (t1.m_m_pipi > 0.491036 and t1.m_m_pipi < 0.503471):
            h1.Fill(t1.m_ctau_svf)
    for i in xrange(t2.GetEntries()):
        t2.GetEntry(i)
        if (t2.m_m_pipi > 0.491036 and t2.m_m_pipi < 0.503471):
            h2.Fill(t2.m_ctau_svf)
    for i in xrange(t3.GetEntries()):
        t3.GetEntry(i)
        if (t3.m_m_pipi > 0.491036 and t3.m_m_pipi < 0.503471):
            h3.Fill(t3.m_ctau_svf)
    for i in xrange(t4.GetEntries()):
        t4.GetEntry(i)
        if (t4.m_m_pipi > 0.491036 and t4.m_m_pipi < 0.503471):
            h4.Fill(t4.m_ctau_svf)

def set_histo_style(h1, h2, h3, h4, xtitle, ytitle):
    h3.GetXaxis().SetNdivisions(509)
    h3.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h3.SetLineWidth(2)
    h4.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h3.SetStats(0)
    h4.SetStats(0)
    h3.GetXaxis().SetTitleSize(0.04)
    h3.GetXaxis().SetTitleOffset(1.4)
    h3.GetXaxis().SetLabelOffset(0.01)
    h3.GetYaxis().SetTitleSize(0.04)
    h3.GetYaxis().SetTitleOffset(1.5)
    h3.GetYaxis().SetLabelOffset(0.01)
    h3.GetXaxis().SetTitle(xtitle)
    h3.GetXaxis().CenterTitle()
    h3.GetYaxis().SetTitle(ytitle)
    h3.GetYaxis().CenterTitle()
    h3.GetYaxis().SetRangeUser(0, 50)
    h1.SetLineColor(1)
    h2.SetLineColor(2)
    h3.SetLineColor(3)
    h4.SetLineColor(4)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(sigMC1_path, sigMC2_path, incMC1_path, incMC2_path, leg_title, ecms, xmax, arrow_left, arrow_right, arrow_bottom, arrow_top):
    try:
        f_sigMC1 = TFile(sigMC1_path)
        f_sigMC2 = TFile(sigMC2_path)
        f_incMC1 = TFile(incMC1_path)
        f_incMC2 = TFile(incMC2_path)
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        t_incMC1 = f_incMC1.Get('save')
        t_incMC2 = f_incMC2.Get('save')
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        entries_incMC1 = t_incMC1.GetEntries()
        entries_incMC2 = t_incMC2.GetEntries()
        logging.info('signal MC(D1(2420)D) entries :'+str(entries_sigMC1))
        logging.info('signal MC(psi(3770)) entries :'+str(entries_sigMC2))
        logging.info('inclusive MC(open charm) entries :'+str(entries_incMC1))
        logging.info('inclusive MC(qqbar) entries :'+str(entries_incMC2))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = -2.
    xbins = 75
    ytitle = "Events"
    xtitle = "c#tau_{#pi^{+}_{0}#pi^{-}_{0}}"
    h_sigMC1 = TH1F('sigMC1', 'D1(2420)', xbins, xmin, xmax)
    h_sigMC2 = TH1F('sigMC2', 'psi(3770)', xbins, xmin, xmax)
    h_incMC1 = TH1F('incMC1', 'open charm', xbins, xmin, xmax)
    h_incMC2 = TH1F('incMC2', 'qqbar', xbins, xmin, xmax)

    set_histo_style(h_sigMC1, h_sigMC2, h_incMC1, h_incMC2, xtitle, ytitle)
    ctau_fill(t_sigMC1, t_sigMC2, t_incMC1, t_incMC2, h_sigMC1, h_sigMC2, h_incMC1, h_incMC2)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_sigMC1.Scale(0.04)
    h_sigMC2.Scale(0.04)
    h_incMC1.Draw('')
    h_sigMC1.Draw('same')
    h_sigMC2.Draw('same')
    h_incMC2.Draw('same')

    arrow = TArrow(arrow_left, arrow_bottom, arrow_right, arrow_top, 0.01, '<')
    set_arrow(arrow)
    arrow.Draw()

    legend = TLegend(0.45, 0.6, 0.82, 0.8)
    set_legend(legend, h_sigMC1, h_sigMC2, h_incMC1, h_incMC2, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/ctau_pipi_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = args[0]

    if int(ecms) == 4360:
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_before.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_before.root'
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_before.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_before.root'
        leg_title = '(a)'
        xmax = 4.
        arrow_left = 0.5
        arrow_right = 0.5
        arrow_bottom = 0 
        arrow_top = 25
        plot(sigMC1_path, sigMC2_path, incMC1_path, incMC2_path, leg_title, ecms, xmax, arrow_left, arrow_right, arrow_bottom, arrow_top)

    if int(ecms) == 4420:
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_before.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_before.root'
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_before.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_before.root'
        leg_title = '(b)'
        xmax = 4.
        arrow_left = 0.5
        arrow_right = 0.5
        arrow_bottom = 0 
        arrow_top = 40
        plot(sigMC1_path, sigMC2_path, incMC1_path, incMC2_path, leg_title, ecms, xmax, arrow_left, arrow_right, arrow_bottom, arrow_top)

    if int(ecms) == 4600:
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_before.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_before.root'
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_before.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_before.root'
        leg_title = '(c)'
        xmax = 4.
        arrow_left = 0.5
        arrow_right = 0.5
        arrow_bottom = 0 
        arrow_top = 25
        plot(sigMC1_path, sigMC2_path, incMC1_path, incMC2_path, leg_title, ecms, xmax, arrow_left, arrow_right, arrow_bottom, arrow_top)
