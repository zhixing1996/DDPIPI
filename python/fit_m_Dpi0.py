#!/usr/bin/env python
"""
Fit to invariant mass of Dpi0
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-27 Wed 01:14]"

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
    fit_m_Dpi0.py

SYNOPSIS
    ./fit_m_Dpi0.py [ecms]

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

def fit(path, ecms):
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

    xmin = 2.006
    xmax = 2.016
    xbins = 40
    m_Dpi0 = RooRealVar('m_Dpi0', 'm_Dpi0', xmin, xmax)
    data = RooDataSet('data', 'dataset', t_data, RooArgSet(m_Dpi0))

    # signal
    mean = RooRealVar('mean', 'mean of gaussian', 2.01026, 2.008, 2.012)
    sigma = RooRealVar('sigma', 'sigma of gaussian', 0.0001, 0, 0.0012)
    gauss = RooGaussian('gauss', 'gaussian', m_Dpi0, mean, sigma)

    # background
    a = RooRealVar('a', 'a', 0, -99, 99)
    b = RooRealVar('b', 'b', 0, -99, 99)
    c = RooRealVar('c', 'c', 0, -99, 99)
    bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', m_Dpi0, RooArgList(a, b))

    # event number
    nsig = RooRealVar('nsig', 'nsig', 500, 0, 100000)
    nbkg = RooRealVar('nbkg', 'nbkg', 1000, 0, 100000)

    # fit model
    model = RooAddPdf('model', 'gauss+bkgpdf', RooArgList(gauss, bkgpdf), RooArgList(nsig, nbkg))
    model.fitTo(data)

    # plot results
    xframe = m_Dpi0.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
    data.plotOn(xframe)
    model.plotOn(xframe)
    model.plotOn(xframe, RooFit.Components('gauss'), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(1))
    model.plotOn(xframe, RooFit.Components('bkgpdf'), RooFit.LineColor(kGreen), RooFit.LineWidth(2), RooFit.LineStyle(1))
    xtitle = 'M(D^{+}#pi^{0})(GeV)'
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    set_xframe_style(xframe, xtitle, ytitle)
    xframe.Draw()
    range = 'Mass Region: [' + str(mean.getVal() - 3*sigma.getVal()) + ', ' + str(mean.getVal() + 3*sigma.getVal()) + ']'
    print range

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    mbc.SaveAs('./figs/fit_m_Dpi0_'+str(ecms)+'.pdf')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()

    ecms = int(args[0])

    path = []

    if ecms == 4360:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_before.root')
        fit(path, ecms)

    if ecms == 4420:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_before.root')
        fit(path, ecms)

    if ecms == 4600:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_before.root')
        fit(path, ecms)

if __name__ == '__main__':
    main()
