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
    fit_rm_Dpipi.py

SYNOPSIS
    ./fit_rm_Dpipi.py [ecms] [mode] [patch]

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

def fit(path, shape_path, ecms, mode, patch):
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

    is_OK = 2
    chi2_ndf = 999.
    while True:
        # signal
        f_shape = TFile(shape_path, 'READ')
        h_shape = f_shape.Get('h_hist')
        h_signal = RooDataHist('h_shape', 'h_shape', RooArgList(rm_Dpipi), h_shape)
        pdf_signal = RooHistPdf('pdf_signal', 'pdf_signal', RooArgSet(rm_Dpipi), h_signal, 0)
        mean_low, mean_up, sigma_up =  param_rm_Dpipi(ecms)
        if not mode == 'data': mean_low, mean_up, sigma_up = mean_low*(1 + random.uniform(-1, 1)), mean_up*(1 + random.uniform(-1, 1)), sigma_up*(1 + random.uniform(-1, 1))
        if sigma_up > 0.001: sigma_up += 0.001
        mean = RooRealVar('mean', 'mean of gaussian', 0., mean_low, mean_up)
        sigma = RooRealVar('sigma', 'sigma of gaussian', 0.001, 0, sigma_up)
        if mode == 'data' and (ecms == 4390 or ecms == 4575):
            if ecms == 4390: f_param = open('./txts/param_4380_' + patch + '.txt', 'r')
            if ecms == 4575: f_param = open('./txts/param_4440_' + patch + '.txt', 'r')
            lines_param = f_param.readlines()
            for line_param in lines_param:
                rs_param = line_param.rstrip('\n')
                rs_param = filter(None, rs_param.split(" "))
                ndf = float(float(rs_param[0]))
                a_val = float(float(rs_param[1]))
                if ndf == 6:
                    b_val = float(float(rs_param[2]))
                    mean_val = float(float(rs_param[3]))
                    sigma_val = float(float(rs_param[4]))
                else:
                    mean_val = float(float(rs_param[2]))
                    sigma_val = float(float(rs_param[3]))
            mean = RooRealVar('mean', 'mean of gaussian', mean_val)
            sigma = RooRealVar('sigma', 'sigma of gaussian', sigma_val)
        gauss = RooGaussian('gauss', 'gaussian', rm_Dpipi, mean, sigma)
        rm_Dpipi.setBins(xbins, 'cache')
        sigpdf = RooFFTConvPdf('sigpdf', 'sigpdf', rm_Dpipi, pdf_signal, gauss)

        # background
        a = RooRealVar('a', 'a', 0, -99, 99)
        b = RooRealVar('b', 'b', 0, -99, 99)
        if ecms == 4700:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4680:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4640:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4600:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4440:
            a = RooRealVar('a', 'a', 0, -3, 1)
            b = RooRealVar('b', 'b', 0, -3, 1)
        if ecms == 4420:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4400:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4380:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        c = RooRealVar('c', 'c', 0, -99, 99)
        d = RooRealVar('c', 'c', 0, -99, 99)
        bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a, b))
        n_free = 6
        if ecms == 4237 or ecms == 4245 or ecms == 4270 or ecms == 4280 or ecms == 4310 or ecms == 4360 or ecms == 4390:
            bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))
            n_free = 5
        if ecms == 4290 or ecms == 4315 or ecms == 4340 or ecms == 4575 or ecms == 4620:
            bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))
            n_free = 5

        # event number
        nsig = RooRealVar('nsig', 'nsig', 100, -500000, 500000)
        nbkg = RooRealVar('nbkg', 'nbkg', 80, 0, 500000)

        # fit model
        model = RooAddPdf('model', 'sigpdf + bkgpdf', RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg))

        results = model.fitTo(data, RooFit.Save())
        is_OK = int(results.covQual())
        status = int(results.status())

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

        if mode == 'data' or mode == 'DDPIPI' or mode == 'D1_2420' or mode == 'psipp':
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
            if mode == 'data': pt = TPaveText(0.17, 0.17, 0.3, 0.35, "BRNDC")
            else: pt = TPaveText(0.17, 0.7, 0.3, 0.85, "BRNDC")
            set_pavetext(pt)
            pt.Draw()
            pt_title = str(ecms) + ' MeV: '
            pt.AddText(pt_title)
            n_param = results.floatParsFinal().getSize()
            pt_title = '#chi^{2}/ndf = '
            pt.AddText(pt_title)
            pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1) + '=' + str(round(chi2_tot/(nbin - n_param -1), 2))
            pt.AddText(pt_title)
            chi2_ndf = chi2_tot/(nbin - n_param -1)
            print 'chi2 vs ndf = ' + str(round(chi2_tot/(nbin - n_param -1), 2))

        if not os.path.exists('./figs/'):
            os.makedirs('./figs/')
        mbc.SaveAs('./figs/fit_rm_Dpipi_' + str(ecms) + '_' + mode + '.pdf')

        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')
        path_sig = './txts/' + mode + '_events_'+ str(ecms) +'_' + patch + '.txt'
        f_sig = open(path_sig, 'w')
        out = str(nsig.getVal()) + ' ' + str(nsig.getError()) + '\n'
        f_sig.write(out)
        f_sig.close()
        if mode == 'data':
            path_param = './txts/param_'+ str(ecms) +'_' + patch + '.txt'
            f_param = open(path_param, 'w')
            param = str(n_free) + ' '
            param += str(a.getVal()) + ' '
            if n_free == 6:
                param += str(b.getVal()) + ' '
            param += str(mean.getVal()) + ' '
            param += str(sigma.getVal()) + ' '
            f_param.write(param)
            f_param.close()

        if mode == 'data': is_OK = -1

        if is_OK == -1: break
        if (is_OK == 3 and status == 0 and chi2_ndf < 1.8 and ecms < 4221): break
        if (is_OK == 3 and status == 0 and chi2_ndf < 1.9 and ecms > 4221): break

    # raw_input('enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<3:
        return usage()
    ecms = int(args[0])
    mode = args[1]
    patch = args[2]

    path = []
    shape_path = ''
    if mode == 'data':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/scale_factor/shape_' + str(ecms) + '_mixed.root'
    if mode == 'psipp' or mode == 'D1_2420':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/' + mode + '/' + str(ecms) + '/sigMC_' + mode + '_' + str(ecms) + '_raw_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/scale_factor/shape_' + mode + '_' + str(ecms) + '_signal.root'
    if mode == 'DDPIPI':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/' + mode + '/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/scale_factor/shape_D_D_PI_PI_' + str(ecms) + '_signal.root'
    fit(path, shape_path, ecms, mode, patch)

if __name__ == '__main__':
    main()
