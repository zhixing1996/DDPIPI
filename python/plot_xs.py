#!/usr/bin/env python
"""
Plot cross section of DDPIPI
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
    ./plot_xs.py

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
    gr.GetYaxis().SetTitleSize(0.04)
    gr.GetYaxis().SetTitleOffset(1.5)
    gr.GetYaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetXaxis().CenterTitle()
    gr.GetYaxis().SetTitle(ytitle)
    gr.GetYaxis().CenterTitle()
    gr.SetMarkerColor(4)
    gr.SetMarkerStyle(21)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)
    mbc.SetGrid()

def draw():
    N = 18
    ecms = array('f', N*[0])
    ecms_err = array('f', N*[0])
    xs = array('f', N*[0])
    xs_err = array('f', N*[0])
    path = './txts/xs_info_modified_read.txt'

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    f = open(path, 'r')
    lines = f.readlines()
    count = 0
    for line in lines:
        rs = line.rstrip('\n')
        rs = filter(None, rs.split(' '))
        ecms[count] = float(rs[0])/1000.
        ecms_err[count] = 0.0022
        xs[count] = float(rs[-2])
        xs_err[count] = float(rs[-1])
        count += 1

    gr = TGraphErrors(N, ecms, xs, ecms_err, xs_err)
    xtitle = 'E_{cms}(GeV)'
    ytitle = '#sigma(e^{+}e^{-}#rightarrowD^{+}D^{-}#pi^{+}#pi^{-})(pb)'
    set_graph_style(gr, xtitle, ytitle)
    gr.Draw('ALP')

    mbc.Update()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/xs_DDPIPI.pdf')
    
if __name__ == '__main__':
    usage()
    draw()
