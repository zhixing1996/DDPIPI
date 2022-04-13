#!/usr/bin/env python
"""
Fit to recoiling mass of Dpipi in M(Kpipi) sideband
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2021-01-04 Mon 12:20]"

import math
from array import array
import sys, os
import logging
from math import *
from tools import *
from ROOT import *
import random
from tools import width, set_pub_style, set_prelim_style, name_axis, format_data_hist, set_arrow, set_pavetext, position_convert, set_legend, format_mc_hist
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

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

def set_pad_style(pad):
    pad.SetLeftMargin(0.35)
    pad.SetRightMargin(0.15)
    pad.SetTopMargin(0.1)
    pad.SetBottomMargin(0.15)
    pad.SetFrameLineColor(kBlack)

def fit(path, shape_path, ecms, mode, patch):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('Entries :'+str(entries_data))
    except:
        logging.error('File paths are invalid!')

    set_pub_style()
    set_prelim_style()

    mbc = TCanvas('mbc', 'mbc', 1000, 700)

    pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    # set_pad_style(pad)
    pad.Draw()

    xmin = 1.75
    xmax = 1.95
    xbins = 100
    if mode == 'data' and (ecms == 4245 or ecms == 4280 or ecms == 4310 or ecms == 4575): xbins = 50
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
        if mode == 'data' and (ecms == 4245 or ecms == 4390 or ecms == 4575 or ecms == 4946 or ecms == 4237 or ecms == 4220 or ecms == 4210 or ecms == 4200 or ecms == 4190):
            if ecms == 4190: f_param = open('./txts/param_4230_' + patch + '.txt', 'r')
            if ecms == 4200: f_param = open('./txts/param_4230_' + patch + '.txt', 'r')
            if ecms == 4210: f_param = open('./txts/param_4230_' + patch + '.txt', 'r')
            if ecms == 4220: f_param = open('./txts/param_4230_' + patch + '.txt', 'r')
            if ecms == 4237: f_param = open('./txts/param_4230_' + patch + '.txt', 'r')
            if ecms == 4245: f_param = open('./txts/param_4246_' + patch + '.txt', 'r')
            if ecms == 4390: f_param = open('./txts/param_4380_' + patch + '.txt', 'r')
            if ecms == 4575 or ecms == 4530: f_param = open('./txts/param_4440_' + patch + '.txt', 'r')
            if ecms == 4946: f_param = open('./txts/param_4914_' + patch + '.txt', 'r')
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
        if ecms == 4780:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4700:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4640:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4600:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4440:
            a = RooRealVar('a', 'a', 0, -9, 9)
            b = RooRealVar('b', 'b', 0, -9, 9)
        if ecms == 4400:
            a = RooRealVar('a', 'a', 0, -1, 1)
            b = RooRealVar('b', 'b', 0, -1, 1)
        if ecms == 4380:
            a = RooRealVar('a', 'a', 0, -9, 9)
            b = RooRealVar('b', 'b', 0, -9, 9)
        c = RooRealVar('c', 'c', 0, -99, 99)
        d = RooRealVar('c', 'c', 0, -99, 99)
        bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a, b))
        n_free = 6
        if ecms == 4237 or ecms == 4245 or ecms == 4270 or ecms == 4280 or ecms == 4310 or ecms == 4360 or ecms == 4390:
            bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))
            n_free = 5
        if ecms == 4290 or ecms == 4315 or ecms == 4340 or ecms == 4575 or ecms == 4620 or ecms == 4740 or ecms == 4750 or ecms == 4780 or ecms == 4840:
            bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))
            n_free = 5

        # event number
        nsig = RooRealVar('nsig', 'nsig', 100, -500000, 500000)
        nbkg = RooRealVar('nbkg', 'nbkg', 80, 0, 500000)

        # fit model
        model = RooAddPdf('model', 'sigpdf + bkgpdf', RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg))
        if mode == 'none_sig': model = RooAddPdf('model', 'bkgpdf', RooArgList(bkgpdf), RooArgList(nbkg))

        results = model.fitTo(data, RooFit.Save())
        is_OK = int(results.covQual())
        status = int(results.status())

        # plot results
        xframe = rm_Dpipi.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
        data.plotOn(xframe)
        model.plotOn(xframe, RooFit.LineWidth(5))
        if not mode == 'none_sig': model.plotOn(xframe, RooFit.Components('sigpdf'), RooFit.LineColor(kRed), RooFit.LineWidth(5), RooFit.LineStyle(9))
        model.plotOn(xframe, RooFit.Components('bkgpdf'), RooFit.LineColor(kGreen), RooFit.LineWidth(5), RooFit.LineStyle(6))
        data.plotOn(xframe)
        xtitle = 'RM(D^{+}#pi^{+}_{d}#pi^{-}_{d}) (GeV/c^{2})'
        content = (xmax - xmin)/xbins * 1000
        ytitle = 'Events/%.1f MeV/c^{2}'%content
        format_data_hist(xframe)
        name_axis(xframe, xtitle, ytitle)
        xframe.Draw()

        if mode == 'data' or mode == 'DDPIPI' or mode == 'psipp' or mode == 'D1_2420' or mode == 'MC':
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
            if mode == 'data':
                if ecms == 4245 or ecms == 4310: pt = TPaveText(0.6, 0.7, 0.75, 0.85, "BRNDC")
                else: pt = TPaveText(0.17, 0.15, 0.3, 0.25, "BRNDC")
            else: pt = TPaveText(0.17, 0.7, 0.3, 0.85, "BRNDC")
            set_pavetext(pt)
            pt.Draw()
            if ecms == 4230: pt_title = '(a)'
            elif ecms == 4420: pt_title = '(c)'
            elif ecms == 4680: pt_title = '(e)'
            else: pt_title = str(ecms) + ' MeV: '
            pt.AddText(pt_title)
            n_param = results.floatParsFinal().getSize()
            pt_title = '#chi^{2}/ndf = '
            # pt.AddText(pt_title)
            pt_title = str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1) + '=' + str(round(chi2_tot/(nbin - n_param -1), 2))
            chi2_ndf = chi2_tot/(nbin - n_param -1)
            # pt.AddText(pt_title)
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

        if mode == 'data' or mode == 'D1_2420' or mode == 'DDPIPI' or mode == 'psipp' or mode == 'MC':
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
            factor_err = sqrt(abs(factor*(1 - factor)/n_all))
            print 'factor = n(signal) / n(all) = ' + str(round(factor, 4)) + '+/-' + str(round(factor_err, 4))
            path_factor = './txts/factor_rm_Dpipi_' + str(ecms) + '_' + mode + '.txt'
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

        if mode == 'data' or mode == 'none_sig': is_OK = -1

        if is_OK == -1: break
        if (is_OK == 3 and status == 0 and chi2_ndf < 3. and ecms > 4221): break
        if (is_OK == 3 and status == 0 and chi2_ndf < 5. and ecms < 4221): break

    raw_input('enter anything to end...')

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
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    if mode == 'psipp' or mode == 'D1_2420':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/' + mode + '/' + str(ecms) + '/sigMC_' + mode + '_' + str(ecms) + '_raw_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_' + mode + '_' + str(ecms) + '_signal.root'
    if mode == 'DDPIPI':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/' + mode + '/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_' + str(ecms) + '_signal.root'
    if mode == 'MC':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sigMC_mixed_window_' + str(ecms) + '_raw_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    fit(path, shape_path, ecms, mode, patch)

if __name__ == '__main__':
    main()
