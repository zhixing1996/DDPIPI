#!/usr/bin/env python
"""
Calculate upper limit of total DDpipi cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-12-03 Thu 21:24]"

import math
from array import array
from ROOT import *
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
    upper_limit.py

SYNOPSIS
    ./upper_limit.py [ecms] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2020
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetTextSize(0.06)
    pt.SetFillColor(10)
    pt.SetTextColor(2)

def set_graph_style(gr, xtitle, ytitle):
    gr.GetXaxis().SetNdivisions(509)
    gr.GetYaxis().SetNdivisions(504)
    gr.SetLineWidth(2)
    gr.SetLineWidth(2)
    gr.GetXaxis().SetTitleSize(0.06)
    gr.GetXaxis().SetTitleOffset(0.9)
    gr.GetXaxis().SetLabelOffset(0.01)
    gr.GetYaxis().SetTitleSize(0.06)
    gr.GetYaxis().SetTitleOffset(0.9)
    gr.GetYaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetXaxis().CenterTitle()
    gr.GetYaxis().SetTitle(ytitle)
    gr.GetYaxis().CenterTitle()
    gr.SetMarkerStyle(8)
    gr.SetMarkerSize(0.65)
    gr.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)
    mbc.SetFillColor(10)
    mbc.SetGrid()

def upper_limit(path, ecms, patch):
    try:
        f = open(path, 'r')
    except:
        logging.error(path + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    mbc.cd()

    xtitle = 'Cross Section (pb)'
    ytitle = 'Normalized likelihood'

    with open('../fit_xs/txts/xs_info_' + str(ecms) + '_read_' + patch + '.txt') as f:
        for line in f.readlines():
            fargs = map(float, line.strip('\n').strip().split())
            f, eff_D1_2420, eff_psipp, eff_DDPIPI, omega_D1_2420, omega_psipp, omega_DDPIPI, ISR_D1_2420, ISR_psipp, ISR_DDPIPI, VP, lum, Br = fargs[5], fargs[6]/100., fargs[7]/100., fargs[8]/100., fargs[9], fargs[10], fargs[11], fargs[12],fargs[13], fargs[14], fargs[15], fargs[16], fargs[17]
    muldel = 1./(2*f*(eff_D1_2420*omega_D1_2420*ISR_D1_2420*VP + eff_psipp*omega_psipp*ISR_psipp*VP + eff_DDPIPI*omega_DDPIPI*ISR_DDPIPI*VP)*Br/100.*lum)
    FCN_sum = 0

    with open(path, 'r') as f:
        lines = f.readlines()
        N = len(lines) - 1
        xs_set = array('f', N*[0])
        likelihood = array('f', N*[0])
        count = 0
        # for line in lines:
        for i in xrange(len(lines) - 1):
            fargs = map(float, lines[i].strip('\n').strip().split())
            xs_set[count] = fargs[0]*muldel
            likelihood[count] = fargs[1]
            if xs_set[count] < 0: continue
            FCN_sum += fargs[1]
            count += 1
    print 'Number = ' + str(N)
    print 'Sum of FCN: ' + str(FCN_sum)

    t = 0
    sum_90 = 0
    for i in xrange(N):
        if xs_set[i] < 0: continue
        if sum_90 < FCN_sum*0.9:
            sum_90 += likelihood[i]
            pos_90 = xs_set[i]
            t += 1

    nf = t + 3
    xs_set_f = array('f', nf*[0])
    likelihood_f = array('f', nf*[0])
    xs_set_f[0], likelihood_f[0] = 0, 0
    xs_set_f[nf - 2], likelihood_f[nf - 2] = pos_90, 0
    xs_set_f[nf - 1], likelihood_f[nf - 1] = 0, 0

    j = 0
    sumf_90 = 0
    for i in xrange(N):
        if xs_set[i] < 0: continue
        if sumf_90 < FCN_sum*0.9:
            j += 1
            sumf_90 += likelihood[i]
            likelihood_f[j] = likelihood[i]
            xs_set_f[j] = xs_set[i]
            print 'xs(setted): ' + str(xs_set_f[j]) + ', likelihood: ' + str(likelihood_f[j])

    print '90% C.L. = ' + str(pos_90) + ', the 90% of FCN sum = ' + str(sum_90)

    xs_set_max = -9999
    likelihood_max = 0
    for i in xrange(N):
        if xs_set[i] < 0: continue
        if likelihood_max < likelihood[i]:
            likelihood_max = likelihood[i]
            xs_set_max = xs_set[i]

    print 'The maximum of likelihood = ' + str(likelihood_max) + ', cross section = ' + str(xs_set_max)

    gr = TGraph(N, xs_set, likelihood)
    set_graph_style(gr, xtitle, ytitle)
    gr.Draw('APC')

    gf = TGraph(nf, xs_set_f, likelihood_f)
    gf.SetFillColor(40)
    gf.Draw('LF')

    arrow = TArrow(pos_90, likelihood_max*0.5, pos_90, 0., 0.02)
    arrow.SetLineStyle(1)
    arrow.SetLineColor(kRed)
    arrow.SetFillColor(kRed)
    arrow.SetLineWidth(3)
    arrow.Draw()

    pt = TPaveText(0.45, 0.65, 0.65, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt_title = str(ecms) + ' MeV'
    pt.AddText(pt_title)
    pt_title = '90% C.L.: {}'.format(round(pos_90, 2))
    pt.AddText(pt_title)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    with open('./txts/upl_'+str(ecms)+'.txt', 'w') as f:
        f.write(str(ecms)+' '+str(round(pos_90, 2)))

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/upper_limit_' + str(ecms) + '.pdf')

    raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    patch = args[1]

    path = './txts/likelihood_smear_' + str(ecms) + '.txt'
    upper_limit(path, ecms, patch)

if __name__ == '__main__':
    main()
