#!/usr/bin/env python
"""
Calculate systematic uncertainty
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-12-13 Sun 10:52]"

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
    cal_diff.py

SYNOPSIS
    ./cal_diff.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2020
\n''')

def set_arrow(arrow, color):
    arrow.SetLineWidth(4)
    arrow.SetLineColor(color)
    arrow.SetFillColor(color)

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.04)

def rm_Kspi_fill(t, h):
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if abs(t.vfit2_dl/t.vfit2_dle)>2. and abs(t.vfit2_mks-0.497614)<0.008 and abs(t.var_kstar)<0.12 and t.vfitpt>0.1:
            h.Fill(t.vfitm)

def count(t, region):
    num = 0
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if abs(t.vfit2_dl/t.vfit2_dle)>2. and abs(t.vfit2_mks-0.497614)<0.008 and abs(t.var_kstar)<0.12 and t.vfitp>0.1:
            if region == 'signal' and (t.vfitm > 0.41 and t.vfitm < 0.57): num += 1
            if region == 'side' and ((t.vfitm > 0.3 and t.vfitm < 0.38) or (t.vfitm > 0.6 and t.vfitm < 0.68)): num += 1
    return num

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.06)
    h.GetXaxis().SetTitleOffset(1.1)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(1.1)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def draw(path):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('vfit')
        entries_data = t_data.GetEntries('nMatch==1')
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin, xmax, xbins = 0.28, 0.7, 210
    content = int((xmax - xmin)/xbins * 1000)
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'RM(K_{S}#pi^{+})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    
    set_histo_style(h_data, xtitle, ytitle)
    rm_Kspi_fill(t_data, h_data)

    h_data.Draw('E1')

    Arr_signal_left = TArrow(0.41, 0, 0.41, 1000., 0.01, '<')
    set_arrow(Arr_signal_left, 2)
    Arr_signal_left.Draw()
    Arr_signal_right = TArrow(0.57, 0, 0.57, 1000, 0.01, '<')
    set_arrow(Arr_signal_right, 2)
    Arr_signal_right.Draw()

    Arr_side_left_left = TArrow(0.3, 0, 0.3, 1000., 0.01, '<')
    set_arrow(Arr_side_left_left, 2)
    Arr_side_left_left.Draw()
    Arr_side_left_right = TArrow(0.38, 0, 0.38, 1000, 0.01, '<')
    set_arrow(Arr_side_left_right, 2)
    Arr_side_left_right.Draw()

    Arr_side_right_left = TArrow(0.6, 0, 0.6, 1000., 0.01, '<')
    set_arrow(Arr_side_right_left, 2)
    Arr_side_right_left.Draw()
    Arr_side_right_right = TArrow(0.68, 0, 0.68, 1000, 0.01, '<')
    set_arrow(Arr_side_right_right, 2)
    Arr_side_right_right.Draw()

    n_signal = float(count(t_data, 'signal'))
    n_side = float(count(t_data, 'side'))

    print n_signal, n_side
    pt = TPaveText(0.15, 0.75, 0.55, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt_title = 'Purity of control '
    pt.AddText(pt_title)
    pt_title = 'sample: ' + str(round((n_signal-n_side)/n_signal*100, 2)) + '%'
    pt.AddText(pt_title)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    mbc.SaveAs('./figs/rm_Kspi_'+str(ecms)+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/groups/cal/dedx/$USER/bes/KsKpi/run/KsKpi/anaroot/data/' + str(ecms) + '/data_' + str(ecms) + '_signal.root')
    draw(path)
