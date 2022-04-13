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
    pad.Draw()

    xmin = 1.75
    xmax = 1.95
    xbins = 100
    if mode == 'data_after' and (ecms == 4245 or ecms == 4280 or ecms == 4310 or ecms == 4575): xbins = 50
    if mode == 'data_before' and (ecms == 4245 or ecms == 4280 or ecms == 4310 or ecms == 4575): xbins = 50
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
        if not (mode == 'data_before' or mode == 'data_after'): mean_low, mean_up, sigma_up = mean_low*(1 + random.uniform(-1, 1)), mean_up*(1 + random.uniform(-1, 1)), sigma_up*(1 + random.uniform(-1, 1))
        if sigma_up > 0.001: sigma_up += 0.001
        mean = RooRealVar('mean', 'mean of gaussian', 0., mean_low, mean_up)
        sigma = RooRealVar('sigma', 'sigma of gaussian', 0.001, 0, sigma_up)
        f_param = open('./txts/param_' + str(ecms) + '_' + patch + '.txt', 'r')
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
        if mode == 'data_before' or mode == 'data_after':
            mean = RooRealVar('mean', 'mean of gaussian', mean_val)
            sigma = RooRealVar('sigma', 'sigma of gaussian', sigma_val)
        gauss = RooGaussian('gauss', 'gaussian', rm_Dpipi, mean, sigma)
        rm_Dpipi.setBins(xbins, 'cache')
        sigpdf = RooFFTConvPdf('sigpdf', 'sigpdf', rm_Dpipi, pdf_signal, gauss)

        # background
        if ndf == 6:
            a = RooRealVar('a', 'a', 0., -99., 99.)
            b = RooRealVar('b', 'b', 0., -99., 99.)
            if ecms == 4440:
                a = RooRealVar('a', 'a', 0., -1., 1.)
                b = RooRealVar('b', 'b', 0., -1., 1.)
            if ecms == 4470:
                a = RooRealVar('a', 'a', 0., -1., 1.)
                b = RooRealVar('b', 'b', 0., -1., 1.)
            if ecms == 4260:
                a = RooRealVar('a', 'a', 0., -1., 1.)
                b = RooRealVar('b', 'b', 0., -1., 1.)
            if ecms == 4190:
                a = RooRealVar('a', 'a', 0., -9., 9.)
                b = RooRealVar('b', 'b', 0., -9., 9.)
            bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a, b))
        if ndf == 5:
            a = RooRealVar('a', 'a', 0., -99., 99.)
            bkgpdf = RooChebychev('bkgpdf', 'bkgpdf', rm_Dpipi, RooArgList(a))

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
        model.plotOn(xframe, RooFit.LineWidth(5))
        model.plotOn(xframe, RooFit.Components('sigpdf'), RooFit.LineColor(kRed), RooFit.LineWidth(5), RooFit.LineStyle(9))
        model.plotOn(xframe, RooFit.Components('bkgpdf'), RooFit.LineColor(kGreen), RooFit.LineWidth(5), RooFit.LineStyle(6))
        data.plotOn(xframe)
        xtitle = 'RM(D^{+}#pi^{+}_{d}#pi^{-}_{d}) (GeV/c^{2})'
        content = (xmax - xmin)/xbins * 1000
        ytitle = 'Events/%.1f MeV/c^{2}'%content
        format_data_hist(xframe)
        name_axis(xframe, xtitle, ytitle)
        xframe.Draw()

        if mode == 'data_before' or mode == 'data_after' or mode == 'DDPIPI' or mode == 'psipp' or mode == 'D1_2420':
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
            if mode == 'data_before' or mode == 'data_after':
                if ecms == 4245 or ecms == 4310: pt = TPaveText(0.6, 0.7, 0.75, 0.85, "BRNDC")
                else: pt = TPaveText(0.17, 0.15, 0.3, 0.25, "BRNDC")
            else: pt = TPaveText(0.17, 0.7, 0.3, 0.85, "BRNDC")
            set_pavetext(pt)
            pt.Draw()
            if ecms == 4230: pt_title = '(b)'
            elif ecms == 4420: pt_title = '(d)'
            elif ecms == 4680: pt_title = '(f)'
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
        mbc.SaveAs('./figs/fit_rm_Dpipi_' + str(ecms) + '_' + mode + '_sideband.pdf')

        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')
        if mode == 'data_after': path_sig = './txts/data_sideband_events_'+ str(ecms) +'_' + patch + '.txt'
        if not mode == 'data_after': path_sig = './txts/' + mode + '_sideband_events_'+ str(ecms) +'_' + patch + '.txt'
        f_sig = open(path_sig, 'w')
        out = str(nsig.getVal()) + ' ' + str(nsig.getError()) + '\n'
        f_sig.write(out)
        f_sig.close()

        if mode == 'data_before': is_OK = -1
        if mode == 'data_after': is_OK = -1
        if mode == 'D1_2420': is_OK = -1
        if mode == 'psipp': is_OK = -1
        if mode == 'DDPIPI': is_OK = -1
        if mode == 'DDPI': is_OK = -1

        if is_OK == -1: break
        if (is_OK == 3 and status == 0 and chi2_ndf < 1.8 and ecms < 4221): break
        if (is_OK == 3 and status == 0 and chi2_ndf < 1.5 and ecms > 4221): break

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
    if mode == 'data_before':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_sideband_before.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    if mode == 'data_after':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_raw_sideband_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
    if mode == 'psipp' or mode == 'D1_2420':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/' + mode + '/' + str(ecms) + '/sigMC_' + mode + '_' + str(ecms) + '_raw_sideband_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_' + mode + '_' + str(ecms) + '_signal.root'
    if mode == 'DDPIPI':
        path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/' + mode + '/' + str(ecms) + '/sigMC_D_D_PI_PI_' + str(ecms) + '_raw_sideband_after.root')
        shape_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_' + str(ecms) + '_signal.root'
    fit(path, shape_path, ecms, mode, patch)

if __name__ == '__main__':
    main()
