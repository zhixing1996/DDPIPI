#!/usr/bin/env python
"""
Plot cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-20 Fri 23:27]"

import ROOT
from ROOT import TCanvas, gStyle, TGraphErrors
from ROOT import TFile, TH1F, TLegend, TPaveText
from array import array
import sys, os
import logging
from math import *
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    plot_xs.py

SYNOPSIS
    ./plot_xs.py [mode] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def set_graph_style(gr, xtitle, ytitle):
    gr.GetXaxis().SetNdivisions(509)
    gr.GetYaxis().SetNdivisions(504)
    gr.SetLineWidth(2)
    gr.GetXaxis().SetTitleSize(0.04)
    gr.GetXaxis().SetTitleOffset(1.3)
    gr.GetXaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetRangeUser(4.17, 4.70)
    gr.GetYaxis().SetTitleSize(0.04)
    gr.GetYaxis().SetTitleOffset(1.5)
    gr.GetYaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetXaxis().CenterTitle()
    gr.GetYaxis().SetTitle(ytitle)
    gr.GetYaxis().CenterTitle()
    gr.SetMarkerColor(1)
    gr.SetMarkerStyle(21)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)
    mbc.SetGrid()

def draw(mode, patch):
    if mode == 'DDPIPI' or mode == 'psipp' or mode == 'total':
        N = 19 + 6 + 6 # 19: 703p01, 6: 705, 4: 705 above 4600
    if mode == 'D1_2420':
        N = 19 + 6 + 6 # 18: 703p01, 6: 705, 4: 705 above 4600
    sys_err = array('f', N*[0])
    ecms = array('f', N*[0])
    ecms_err = array('f', N*[0])
    xs = array('f', N*[0])
    xs_err = array('f', N*[0])
    path = './txts/xs_' + mode + '_' + patch + '_plot.txt'

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    f = open(path, 'r')
    lines = f.readlines()
    count = 0
    for line in lines:
        rs = line.rstrip('\n')
        rs = filter(None, rs.split(' '))
        ecms[count] = float(rs[0])
        ecms_err[count] = 0.0022
        xs[count] = float(rs[1])
        xs_err[count] = float(rs[2])
        count += 1

    grerr = TGraphErrors(N, ecms, xs, ecms_err, xs_err)
    xtitle = 'E_{cms}(GeV)'
    if mode == 'D1_2420':
        ytitle = '#sigma(e^{+}e^{-}#rightarrowD_{1}(2420)D)(pb)'
    if mode == 'psipp':
        ytitle = '#sigma(e^{+}e^{-}#rightarrow#psi(3770)#pi^{+}#pi^{-})(pb)'
    if mode == 'DDPIPI':
        ytitle = '#sigma(e^{+}e^{-}#rightarrowD^{+}D^{-}#pi^{+}#pi^{-})(PHSP)(pb)'
    if mode == 'total':
        ytitle = '#sigma(e^{+}e^{-}#rightarrowD^{+}D^{-}#pi^{+}#pi^{-})(pb)'
    set_graph_style(grerr, xtitle, ytitle)
    grerr.Draw('AP')

    mbc.Update()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/xs_' + mode + '_' + patch + '.pdf')

    raw_input('Enter anything to end...')
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    mode = args[0]
    patch = args[1]

    draw(mode, patch)
