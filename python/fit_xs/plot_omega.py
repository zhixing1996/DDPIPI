#!/usr/bin/env python
"""
Plot cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-20 Fri 23:27]"

import ROOT
from ROOT import TCanvas, gStyle, TGraphErrors
from ROOT import TFile, TH1F, TLegend, TPaveText, TGaxis
from array import array
import sys, os
import logging
from math import *
from tools import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

# TGaxis::SetMaxDigits(6)
# TGaxis.SetMaxDigits(2)

def usage():
    sys.stdout.write('''
NAME
    plot_xs.py

SYNOPSIS
    ./plot_xs.py [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def set_graph_style(gr, xtitle, ytitle, mode):
    gr.GetXaxis().SetNdivisions(509)
    gr.GetYaxis().SetNdivisions(504)
    gr.SetLineWidth(2)
    gr.GetXaxis().SetTitleSize(0.06)
    gr.GetXaxis().SetTitleOffset(1.)
    gr.GetXaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetLabelSize(0.05)
    # gr.GetXaxis().SetRangeUser(4.17, 4.95)
    if mode != 'D1_2420': gr.GetXaxis().SetRangeUser(4.17, 4.7)
    if mode == 'D1_2420': gr.GetXaxis().SetRangeUser(4.33, 4.7)
    gr.GetYaxis().SetTitleSize(0.06)
    gr.GetYaxis().SetTitleOffset(1.)
    gr.GetYaxis().SetLabelOffset(0.01)
    gr.GetYaxis().SetLabelSize(0.05)
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

def draw(mode):
    if mode == 'DDPIPI' or mode == 'psipp':
        N = 31
    if mode == 'D1_2420':
        N = 17
    sys_err = array('f', N*[0])
    ecms = array('f', N*[0])
    ecms_err = array('f', N*[0])
    omega = array('f', N*[0])
    omega_err = array('f', N*[0])
    path = './txts/omega_SAMPLE.txt'

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    if mode != 'D1_2420': samples = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700]
    if mode == 'D1_2420': samples = [4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700]
    count = 0
    for sample in samples:
        with open(path.replace('SAMPLE', str(sample)), 'r') as f:
            lines = f.readlines()
            ecms[count] = ECMS(sample)
            ecms_err[count] = 0.0022
            if sample >= 4340:
                if mode == 'D1_2420':
                    fargs = map(float, lines[0].strip('\n').strip().split())
                    omega[count] = fargs[0]
                    omega_err[count] = fargs[1]
                if mode == 'psipp':
                    fargs = map(float, lines[1].strip('\n').strip().split())
                    omega[count] = fargs[0]
                    omega_err[count] = fargs[1]
                if mode == 'DDPIPI':
                    fargs = map(float, lines[2].strip('\n').strip().split())
                    omega[count] = fargs[0]
                    omega_err[count] = fargs[1]
            if sample < 4340:
                if mode == 'psipp':
                    fargs = map(float, lines[0].strip('\n').strip().split())
                    omega[count] = fargs[0]
                    omega_err[count] = fargs[1]
                if mode == 'DDPIPI':
                    fargs = map(float, lines[1].strip('\n').strip().split())
                    omega[count] = fargs[0]
                    omega_err[count] = fargs[1]
        count += 1

    grerr = TGraphErrors(N, ecms, omega, ecms_err, omega_err)
    xtitle = '#sqrt{s}(GeV)'
    if mode == 'D1_2420':
        ytitle = '#omega(e^{+}e^{-}#rightarrowD_{1}(2420)D)(%)'
    if mode == 'psipp':
        ytitle = '#omega(e^{+}e^{-}#rightarrow#psi(3770)#pi^{+}#pi^{-})(%)'
    if mode == 'DDPIPI':
        ytitle = '#omega(e^{+}e^{-}#rightarrowD^{+}D^{-}#pi^{+}#pi^{-})(PHSP)(%)'
    set_graph_style(grerr, xtitle, ytitle, mode)
    grerr.Draw('AP')

    mbc.Update()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/omega_' + mode + '.pdf')

    raw_input('Enter anything to end...')
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    mode = args[0]

    draw(mode)
