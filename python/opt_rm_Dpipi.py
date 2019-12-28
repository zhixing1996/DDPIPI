#!/usr/bin/env python
"""
Optiomize recoiling mass of Dpipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-12 Tue 21:37]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH2F, TPaveText, TArrow
import sys, os
import logging
from math import *
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetPaperSize(20,30)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadRightMargin(0.08)
gStyle.SetPadBottomMargin(0.18)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    opt_rm_Dpipi.py

SYNOPSIS
    ./opt_rm_Dpipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    September 2019
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.04)

def set_arrow(arrow):
    arrow.SetLineWidth(0)
    arrow.SetLineColor(2)
    arrow.SetFillColor(2)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetTitleOffset(1.4)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.5)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetMarkerStyle(8)
    h.SetMarkerSize(0.65)
    h.SetLineColor(1)

def cal_significance(t1, t2, t3, t4, N, step, ecms):
    ymax = 0
    NEntry = 0
    B1_list = []
    B2_list = []
    B_list = []
    print 'Start of incMC1...'
    for i in xrange(N):
        B1 = 0
        for j in xrange(int(t1.GetEntries()*scale_factor(ecms, 'qq'))):
            t1.GetEntry(j)
            if fabs(t1.m_rm_Dpipi - 1.86965) < (step + i*step) and fabs(t1.m_rawm_D - 1.86965) < width(ecms)/2.:
                B1 = B1 + 1
        print 'processing: ' + str(i)
        B1_list.append(B1)
    print 'Start of incMC2...'
    for i in xrange(N):
        B2 = 0
        for j in xrange(int(t2.GetEntries()*scale_factor(ecms, 'DD'))):
            t2.GetEntry(j)
            if fabs(t2.m_rm_Dpipi - 1.86965) < (step + i*step) and fabs(t2.m_rawm_D - 1.86965) < width(ecms)/2.:
                B2 = B2 + 1
        print 'processing: ' + str(i)
        B2_list.append(B2)
    for i in xrange(N):
        B_list.append(B1_list[i]+B2_list[i])
    S1_list = []
    S2_list = []
    S_list = []
    print 'Start of sigMC1...'
    for i in xrange(N):
        S1 = 0
        for j in xrange(int(t3.GetEntries()*scale_factor(ecms, 'D1_2420'))):
            t3.GetEntry(j)
            if fabs(t3.m_rm_Dpipi - 1.86965) < (step + i*step) and fabs(t3.m_rawm_D - 1.86965) < width(ecms)/2.:
                S1 = S1 + 1
        print 'processing: ' + str(i)
        S1_list.append(S1)
    print 'Start of sigMC2...'
    for i in xrange(N):
        S2 = 0
        for j in xrange(int(t4.GetEntries()*scale_factor(ecms, 'psipp'))):
            t4.GetEntry(j)
            if fabs(t4.m_rm_Dpipi - 1.86965) < (step + i*step) and fabs(t4.m_rawm_D - 1.86965) < width(ecms)/2.:
                S2 = S2 + 1
        print 'processing: ' + str(i)
        S2_list.append(S2)
    for i in xrange(N):
        S_list.append(S1_list[i]+S2_list[i])
    Ratio_list = []
    for i in xrange(N):
        if B_list[i] == 0:
            significance = 0
        else:
            significance = S_list[i]/sqrt(S_list[i] + B_list[i])
        Ratio_list.append(significance)
        if significance > ymax:
            ymax = significance
            NEntry = i
    xmin = step
    xmax = N*step
    xtitle = '|RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})-m_{D^{-}}|'
    ytitle = '#frac{S}{#sqrt{S+B}}'
    h_FOM = TH2F('h_FOM', 'FOM', N, xmin, xmax, N, 0, ymax + 5)
    set_histo_style(h_FOM, xtitle, ytitle)
    for i in xrange(N):
        h_FOM.Fill(step + i*step, Ratio_list[i])
    return h_FOM, NEntry, ymax

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, pt_title, ecms, arrow_left, arrow_bottom, arrow_right, arrow_top):
    try:
        f_incMC1 = TFile(path[0])
        f_incMC2 = TFile(path[1])
        f_sigMC1 = TFile(path[2])
        f_sigMC2 = TFile(path[3])
        t_incMC1 = f_incMC1.Get('save')
        t_incMC2 = f_incMC2.Get('save')
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        entries_incMC1 = t_incMC1.GetEntries()
        entries_incMC2 = t_incMC2.GetEntries()
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        logging.info('inclusive MC (qqbar) entries :'+str(entries_incMC1))
        logging.info('inclusive MC (open charm) entries :'+str(entries_incMC2))
        logging.info('D1(2420) signal MC entries :'+str(entries_sigMC1))
        logging.info('psi(3770) signal MC entries :'+str(entries_sigMC2))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xbins = 150
    M_Dplus = 1.86965
    step = (1.91965 - M_Dplus)/xbins

    h_FOM, ientry, arrow_top = cal_significance(t_incMC1, t_incMC2, t_sigMC1, t_sigMC2, xbins, step, ecms)
    h_FOM.Draw()
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    arrow_left = ientry*step + step
    arrow_right = ientry*step + step
    arrow_bottom = 0.
    arrow = TArrow(arrow_left, arrow_bottom, arrow_right, arrow_top, 0.01,'>')
    set_arrow(arrow)
    arrow.Draw()

    pt = TPaveText(0.6, 0.8, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)

    mass_low = str(M_Dplus - (step + step*ientry))
    mass_up = str(M_Dplus + (step + step*ientry))
    window_width = str(2*(step + step*ientry))
    range = 'Recoiling mass window of D^{+}#pi^{+}#pi^{-}: : [' + mass_low + ', ' + mass_up + '] GeV/c2' + ' with mass window width: ' + window_width + ' GeV/c2'
    print range

    mbc.Update()
    mbc.SaveAs('./figs/opt_rm_Dpipi_'+str(ecms)+'.pdf')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = args[0]

    path = []
    if int(ecms) == 4360:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_raw.root')
        pt_title = '(a)'
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 29
        plot(path, pt_title, ecms, arrow_left, arrow_bottom, arrow_right, arrow_top)

    path = []
    if int(ecms) == 4420:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_raw.root')
        pt_title = '(b)'
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 29
        plot(path, pt_title, ecms, arrow_left, arrow_bottom, arrow_right, arrow_top)

    path = []
    if int(ecms) == 4600:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_raw.root')
        pt_title = '(c)'
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 22
        plot(path, pt_title, ecms, arrow_left, arrow_bottom, arrow_right, arrow_top)

if __name__ == '__main__':
    main()
