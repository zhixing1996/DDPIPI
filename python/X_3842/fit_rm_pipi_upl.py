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
import random
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
    ./fit_rm_pipi.py [ecms] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

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

def fit(path, shape_path, ecms, patch):
    try:
        f_data = TFile(path[0])
        f_X_3842 = TFile(shape_path)
        t_data = f_data.Get('save')
        t_X_3842 = f_X_3842.Get('save')
        entries_data = t_data.GetEntries()
        entries_X_3842 = t_X_3842.GetEntries()
        logging.info('Entries(data) :'+str(entries_data))
        logging.info('Entries(X_3842) :'+str(entries_X_3842))
    except:
        logging.error('File paths are invalid!')

    mbc = TCanvas('mbc', 'mbc', 1000, 700)
    set_canvas_style(mbc)

    pad = TPad('pad', 'pad', 0.0, 0.0, 1.0, 1.0)
    set_pad_style(pad)
    pad.Draw()

    xmin = 3.79
    xmax = 3.89
    xbins = 50
    rm_pipi = RooRealVar('rm_pipi', 'rm_pipi', xmin, xmax)
    data = RooDataSet('data', 'dataset', t_data, RooArgSet(rm_pipi))

    n_offset, step_size, step_n = upl_rm_pipi(ecms)
    offset = False
    offsetValue = 0.
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    path_out = './txts/upper_limit_likelihood_total_' + str(ecms) + '.txt'
    f_out = open(path_out, 'w')

    f_param = open('./txts/param_' + str(ecms) + '_' + patch + '.txt', 'r')
    lines_param = f_param.readlines()
    for line_param in lines_param:
        rs_param = line_param.rstrip('\n')
        rs_param = filter(None, rs_param.split(" "))
        ndf = float(float(rs_param[0]))
        a_val = float(float(rs_param[1]))
        b_val = float(float(rs_param[2]))
        mean_val = float(float(rs_param[3]))
        sigma_val = float(float(rs_param[4]))

    # signal
    cut = ''
    h_X_3842_rm_pipi = TH1F('h_X_3842_rm_pipi', '', xbins, xmin, xmax)
    t_X_3842.Project('h_X_3842_rm_pipi', 'rm_pipi', cut)
    hist_X_3842_rm_pipi = RooDataHist('hist_X_3842_rm_pipi', 'hist_X_3842_rm_pipi', RooArgList(rm_pipi), h_X_3842_rm_pipi)
    pdf_signal = RooHistPdf('pdf_X_3842_rm_pipi', 'pdf_X_3842_rm_pipi', RooArgSet(rm_pipi), hist_X_3842_rm_pipi, 1)
    mean = RooRealVar('mean', 'mean of gaussian', mean_val)
    sigma = RooRealVar('sigma', 'sigma of gaussian', sigma_val)
    gauss = RooGaussian('gauss', 'gaussian', rm_pipi, mean, sigma)
    rm_pipi.setBins(xbins, 'cache')
    sigpdf = RooFFTConvPdf('sigpdf', 'sigpdf', rm_pipi, pdf_signal, gauss)

    # background
    a = RooRealVar('a', 'a', a_val)
    b = RooRealVar('b', 'b', b_val)
    bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_pipi, RooArgList(a, b))

    # event number
    nsig = RooRealVar('nsig', 'nsig', 100, -500000, 500000)
    nbkg = RooRealVar('nbkg', 'nbkg', 80, 0, 500000)

    # fit model
    model = RooAddPdf('model', 'sigpdf + bkgpdf', RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg))

    for i in xrange(step_n):
        nsignal = n_offset + i * step_size
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
    patch = args[1]

    path = []
    shape_path = ''
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_after.root')
    shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/' + str(ecms) + '/sigMC_X_3842_' + str(ecms) + '_after.root'
    fit(path, shape_path, ecms, patch)

if __name__ == '__main__':
    main()
