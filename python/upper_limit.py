#!/usr/bin/env python
"""
Calculate upper limit of X(3842) events number
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-05 Thu 21:39]"

import math
from array import array
from ROOT import *
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
    upper_limit.py

SYNOPSIS
    ./significance.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def set_histo_style(h, xtitle, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetTitleOffset(1.4)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.5)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().SetTitle(xtitle)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.SetMarkerStyle(8)
    h.SetMarkerSize(0.65)
    h.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def upper_limit(step_size, path, root, ecms, mode, arrow_top):
    try:
        f = open(path, 'r')
    except:
        logging.error(path + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    mbc.cd()

    lines = f.readlines()
    N = len(lines)
    max = N*step_size
    h = TH2F('h', 'h', N, 0, max, N, 0, 2)
    count = 0
    for line in lines:
        rs = line.rstrip('\n')
        rs = filter(None, rs.split(" "))
        n = float(rs[0])
        likelihood = float(rs[1])
        h.Fill(n, likelihood)
        count += 1

    par = array('d', 6*[0.])
    g1 = TF1('g1', 'gaus', 0, max)
    g2 = TF1('g2', 'gaus', 0, max)
    f_gauss = TF1('f_gauss', 'gaus(0)+gaus(3)', 0, max)
    h.Fit(g1, 'R')
    h.Fit(g2, 'R+')
    par1 = g1.GetParameters()
    par2 = g2.GetParameters()
    par[0], par[1], par[2] = par1[0], par1[1], par1[2]
    par[3], par[4], par[5] = par2[0], par2[1], par2[2]
    f_gauss.SetParameters(par)
    h.Fit(f_gauss, 'R+')
    xtitle = 'yields'
    ytitle = 'normalized likehood value'
    set_histo_style(h, xtitle, ytitle)
    h.Draw()

    max_prob = f_gauss.Integral(0, max)
    print 'Maximum Probility: ' + str(max_prob)

    for i in xrange(N):
        n_upl = i * step_size
        prob_ = f_gauss.Integral(0, n_upl)
        prob =prob_/max_prob
        if prob >= 0.9:
            print 'prob >= 0.9 , N = ' + str(n_upl)
            break
        print 'prob = ' + str(prob)

    arrow = TArrow(n_upl, 0.0, n_upl, arrow_top, 0.01, '<')
    arrow.SetLineColor(kRed)
    arrow.SetLineWidth(3)
    arrow.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/upper_limit_'+str(ecms)+'.pdf')

    f = TFile(root)
    t = f.Get('save')
    entries = t.GetEntries()
    if (ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420):
        eff = entries/100000.
    else:
        eff = entries/50000.
    temp1, temp2, lum = data_base(ecms)
    Br = 0.0938
    xs = round(n_upl/2./Br/eff/lum, 2)
    if not os.path.exists('./txts/'): 
        os.makedirs('./txts/')
    path_out = './txts/xs_upper_limit_' + mode + '_' + str(ecms) + '.txt'
    f_out = open(path_out, 'w')
    out = '& @' + str(ecms) + 'MeV& ' + str(n_upl) + '& ' + str(round(eff*100, 2)) + '\%& ' + str(lum) + '& ' + str(Br*100) + '\%& ' + str(xs) + '& \\\\'
    f_out.write(out)
    f_out.close()

    raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    mode = args[1]

    path = './txts/upper_limit_likelihood_' + str(ecms) + '.txt'
    root = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/' + str(ecms) + '/sigMC_X_3842_' + str(ecms) + '_after.root'
    step_size = 0.1
    arrow_top = 0.3
    upper_limit(step_size, path, root, ecms, mode, arrow_top)

if __name__ == '__main__':
    main()
