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
    ./fit_rm_Dpipi.py [ecms] [mode] [patch]

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

def fit(path, ecms, mode, patch):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('Entries :'+str(entries_data))
    except:
        logging.error('File paths are invalid!')

    mbc = TCanvas('mbc', 'mbc', 1000, 700)
    set_canvas_style(mbc)

    pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    set_pad_style(pad)
    pad.Draw()

    xmin = 1.75
    xmax = 1.95
    xbins = 100
    rm_Dpipi = RooRealVar('rm_Dpipi', 'rm_Dpipi', xmin, xmax)
    data = RooDataSet('data', 'dataset', t_data, RooArgSet(rm_Dpipi))

    # signal
    mean_up, mean_low, sigma_up = param_rm_Dpipi(ecms)
    mean1 = RooRealVar('mean1', 'mean of gaussian', 1.86965, mean_low, mean_up)
    sigma1 = RooRealVar('sigma1', 'sigma of gaussian', 0.001, 0, sigma_up)
    gauss1 = RooGaussian('gauss1', 'gaussian', rm_Dpipi, mean1, sigma1)
    mean2 = RooRealVar('mean2', 'mean of gaussian', 1.86965, mean_low, mean_up)
    sigma2 = RooRealVar('sigma2', 'sigma of gaussian', 0.001, 0, sigma_up)
    gauss2 = RooGaussian('gauss2', 'gaussian', rm_Dpipi, mean2, sigma2)
    frac = RooRealVar('frac', 'fraction od two gaussian', 0.5, 0., 2.)
    sigpdf = RooAddPdf('sigpdf', 'signal pdf', RooArgList(gauss1, gauss2), RooArgList(frac))

    # background
    a = RooRealVar('a', 'a', 0, -99, 99)
    b = RooRealVar('b', 'b', 0, -99, 99)
    c = RooRealVar('c', 'c', 0, -99, 99)
    d = RooRealVar('c', 'c', 0, -99, 99)
    bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))

    if mode == 'upper_limit':
        if not (ecms == 4190 or ecms == 4200 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4237 or ecms == 4245 or ecms == 4246 or ecms == 4270 or ecms == 4280 or ecms == 4310 or ecms == 4530):
            print str(ecms) + ' MeV\'s sigma is larger than 5 sigma, no need to calculate upper limit!'
            sys.exit()
        f_DDPIPI = TFile('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_before.root')
        t_DDPIPI = f_DDPIPI.Get('save')
        cut = ''
        h_DDPIPI = TH1F('h_DDPIPI', '', xbins, xmin, xmax)
        t_DDPIPI.Project('h_DDPIPI', 'rm_Dpipi', cut)
        hist_DDPIPI = RooDataHist('hist_DDPIPI', 'hist_DDPIPI', RooArgList(rm_Dpipi), h_DDPIPI)
        pdf_DDPIPI = RooHistPdf('pdf_DDPIPI', 'pdf_DDPIPI', RooArgSet(rm_Dpipi), hist_DDPIPI, 2)
        mean = RooRealVar('mean', 'mean', 0)
        sigma = RooRealVar('sigma', 'sigma', 0.00123)
        gauss = RooGaussian('gauss', 'guass', rm_Dpipi, mean, sigma)
        rm_Dpipi.setBins(xbins, 'cache')
        sigpdf = RooFFTConvPdf('sigpdf', 'sigpdf', rm_Dpipi, pdf_DDPIPI, gauss)
        
        param_bkg, step_size, step_n = upl_rm_Dpipi(ecms)
        a = RooRealVar('a', 'a', param_bkg)
        bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))

    # event number
    num_low, num_up = num_rm_Dpipi(ecms)
    nsig = RooRealVar('nsig', 'nsig', 100, num_low, num_up)
    nbkg = RooRealVar('nbkg', 'nbkg', 80, 0, 500000)

    # fit model
    if mode == 'data' or mode == 'D1_2420' or mode == 'psipp' or mode == 'DDPIPI' or mode == 'upper_limit':
        model = RooAddPdf('model', 'sigpdf + bkgpdf', RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg))
        results = model.fitTo(data, RooFit.Save())
    if mode == 'none_sig':
        model = RooAddPdf('model', 'bkgpdf', RooArgList(bkgpdf), RooArgList(nbkg))
        results = model.fitTo(data, RooFit.Save())

    if mode == 'data' or mode == 'D1_2420' or mode == 'psipp' or mode == 'DDPIPI' or mode == 'none_sig':
        # plot results
        xframe = rm_Dpipi.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
        data.plotOn(xframe)
        model.plotOn(xframe)
        model.plotOn(xframe, RooFit.Components('gauss1'), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(1))
        model.plotOn(xframe, RooFit.Components('gauss2'), RooFit.LineColor(kYellow), RooFit.LineWidth(2), RooFit.LineStyle(1))
        model.plotOn(xframe, RooFit.Components('bkgpdf'), RooFit.LineColor(kGreen), RooFit.LineWidth(2), RooFit.LineStyle(1))
        xtitle = 'RM(D^{+}#pi^{+}_{0}#pi^{-}_{0})(GeV)'
        content = (xmax - xmin)/xbins * 1000
        ytitle = 'Events/%.1f MeV'%content
        set_xframe_style(xframe, xtitle, ytitle)
        xframe.Draw()

        if not os.path.exists('./figs/'):
            os.makedirs('./figs/')
        mbc.SaveAs('./figs/fit_rm_Dpipi_' + str(ecms) + '_' + mode + '.pdf')

        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')
        path_sig = './txts/' + mode + '_signal_events_'+ str(ecms) +'_' + patch + '.txt'
        f_sig = open(path_sig, 'w')
        out = str(nsig.getVal()) + ' ' + str(nsig.getError()) + '\n'
        f_sig.write(out)
        f_sig.close()
        if mode == 'data' or mode == 'none_sig':
            path_out = './txts/significance_likelihood_total_' + str(ecms) + '.txt'
            f_out = open(path_out, 'a')
            # -log(L) minimum
            sig_out = str(results.minNll()) + '\n'
            f_out.write(sig_out)
            f_out.close()

    if mode == 'upper_limit':
        offset = False
        offsetValue = 0.
        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')

        path_out = './txts/upper_limit_likelihood_total_'+ str(ecms) +'.txt'
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

    # raw_input('enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<3:
        return usage()
    ecms = int(args[0])
    mode = args[1]
    patch = args[2]

    path = []
    if mode == 'data' or mode == 'none_sig' or mode == 'upper_limit':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_before.root')
    if mode == 'D1_2420':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/' + str(ecms) + '/sigMC_D1_2420_' + str(ecms) + '_raw_before.root')
    if mode == 'psipp':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/' + str(ecms) + '/sigMC_psipp_' + str(ecms) + '_raw_before.root')
    if mode == 'DDPIPI':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_before.root')
    fit(path, ecms, mode, patch)

if __name__ == '__main__':
    main()
