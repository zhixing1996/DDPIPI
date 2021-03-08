#!/usr/bin/env python
"""
Optiomize invariant mass of Kpipipi1 and Kpipipi2
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2021-02-27 Sat 10:41]"

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
    opt_2D_m_Kpipipi.py

SYNOPSIS
    ./opt_2D_m_Kpipipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    February 2021
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
    t1 = t[0]
    t2 = t[1]
    t3 = t[2]
    xbins, xmin, xmax = 75, 0.0, 0.09
    ybins, ymin, ymax = 75, 0.0, 0.09
    n_incMC, n_DDPIPI, n_DDPI = 0, 0, 0
    h_FOM = TH2F('h_FOM', 'h_FOM', xbins, xmin, xmax, ybins, ymin, ymax)
    xtitle = '|M(K^{+}#pi_{0}^{+}#pi_{0}^{-}#pi_{1}^{+})-m_{D^{0}}| (GeV)'
    ytitle = '|M(K^{+}#pi_{0}^{+}#pi_{0}^{-}#pi_{2}^{+})-m_{D^{0}}| (GeV)'
    set_histo_style(h_FOM, xtitle, ytitle)
    width_low = 1.86965 - width(ecms)/2.
    width_up = 1.86965 + width(ecms)/2.
    window_low = 1.86965 - window(ecms)/2.
    window_up = 1.86965 + window(ecms)/2.
    for xbin in xrange(xbins):
        for ybin in xrange(ybins):
            w_m_Kpipipi1_max = (xbin + 1) * (xmax - xmin) / float(xbins) + xmin
            w_m_Kpipipi2_max = (ybin + 1) * (ymax - ymin) / float(ybins) + ymin
            m_D0 = 1.86483
            m_Kpipipi1_low = m_D0 - w_m_Kpipipi1_max/2.
            m_Kpipipi1_up = m_D0 + w_m_Kpipipi1_max/2.
            m_Kpipipi2_low = m_D0 - w_m_Kpipipi2_max/2.
            m_Kpipipi2_up = m_D0 + w_m_Kpipipi2_max/2.
            n_incMC = float(t1.GetEntries('(rawm_D > %.5f && rawm_D < %.5f) && (rm_Dpipi > %.5f && rm_Dpipi < %.5f) && (m_m_Kpipipi1 < %.5f || m_m_Kpipipi1 > %.5f) && (m_m_Kpipipi2 < %.5f || m_m_Kpipipi2 > %.5f)' %(width_low, width_up, window_low, window_up, m_Kpipipi1_low, m_Kpipipi1_up, m_Kpipipi2_low, m_Kpipipi2_up))) * scale_factor(ecms, 'DD')
            n_DDPIPI = float(t2.GetEntries('(rawm_D > %.5f && rawm_D < %.5f) && (rm_Dpipi > %.5f && rm_Dpipi < %.5f) && (m_m_Kpipipi1 < %.5f || m_m_Kpipipi1 > %.5f) && (m_m_Kpipipi2 < %.5f || m_m_Kpipipi2 > %.5f)' %(width_low, width_up, window_low, window_up, m_Kpipipi1_low, m_Kpipipi1_up, m_Kpipipi2_low, m_Kpipipi2_up))) * scale_factor(ecms, 'DDPIPI')
            n_DDPI = float(t3.GetEntries('(rawm_D > %.5f && rawm_D < %.5f) && (rm_Dpipi > %.5f && rm_Dpipi < %.5f) && (m_m_Kpipipi1 < %.5f || m_m_Kpipipi1 > %.5f) && (m_m_Kpipipi2 < %.5f || m_m_Kpipipi2 > %.5f)' %(width_low, width_up, window_low, window_up, m_Kpipipi1_low, m_Kpipipi1_up, m_Kpipipi2_low, m_Kpipipi2_up))) * scale_factor(ecms, 'DDPI')
            if not (n_incMC + n_DDPIPI + n_DDPI) == 0:
                FOM = n_DDPIPI/sqrt(n_incMC + n_DDPIPI + n_DDPI)
                print '(xbin: %i/%i, ybin, %i/%i): M(Kpipipi1)(%5f), M(Kpipipi2)(%5f), FOM(%3f)' %(xbin, xbins, ybin, ybins, w_m_Kpipipi1_max, w_m_Kpipipi2_max, FOM)
                h_FOM.Fill(w_m_Kpipipi1_max - 0.5*(xmax - xmin) / float(xbins), w_m_Kpipipi2_max - 0.5*(ymax - ymin) / float(ybins), FOM)
    return h_FOM

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, pt_title, ecms):
    try:
        f_incMC = TFile(path[0])
        t_incMC = f_incMC.Get('save')
        entries_incMC = t_incMC.GetEntries()
        logging.info('inclusive MC (open charm) entries :'+str(entries_incMC))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()
    try:
        f_DDPIPI = TFile(path[1])
        t_DDPIPI = f_DDPIPI.Get('save')
        entries_DDPIPI = t_DDPIPI.GetEntries()
        logging.info('signal MC (DDPIPI) entries :'+str(entries_DDPIPI))
    except:
        logging.error(path[1] + ' is invalid!')
        sys.exit()
    try:
        f_DDPI = TFile(path[2])
        t_DDPI = f_DDPI.Get('save')
        entries_DDPI = t_DDPI.GetEntries()
        logging.info('background MC (DDPI) entries :'+str(entries_DDPI))
    except:
        logging.error(path[1] + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    t = [t_incMC, t_DDPIPI, t_DDPI]
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
    mbc.SaveAs('./figs/opt_m_Kpipipi1_m_Kpipipi2_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = int(args[0])

    path = []
    if int(ecms) == 4230:
        path.append('/scratchfs/users/$USER/bes/DDPIPI/v0.2/incMC/DD/4230/incMC_DD_4230_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4230/sigMC_D_D_PI_PI_4230_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPI/4230/sigMC_D_D_PI_4230_raw.root')
        pt_title = str(ecms) + ' MeV'
        plot(path, pt_title, ecms)

    path = []
    if int(ecms) == 4360:
        path.append('/scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/incMC_DD_4360_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4360/sigMC_D_D_PI_PI_4360_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPI/4360/sigMC_D_D_PI_4360_raw.root')
        pt_title = str(ecms) + ' MeV'
        plot(path, pt_title, ecms)

    path = []
    if int(ecms) == 4420:
        path.append('/scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/rootfile/incMC_DD_4420_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4420/sigMC_D_D_PI_PI_4420_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPI/4420/sigMC_D_D_PI_4420_raw.root')
        pt_title = str(ecms) + ' MeV'
        plot(path, pt_title, ecms)

    path = []
    if int(ecms) == 4600:
        path.append('/scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/rootfile/incMC_DD_4600_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/sigMC_D_D_PI_PI_4600_raw.root')
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPI/4600/sigMC_D_D_PI_4600_raw.root')
        pt_title = str(ecms) + ' MeV'
        plot(path, pt_title, ecms)

if __name__ == '__main__':
    main()
