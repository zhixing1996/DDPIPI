#!/usr/bin/env python
"""
Calculate cross section differences between two patches
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-30 Mon 22:55]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TPaveText
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
    cal_xs_diff.py

SYNOPSIS
    ./cal_xs_diff.py [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def set_legend(legend, gr1):
    legend.AddEntry(gr1, 'ini. #rightarrow 1th', 'lp')
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

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

def cal_diff(patch1, patch2, mode):
    grerr= TGraphErrors(0)
    ipoint = 0
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_xs_diff = './txts/xs_diff_' + mode + '_' + patch1 + '_' + patch2 + '.txt'
    f_xs_diff = open(path_xs_diff, 'w')

    path1 = './txts/xs_info_' + mode + '_' + patch1 + '.txt'
    path2 = './txts/xs_info_' + mode + '_' + patch2 + '.txt'
    XS1, XS2 = open(path1, 'r'), open(path2, 'r')
    if not (len(XS1) == len(XS2)):
        print 'Number of energy points is not the same, please check...'
        sys.exit()
    for line1, line2 in zip(XS1, XS2):
        info1 = line1.strip().split()
        info2 = line2.strip().split()
        finfo1 = map(float, info1)
        finfo2 = map(float, info2)
        ecms, xs1 = finfo1[0], finfo1[1]
        ecms, xs2 = finfo2[0], finfo2[1]
        grerr.Set(ipoint + 1)
        grerr.SetPoint(ipoint, ecms, (xs1 - xs2)/xs1)
        ipoint += 1
        out = str(ecms) + ' ' + str((xs1 - xs2)/xs1) + '\n'
        f_xs_diff.write(out)
    f_xs_diff.close()
    return grerr

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def main(mode):
    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    grerr_0_to_1 = cal_diff('round0', 'round1', mode)
    xtitle = 'E_{cms}(GeV)'
    ytitle = '#Delta#sigma^{dress}/#sigma^{dress} (pb)'
    set_graph_style(grerr_0_to_1, xtitle, ytitle)
    grerr_0_to_1.SetMarkerColor(2)
    grerr_0_to_1.SetLineColor(2)
    grerr_0_to_1.SetMarkerStyle(20)
    grerr_0_to_1.SetName('gecs')
    gaxis = TGaxis(0, 0, 0, 0, 'gecs')
    gaxis.SetMaxDigits(3)
    grerr_0_to_1.Draw('ALP')

    legend = TLegend(0.5, 0.6, 0.95, 0.90)
    set_legend(legend, grerr_0_to_1)
    legend.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    mbc.SaveAs('./figs/xs_iteration_diff_'+str(mode)+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    mode = str(args[0])

    main(mode)
