#!/usr/bin/env python
"""
Fit cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-01-04 Sat 15:08]"

import math
import sys, os
import logging
from math import *
from tools import *
from ROOT import *
from array import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

# set the paper & margin sizes
gStyle.SetPaperSize(20,26)
gStyle.SetPadColor(0)
gStyle.SetPadBorderMode(0)
gStyle.SetPadTopMargin(0.03)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.22)
gStyle.SetPadLeftMargin(0.12)
gStyle.SetTitleFillColor(0)
gStyle.SetTitleFont(22, "xyz") # set the all 3 axes title font 
gStyle.SetTitleFont(22, " ") # set the pad title font
gStyle.SetTitleSize(0.06, "xyz") # set the 3 axes title size
gStyle.SetTitleSize(0.06, " ") # set the pad title size
gStyle.SetLabelFont(22, "xyz")
gStyle.SetLabelSize(0.05, "xyz")
gStyle.SetTextFont(22)
gStyle.SetTextSize(0.08)
gStyle.SetStatFont(22)
gStyle.SetFrameBorderMode(0)
gStyle.SetCanvasBorderMode(0)
gStyle.SetCanvasColor(0)
gStyle.SetStatColor(0)
gStyle.SetMarkerStyle(8)
gStyle.SetHistFillColor(0)
gStyle.SetLineWidth(2)
gStyle.SetLineStyleString(2,"[12 12]"); # postscript dashes
gStyle.SetErrorX(0.001)

# do not display any of the standard histogram decorations
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)

# put tick marks on top and RHS of plots
gStyle.SetPadTickX(0)
gStyle.SetPadTickY(0)

def usage():
    sys.stdout.write('''
NAME
    fit_xs.py

SYNOPSIS
    ./fit_xs.py [mode] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    January 2020
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

def set_pad_style(pad):
    pad.SetLeftMargin(0.35)
    pad.SetRightMargin(0.15)
    pad.SetTopMargin(0.1)
    pad.SetBottomMargin(0.15)
    pad.SetFrameLineColor(kBlack)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)
    mbc.SetGrid()

def fit(mode, patch):
    mbc = TCanvas('mbc', 'mbc', 1000, 700)
    set_canvas_style(mbc)

    pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    set_pad_style(pad)
    pad.Draw()

    xs_path = 'txts/xs_' + mode + '_' + patch + '.txt'
    if mode == 'D1_2420':
        xs_func, xs_pars = '[0] * TMath::Gaus(x, [1], [2]) + [3] * x * x + [4] * x + [5]', array('d', [0.1, 4.4, 0.1, 0.1, 0.1, 0.1])
    if mode == 'psipp':
        xs_func, xs_pars = '[0] * TMath::Gaus(x, [1], [2]) + [3] * x * x + [4] * x + [5]', array('d', [0.1, 4.45, 0.1, 0.1, 0.1, 0.1])
    if mode == 'DDPIPI':
        xs_func, xs_pars = '[0] * TMath::Gaus(x, [1], [2])', array('d', [1.1, 4.45, 1.1])
    if mode == 'total':
        xs_func, xs_pars = '[0] * TMath::BreitWigner(x, [1], [2]) + [3] * TMath::BreitWigner(x, [4], [5]) + [6] * TMath::Gaus(x, [7], [8])', array('d', [0.1, 4.39, 0.096, 0.1, 4.455, 1.1, 0.1, 4.415, 2.2])

    ipoint = 0
    grerr = TGraphErrors(ipoint)

    xs_file = open(xs_path)
    for line in xs_file:
        rs = line.rstrip('\n')
        rs = filter(None, rs.split(" "))
        ecms = float(rs[0])
        xs = float(rs[1])
        xs_err = float(rs[2])
        grerr.Set(ipoint + 1)
        grerr.SetPoint(ipoint, ecms, xs)
        grerr.SetPointError(ipoint, 0.0, xs_err)
        ipoint += 1

    if mode == 'psipp' or mode == 'DDPIPI':
        xs_f = TF1('xs_f', xs_func, 4.190, 4.600)
    if mode == 'D1_2420':
        xs_f = TF1('xs_f', xs_func, 4.310, 4.600)
        xs_f.SetParameters(xs_pars)
        xs_f.SetParName(0, 'par[0] of 1st Gauss\t')
        xs_f.SetParLimits(0, -10., 20.)
        xs_f.SetParName(1, 'mean of 1st Gauss\t')
        xs_f.SetParLimits(1, 4.35, 4.45)
        xs_f.SetParName(2, 'width of 1st Gauss\t')
        xs_f.SetParLimits(2, 0.1 - 0.07, 0.1 + 0.07)
        xs_f.SetParName(3, 'par[0] of pol\t')
        xs_f.SetParLimits(3, -10., 10.)
        xs_f.SetParName(4, 'par[1] of pol\t')
        xs_f.SetParLimits(4, -10., 10.)
        xs_f.SetParName(5, 'par[2] of pol\t')
        xs_f.SetParLimits(5, -10., 10.)
        xtitle = '#sqrt{s}(GeV)'
        ytitle = '#sigma^{dress}(e^{+}e^{-}#rightarrowD_{1}(2420)D)(pb)'

    if mode == 'psipp':
        xs_f = TF1('xs_f', xs_func, 4.310, 4.600)
        xs_f.SetParameters(xs_pars)
        xs_f.SetParName(0, 'par[0] of 1st Gauss\t')
        xs_f.SetParLimits(0, -10., 20.)
        xs_f.SetParName(1, 'mean of 1st Gauss\t')
        xs_f.SetParLimits(1, 4.39, 4.49)
        xs_f.SetParName(2, 'width of 1st Gauss\t')
        xs_f.SetParLimits(2, 0.1 - 0.07, 0.1 + 0.07)
        xs_f.SetParName(3, 'par[0] of pol\t')
        xs_f.SetParLimits(3, -10., 10.)
        xs_f.SetParName(4, 'par[1] of pol\t')
        xs_f.SetParLimits(4, -10., 10.)
        xs_f.SetParName(5, 'par[2] of pol\t')
        xs_f.SetParLimits(5, -10., 10.)
        xtitle = '#sqrt{s}(GeV)'
        ytitle = '#sigma^{dress}(e^{+}e^{-}#rightarrow#psi(3770)#pi^{+}#pi^{-})(pb)'

    if mode == 'DDPIPI':
        xs_f = TF1('xs_f', xs_func, 4.310, 4.600)
        xs_f.SetParameters(xs_pars)
        xs_f.SetParName(0, 'par[0] of pol\t')
        xs_f.SetParLimits(0, 1., 10.)
        xs_f.SetParName(1, 'par[1] of pol\t')
        xs_f.SetParLimits(1, 4.4, 4.5)
        xs_f.SetParName(2, 'par[2] of pol\t')
        xs_f.SetParLimits(2, 1., 10.)
        xs_f.SetParName(3, 'par[3] of pol\t')
        xs_f.SetParLimits(3, 1., 10.)
        xtitle = '#sqrt{s}(GeV)'
        ytitle = '#sigma^{dress}(e^{+}e^{-}#rightarrowD^{+}D^{-}#pi^{+}#pi^{-})(PHSP)(pb)'

    if mode == 'total':
        xs_f = TF1('xs_f', xs_func, 4.310, 4.600)
        xs_f.SetParameters(xs_pars)
        xs_f.SetParName(0, 'par[0] of 1st B-W\t')
        xs_f.SetParLimits(0, -10., 20.)
        xs_f.SetParName(1, 'mean of 1st B-W\t')
        xs_f.SetParLimits(1, 3, 5)
        xs_f.SetParName(2, 'width of 1st B-W\t')
        xs_f.SetParLimits(2, 0.96 - 0.7, 0.96 + 0.7)
        xs_f.SetParName(3, 'par[0] of 2rd B-W\t')
        xs_f.SetParLimits(3, -5., 1.)
        xs_f.SetParName(4, 'mean of 2rd B-W\t')
        xs_f.SetParLimits(4, 3, 5)
        xs_f.SetParName(5, 'width of 2rd B-W\t')
        xs_f.SetParLimits(5, 1.1 - 0.7, 1.1 + 0.7)
        xs_f.SetParName(6, 'par[0] of Gaussian\t')
        xs_f.SetParLimits(6, 0., 100.)
        xs_f.SetParName(7, 'mean of Gaussian\t')
        xs_f.SetParLimits(7, 4, 5)
        xs_f.SetParName(8, 'width of Gaussian\t')
        xs_f.SetParLimits(8, -10., 10.)
        xtitle = '#sqrt{s}(GeV)'
        ytitle = '#sigma^{dress}(e^{+}e^{-}#rightarrowD^{+}D^{-}#pi^{+}#pi^{-})(pb)'
    set_graph_style(grerr, xtitle, ytitle)
    grerr.Fit(xs_f)
    grerr.Draw('ap')

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    mbc.SaveAs('./figs/fit_xs_'+ mode + '_' + patch + '.pdf')
    
    raw_input('enter anything to end')

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    mode = args[0]
    patch = args[1]

    fit(mode, patch)

if __name__ == '__main__':
    main()
