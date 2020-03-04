#!/usr/bin/env python
"""
Fit of recoiling mass of D and Dmiss
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

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)
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
        if ecms >= 4290:
            f_D1_2420 = TFile(shape[0], 'READ')
            f_D1_2420_root = TFile(root[2], 'READ')
            t_D1_2420_root = f_D1_2420_root.Get('save')
            entries_D1_2420_root = t_D1_2420_root.GetEntries()
    except:
        logging.error('Files are invalid!')
        sys.exit()

    xmin, xmax, temp = param_rm_D(ecms)
    xbins = int((xmax - xmin)/0.002)

    rm_D = RooRealVar('rm_D', 'rm_D', xmin, xmax)
    N_D1_2420, N_PSIPP, N_DDPIPI = num_rm_D(ecms)
    if ecms >= 4290:
        n2420 = RooRealVar('n2420', 'n2420', 500, 0, N_D1_2420)
    nsideband = RooRealVar('nsideband', 'nsideband', int(entries_sideband/2.))
    npsipp = RooRealVar('npsipp', 'npsipp', 0, N_PSIPP)
    nDDPIPI = RooRealVar('nDDPIPI', 'nDDPIPI', 0, N_DDPIPI)

    h_sideband = TH1F('h_sideband', '', xbins, xmin, xmax)
    h_psipp = TH1F('h_psipp', '', xbins, xmin, xmax)
    h_DDPIPI = TH1F('h_DDPIPI', '', xbins, xmin, xmax)

    cut = ''
    t_sideband.Project('h_sideband', 'rm_D', cut)
    t_psipp.Project('h_psipp', 'rm_D', cut)
    t_DDPIPI.Project('h_DDPIPI', 'rm_D', cut)

    set_data = RooDataSet('set_data', ' set_data', t_data, RooArgSet(rm_D))
    hist_sideband = RooDataHist('hist_sideband', 'hist_sideband', RooArgList(rm_D), h_sideband)
    hist_psipp = RooDataHist('hist_psipp', 'hist_psipp', RooArgList(rm_D), h_psipp)
    hist_DDPIPI = RooDataHist('hist_DDPIPI', 'hist_DDPIPI', RooArgList(rm_D), h_DDPIPI)

    pdf_sideband = RooHistPdf('pdf_sideband', 'pdf_sideband', RooArgSet(rm_D), hist_sideband, 0)
    pdf_psipp = RooHistPdf('pdf_psipp', 'pdf_psipp', RooArgSet(rm_D), hist_psipp, 2)
    pdf_DDPIPI = RooHistPdf('pdf_DDPIPI', 'pdf_DDPIPI', RooArgSet(rm_D), hist_DDPIPI, 2)

    canvas_name = './figs/canvas_rm_D_' + str(0) + '_' +str(0) + '_' + str(ecms) + '.pdf'
    if ecms >= 4290:
        pdf_name = 'h_' + str(0) + '_' + str(0)
        h_D1_2420 = f_D1_2420.Get(pdf_name)
        pdf_name = 'Covpdf_D1_2420_' + str(ecms) + '_' + str(0) + '_' + str(0)
        hist_D1_2420 = RooDataHist('h_D1_2420', 'h_D1_2420', RooArgList(rm_D), h_D1_2420)
        pdf_D1_2420 = RooHistPdf('pdf_D1_2420', 'pdf_D1_2420', RooArgSet(rm_D), hist_D1_2420, 0)
        mean = RooRealVar('mean', 'mean', 0)
        sigma = RooRealVar('sigma', 'sigma', 0.00123, 0., 0.02)
        gauss = RooGaussian('gauss', 'guass', rm_D, mean, sigma)
        rm_D.setBins(xbins, 'cache')
        covpdf_D1_2420 = RooFFTConvPdf(pdf_name, pdf_name, rm_D, pdf_D1_2420, gauss)
        model = RooAddPdf('model', 'model', RooArgList(covpdf_D1_2420, pdf_sideband, pdf_psipp, pdf_DDPIPI), RooArgList(n2420, nsideband, npsipp, nDDPIPI))
    else:
        model = RooAddPdf('model', 'model', RooArgList(pdf_sideband, pdf_psipp, pdf_DDPIPI), RooArgList(nsideband, npsipp, nDDPIPI))
    model.fitTo(set_data)

    Br = 0.0938
    lum = luminosity(ecms)

    n_D1_2420 = 0.
    eff_D1_2420 = 0.
    ISR_D1_2420 = 1.
    VP_D1_2420 = 1.
    xs_D1_2420 = 0.
    xserr_D1_2420 = 0.
    if ecms >= 4290:
        n_D1_2420 = n2420.getVal()
        if ecms == 4420:
            eff_D1_2420 = entries_D1_2420_root/100000.
            if not patch == 'round0':
                f_D1_2420_factor = open('../../python/txts/factor_info_' + str(ecms) + '_D1_2420_' + patch + '.txt', 'r')
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
            f_D1_2420_factor = open('../../python/txts/factor_info_' + str(ecms) + '_D1_2420_' + patch + '.txt', 'r')
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
        f_psipp_factor = open('../../python/txts/factor_info_' + str(ecms) + '_psipp_' + patch + '.txt', 'r')
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
        f_DDPIPI_factor = open('../../python/txts/factor_info_' + str(ecms) + '_DDPIPI_' + patch + '.txt', 'r')
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
    line = '& @' + str(ecms) + 'MeV&\n' 
    if ecms >= 4290:
        line += str(int(n_D1_2420)) + ' \pm '+ str(int(n2420.getError()))  + '&\n' 
    else:
        line += str(0) + ' \pm ' + str(0) + '\&\n'
    line += str(int(npsipp.getVal())) + ' \pm ' + str(int(npsipp.getError())) + '&\n' 
    line += str(int(nDDPIPI.getVal())) + ' \pm ' + str(int(nDDPIPI.getError())) + '\&\n'
    line += str(round(eff_D1_2420*100, 2)) + '\%&\n' 
    line += str(round(eff_psipp*100, 2)) + '\%&\n' 
    line += str(round(eff_DDPIPI*100, 2)) + '\%&\n' 
    line += str(round(VP_psipp, 2)) + '\n'
    line += str(lum) + '&\n' 
    line += str(Br*100) + '\%&\n' 
    line += str(round(xs_D1_2420, 2)) + ' \pm ' + str(round(xserr_D1_2420, 2)) + '&\n' 
    line += str(round(xs_psipp, 2)) + ' \pm ' + str(round(xserr_psipp, 2)) + '&\n' 
    line += str(round(xs_DDPIPI, 2)) + '\pm ' + str(round(xserr_DDPIPI, 2)) + '&\n'
    line += str(round(xs_D1_2420 + xs_psipp + xs_DDPIPI, 2)) + '\pm ' + str(round((xserr_D1_2420**2 + xserr_psipp**2 + xserr_DDPIPI**2)**0.5, 2)) + '&\n'
    f_out.write(line)
    f_out.close()

    path_out_read = './txts/fit_rm_D_' + str(ecms) + '_read_' + patch + '.txt'
    f_out_read = open(path_out_read, 'w')
    N_tot = n_D1_2420 + npsipp.getVal() + nDDPIPI.getVal()
    line_read = str(ecms) + ' ' 
    line_read += str(round(n_D1_2420/N_tot, 2)) + ' ' 
    line_read += str(round(npsipp.getVal()/N_tot, 2)) + ' ' 
    line_read += str(round(nDDPIPI.getVal()/N_tot, 2)) + ' ' 
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

    c = TCanvas('c', 'c', 800, 600)
    set_canvas_style(c)
    c.cd()

    xframe = rm_D.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
    xtitle = 'RM(D^{+}) and RM(D^{-}_{miss})(GeV)'
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    set_xframe_style(xframe, xtitle, ytitle)
    set_data.plotOn(xframe, RooFit.MarkerSize(1), RooFit.LineWidth(1))
    model.plotOn(xframe, RooFit.Components('pdf_sideband'), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    if ecms >= 4290:
        covpdf_name = 'Covpdf_D1_2420_' + str(ecms) + '_' + str(0) + '_' + str(0)
        model.plotOn(xframe, RooFit.Components(covpdf_name), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    model.plotOn(xframe, RooFit.Components('pdf_psipp'), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    model.plotOn(xframe, RooFit.Components('pdf_DDPIPI'), RooFit.LineColor(kBlack), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
    model.plotOn(xframe, RooFit.LineColor(kBlack), RooFit.LineWidth(3))

    name = []
    name.append('Data')
    name.append('Backgrounds')
    if ecms >= 4290:
        name.append('D_{1}(2420)^{+}D^{-}')
    name.append('#psi(3770)#pi^{+}#pi^{-}')
    name.append('D^{+}D^{-}#pi^{+}#pi^{-}')

    lg = TLegend(.2, .6, .4, .85)
    for m in xrange(len(name)):
        objName = xframe.nameOf(m)
        obj = xframe.findObject(objName)
        if m != 1:
            lg.AddEntry(obj, name[m], 'PL')
        if m == 1:
            lg.AddEntry(obj, name[m], 'F')
        lg.SetTextFont(42)
        lg.SetTextSize(0.03)
    lg.SetBorderSize(1)
    lg.SetLineColor(0)
    lg.SetFillColor(0)
    xframe.Draw()
    lg.Draw()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    c.SaveAs(canvas_name)

    raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    patch = args[1]

    path = []
    shape = []
    root = []
    if ecms >= 4290:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/sys_err/window/data_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/sys_err/window/data_'+str(ecms)+'_sideband_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sys_err/window/sigMC_psipp_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sys_err/window/sigMC_D_D_PI_PI_'+str(ecms)+'_fit.root')
        shape.append('/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/window/shape_D1_2420_'+str(ecms)+'.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sys_err/window/sigMC_psipp_'+str(ecms)+'_after.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sys_err/window/sigMC_D_D_PI_PI_'+str(ecms)+'_after.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/'+str(ecms)+'/sys_err/window/sigMC_D1_2420_'+str(ecms)+'_after.root')
        fit(ecms, patch, path, shape, root)

    if ecms < 4290:
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/sys_err/window/data_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/sys_err/window/data_'+str(ecms)+'_sideband_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sys_err/window/sigMC_psipp_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sys_err/window/sigMC_D_D_PI_PI_'+str(ecms)+'_fit.root')
        shape.append('')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sys_err/window/sigMC_psipp_'+str(ecms)+'_after.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sys_err/window/sigMC_D_D_PI_PI_'+str(ecms)+'_after.root')
        fit(ecms, patch, path, shape, root)

if __name__ == '__main__':
    main()
