#!/usr/bin/env python
"""
Fit to invariant mass of Kpipi
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-04-17 Fri 21:09]"

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

# TGaxis::SetMaxDigits(6)
TGaxis.SetMaxDigits(3)

def usage():
    sys.stdout.write('''
NAME
    fit_m_Kpipi.py

SYNOPSIS
    ./fit_m_Kpipi.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    April 2020
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
    xframe.GetYaxis().SetTitleOffset(0.8)
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

def fit(path, ecms, mode, shape_path):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('Entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')

    mbc = TCanvas('mbc', 'mbc', 1000, 700)
    set_canvas_style(mbc)

    pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    set_pad_style(pad)
    pad.Draw()

    xmin = 1.82
    xmax = 1.92
    xbins = 50
    if mode == 'data' and (ecms == 4245 or ecms == 4310): xbins = 25
    m_Kpipi = RooRealVar('rawm_D', 'rawm_D', xmin, xmax)
    data = RooDataSet('data', 'dataset', t_data, RooArgSet(m_Kpipi))

    # signal
    f_shape = TFile(shape_path, 'READ')
    h_shape = f_shape.Get('h_hist')
    h_signal = RooDataHist('h_shape', 'h_shape', RooArgList(m_Kpipi), h_shape)
    pdf_signal = RooHistPdf('pdf_signal', 'pdf_signal', RooArgSet(m_Kpipi), h_signal, 0)
    mean_low, mean_up, sigma_up =  param_m_Kpipi(ecms)
    mean = RooRealVar('mean', 'mean of gaussian', 0., mean_low, mean_up)
    sigma = RooRealVar('sigma', 'sigma of gaussian', 0.001, 0, sigma_up)
    gauss = RooGaussian('gauss', 'gaussian', m_Kpipi, mean, sigma)
    m_Kpipi.setBins(xbins, 'cache')
    sigpdf = RooFFTConvPdf('sigpdf', 'sigpdf', m_Kpipi, pdf_signal, gauss)

    # background
    a = RooRealVar('a', 'a', 0, -99, 99)
    b = RooRealVar('b', 'b', 0, -99, 99)
    c = RooRealVar('c', 'c', 0, -99, 99)
    d = RooRealVar('c', 'c', 0, -99, 99)
    if ecms == 4310:
        a = RooRealVar('a', 'a', 0, -1, 1)
        b = RooRealVar('b', 'b', 0, -1, 1)
    if ecms == 4420:
        a = RooRealVar('a', 'a', 0, -1, 1)
        b = RooRealVar('b', 'b', 0, -1, 1)
    bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', m_Kpipi, RooArgList(a, b))

    # event number
    nsig = RooRealVar('nsig', 'nsig', 100, -5000000, 5000000)
    nbkg = RooRealVar('nbkg', 'nbkg', 80, 0, 5000000)

    # fit model
    model = RooAddPdf('model', 'sigpdf + bkgpdf', RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg))
    results = model.fitTo(data, RooFit.Save())

    # plot results
    xframe = m_Kpipi.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
    data.plotOn(xframe)
    model.plotOn(xframe)
    model.plotOn(xframe, RooFit.Components('sigpdf'), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(1))
    model.plotOn(xframe, RooFit.Components('bkgpdf'), RooFit.LineColor(kGreen), RooFit.LineWidth(2), RooFit.LineStyle(1))

    xtitle = 'M(K^{-}#pi^{+}#pi^{+})(GeV)'
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    set_xframe_style(xframe, xtitle, ytitle)
    xframe.Draw()

    fr = model.fitTo(data, RooFit.Extended(kTRUE), RooFit.Save(kTRUE))
    curve = xframe.getObject(1)
    histo = xframe.getObject(0)
    chi2_tot, nbin, ytot, avg, eyl, eyh = 0, 0, 0, 0, 0, 0
    x = array('d', 999*[0])
    y = array('d', 999*[0])
    for i in xrange(xbins):
        histo.GetPoint(i, x, y)
        exl = histo.GetEXlow()[i]
        exh = histo.GetEXhigh()[i]
        avg += curve.average(x[0] - exl, x[0] + exh)
        ytot += y[0]
        eyl += histo.GetEYlow()[i]  * histo.GetEYlow()[i]
        eyh += histo.GetEYhigh()[i] * histo.GetEYhigh()[i]
        if ytot >= 7:
            if ytot > avg:
                pull = (ytot - avg)/sqrt(eyl)
            else:
                pull = (ytot - avg)/sqrt(eyh)
            chi2_tot += pull * pull
            nbin += 1
            ytot, avg, eyl, eyh = 0, 0, 0, 0
    pt = TPaveText(0.17, 0.7, 0.3, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt_title = str(ecms) + ' MeV: '
    pt.AddText(pt_title)
    n_param = results.floatParsFinal().getSize()
    pt_title = '#chi^{2}/ndf = '
    pt.AddText(pt_title)
    if not (nbin - n_param -1) == 0:
        pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1) + '=' + str(round(chi2_tot/(nbin - n_param -1), 2))
        pt.AddText(pt_title)
        chi2_ndf = chi2_tot/(nbin - n_param - 1)
        print 'chi2 vs ndf = ' + str(round(chi2_tot/(nbin - n_param - 1), 2))
    else:
        pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param) + '=' + str(round(chi2_tot/(nbin - n_param), 2))
        pt.AddText(pt_title)
        chi2_ndf = chi2_tot/(nbin - n_param)
        print 'chi2 vs ndf = ' + str(round(chi2_tot/(nbin - n_param), 2))

    width_low = 1.86965 - width(ecms)/2.
    width_up = 1.86965 + width(ecms)/2.
    widthlow_up = width_low - (width_up - width_low)
    widthlow_low = widthlow_up - (width_up - width_low)
    widthup_low = width_up + (width_up - width_low)
    widthup_up = widthup_low + (width_up - width_low)
    m_Kpipi.setRange('srange', width_low, width_up)
    m_Kpipi.setRange('sbrangel', widthlow_low, widthlow_up)
    m_Kpipi.setRange('sbrangeh', widthup_low, widthup_up)
    nsrange = bkgpdf.createIntegral(RooArgSet(m_Kpipi), RooFit.NormSet(RooArgSet(m_Kpipi)), RooFit.Range('srange'))
    nsbrangel = bkgpdf.createIntegral(RooArgSet(m_Kpipi), RooFit.NormSet(RooArgSet(m_Kpipi)), RooFit.Range('sbrangel'))
    nsbrangeh = bkgpdf.createIntegral(RooArgSet(m_Kpipi), RooFit.NormSet(RooArgSet(m_Kpipi)), RooFit.Range('sbrangeh'))
    n_signal = nsrange.getVal()
    n_sidebandlow = nsbrangel.getVal() 
    n_sidebandup = nsbrangeh.getVal()
    scale_factor = n_signal/(n_sidebandlow + n_sidebandup)
    print 'scale_factor = n(signal) / n(sideband) = ' + str(scale_factor)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_factor = './txts/scale_factor_m_Kpipi_' + str(ecms) + '.txt'
    f_factor = open(path_factor, 'w')
    out = str(scale_factor) + '\n'
    f_factor.write(out)
    f_factor.close()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/fit_m_Kpipi_' + str(ecms) + '_' + mode + '_scale.pdf')

    raw_input('enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    mode = args[1]

    path = []
    if mode == 'data':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_rm_Dpipi_signal.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/scale_factor/shape_' + str(ecms) + '_mixed_scale.root'
        fit(path, ecms, mode, shape_path)
    if mode == 'MC':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sigMC_mixed_width_' + str(ecms) + '_raw.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/scale_factor/shape_' + str(ecms) + '_mixed_scale.root'
        fit(path, ecms, mode, shape_path)

if __name__ == '__main__':
    main()
