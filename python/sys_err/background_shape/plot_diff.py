#!/usr/bin/env python
"""
Plot systematic uncertainty
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-11-26 Thr 21:43]"

import ROOT
from ROOT import TCanvas, gStyle, TGraph, TF1, TGraphErrors
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
    plot_diff.py

SYNOPSIS
    ./plot_diff.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2020
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def set_graph_style(gr, xtitle, ytitle):
    gr.GetXaxis().SetNdivisions(509)
    gr.GetYaxis().SetNdivisions(504)
    gr.SetLineWidth(2)
    gr.GetXaxis().SetTitleSize(0.06)
    gr.GetXaxis().SetTitleOffset(1.1)
    gr.GetXaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetLabelSize(0.05)
    gr.GetXaxis().SetRangeUser(4.17, 4.70)
    gr.GetYaxis().SetTitleSize(0.06)
    gr.GetYaxis().SetTitleOffset(0.8)
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

def draw():
    N = 8
    ecms = array('f', N*[0])
    ecms_err = array('f', N*[0])
    sys_err = array('f', N*[0])
    sys_err_err = array('f', N*[0])
    path = './txts/sys_err_background_shape_raw.txt'

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    f = open(path, 'r')
    lines = f.readlines()
    count = 0
    sum = 0
    sys_max = 0.
    for line in lines:
        fargs = map(float, line.strip('\n').strip().split())
        ecms[count] = fargs[0]
        ecms_err[count] = 0.0022
        sys_err[count] = fargs[1]
        sys_err_err[count] = fargs[2]
        if sys_err[count] > sys_max: sys_max = sys_err[count]
        sum += fargs[1]
        count += 1
    ave = sum/count

    f_ave = TF1('f_ave', str(sys_max), ecms[0] - 0.1, ecms[-1] + 0.1)
    gr = TGraphErrors(N, ecms, sys_err, ecms_err, sys_err_err)
    xtitle = 'E_{cms} (GeV)'
    ytitle = 'Sys. Uncertainty_{BKG Shape} (%)'
    set_graph_style(gr, xtitle, ytitle)
    gr.Draw('AP')
    f_ave.Draw('same')

    pt = TPaveText(0.17, 0.8, 0.3, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    line = 'Maximum: ' + str(round(sys_max, 1)) + '%'
    pt.AddText(line)
    mbc.Update()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/sys_err_background_shape.pdf')

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    with open('./txts/sys_err_background_shape.txt', 'w') as f:
        for ecm in ecms:
            out = str(ecm/1000.) + '\t' + str(round(sys_max, 2)) + '\n'
            f.write(out)

    raw_input('Enter anything to end...')
    
if __name__ == '__main__':
    draw()
