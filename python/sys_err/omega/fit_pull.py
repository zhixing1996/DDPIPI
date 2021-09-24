#!/usr/bin/env python
"""
Fit to pull distribution
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-07-18 Sat 23:21]"

import math
from array import array
import sys, os
import logging
from math import *
from ROOT import *
from tools import pull_range, param_mean, param_sigma
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
    fit_pull.py

SYNOPSIS
    ./fit_pull.py [var]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    July 2020
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.05)

def set_xframe_style(xframe, xtitle, ytitle):
    xframe.GetXaxis().SetTitle(xtitle)
    xframe.GetXaxis().SetTitleSize(0.06)
    xframe.GetXaxis().SetLabelSize(0.06)
    xframe.GetXaxis().SetTitleOffset(1.0)
    xframe.GetXaxis().SetLabelOffset(0.008)
    xframe.GetXaxis().SetNdivisions(508)
    xframe.GetXaxis().CenterTitle()
    xframe.GetYaxis().SetNdivisions(504)
    xframe.GetYaxis().SetTitleSize(0.06)
    xframe.GetYaxis().SetLabelSize(0.06)
    xframe.GetYaxis().SetTitleOffset(1.0)
    xframe.GetYaxis().SetLabelOffset(0.008)
    xframe.GetYaxis().SetTitle(ytitle)
    xframe.GetYaxis().CenterTitle()

def set_pad_style(pad):
    pad.SetLeftMargin(0.15)
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

def fit(ecms, path):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('pull entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')

    mbc = TCanvas('mbc', 'mbc', 1000, 700)
    set_canvas_style(mbc)

    pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    set_pad_style(pad)
    pad.Draw()

    xmin, xmax = pull_range(ecms)
    xbins = 100
    PULL = RooRealVar('pull', 'pull', xmin, xmax)
    data = RooDataSet('data', 'dataset', t_data, RooArgSet(PULL))

    # signal
    mean_low, mean_up = param_mean(ecms)
    sigma_mean, sigma_low, sigma_up = param_sigma(ecms)
    mean = RooRealVar('mean', 'mean of gaussian', 0.0, mean_low, mean_up)
    sigma = RooRealVar('sigma', 'sigma of gaussian', sigma_mean, sigma_low, sigma_up)
    gauss = RooGaussian('gauss', 'gaussian', PULL, mean, sigma)

    # event number
    nsig = RooRealVar('nsig', 'nsig', 500, 0, 100000)

    # fit model
    model = RooAddPdf('model', 'gauss', RooArgList(gauss), RooArgList(nsig))
    model.fitTo(data)

    # plot results
    xframe = PULL.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
    data.plotOn(xframe)
    model.plotOn(xframe)
    model.plotOn(xframe, RooFit.Components('gauss'), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(1))
    xtitle = '(#sigma_{old}-#sigma_{new})/#sigma_{old}'
    ytitle = 'Events'
    set_xframe_style(xframe, xtitle, ytitle)
    xframe.Draw()

    pt = TPaveText(0.6, 0.65, 0.75, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(str(ecms) + ' MeV')
    pt.AddText('#mu: ' + str(round(mean.getVal(), 4)) + '#pm' + str(round(mean.getError(), 4)))
    pt.AddText('#sigma: ' + str(round(sigma.getVal(), 4)) + '#pm' + str(round(sigma.getError(), 4)))

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    with open('./txts/sys_err_' + str(ecms) + '.txt', 'w') as f:
        f.write(str(round(sigma.getVal()*100, 1)) + '\n')

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    mbc.SaveAs('./figs/fit_' + str(ecms) + '_pull.pdf')

    # raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/sys_err/omega/' + str(ecms) + '/xs_diff_' + str(ecms) + '.root')
    fit(ecms, path)

if __name__ == '__main__':
    main()
