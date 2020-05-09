#!/usr/bin/env python
"""
Simultaneous fit of recoiling mass of D and Dmiss and recoiling mass of tagged piplus and piminus
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-19 Thu 15:02]"

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
    fit_rm_D.py

SYNOPSIS
    ./fit_rm_D.py [ecms] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def set_frame_style(frame, xtitle, ytitle):
    frame.GetXaxis().SetTitle(xtitle)
    frame.GetXaxis().SetTitleSize(0.06)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetXaxis().SetTitleOffset(1.0)
    frame.GetXaxis().SetLabelOffset(0.008)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetXaxis().CenterTitle()
    frame.GetYaxis().SetNdivisions(504)
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleOffset(1.0)
    frame.GetYaxis().SetLabelOffset(0.008)
    frame.GetYaxis().SetTitle(ytitle)
    frame.GetYaxis().CenterTitle()

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.1)
    mbc.SetRightMargin(0.1)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.1)
    mbc.SetGrid()

def fit(ecms, patch, path, shape, root):
    try:
        f_data = TFile(path[0], 'READ')
        f_sideband = TFile(path[1], 'READ')
        f_psipp = TFile(path[2], 'READ')
        f_DDPIPI = TFile(path[3], 'READ')
        f_psipp_root = TFile(root[0], 'READ')
        f_DDPIPI_root = TFile(root[1], 'READ')
        t_data = f_data.Get('save')
        t_sideband = f_sideband.Get('save')
        t_psipp = f_psipp.Get('save')
        t_DDPIPI = f_DDPIPI.Get('save')
        t_psipp_root = f_psipp_root.Get('save')
        t_DDPIPI_root = f_DDPIPI_root.Get('save')
        entries_data = t_data.GetEntries()
        entries_sideband = t_sideband.GetEntries()
        entries_psipp = t_psipp.GetEntries()
        entries_DDPIPI = t_DDPIPI.GetEntries()
        entries_psipp_root = t_psipp_root.GetEntries()
        entries_DDPIPI_root = t_DDPIPI_root.GetEntries()
        logging.info('data('+str(ecms)+') entries :'+str(entries_data))
        logging.info('sideband('+str(ecms)+') entries :'+str(entries_sideband))
        logging.info('psipp('+str(ecms)+') entries :'+str(entries_psipp))
        logging.info('DDPIPI('+str(ecms)+') entries :'+str(entries_DDPIPI))
        if ecms > 4290:
            shape_D1_2420 = TFile(shape[0], 'READ')
            f_D1_2420_root = TFile(root[2], 'READ')
            t_D1_2420_root = f_D1_2420_root.Get('save')
            entries_D1_2420_root = t_D1_2420_root.GetEntries()
            f_D1_2420 = TFile(path[4], 'READ')
            t_D1_2420 = f_D1_2420.Get('save')
            entries_D1_2420 = t_D1_2420.GetEntries()
            logging.info('D1(2420)('+str(ecms)+') entries :'+str(entries_D1_2420))
    except:
        logging.error('Files are invalid!')
        sys.exit()
    
    # model for RM(D/Dmiss)
    xmin_rm_D, xmax_rm_D, temp = param_rm_D(ecms)
    xbins_rm_D = int((xmax_rm_D - xmin_rm_D)/0.002)

    rm_D = RooRealVar('rm_D', 'rm_D', xmin_rm_D, xmax_rm_D)
    rm_D.setRange('signal', xmin_rm_D, xmax_rm_D)
    N_D1_2420, N_PSIPP, N_DDPIPI = num_rm_D(ecms)
    if ecms > 4290:
        n2420 = RooRealVar('n2420', 'n2420', 500, 0, N_D1_2420)
    nsideband = RooRealVar('nsideband', 'nsideband', int(entries_sideband/2.))
    npsipp = RooRealVar('npsipp', 'npsipp', 0, N_PSIPP)
    nDDPIPI = RooRealVar('nDDPIPI', 'nDDPIPI', 0, N_DDPIPI)

    h_sideband_rm_D = TH1F('h_sideband_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)
    h_psipp_rm_D = TH1F('h_psipp_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)
    h_DDPIPI_rm_D = TH1F('h_DDPIPI_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)

    cut = ''
    t_sideband.Project('h_sideband_rm_D', 'rm_D', cut)
    t_psipp.Project('h_psipp_rm_D', 'rm_D', cut)
    t_DDPIPI.Project('h_DDPIPI_rm_D', 'rm_D', cut)

    set_data_rm_D = RooDataSet('set_data_rm_D', ' set_data_rm_D', t_data, RooArgSet(rm_D))
    hist_sideband_rm_D = RooDataHist('hist_sideband_rm_D', 'hist_sideband_rm_D', RooArgList(rm_D), h_sideband_rm_D)
    hist_psipp_rm_D = RooDataHist('hist_psipp_rm_D', 'hist_psipp_rm_D', RooArgList(rm_D), h_psipp_rm_D)
    hist_DDPIPI_rm_D = RooDataHist('hist_DDPIPI_rm_D', 'hist_DDPIPI_rm_D', RooArgList(rm_D), h_DDPIPI_rm_D)

    pdf_sideband_rm_D = RooHistPdf('pdf_sideband_rm_D', 'pdf_sideband_rm_D', RooArgSet(rm_D), hist_sideband_rm_D, 0)
    pdf_psipp_rm_D = RooHistPdf('pdf_psipp_rm_D', 'pdf_psipp_rm_D', RooArgSet(rm_D), hist_psipp_rm_D, 2)
    pdf_DDPIPI_rm_D = RooHistPdf('pdf_DDPIPI_rm_D', 'pdf_DDPIPI_rm_D', RooArgSet(rm_D), hist_DDPIPI_rm_D, 2)

    # model for RM(pipi)
    xmin_rm_pipi, xmax_rm_pipi = param_rm_pipi(ecms)
    xbins_rm_pipi = int((xmax_rm_pipi - xmin_rm_pipi)/0.002)

    rm_pipi = RooRealVar('rm_pipi', 'rm_pipi', xmin_rm_pipi, xmax_rm_pipi)
    rm_pipi.setRange('signal', xmin_rm_pipi, xmax_rm_pipi)

    h_sideband_rm_pipi = TH1F('h_sideband_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
    h_psipp_rm_pipi = TH1F('h_psipp_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
    h_DDPIPI_rm_pipi = TH1F('h_DDPIPI_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)

    cut = ''
    t_sideband.Project('h_sideband_rm_pipi', 'rm_pipi', cut)
    t_psipp.Project('h_psipp_rm_pipi', 'rm_pipi', cut)
    t_DDPIPI.Project('h_DDPIPI_rm_pipi', 'rm_pipi', cut)

    set_data_rm_pipi = RooDataSet('set_data_rm_pipi', ' set_data_rm_pipi', t_data, RooArgSet(rm_pipi))
    hist_sideband_rm_pipi = RooDataHist('hist_sideband_rm_pipi', 'hist_sideband_rm_pipi', RooArgList(rm_pipi), h_sideband_rm_pipi)
    hist_psipp_rm_pipi = RooDataHist('hist_psipp_rm_pipi', 'hist_psipp_rm_pipi', RooArgList(rm_pipi), h_psipp_rm_pipi)
    hist_DDPIPI_rm_pipi = RooDataHist('hist_DDPIPI_rm_pipi', 'hist_DDPIPI_rm_pipi', RooArgList(rm_pipi), h_DDPIPI_rm_pipi)

    pdf_psipp_rm_pipi = RooHistPdf('pdf_psipp_rm_pipi', 'pdf_psipp_rm_pipi', RooArgSet(rm_pipi), hist_psipp_rm_pipi, 2)
    pdf_sideband_rm_pipi = RooHistPdf('pdf_sideband_rm_pipi', 'pdf_sideband_rm_pipi', RooArgSet(rm_pipi), hist_sideband_rm_pipi, 0)
    pdf_DDPIPI_rm_pipi = RooHistPdf('pdf_DDPIPI_rm_pipi', 'pdf_DDPIPI_rm_pipi', RooArgSet(rm_pipi), hist_DDPIPI_rm_pipi, 2)
    mean_rm_pipi = RooRealVar('mean_rm_pipi', 'mean_rm_pipi', 0)
    sigma_rm_pipi = RooRealVar('sigma_rm_pipi', 'sigma_rm_pipi', 0.00123, 0., 0.02)
    gauss_rm_pipi = RooGaussian('gaus_rm_pipi', 'guass_rm_pipi', rm_pipi, mean_rm_pipi, sigma_rm_pipi)
    rm_pipi.setBins(xbins_rm_pipi, 'cache')
    covpdf_psipp = RooFFTConvPdf('covpdf_psipp', 'covpdf_psipp', rm_pipi, pdf_psipp_rm_pipi, gauss_rm_pipi)

    # model for RM(D/Dmiss)
    if ecms > 4290:
        pdf_name = 'h_' + str(0) + '_' + str(0)
        h_D1_2420_rm_D = shape_D1_2420.Get(pdf_name)
        pdf_name = 'Covpdf_D1_2420_' + str(ecms) + '_' + str(0) + '_' + str(0)
        hist_D1_2420_rm_D = RooDataHist('h_D1_2420_rm_D', 'h_D1_2420_rm_D', RooArgList(rm_D), h_D1_2420_rm_D)
        pdf_D1_2420_rm_D = RooHistPdf('pdf_D1_2420_rm_D', 'pdf_D1_2420_rm_D', RooArgSet(rm_D), hist_D1_2420_rm_D, 0)
        mean_rm_D = RooRealVar('mean_rm_D', 'mean_rm_D', 0)
        sigma_rm_D = RooRealVar('sigma_rm_D', 'sigma_rm_D', 0.00123, 0., 0.02)
        gauss_rm_D = RooGaussian('gaus_rm_D', 'guass_rm_D', rm_D, mean_rm_D, sigma_rm_D)
        rm_D.setBins(xbins_rm_D, 'cache')
        covpdf_D1_2420 = RooFFTConvPdf(pdf_name, pdf_name, rm_D, pdf_D1_2420_rm_D, gauss_rm_D)
        model_rm_D = RooAddPdf('model_rm_D', 'model_rm_D', RooArgList(covpdf_D1_2420, pdf_sideband_rm_D, pdf_psipp_rm_D, pdf_DDPIPI_rm_D), RooArgList(n2420, nsideband, npsipp, nDDPIPI))
    else:
        model_rm_D = RooAddPdf('model_rm_D', 'model_rm_D', RooArgList(pdf_sideband_rm_D, pdf_psipp_rm_D, pdf_DDPIPI_rm_D), RooArgList(nsideband, npsipp, nDDPIPI))

    # model for RM(pipi)
    if ecms > 4290:
        h_D1_2420_rm_pipi = TH1F('h_D1_2420_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
        cut = ''
        t_D1_2420.Project('h_D1_2420_rm_pipi', 'rm_pipi', cut)
        hist_D1_2420_rm_pipi = RooDataHist('hist_D1_2420_rm_pipi', 'hist_D1_2420_rm_pipi', RooArgList(rm_pipi), h_D1_2420_rm_pipi)
        pdf_D1_2420_rm_pipi = RooHistPdf('pdf_D1_2420_rm_pipi', 'pdf_D1_2420_rm_pipi', RooArgSet(rm_pipi), hist_D1_2420_rm_pipi, 2)
        model_rm_pipi = RooAddPdf('model_rm_pipi', 'model_rm_pipi', RooArgList(pdf_D1_2420_rm_pipi, pdf_sideband_rm_pipi, covpdf_psipp, pdf_DDPIPI_rm_pipi), RooArgList(n2420, nsideband, npsipp, nDDPIPI))
    else:
        model_rm_pipi = RooAddPdf('model_rm_pipi', 'model_rm_pipi', RooArgList(pdf_sideband_rm_pipi, covpdf_psipp, pdf_DDPIPI_rm_pipi), RooArgList(nsideband, npsipp, nDDPIPI))

    # simultaneous fit
    sample = RooCategory('sample', 'sample')
    sample.defineType('rm_D')
    sample.defineType('rm_pipi')
    combData = RooDataSet('combData', 'combined data', RooArgSet(rm_D, rm_pipi), 
        RooFit.Index(sample), RooFit.Import('rm_D', set_data_rm_D), RooFit.Import('rm_pipi', set_data_rm_pipi))
    sim_pdf = RooSimultaneous('sim_pdf', 'simultaneous pdf', sample)
    sim_pdf.addPdf(model_rm_D, 'rm_D')
    sim_pdf.addPdf(model_rm_pipi, 'rm_pipi')
    fit_result = sim_pdf.fitTo(combData)

    # Write necessary info
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    Br = 0.0938
    lum = luminosity(ecms)

    n_D1_2420 = 0.
    eff_D1_2420 = 0.
    ISR_D1_2420 = 1.
    VP_D1_2420 = 1.
    xs_D1_2420 = 0.
    xserr_D1_2420 = 0.
    if ecms > 4290:
        n_D1_2420 = n2420.getVal()
        if ecms == 4420:
            eff_D1_2420 = entries_D1_2420_root/100000.
            if not patch == 'round0':
                f_D1_2420_factor = open('./txts/factor_info_' + str(ecms) + '_D1_2420_' + patch + '.txt', 'r')
                lines_D1_2420 = f_D1_2420_factor.readlines()
                for line_D1_2420 in lines_D1_2420:
                    rs_D1_2420 = line_D1_2420.rstrip('\n')
                    rs_D1_2420 = filter(None, rs_D1_2420.split(" "))
                    ISR_D1_2420 = float(rs_D1_2420[0])
                    VP_D1_2420 = float(rs_D1_2420[1])
        else:
            eff_D1_2420 = entries_D1_2420_root/50000.
        xs_D1_2420 = n_D1_2420/2./2./Br/eff_D1_2420/lum
        xserr_D1_2420 = n2420.getError()/2./2./Br/eff_D1_2420/lum
        if not patch == 'round0':
            f_D1_2420_factor = open('./txts/factor_info_' + str(ecms) + '_D1_2420_' + patch + '.txt', 'r')
            lines_D1_2420 = f_D1_2420_factor.readlines()
            for line_D1_2420 in lines_D1_2420:
                rs_D1_2420 = line_D1_2420.rstrip('\n')
                rs_D1_2420 = filter(None, rs_D1_2420.split(" "))
                ISR_D1_2420 = float(rs_D1_2420[0])
                VP_D1_2420 = float(rs_D1_2420[1])
            xs_D1_2420 = n_D1_2420/2./2./Br/eff_D1_2420/lum/ISR_D1_2420/VP_D1_2420
            xserr_D1_2420 = n2420.getError()/2./2./Br/eff_D1_2420/lum/ISR_D1_2420/VP_D1_2420

    n_psipp = 0.
    eff_psipp = 0.
    ISR_psipp = 1.
    VP_psipp = 1.
    xs_psipp = 0.
    xserr_psipp = 0.
    if ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420:
        eff_psipp = entries_psipp_root/100000.
    else:
        eff_psipp = entries_psipp_root/50000.
    xs_psipp = npsipp.getVal()/2./2./Br/eff_psipp/lum
    xserr_psipp = npsipp.getError()/2./2./Br/eff_psipp/lum
    if not patch == 'round0':
        f_psipp_factor = open('./txts/factor_info_' + str(ecms) + '_psipp_' + patch + '.txt', 'r')
        lines_psipp = f_psipp_factor.readlines()
        for line_psipp in lines_psipp:
            rs_psipp = line_psipp.rstrip('\n')
            rs_psipp = filter(None, rs_psipp.split(" "))
            ISR_psipp = float(rs_psipp[0])
            VP_psipp = float(rs_psipp[1])
        xs_psipp = npsipp.getVal()/2./2./Br/eff_psipp/lum/ISR_psipp/VP_psipp
        xserr_psipp = npsipp.getError()/2./2./Br/eff_psipp/lum/ISR_psipp/VP_psipp

    n_DDPIPI = 0.
    eff_DDPIPI = 0.
    ISR_DDPIPI = 1.
    VP_DDPIPI = 1.
    xs_DDPIPI = 0.
    xserr_DDPIPI = 0.
    if ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420:
        eff_DDPIPI = entries_DDPIPI_root/100000.
    else:
        eff_DDPIPI = entries_DDPIPI_root/50000.
    xs_DDPIPI = nDDPIPI.getVal()/2./2./Br/eff_DDPIPI/lum
    xserr_DDPIPI = nDDPIPI.getError()/2./2./Br/eff_DDPIPI/lum
    if not patch == 'round0':
        f_DDPIPI_factor = open('./txts/factor_info_' + str(ecms) + '_DDPIPI_' + patch + '.txt', 'r')
        lines_DDPIPI = f_DDPIPI_factor.readlines()
        for line_DDPIPI in lines_DDPIPI:
            rs_DDPIPI = line_DDPIPI.rstrip('\n')
            rs_DDPIPI = filter(None, rs_DDPIPI.split(" "))
            ISR_DDPIPI = float(rs_DDPIPI[0])
            VP_DDPIPI = float(rs_DDPIPI[1])
        xs_DDPIPI = nDDPIPI.getVal()/2./2./Br/eff_DDPIPI/lum/ISR_DDPIPI/VP_DDPIPI
        xserr_DDPIPI = nDDPIPI.getError()/2./2./Br/eff_DDPIPI/lum/ISR_DDPIPI/VP_DDPIPI

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_out = './txts/fit_rm_D_' + str(ecms) + '_' + patch + '.txt'
    f_out = open(path_out, 'w')
    line = '@' + str(ecms) + 'MeV\n' 
    if ecms > 4290:
        line += str(int(n_D1_2420)) + ' $\pm$ '+ str(int(n2420.getError()))  + '\n' 
    else:
        line += str(0) + ' $\pm$ ' + str(0) + '\n'
    line += str(int(npsipp.getVal())) + ' $\pm$ ' + str(int(npsipp.getError())) + '\n' 
    line += str(int(nDDPIPI.getVal())) + ' $\pm$ ' + str(int(nDDPIPI.getError())) + '\n'
    line += str(round(eff_D1_2420*100, 2)) + '\%\n' 
    line += str(round(eff_psipp*100, 2)) + '\%\n' 
    line += str(round(eff_DDPIPI*100, 2)) + '\%\n' 
    line += str(round(ISR_D1_2420, 2)) + '\n' 
    line += str(round(ISR_psipp, 2)) + '\n' 
    line += str(round(ISR_DDPIPI, 2)) + '\n' 
    line += str(round(VP_psipp, 2)) + '\n'
    line += str(Br*100) + '\%\n' 
    line += str(lum) + '\n' 
    line += str(round(xs_D1_2420, 2)) + ' $\pm$ ' + str(round(xserr_D1_2420, 2)) + '\n' 
    line += str(round(xs_psipp, 2)) + ' $\pm$ ' + str(round(xserr_psipp, 2)) + '\n' 
    line += str(round(xs_DDPIPI, 2)) + ' $\pm$ ' + str(round(xserr_DDPIPI, 2)) + '\n'
    line += str(round(xs_D1_2420 + xs_psipp + xs_DDPIPI, 2)) + ' $\pm$ ' + str(round((xserr_D1_2420**2 + xserr_psipp**2 + xserr_DDPIPI**2)**0.5, 2)) + '\n'
    f_out.write(line)
    f_out.close()

    path_out_read = './txts/fit_rm_D_' + str(ecms) + '_read_' + patch + '.txt'
    f_out_read = open(path_out_read, 'w')
    xs_tot = xs_D1_2420 + xs_psipp + xs_DDPIPI
    line_read = str(ecms) + ' ' 
    line_read += str(round(xs_D1_2420/xs_tot, 2)) + ' ' 
    line_read += str(round(xs_psipp/xs_tot, 2)) + ' ' 
    line_read += str(round(xs_DDPIPI/xs_tot, 2)) + ' ' 
    line_read += str(round(eff_D1_2420, 2)) + ' ' 
    line_read += str(round(eff_psipp, 2)) + ' ' 
    line_read += str(round(eff_DDPIPI, 2)) + ' '
    line_read += str(round(ISR_D1_2420, 2)) + ' ' 
    line_read += str(round(ISR_psipp, 2)) + ' ' 
    line_read += str(round(ISR_DDPIPI, 2)) + ' ' 
    line_read += str(round(VP_DDPIPI, 2)) + ' ' 
    line_read += str(lum) + ' ' 
    line_read += str(Br) + ' ' 
    line_read += str(round(xs_D1_2420, 2)) + ' ' 
    line_read += str(round(xs_psipp, 2)) + ' ' 
    line_read += str(round(xs_DDPIPI, 2)) + ' ' 
    line_read += str(round(xserr_D1_2420, 2)) + ' ' 
    line_read += str(round(xserr_psipp, 2)) + ' ' 
    line_read += str(round(xserr_DDPIPI, 2)) + ' ' 
    line_read += '\n'
    f_out_read.write(line_read)
    f_out_read.close()

    # Draw fitting results
    c = TCanvas('c', 'c', 1200, 600)
    set_canvas_style(c)
    c.Divide(2, 1)

    c.cd(1)
    frame_rm_D = rm_D.frame(RooFit.Bins(xbins_rm_D), RooFit.Title('rm_D'))
    xtitle_rm_D = 'RM(D^{+}) and RM(D^{-}_{miss})(GeV)'
    content_rm_D = (xmax_rm_D - xmin_rm_D)/xbins_rm_D * 1000
    ytitle_rm_D = 'Events/%.1f MeV'%content_rm_D 
    set_frame_style(frame_rm_D, xtitle_rm_D, ytitle_rm_D)
    combData.plotOn(frame_rm_D, RooFit.Cut('sample==sample::rm_D'))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components('pdf_sideband_rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if ecms > 4290:
        sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components(pdf_name), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components('pdf_psipp_rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components('pdf_DDPIPI_rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kYellow), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))

    name = []
    name.append('Data')
    name.append('Total Fit')
    name.append('Backgrounds')
    if ecms > 4290:
        name.append('D_{1}(2420)^{+}D^{-}')
    name.append('#psi(3770)#pi^{+}#pi^{-}')
    name.append('D^{+}D^{-}#pi^{+}#pi^{-}')

    lg_rm_D = TLegend(.2, .6, .4, .85)
    for m in xrange(len(name)):
        objName = frame_rm_D.nameOf(m)
        obj = frame_rm_D.findObject(objName)
        if objName == 'model_rm_D_Norm[rm_D]_Comp[pdf_sideband_rm_D]':
            lg_rm_D.AddEntry(obj, name[m], 'F')
        else:
            lg_rm_D.AddEntry(obj, name[m], 'PL')
        lg_rm_D.SetTextFont(42)
        lg_rm_D.SetTextSize(0.03)
    lg_rm_D.SetBorderSize(1)
    lg_rm_D.SetLineColor(0)
    lg_rm_D.SetFillColor(0)
    lg_rm_D.SetHeader(str(ecms) + ' MeV')
    frame_rm_D.Draw()
    lg_rm_D.Draw()

    c.cd(2)
    frame_rm_pipi = rm_pipi.frame(RooFit.Bins(xbins_rm_pipi), RooFit.Title('rm_pipi'))
    xtitle_rm_pipi = 'RM(#pi_{0}^{+}#pi_{0}^{-})(GeV)'
    content_rm_pipi = (xmax_rm_pipi - xmin_rm_pipi)/xbins_rm_pipi * 1000
    ytitle_rm_pipi = 'Events/%.1f MeV'%content_rm_pipi 
    set_frame_style(frame_rm_pipi, xtitle_rm_pipi, ytitle_rm_pipi)
    combData.plotOn(frame_rm_pipi, RooFit.Cut('sample==sample::rm_pipi'))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('pdf_sideband_rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if ecms > 4290:
        sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('pdf_D1_2420_rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('covpdf_psipp'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('pdf_DDPIPI_rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kYellow), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))

    name = []
    name.append('Data')
    name.append('Total Fit')
    name.append('Backgrounds')
    if ecms > 4290:
        name.append('D_{1}(2420)^{+}D^{-}')
    name.append('#psi(3770)#pi^{+}#pi^{-}')
    name.append('D^{+}D^{-}#pi^{+}#pi^{-}')

    lg_rm_pipi = TLegend(.65, .6, .85, .85)
    for m in xrange(len(name)):
        objName = frame_rm_pipi.nameOf(m)
        obj = frame_rm_pipi.findObject(objName)
        if objName == 'model_rm_pipi_Norm[rm_pipi]_Comp[pdf_sideband_rm_pipi]':
            lg_rm_pipi.AddEntry(obj, name[m], 'F')
        else:
            lg_rm_pipi.AddEntry(obj, name[m], 'PL')
        lg_rm_pipi.SetTextFont(42)
        lg_rm_pipi.SetTextSize(0.03)
    lg_rm_pipi.SetBorderSize(1)
    lg_rm_pipi.SetLineColor(0)
    lg_rm_pipi.SetFillColor(0)
    lg_rm_pipi.SetHeader(str(ecms) + ' MeV')
    frame_rm_pipi.Draw()
    lg_rm_pipi.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    canvas_name = './figs/simul_fit_' + str(ecms) + '.pdf'
    c.SaveAs(canvas_name)

    # raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    patch = args[1]

    path = []
    shape = []
    root = []
    if ecms > 4290:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_sideband_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_fit.root')
        shape.append('/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/SHAPE_D1_2420_'+str(ecms)+'.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_after.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_after.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_after.root')
        if ecms > 4600 and not ecms == 4660:
            root = []
            path[2] = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_fit.root'
            path[3] = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/sigMC_D_D_PI_PI_4600_fit.root'
            path[4] = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_fit.root'
            shape[0] = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/SHAPE_D1_2420_4600.root'
            root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_after.root')
            root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/sigMC_D_D_PI_PI_4600_after.root')
            root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_after.root')
        if ecms == 4660:
            root = []
            path[2] = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_fit.root'
            path[3] = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/sigMC_D_D_PI_PI_4600_fit.root'
            path[4] = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_fit.root'
            shape[0] = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/SHAPE_D1_2420_4600.root'
            root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_after.root')
            root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/sigMC_D_D_PI_PI_4600_after.root')
            root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_after.root')
        fit(ecms, patch, path, shape, root)

    if ecms <= 4290:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_sideband_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_fit.root')
        shape.append('')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_after.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_after.root')
        fit(ecms, patch, path, shape, root)

if __name__ == '__main__':
    main()
