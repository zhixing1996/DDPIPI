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

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.04)

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

    # signal
    f_shape = TFile(shape_path, 'READ')
    h_shape = f_shape.Get('h_hist')
    h_signal = RooDataHist('h_shape', 'h_shape', RooArgList(rm_Dpipi), h_shape)
    pdf_signal = RooHistPdf('pdf_signal', 'pdf_signal', RooArgSet(rm_Dpipi), h_signal, 0)
    mean = RooRealVar('mean', 'mean of gaussian', 0.001, -0.003, 0.003)
    if ecms == 4290 or ecms == 4315 or ecms == 4340 or ecms == 4380 or ecms == 4390 or ecms == 4400 or ecms == 4420 or ecms == 4440 or ecms == 4600:
        mean = RooRealVar('mean', 'mean of gaussian', 0.001, -0.005, 0.005)
    if ecms == 4237:
        mean = RooRealVar('mean', 'mean of gaussian', 0.001, -0.007, 0.007)
    if ecms == 4260 or ecms == 4237:
        mean = RooRealVar('mean', 'mean of gaussian', 0.001, -0.002, 0.002)
    sigma = RooRealVar('sigma', 'sigma of gaussian', 0.001, 0, 0.003)
    if ecms == 4245 or ecms == 4620:
        sigma = RooRealVar('sigma', 'sigma of gaussian', 0.001, 0, 0.005)
    gauss = RooGaussian('gauss', 'gaussian', rm_Dpipi, mean, sigma)
    rm_Dpipi.setBins(xbins, 'cache')
    sigpdf = RooFFTConvPdf('sigpdf', 'sigpdf', rm_Dpipi, pdf_signal, gauss)

    if mode == 'D1_2420' or mode == 'DDPIPI' or mode == 'psipp':
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
    bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a, b))
    n_free = 6
    if ecms == 4237 or ecms == 4245 or ecms == 4246 or ecms == 4260 or ecms == 4270 or ecms == 4280 or ecms == 4310 or ecms == 4360 or ecms == 4390 or ecms == 4470 or ecms == 4600:
        bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))
        n_free = 5
    if ecms == 4290 or ecms == 4315 or ecms == 4340 or ecms == 4400 or ecms == 4575 or ecms == 4620 or ecms == 4640 or ecms == 4660 or ecms == 4680:
        bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))
        n_free = 5

    if mode == 'upper_limit':
        if not (ecms == 4190 or ecms == 4200 or ecms == 4210 or ecms == 4220 or ecms == 4237 or ecms == 4245 or ecms == 4246 or ecms == 4270 or ecms == 4280 or ecms == 4310 or ecms == 4530 or ecms == 4575):
            print str(ecms) + ' MeV\'s sigma is larger than 5 sigma, no need to calculate upper limit!'
            sys.exit()

    # event number
    nsig = RooRealVar('nsig', 'nsig', 100, -500000, 500000)
    nbkg = RooRealVar('nbkg', 'nbkg', 80, 0, 500000)

    # fit model
    model = RooAddPdf('model', 'sigpdf + bkgpdf', RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg))
    if mode == 'none_sig':
        model = RooAddPdf('model', 'bkgpdf', RooArgList(bkgpdf), RooArgList(nbkg))
    results = model.fitTo(data, RooFit.Save())

    if not mode == 'upper_limit':
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

        if not (mode == 'D1_2420' or mode == 'DDPIPI' or mode == 'psipp' or mode == 'none_sig' or mode == 'MC'):
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
            pt = TPaveText(0.65, 0.65, 0.75, 0.8, "BRNDC")
            set_pavetext(pt)
            pt.Draw()
            pt_title = str(ecms) + ' MeV: '
            pt.AddText(pt_title)
            n_param = results.floatParsFinal().getSize()
            pt_title = '#chi^{2}/ndf = '
            pt.AddText(pt_title)
            pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1) + '=' + str(round(chi2_tot/(nbin - n_param -1), 2))
            pt.AddText(pt_title)
            print 'chi2 vs ndf = ' + str(round(chi2_tot/(nbin - n_param -1), 2))

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
        if mode == 'data':
            path_sig_tot = './txts/' + mode + '_signal_events_total_' + patch + '.txt'
            f_sig_tot = open(path_sig_tot, 'a')
            out_tot = str(ecms) + '\t' + str(int(nsig.getVal())) + '\t' + str(int(nsig.getError())) + '\n'
            f_sig_tot.write(out_tot)
            f_sig_tot.close()
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

        if mode == 'data' or mode == 'MC':
            signal_low = 1.86965 - window(ecms)/2.
            signal_up = 1.86965 + window(ecms)/2.
            rm_Dpipi.setRange('srange', signal_low, signal_up)
            rm_Dpipi.setRange('allrange', xmin, xmax)
            nsrange = sigpdf.createIntegral(RooArgSet(rm_Dpipi), RooFit.NormSet(RooArgSet(rm_Dpipi)), RooFit.Range('srange'))
            nallrange = sigpdf.createIntegral(RooArgSet(rm_Dpipi), RooFit.NormSet(RooArgSet(rm_Dpipi)), RooFit.Range('allrange'))
            n_signal = nsrange.getVal()/nallrange.getVal() * (nsig.getVal())
            n_all = nsig.getVal()
            n_signal_err = nsrange.getVal()/nallrange.getVal() * (nsig.getError())
            n_all_err = nsig.getError()
            factor = n_signal/n_all
            factor_err = sqrt(n_signal_err**2/n_signal**2 + n_all_err**2/n_all**2)
            print 'factor = n(signal) / n(all) = ' + str(round(factor, 4)) + '+/-' + str(round(factor_err, 4))
            path_factor = './txts/factor_rm_Dpipi_' + str(ecms) + '_' + mode + '_' + patch + '.txt'
            f_factor = open(path_factor, 'w')
            out = str(round(factor, 4)) + ' ' + str(round(factor_err, 4)) + '\n'
            f_factor.write(out)
            f_factor.close()

        if mode == 'data' or mode == 'none_sig':
            path_out = './txts/significance_likelihood_total_' + str(ecms) + '.txt'
            f_out = open(path_out, 'a')
            # -log(L) minimum
            sig_out = str(results.minNll()) + '\n'
            f_out.write(sig_out)
            f_out.close()

    if mode == 'upper_limit':
        n_offset, step_size, step_n = upl_rm_Dpipi(ecms)
        offset = False
        offsetValue = 0.
        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')

        path_out = './txts/upper_limit_likelihood_total_'+ str(ecms) +'.txt'
        f_out = open(path_out, 'w')

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
    if mode == 'data' or mode == 'none_sig' or mode == 'upper_limit':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_before.root')
        shape_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    if mode == 'MC':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sigMC_mixed_window_' + str(ecms) + '.root')
        shape_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    if mode == 'sideband':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_sideband_before.root')
        shape_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    if mode == 'psipp' or mode == 'D1_2420':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/' + str(mode) + '/' + str(ecms) + '/sigMC_' + str(mode) + '_' + str(ecms) + '_raw_before.root')
        shape_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    if mode == 'DDPIPI':
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/' + str(mode) + '/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_before.root')
        shape_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    fit(path, shape_path, ecms, mode, patch)

if __name__ == '__main__':
    main()
