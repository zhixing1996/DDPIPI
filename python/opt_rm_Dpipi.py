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
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetPaperSize(20,30)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadRightMargin(0.08)
gStyle.SetPadBottomMargin(0.18)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

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

def cal_significance(t1, t2, t3, t4, entries1, entries2, entries3, entries4, N, step, ratio1, ratio2, ratio3, ratio4, width):
    ymax = 0
    NEntry = 0
    B1_list = []
    B2_list = []
    B_list = []
    print 'Start of incMC1...'
    for i in xrange(N):
        B1 = 0
        for j in xrange(int(entries1*ratio1)):
            t1.GetEntry(j)
            if fabs(t1.m_rm_Dpipi - 1.86965) < (step + i*step) and fabs(t1.m_rawm_D - 1.86965) < width/2.:
                B1 = B1 + 1
        print 'processing: ' + str(i)
        B1_list.append(B1)
    print 'Start of incMC2...'
    for i in xrange(N):
        B2 = 0
        for j in xrange(int(entries2*ratio2)):
            t2.GetEntry(j)
            if fabs(t2.m_rm_Dpipi - 1.86965) < (step + i*step) and fabs(t2.m_rawm_D - 1.86965) < width/2.:
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
        for j in xrange(int(entries3*ratio3)):
            t3.GetEntry(j)
            if fabs(t3.m_rm_Dpipi - 1.86965) < (step + i*step) and fabs(t3.m_rawm_D - 1.86965) < width/2.:
                S1 = S1 + 1
        print 'processing: ' + str(i)
        S1_list.append(S1)
    print 'Start of sigMC2...'
    for i in xrange(N):
        S2 = 0
        for j in xrange(int(entries4*ratio4)):
            t4.GetEntry(j)
            if fabs(t4.m_rm_Dpipi - 1.86965) < (step + i*step) and fabs(t4.m_rawm_D - 1.86965) < width/2.:
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
    xtitle = 'RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})'
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

def plot(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, pt_title, ecms, ratio1, ratio2, ratio3, ratio4, arrow_left, arrow_bottom, arrow_right, arrow_top, width):
    try:
        f_incMC1 = TFile(incMC1_path)
        f_incMC2 = TFile(incMC2_path)
        f_sigMC1 = TFile(sigMC1_path)
        f_sigMC2 = TFile(sigMC2_path)
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
    step = (1.94 - M_Dplus)/xbins

    h_FOM, ientry, arrow_top = cal_significance(t_incMC1, t_incMC2, t_sigMC1, t_sigMC2, entries_incMC1, entries_incMC2, entries_sigMC1, entries_sigMC2, xbins, step, ratio1, ratio2, ratio3, ratio4, width)
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
    energy = args[0]

    if int(energy) == 4360:
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_raw.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_raw.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_raw.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_raw.root'
        pt_title = '(a)'
        ecms = 4360
        lum = 539.84
        XS1 = 17500.0
        XS2 = 1000.0
        XS3 = 41.8
        XS4 = 17.3
        GenNum = 500000
        GenNum1 = 9400000
        GenNum2 = 500000
        ratio1 = lum*XS1/GenNum1
        ratio2 = lum*XS2/GenNum2
        ratio3 = lum*XS3*0.0938/GenNum
        ratio4 = lum*XS4*0.0938/GenNum
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 29
        width = 0.02063
        plot(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, pt_title, ecms, ratio1, ratio2, ratio3, ratio4, arrow_left, arrow_bottom, arrow_right, arrow_top, width)

    if int(energy) == 4420:
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_raw.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_raw.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_raw.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_raw.root'
        pt_title = '(b)'
        ecms = 4420
        lum1 = 1028.89
        lum2 = 1073.56
        XS1 = 7000.0
        XS2 = 10200.0
        XS3 = 65.4
        XS4 = 23.8
        GenNum = 500000
        GenNum1 = 14000000
        GenNum2 = 40300000
        ratio1 = lum1*XS1/GenNum1
        ratio2 = lum1*XS2/GenNum2
        ratio3 = lum2*XS3*0.0938/GenNum
        ratio4 = lum2*XS4*0.0938/GenNum
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 29
        width = 0.02063
        plot(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, pt_title, ecms, ratio1, ratio2, ratio3, ratio4, arrow_left, arrow_bottom, arrow_right, arrow_top, width)

    if int(energy) == 4600:
        incMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_raw.root'
        incMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_raw.root'
        sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_raw.root'
        sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_raw.root'
        pt_title = '(c)'
        ecms = 4600
        lum = 566.93
        XS1 = 6000.0
        XS2 = 7800.0
        XS3 = 27.7
        XS4 = 7.2
        GenNum = 500000
        GenNum1 = 2800000
        GenNum2 = 3100000
        ratio1 = lum*XS1/GenNum1
        ratio2 = lum*XS2/GenNum2
        ratio3 = lum*XS3*0.0938/GenNum
        ratio4 = lum*XS4*0.0938/GenNum
        arrow_left = 15
        arrow_right = 15
        arrow_bottom = 0
        arrow_top = 22
        width = 0.02063
        plot(incMC1_path, incMC2_path, sigMC1_path, sigMC2_path, pt_title, ecms, ratio1, ratio2, ratio3, ratio4, arrow_left, arrow_bottom, arrow_right, arrow_top, width)

if __name__ == '__main__':
    main()
