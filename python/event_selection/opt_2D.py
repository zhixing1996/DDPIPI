#!/usr/bin/env python
"""
Optiomize invariant mass of Kpipi and recoiling mass of Dpipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-08-27 Thr 22:29]"

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
    opt_2D.py

SYNOPSIS
    ./opt_2D.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    August 2020
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetTitleOffset(1.15)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleOffset(1.15)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetMarkerStyle(8)
    h.SetMarkerSize(0.65)
    h.SetLineColor(1)

def cal_significance(t, ecms):
    if ecms > 4230:
        t1 = t[0]
        t2 = t[1]
        t3 = t[2]
        t4 = t[3]
    else:
        t1 = t[0]
        t2 = t[1]
        t3 = t[2]
    xbins, xmin, xmax = 75, 0.0, 0.09
    ybins, ymin, ymax = 75, 0.0, 0.09
    n_incMC1, n_incMC2, n_sigMC1, n_sigMC2 = 0, 0, 0, 0
    h_FOM = TH2F('h_FOM', 'h_FOM', xbins, xmin, xmax, ybins, ymin, ymax)
    xtitle = '|M(K^{+}#pi^{+}#pi^{-})-m_{D^{+}}| (GeV)'
    ytitle = '|RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})-m_{D^{-}}| (GeV)'
    set_histo_style(h_FOM, xtitle, ytitle)
    for xbin in xrange(xbins):
        for ybin in xrange(ybins):
            w_m_Kpipi_max = (xbin + 1) * (xmax - xmin) / float(xbins) + xmin
            w_rm_Dpipi_max = (ybin + 1) * (ymax - ymin) / float(ybins) + ymin
            m_D = 1.86965
            m_Kpipi_low = m_D - w_m_Kpipi_max/2.
            m_Kpipi_up = m_D + w_m_Kpipi_max/2.
            rm_Dpipi_low = m_D - w_rm_Dpipi_max/2.
            rm_Dpipi_up = m_D + w_rm_Dpipi_max/2.
            n_incMC1 = float(t1.GetEntries('(m_rawm_D > %.5f && m_rawm_D < %.5f) && (m_rm_Dpipi > %.5f && m_rm_Dpipi < %.5f)' %(m_Kpipi_low, m_Kpipi_up, rm_Dpipi_low, rm_Dpipi_up))) * scale_factor(ecms, 'qq')
            n_incMC2 = float(t2.GetEntries('(m_rawm_D > %.5f && m_rawm_D < %.5f) && (m_rm_Dpipi > %.5f && m_rm_Dpipi < %.5f)' %(m_Kpipi_low, m_Kpipi_up, rm_Dpipi_low, rm_Dpipi_up))) * scale_factor(ecms, 'DD')
            if ecms > 4230:
                n_sigMC1 = float(t3.GetEntries('(m_rawm_D > %.5f && m_rawm_D < %.5f) && (m_rm_Dpipi > %.5f && m_rm_Dpipi < %.5f)' %(m_Kpipi_low, m_Kpipi_up, rm_Dpipi_low, rm_Dpipi_up))) * scale_factor(ecms, 'D1_2420')
                n_sigMC2 = float(t4.GetEntries('(m_rawm_D > %.5f && m_rawm_D < %.5f) && (m_rm_Dpipi > %.5f && m_rm_Dpipi < %.5f)' %(m_Kpipi_low, m_Kpipi_up, rm_Dpipi_low, rm_Dpipi_up))) * scale_factor(ecms, 'psipp')
            else:
                n_sigMC1 = float(t3.GetEntries('(m_rawm_D > %.5f && m_rawm_D < %.5f) && (m_rm_Dpipi > %.5f && m_rm_Dpipi < %.5f)' %(m_Kpipi_low, m_Kpipi_up, rm_Dpipi_low, rm_Dpipi_up))) * scale_factor(ecms, 'psipp')
            if not (n_sigMC1 + n_sigMC2 + n_incMC1 + n_incMC2) == 0:
                if ecms > 4230: FOM = (n_sigMC1 + n_sigMC2)/sqrt(n_sigMC1 + n_sigMC2 + n_incMC1 + n_incMC2)
                else: FOM = n_sigMC1/sqrt(n_sigMC1 + n_incMC1 + n_incMC2)
                print '(xbin: %i/%i, ybin, %i/%i): M(Kpippi)(%5f), RM(Dpipi)(%5f), FOM(%3f)' %(xbin, xbins, ybin, ybins, w_m_Kpipi_max, w_rm_Dpipi_max, FOM)
                h_FOM.Fill(w_m_Kpipi_max - 0.5*(xmax - xmin) / float(xbins), w_rm_Dpipi_max - 0.5*(ymax - ymin) / float(ybins), FOM)
    return h_FOM

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, pt_title, ecms):
    try:
        f_incMC1 = TFile(path[0])
        f_incMC2 = TFile(path[1])
        t_incMC1 = f_incMC1.Get('save')
        t_incMC2 = f_incMC2.Get('save')
        entries_incMC1 = t_incMC1.GetEntries()
        entries_incMC2 = t_incMC2.GetEntries()
        logging.info('inclusive MC (qqbar) entries :'+str(entries_incMC1))
        logging.info('inclusive MC (open charm) entries :'+str(entries_incMC2))
        if ecms > 4230:
            f_sigMC1 = TFile(path[2])
            f_sigMC2 = TFile(path[3])
            t_sigMC1 = f_sigMC1.Get('save')
            t_sigMC2 = f_sigMC2.Get('save')
            entries_sigMC1 = t_sigMC1.GetEntries()
            entries_sigMC2 = t_sigMC2.GetEntries()
            logging.info('D1(2420) signal MC entries :'+str(entries_sigMC1))
            logging.info('psi(3770) signal MC entries :'+str(entries_sigMC2))
        else:
            f_sigMC1 = TFile(path[2])
            t_sigMC1 = f_sigMC1.Get('save')
            entries_sigMC1 = t_sigMC1.GetEntries()
            logging.info('psi(3770) signal MC entries :'+str(entries_sigMC1))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    if ecms > 4230:
        t = [t_incMC1, t_incMC2, t_sigMC1, t_sigMC2]
    else:
        t = [t_incMC1, t_incMC2, t_sigMC1]
    h_FOM = cal_significance(t, ecms)
    h_FOM.Draw('col')
    
    pt = TPaveText(0.6, 0.8, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    mbc.RedrawAxis()
    mbc.Update()
    mbc.SaveAs('./figs/opt_m_Kpipi_rm_Dpipi_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = int(args[0])

    path = []
    if int(ecms) == 4230:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4230/incMC_qq_4230_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4230/incMC_DD_4230_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4230/sigMC_psipp_4230_raw.root')
        pt_title = str(ecms) + ' MeV'
        plot(path, pt_title, ecms)

    path = []
    if int(ecms) == 4360:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/incMC_qq_4360_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_raw.root')
        pt_title = str(ecms) + ' MeV'
        plot(path, pt_title, ecms)

    path = []
    if int(ecms) == 4420:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/incMC_qq_4420_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/incMC_DD_4420_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_raw.root')
        pt_title = str(ecms) + ' MeV'
        plot(path, pt_title, ecms)

    path = []
    if int(ecms) == 4600:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/incMC_qq_4600_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/incMC_DD_4600_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_raw.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_raw.root')
        pt_title = str(ecms) + ' MeV'
        plot(path, pt_title, ecms)

if __name__ == '__main__':
    main()
