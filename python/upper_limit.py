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
    ./upper_limit.py [ecms] [mode] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def set_graph_style(gr, xtitle, ytitle, xmin, xmax):
    gr.GetXaxis().SetNdivisions(509)
    gr.GetYaxis().SetNdivisions(504)
    gr.SetLineWidth(2)
    gr.SetLineWidth(2)
    gr.GetXaxis().SetTitleSize(0.04)
    gr.GetXaxis().SetTitleOffset(1.4)
    gr.GetXaxis().SetLabelOffset(0.01)
    gr.GetYaxis().SetTitleSize(0.04)
    gr.GetYaxis().SetTitleOffset(1.5)
    gr.GetYaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetXaxis().CenterTitle()
    gr.GetXaxis().SetRangeUser(xmin, xmax)
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

def upper_limit(step_size, path, FILE, ecms, mode, n_offset, patch):
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
    max = n_offset + N*step_size
    count = 0
    likelihood = array('d', N*[0.])
    nsignal = array('d', N*[0.])
    for line in lines:
        rs = line.rstrip('\n')
        rs = filter(None, rs.split(" "))
        nsignal[count] = float(rs[0])
        likelihood[count] = float(rs[1])
        count += 1
    gr = TGraph(N, nsignal, likelihood)

    par = array('d', 6*[0.])
    g1 = TF1('g1', 'gaus', n_offset, max)
    g2 = TF1('g2', 'gaus', n_offset, max)
    f_gauss = TF1('f_gauss', 'gaus(0)+gaus(3)', n_offset, max)
    gr.Fit(g1, 'R')
    gr.Fit(g2, 'R+')
    par1 = g1.GetParameters()
    par2 = g2.GetParameters()
    par[0], par[1], par[2] = par1[0], par1[1], par1[2]
    par[3], par[4], par[5] = par2[0], par2[1], par2[2]
    f_gauss.SetParameters(par)
    gr.Fit(f_gauss, 'R+')
    xtitle = 'yields'
    ytitle = 'normalized likehood value'
    xmin = n_offset
    xmax = max
    set_graph_style(gr, xtitle, ytitle, xmin, xmax)
    gr.Draw('ALP')

    max_prob = f_gauss.Integral(n_offset, max)
    print 'Maximum Probility: ' + str(max_prob)

    for i in xrange(N):
        n_upl = i * step_size
        prob_ = f_gauss.Integral(n_offset, n_upl)
        prob =prob_/max_prob
        if prob >= 0.9:
            print 'prob >= 0.9 , N = ' + str(n_upl)
            break
        print 'prob = ' + str(prob)

    arrow_top = f_gauss.Eval(n_upl)
    arrow = TArrow(n_upl, 0.0, n_upl, arrow_top, 0.01, '<')
    arrow.SetLineColor(kRed)
    arrow.SetLineWidth(3)
    arrow.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/upper_limit_' + mode + '_' + str(ecms) + '.pdf')

    if mode == 'X_3842':
        f = TFile(FILE)
        t = f.Get('save')
        entries = t.GetEntries()
        if (ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420):
            eff = entries/100000.
        else:
            eff = entries/50000.
        lum = luminosity(ecms)
        Br = 0.0938
        xs = round(n_upl/2./Br/eff/lum, 2)
        if not os.path.exists('./txts/'): 
            os.makedirs('./txts/')
        path_out = './txts/xs_upper_limit_' + mode + '_' + str(ecms) + '.txt'
        f_out = open(path_out, 'w')
        out = '& @' + str(ecms) + 'MeV& ' + str(n_upl) + '& ' + str(round(eff*100, 2)) + '\%& ' + str(lum) + '& ' + str(Br*100) + '\%& ' + str(xs) + '& \\\\'
        f_out.write(out)
        f_out.close()
    if mode == 'total':
        f_xs_info = open(FILE, 'r')
        lines_xs = f_xs_info.readlines()
        for line_xs in lines_xs:
            rs_xs = line_xs.rstrip('\n')
            rs_xs = filter(None, rs_xs.split(' '))
            N_data = int(rs_xs[1])
            eff_D1_2420 = float(rs_xs[2])/100.
            eff_psipp = float(rs_xs[3])/100.
            eff_DDPIPI = float(rs_xs[4])/100.
            omega_D1_2420 = float(rs_xs[5])
            omega_psipp = float(rs_xs[6])
            omega_DDPIPI = float(rs_xs[7])
            ISR_D1_2420 = float(rs_xs[8])
            ISR_psipp = float(rs_xs[9])
            ISR_DDPIPI = float(rs_xs[10])
            VP = float(rs_xs[11])
            lum = float(rs_xs[12])
            Br = float(rs_xs[13])/100.
            if omega_D1_2420 == 0:
                flag_D1_2420 = 0
                eff_ISR_VP_D1_2420 = 1
            else:
                flag_D1_2420 = 1
                eff_ISR_VP_D1_2420 = eff_D1_2420*ISR_D1_2420*omega_D1_2420*VP
            if omega_psipp == 0:
                flag_psipp = 0
                eff_ISR_VP_psipp = 1
            else:
                flag_psipp = 1
                eff_ISR_VP_psipp = eff_psipp*ISR_psipp*omega_psipp*VP
            if omega_DDPIPI == 0:
                flag_DDPIPI = 0
                eff_ISR_VP_DDPIPI = 1
            else:
                flag_DDPIPI = 1
                eff_ISR_VP_DDPIPI = eff_DDPIPI*ISR_DDPIPI*omega_DDPIPI*VP
            xs = n_upl/(2*(flag_D1_2420*eff_ISR_VP_D1_2420 + flag_psipp*eff_ISR_VP_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI)*Br*lum)

        if not os.path.exists('./txts/'): 
            os.makedirs('./txts/')
        path_out = './txts/xs_upper_limit_' + mode + '.txt'
        f_out = open(path_out, 'a')
        out = '@' + str(ecms) + 'MeV ' + str(round(xs, 3)) + '\n'
        f_out.write(out)
        f_out.close()

    # raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<3:
        return usage()
    ecms = int(args[0])
    mode = args[1]
    patch = args[2]

    path = './txts/upper_limit_likelihood_' + mode + '_' + str(ecms) + '.txt'
    if mode == 'X_3842':
        FILE = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/' + str(ecms) + '/sigMC_X_3842_' + str(ecms) + '_after.root'
        step_size = 0.1
    if mode == 'total':
        if not (ecms == 4190 or ecms == 4200 or ecms == 4210 or ecms == 4220 or ecms == 4237 or ecms == 4245 or ecms == 4246 or ecms == 4270 or ecms == 4280 or ecms == 4310 or ecms == 4530 or ecms == 4575):
            print str(ecms) + ' MeV\'s sigma is larger than 5 sigma, no need to calculate upper limit!'
            sys.exit()
        FILE = './txts/xs_info_' + str(ecms) + '_read_' + patch + '.txt'
        n_offset, step_size, temp = upl_rm_Dpipi(ecms)
    upper_limit(step_size, path, FILE, ecms, mode, n_offset, patch)

if __name__ == '__main__':
    main()
