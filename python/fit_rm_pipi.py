#!/usr/bin/env python
"""
Fit to recoiling mass of pipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-27 Wed 06:41]"

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
    fit_rm_pipi.py

SYNOPSIS
    ./fit_rm_pipi.py [ecms] [mode] (mode = sig or none_sig)

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

def fit(path, ecms, xmin, xmax, xbins, mode, step_size, step_n):
    try:
        f_data = TFile(path[0])
        f_X3842 = TFile(path[1])
        t_data = f_data.Get('save')
        t_X3842 = f_X3842.Get('save')
        entries_data = t_data.GetEntries()
        entries_X3842 = t_X3842.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('X(3842) entries :'+str(entries_X3842))
    except:
        logging.error('File paths are invalid!')

    mbc = TCanvas('mbc', 'mbc', 1000, 700)
    set_canvas_style(mbc)

    pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    set_pad_style(pad)
    pad.Draw()

    rm_pipi = RooRealVar('rm_pipi', 'rm_pipi', xmin, xmax)
    data = RooDataSet('data', 'dataset', t_data, RooArgSet(rm_pipi))

    # signal
    cut = ''
    h_X3842 = TH1F('h_X3842', '', xbins, xmin, xmax)
    t_X3842.Project('h_X3842', 'rm_pipi', cut)
    hist_X3842 = RooDataHist('hist_X3842', 'hist_X3842', RooArgList(rm_pipi), h_X3842)
    pdf_X3842 = RooHistPdf('pdf_X3842', 'pdf_X3842', RooArgSet(rm_pipi), hist_X3842, 2)
    mean = RooRealVar('mean', 'mean', 0)
    sigma = RooRealVar('sigma', 'sigma', 0.00123)
    gauss = RooGaussian('gauss', 'guass', rm_pipi, mean, sigma)
    rm_pipi.setBins(xbins, 'cache')
    sigpdf = RooFFTConvPdf('sigpdf', 'sigpdf', rm_pipi, pdf_X3842, gauss)

    # background
    a = RooRealVar('a', 'a', 0, -99, 99)
    b = RooRealVar('b', 'b', 0, -99, 99)
    c = RooRealVar('c', 'c', 0, -99, 99)
    bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_pipi, RooArgList(a, b))

    # event number
    nsig = RooRealVar('nsig', 'nsig', 0, 10000)
    nbkg = RooRealVar('nbkg', 'nbkg', 0, 10000)

    # fit model
    if mode == 'sig' or mode == 'upper_limit':
        model = RooAddPdf('model', 'sigpdf + bkgpdf', RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg))
        results = model.fitTo(data, RooFit.Save())
    if mode == 'none_sig':
        model = RooAddPdf('model', 'bkgpdf', RooArgList(bkgpdf), RooArgList(nbkg))
        results = model.fitTo(data, RooFit.Save())

    if mode == 'sig' or mode == 'none_sig':
        # plot results
        xframe = rm_pipi.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
        data.plotOn(xframe)
        model.plotOn(xframe)
        if mode == 'sig':
            model.plotOn(xframe, RooFit.Components('sigpdf'), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(1))
        model.plotOn(xframe, RooFit.Components('bkgpdf'), RooFit.LineColor(kGreen), RooFit.LineWidth(2), RooFit.LineStyle(1))
        xtitle = 'RM(#pi^{+}_{0}#pi^{-}_{0})(GeV)'
        content = (xmax - xmin)/xbins * 1000
        ytitle = 'Events/%.1f MeV'%content
        set_xframe_style(xframe, xtitle, ytitle)
        xframe.Draw()

        if not os.path.exists('./figs/'):
            os.makedirs('./figs/')

        mbc.SaveAs('./figs/fit_rm_pipi_'+str(ecms)+'_'+mode+'.pdf')

        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')

        path_out = './txts/significance_likelihood_' + str(ecms) + '.txt'
        f_out = open(path_out, 'a')
        # -log(L) minimum
        out = str(results.minNll()) + '\n'
        f_out.write(out)
        f_out.close()

    if mode == 'upper_limit':
        offset = False
        offsetValue = 0.
        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')

        path_out = './txts/upper_limit_likelihood_'+ str(ecms) +'.txt'
        f_out = open(path_out, 'w')

        for i in xrange(step_n):
            nsignal = i * step_size
            nsig.setVal(nsignal)
            nsig.setConstant()
            results = model.fitTo(data, RooFit.Save())
            if not offset:
                offsetValue = results.minNll()
                offset = True
            line = str(nsignal) + ' ' + str(TMath.Exp(offsetValue - results.minNll())) + '\n'
            f_out.write(line)
        f_out.close()

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    mode = args[1]

    path = []
    if ecms == 4360:
        xmin = 3.8
        xmax = 3.9
        xbins = 40
        step_size = 0.1
        step_n = 500
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_after.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/sigMC_X_3842_4360_after.root')
        fit(path, ecms, xmin, xmax, xbins, mode, step_size, step_n)

    if ecms == 4420:
        xmin = 3.8
        xmax = 3.9
        xbins = 40
        step_size = 0.1
        step_n = 1000
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_after.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/sigMC_X_3842_4420_after.root')
        fit(path, ecms, xmin, xmax, xbins, mode, step_size, step_n)

    if ecms == 4600:
        xmin = 3.8
        xmax = 3.9
        xbins = 40
        step_size = 0.1
        step_n = 700
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_after.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/sigMC_X_3842_4600_after.root')
        fit(path, ecms, xmin, xmax, xbins, mode, step_size, step_n)

    if not (ecms == 4360 or ecms == 4420 or ecms == 4600) and ecms >= 4190:
        xmin = 3.8
        xmax = 3.9
        xbins = 40
        step_size = 0.1
        step_n = 700
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_after.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/' + str(ecms) + '/sigMC_X_3842_' + str(ecms) + '_after.root')
        fit(path, ecms, xmin, xmax, xbins, mode, step_size, step_n)

if __name__ == '__main__':
    main()
