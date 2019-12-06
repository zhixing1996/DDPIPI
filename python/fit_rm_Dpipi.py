#!/usr/bin/env python
"""
Fit to recoiling mass of Dpipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-27 Wed 01:25]"

import math
from array import array
import sys, os
import logging
from math import *
from tools import *
from ROOT import *
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
    fit_rm_Dpipi.py

SYNOPSIS
    ./fit_rm_Dpipi.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

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
    xframe.GetYaxis().SetTitleOffset(1.1)
    xframe.GetYaxis().SetLabelOffset(0.008)
    xframe.GetYaxis().SetTitle(ytitle)
    xframe.GetYaxis().CenterTitle()

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

def fit(path, ecms, mode):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error('File paths are invalid!')

    mbc = TCanvas('mbc', 'mbc', 1000, 700)
    set_canvas_style(mbc)

    pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    set_pad_style(pad)
    pad.Draw()

    if mode == 'data':
        xmin = 1.75
        xmax = 1.95
        xbins = 50
        rm_Dpipi = RooRealVar('rm_Dpipi', 'rm_Dpipi', xmin, xmax)
        data = RooDataSet('data', 'dataset', t_data, RooArgSet(rm_Dpipi))
    if mode == 'D1_2420' or mode == 'psipp':
        xmin = 1.84
        xmax = 1.9
        xbins = 40
        rm_Dpipi = RooRealVar('rm_Dpipi', 'rm_Dpipi', xmin, xmax)
        data = RooDataSet('data', 'dataset', t_data, RooArgSet(rm_Dpipi))

    # signal
    if ecms == 4360:
        mean = RooRealVar('mean', 'mean of gaussian', 1.86965, 1.865, 1.875)
        sigma = RooRealVar('sigma', 'sigma of gaussian', 0.01, 0, 0.01)
        sigpdf = RooGaussian('sigpdf', 'gaussian', rm_Dpipi, mean, sigma)
    if ecms == 4420:
        mean = RooRealVar('mean', 'mean of gaussian', 1.86965, 1.865, 1.875)
        sigma = RooRealVar('sigma', 'sigma of gaussian', 0.01, 0, 0.1)
        sigpdf = RooGaussian('sigpdf', 'gaussian', rm_Dpipi, mean, sigma)
    if ecms == 4600:
        mean = RooRealVar('mean', 'mean of gaussian', 1.86965, 1.865, 1.875)
        sigma = RooRealVar('sigma', 'sigma of gaussian', 0.01, 0, 0.01)
        sigpdf = RooGaussian('sigpdf', 'gaussian', rm_Dpipi, mean, sigma)

    # background
    a = RooRealVar('a', 'a', 0, -99, 99)
    b = RooRealVar('b', 'b', 0, -99, 99)
    c = RooRealVar('c', 'c', 0, -99, 99)
    d = RooRealVar('c', 'c', 0, -99, 99)
    if ecms == 4360:
        bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a, b))
    if ecms == 4420:
        bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a, b))
    if ecms == 4600:
        bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a, b))

    # event number
    nsig = RooRealVar('nsig', 'nsig', 100, 0, 500000)
    nbkg = RooRealVar('nbkg', 'nbkg', 80, 0, 500000)

    # fit model
    model = RooAddPdf('model', 'sigpdf + bkgpdf', RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg))
    model.fitTo(data)

    # plot results
    xframe = rm_Dpipi.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
    data.plotOn(xframe)
    model.plotOn(xframe)
    model.plotOn(xframe, RooFit.Components('sigpdf'), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(1))
    model.plotOn(xframe, RooFit.Components('bkgpdf'), RooFit.LineColor(kGreen), RooFit.LineWidth(2), RooFit.LineStyle(1))
    xtitle = 'RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})(GeV)'
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    set_xframe_style(xframe, xtitle, ytitle)
    xframe.Draw()

    if mode == 'data':
        window_low = 1.86965 - window(ecms)/2.
        window_up = 1.86965 + window(ecms)/2.
        windowlow_up = window_low - (window_up - window_low)
        windowlow_low = windowlow_up - (window_up - window_low)
        windowup_low = window_up + (window_up - window_low)
        windowup_up = windowup_low + (window_up - window_low)
        rm_Dpipi.setRange('srange', window_low, window_up)
        rm_Dpipi.setRange('sbrangel', windowlow_low, windowlow_up)
        rm_Dpipi.setRange('sbrangeh', windowup_low, windowup_up)
        nsrange = bkgpdf.createIntegral(RooArgSet(rm_Dpipi), RooFit.NormSet(RooArgSet(rm_Dpipi)), RooFit.Range('srange'))
        nsbrangel = bkgpdf.createIntegral(RooArgSet(rm_Dpipi), RooFit.NormSet(RooArgSet(rm_Dpipi)), RooFit.Range('sbrangel'))
        nsbrangeh = bkgpdf.createIntegral(RooArgSet(rm_Dpipi), RooFit.NormSet(RooArgSet(rm_Dpipi)), RooFit.Range('sbrangeh'))
        S_srv = nsrange.getVal()*(nbkg.getVal()) + nsig.getVal()
        srv = nsrange.getVal()*nbkg.getVal()
        srv_err = nsrange.getVal()*nbkg.getError()
        sbrlv = nsbrangel.getVal()*nbkg.getVal()
        sbrhv = nsbrangeh.getVal()*nbkg.getVal()
        out1 = 'S_srv: ' + str(S_srv) + ' srv: ' + str(srv) + ' srv_err: ' + str(srv_err) + ' sbrlv: ' + str(sbrlv) + ' sbrhv: ' + str(sbrhv)
        out2 = 'nsrange: ' + str(nsrange.getVal()) + ' nsbrangl: ' + str(nsbrangel.getVal()) + ' nsbrangeh: ' + str(nsbrangeh.getVal())
        print out1
        print out2

        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')

        path_out = './txts/background_events_'+ str(ecms) +'.txt'
        f_out = open(path_out, 'w')
        f_out.write(out1)
        f_out.write(out2)
        f_out.close()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    mbc.SaveAs('./figs/fit_rm_Dpipi_'+str(ecms)+'_'+mode+'.pdf')

    range = 'Mass Region: [' + str(mean.getVal() - 3*sigma.getVal()) + ', ' + str(mean.getVal() + 3*sigma.getVal()) + ']'
    print range

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()

    ecms = int(args[0])
    mode = args[1]

    path = []

    if ecms == 4360:
        if mode == 'data':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_raw_before.root')
        if mode == 'D1_2420':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_raw_before.root')
        if mode == 'psipp':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_raw_before.root')
        fit(path, ecms, mode)

    if ecms == 4420:
        if mode == 'data':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_raw_before.root')
        if mode == 'D1_2420':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_raw_before.root')
        if mode == 'psipp':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_raw_before.root')
        fit(path, ecms, mode)

    if ecms == 4600:
        if mode == 'data':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_raw_before.root')
        if mode == 'D1_2420':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_raw_before.root')
        if mode == 'psipp':
            path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_raw_before.root')
        fit(path, ecms, mode)

if __name__ == '__main__':
    main()
