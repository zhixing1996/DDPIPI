#!/usr/bin/env python
"""
Optiomize Vr of tracks and Vz of tracks
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-10-20 Tue 20:13]"

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

def usage():
    sys.stdout.write('''
NAME
    opt_2D.py

SYNOPSIS
    ./opt_2D.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    October 2020
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def set_arrow(arrow, color):
    arrow.SetLineWidth(4)
    arrow.SetLineColor(color)
    arrow.SetFillColor(color)

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

def cal_significance(t_data, t_sideband):
    xbins, xmin, xmax = 75, 0.0, 1.
    ybins, ymin, ymax = 75, 0.0, 10.
    n_sig, n_data, n_sideband = 0, 0, 0
    h_FOM = TH2F('h_FOM', 'h_FOM', xbins, xmin, xmax, ybins, ymin, ymax)
    xtitle = '|V_{xy}| (cm)'
    ytitle = '|V_{z}| (cm)'
    set_histo_style(h_FOM, xtitle, ytitle)
    for xbin in xrange(xbins):
        for ybin in xrange(ybins):
            Vr_max = (xbin + 1) * (xmax - xmin) / float(xbins) + xmin
            Vz_max = (ybin + 1) * (ymax - ymin) / float(ybins) + ymin
            cut_base = '(m_n_p == 0 && m_n_pbar == 0 && m_n_othertrks <= 3 && m_n_othershws <= 6)'
            cut_Vr = '(m_Vxy_Dtrks[0] < %.5f && m_Vxy_Dtrks[1] < %.5f && m_Vxy_Dtrks[2] < %.5f && m_Vxy_pip < %.5f && m_Vxy_pim < %.5f)' %(Vr_max, Vr_max, Vr_max, Vr_max, Vr_max)
            cut_Vz = '(m_Vz_Dtrks[0] < %.5f && m_Vz_Dtrks[1] < %.5f && m_Vz_Dtrks[2] < %.5f && m_Vz_pip < %.5f && m_Vz_pim < %.5f)' %(Vz_max, Vz_max, Vz_max, Vz_max, Vz_max)
            n_data = float(t_data.GetEntries(cut_base + ' && ' + cut_Vr + ' && ' + cut_Vz))
            n_sideband = float(t_data.GetEntries(cut_base + ' && ' + cut_Vr + ' && ' + cut_Vz)) * 0.5
            if not n_data == 0:
                FOM = (n_data - n_sideband)/sqrt(n_data)
                print '(xbin: %i/%i, ybin, %i/%i): Vr(%5f), Vz(%5f), FOM(%3f)' %(xbin, xbins, ybin, ybins, Vr_max, Vz_max, FOM)
                h_FOM.Fill(Vr_max - 0.5*(xmax - xmin) / float(xbins), Vz_max - 0.5*(ymax - ymin) / float(ybins), FOM)
    return h_FOM

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(path, pt_title, ecms):
    try:
        f_data = TFile(path[0])
        f_sideband = TFile(path[1])
        t_data = f_data.Get('save')
        t_sideband = f_sideband.Get('save')
        entries_data = t_data.GetEntries()
        entries_sideband = t_sideband.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('data (sideband) entries :'+str(entries_sideband))
    except:
        logging.error('Files are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    h_FOM = cal_significance(t_data, t_sideband)
    h_FOM.Draw('colz')
    
    pt = TPaveText(0.6, 0.8, 0.85, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(pt_title)

    Arr_Vr = TArrow(0.55, 0, 0.55, 10., 0.01, '')
    set_arrow(Arr_Vr, 1)
    Arr_Vr.Draw()
    Arr_Vz = TArrow(0, 3., 1., 3., 0.01, '')
    set_arrow(Arr_Vz, 1)
    Arr_Vz.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    mbc.RedrawAxis()
    mbc.Update()
    mbc.SaveAs('./figs/opt_Vr_Vz_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = int(args[0])

    path = []
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_before.root')
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_sideband_before.root')
    pt_title = str(ecms) + ' MeV'
    plot(path, pt_title, ecms)

if __name__ == '__main__':
    main()
