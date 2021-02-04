#!/usr/bin/env python
"""
IO check of recoiling mass of D fitting
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-08-30 Sun 17:07]"

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
    IO.py

SYNOPSIS
    ./IO.py [ecms] [method]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    August 2020
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

def fit(ecms, method, path):
    try:
        f_D1_2420 = TFile(path[0], 'READ')
        t_D1_2420 = f_D1_2420.Get('save')
        entries_D1_2420 = t_D1_2420.GetEntries()
        logging.info('D1(2420)('+str(ecms)+') entries :'+str(entries_D1_2420))
    except:
        logging.error('Files are invalid!')
        sys.exit()
    
    N_D1_2420, temp, temp = num_rm_D(ecms)
    n2420 = RooRealVar('n2420', 'n2420', 500, 0, N_D1_2420)

    # model for RM(D)
    xmin_rm_D, xmax_rm_D, temp = param_rm_D(ecms)
    xbins_rm_D = int((xmax_rm_D - xmin_rm_D)/0.005)
    rm_D = RooRealVar('rm_D', 'rm_D', xmin_rm_D, xmax_rm_D)
    rm_D.setRange('signal', xmin_rm_D, xmax_rm_D)
    set_MC_rm_D = RooDataSet('set_MC_rm_D', ' set_MC_rm_D', t_D1_2420, RooArgSet(rm_D))
    h_D1_2420_rm_D = TH1F('h_D1_2420_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)
    cut = ''
    t_D1_2420.Project('h_D1_2420_rm_D', 'rm_D', cut)
    hist_D1_2420_rm_D = RooDataHist('hist_D1_2420_rm_D', 'hist_D1_2420_rm_D', RooArgList(rm_D), h_D1_2420_rm_D)
    pdf_D1_2420_rm_D = RooHistPdf('pdf_D1_2420_rm_D', 'pdf_D1_2420_rm_D', RooArgSet(rm_D), hist_D1_2420_rm_D, 2)

    # model for RM(Dmiss)
    xmin_rm_Dmiss, xmax_rm_Dmiss, temp = param_rm_D(ecms)
    xbins_rm_Dmiss = int((xmax_rm_Dmiss - xmin_rm_Dmiss)/0.005)
    rm_Dmiss = RooRealVar('rm_Dmiss', 'rm_Dmiss', xmin_rm_Dmiss, xmax_rm_Dmiss)
    rm_Dmiss.setRange('signal', xmin_rm_Dmiss, xmax_rm_Dmiss)
    set_MC_rm_Dmiss = RooDataSet('set_MC_rm_Dmiss', ' set_MC_rm_Dmiss', t_D1_2420, RooArgSet(rm_Dmiss))
    h_D1_2420_rm_Dmiss = TH1F('h_D1_2420_rm_Dmiss', '', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
    cut = ''
    t_D1_2420.Project('h_D1_2420_rm_Dmiss', 'rm_Dmiss', cut)
    hist_D1_2420_rm_Dmiss = RooDataHist('hist_D1_2420_rm_Dmiss', 'hist_D1_2420_rm_Dmiss', RooArgList(rm_Dmiss), h_D1_2420_rm_Dmiss)
    pdf_D1_2420_rm_Dmiss = RooHistPdf('pdf_D1_2420_rm_Dmiss', 'pdf_D1_2420_rm_Dmiss', RooArgSet(rm_Dmiss), hist_D1_2420_rm_Dmiss, 2)

    # model for RM(pipi)
    xmin_rm_pipi, xmax_rm_pipi = param_rm_pipi(ecms)
    xbins_rm_pipi = int((xmax_rm_pipi - xmin_rm_pipi)/0.005)
    rm_pipi = RooRealVar('rm_pipi', 'rm_pipi', xmin_rm_pipi, xmax_rm_pipi)
    rm_pipi.setRange('signal', xmin_rm_pipi, xmax_rm_pipi)
    set_MC_rm_pipi = RooDataSet('set_MC_rm_pipi', ' set_MC_rm_pipi', t_D1_2420, RooArgSet(rm_pipi))
    h_D1_2420_rm_pipi = TH1F('h_D1_2420_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
    cut = ''
    t_D1_2420.Project('h_D1_2420_rm_pipi', 'rm_pipi', cut)
    hist_D1_2420_rm_pipi = RooDataHist('hist_D1_2420_rm_pipi', 'hist_D1_2420_rm_pipi', RooArgList(rm_pipi), h_D1_2420_rm_pipi)
    pdf_D1_2420_rm_pipi = RooHistPdf('pdf_D1_2420_rm_pipi', 'pdf_D1_2420_rm_pipi', RooArgSet(rm_pipi), hist_D1_2420_rm_pipi, 2)

    # model for RM(D)
    rm_D.setBins(xbins_rm_D, 'cache')
    model_rm_D = RooAddPdf('model_rm_D', 'model_rm_D', RooArgList(pdf_D1_2420_rm_D), RooArgList(n2420))

    # model for RM(Dmiss)
    rm_Dmiss.setBins(xbins_rm_Dmiss, 'cache')
    model_rm_Dmiss = RooAddPdf('model_rm_Dmiss', 'model_rm_Dmiss', RooArgList(pdf_D1_2420_rm_Dmiss), RooArgList(n2420))

    # model for RM(pipi)
    model_rm_pipi = RooAddPdf('model_rm_pipi', 'model_rm_pipi', RooArgList(pdf_D1_2420_rm_pipi), RooArgList(n2420))

    # separate fit
    if method == 'separate':
        # Write necessary info
        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')
        path_out = './txts/IO_num_' + str(ecms) + '_' + method  + '.txt'
        f_out = open(path_out, 'w')

        # Draw fitting results
        c = TCanvas('c', 'c', 1700, 600)
        set_canvas_style(c)
        c.Divide(3, 1)

        c.cd(1)
        # rm_D
        model_rm_D.fitTo(set_MC_rm_D)
        frame_rm_D = rm_D.frame(RooFit.Bins(xbins_rm_D), RooFit.Range(xmin_rm_D, xmax_rm_D))
        xtitle = 'RM(D^{+})(GeV)'
        content = int((xmax_rm_D - xmin_rm_D)/xbins_rm_D * 1000)
        ytitle = 'Events/%.1f MeV'%content
        set_frame_style(frame_rm_D, xtitle, ytitle)
        set_MC_rm_D.plotOn(frame_rm_D, RooFit.MarkerSize(1), RooFit.LineWidth(1))
        model_rm_D.plotOn(frame_rm_D, RooFit.Components('pdf_D1_2420_rm_D'), RooFit.LineColor(kBlack), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
        model_rm_D.plotOn(frame_rm_D, RooFit.LineColor(kBlack), RooFit.LineWidth(3))
        set_MC_rm_D.plotOn(frame_rm_D, RooFit.MarkerSize(1), RooFit.LineWidth(1))

        name = []
        name.append('Toy MC')
        name.append('Total Fit')
        name.append('D_{1}(2420)^{+}D^{-}')

        lg_rm_D = TLegend(.15, .65, .35, .95)
        for m in xrange(len(name)):
            objName = frame_rm_D.nameOf(m)
            obj = frame_rm_D.findObject(objName)
            lg_rm_D.AddEntry(obj, name[m], 'PL')
            lg_rm_D.SetTextFont(42)
            lg_rm_D.SetTextSize(0.06)
        lg_rm_D.SetBorderSize(1)
        lg_rm_D.SetLineColor(0)
        lg_rm_D.SetFillColor(0)
        lg_rm_D.SetHeader(str(ecms) + ' MeV')
        frame_rm_D.Draw()
        lg_rm_D.Draw()

        line = str(n2420.getVal()) + ' ' + str(n2420.getError()) + '\n' 
        f_out.write(line)

        c.cd(2)
        # rm_Dmiss
        model_rm_Dmiss.fitTo(set_MC_rm_Dmiss)
        frame_rm_Dmiss = rm_Dmiss.frame(RooFit.Bins(xbins_rm_Dmiss), RooFit.Range(xmin_rm_Dmiss, xmax_rm_Dmiss))
        xtitle = 'RM(D_{miss}^{-})(GeV)'
        content = int((xmax_rm_Dmiss - xmin_rm_Dmiss)/xbins_rm_Dmiss * 1000)
        ytitle = 'Events/%.1f MeV'%content
        set_frame_style(frame_rm_Dmiss, xtitle, ytitle)
        set_MC_rm_Dmiss.plotOn(frame_rm_Dmiss, RooFit.MarkerSize(1), RooFit.LineWidth(1))
        model_rm_Dmiss.plotOn(frame_rm_Dmiss, RooFit.Components('pdf_D1_2420_rm_Dmiss'), RooFit.LineColor(kBlack), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
        model_rm_Dmiss.plotOn(frame_rm_Dmiss, RooFit.LineColor(kBlack), RooFit.LineWidth(3))
        set_MC_rm_Dmiss.plotOn(frame_rm_Dmiss, RooFit.MarkerSize(1), RooFit.LineWidth(1))

        name = []
        name.append('Toy MC')
        name.append('Total Fit')
        name.append('D_{1}(2420)^{+}D^{-}')

        lg_rm_Dmiss = TLegend(.15, .65, .35, .95)
        for m in xrange(len(name)):
            objName = frame_rm_Dmiss.nameOf(m)
            obj = frame_rm_Dmiss.findObject(objName)
            lg_rm_Dmiss.AddEntry(obj, name[m], 'PL')
            lg_rm_Dmiss.SetTextFont(42)
            lg_rm_Dmiss.SetTextSize(0.06)
        lg_rm_Dmiss.SetBorderSize(1)
        lg_rm_Dmiss.SetLineColor(0)
        lg_rm_Dmiss.SetFillColor(0)
        lg_rm_Dmiss.SetHeader(str(ecms) + ' MeV')
        frame_rm_Dmiss.Draw()
        lg_rm_Dmiss.Draw()

        line = str(n2420.getVal()) + ' ' + str(n2420.getError()) + '\n' 
        f_out.write(line)

        c.cd(3)
        # rm_pipi
        model_rm_pipi.fitTo(set_MC_rm_pipi)
        frame_rm_pipi = rm_pipi.frame(RooFit.Bins(xbins_rm_pipi), RooFit.Range(xmin_rm_pipi, xmax_rm_pipi))
        xtitle = 'RM(#pi_{0}^{+}#pi_{0}^{-})(GeV)'
        content = int((xmax_rm_pipi - xmin_rm_pipi)/xbins_rm_pipi * 1000)
        ytitle = 'Events/%.1f MeV'%content
        set_frame_style(frame_rm_pipi, xtitle, ytitle)
        set_MC_rm_pipi.plotOn(frame_rm_pipi, RooFit.MarkerSize(1), RooFit.LineWidth(1))
        model_rm_pipi.plotOn(frame_rm_pipi, RooFit.Components('pdf_D1_2420_rm_pipi'), RooFit.LineColor(kBlack), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
        model_rm_pipi.plotOn(frame_rm_pipi, RooFit.LineColor(kBlack), RooFit.LineWidth(3))
        set_MC_rm_pipi.plotOn(frame_rm_pipi, RooFit.MarkerSize(1), RooFit.LineWidth(1))

        name = []
        name.append('Toy MC')
        name.append('Total Fit')
        name.append('D_{1}(2420)^{+}D^{-}')

        lg_rm_pipi = TLegend(.6, .6, .8, .85)
        for m in xrange(len(name)):
            objName = frame_rm_pipi.nameOf(m)
            obj = frame_rm_pipi.findObject(objName)
            lg_rm_pipi.AddEntry(obj, name[m], 'PL')
            lg_rm_pipi.SetTextFont(42)
            lg_rm_pipi.SetTextSize(0.06)
        lg_rm_pipi.SetBorderSize(1)
        lg_rm_pipi.SetLineColor(0)
        lg_rm_pipi.SetFillColor(0)
        lg_rm_pipi.SetHeader(str(ecms) + ' MeV')
        frame_rm_pipi.Draw()
        lg_rm_pipi.Draw()

        line = str(n2420.getVal()) + ' ' + str(n2420.getError()) + '\n' 
        f_out.write(line)
        f_out.close()

    if method == 'simul':
        # simultaneous fit
        sample = RooCategory('sample', 'sample')
        sample.defineType('rm_D')
        sample.defineType('rm_Dmiss')
        sample.defineType('rm_pipi')
        combData = RooDataSet('combData', 'combined data', RooArgSet(rm_D, rm_Dmiss, rm_pipi), 
            RooFit.Index(sample), RooFit.Import('rm_D', set_MC_rm_D), RooFit.Import('rm_Dmiss', set_MC_rm_Dmiss), RooFit.Import('rm_pipi', set_MC_rm_pipi))
        sim_pdf = RooSimultaneous('sim_pdf', 'simultaneous pdf', sample)
        sim_pdf.addPdf(model_rm_D, 'rm_D')
        sim_pdf.addPdf(model_rm_Dmiss, 'rm_Dmiss')
        sim_pdf.addPdf(model_rm_pipi, 'rm_pipi')
        fit_result = sim_pdf.fitTo(combData)

        # Draw fitting results
        c = TCanvas('c', 'c', 1700, 600)
        set_canvas_style(c)
        c.Divide(3, 1)

        c.cd(1)
        frame_rm_D = rm_D.frame(RooFit.Bins(xbins_rm_D), RooFit.Title('rm_D'))
        xtitle_rm_D = 'RM(D^{+}) (GeV)'
        content_rm_D = int((xmax_rm_D - xmin_rm_D)/xbins_rm_D * 1000)
        ytitle_rm_D = 'Entries/%.1f MeV'%content_rm_D 
        set_frame_style(frame_rm_D, xtitle_rm_D, ytitle_rm_D)
        combData.plotOn(frame_rm_D, RooFit.Cut('sample==sample::rm_D'))
        sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3))
        sim_pdf.plotOn(frame_rm_D, RooFit.Slice(sample, 'rm_D'), RooFit.Components('pdf_D1_2420_rm_D'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
        combData.plotOn(frame_rm_D, RooFit.Cut('sample==sample::rm_D'))

        name = []
        name.append('Toy MC')
        name.append('Total Fit')
        name.append('D_{1}(2420)^{+}D^{-}')

        lg_rm_D = TLegend(.15, .65, .35, .95)
        for m in xrange(len(name)):
            objName = frame_rm_D.nameOf(m)
            obj = frame_rm_D.findObject(objName)
            lg_rm_D.AddEntry(obj, name[m], 'PL')
            lg_rm_D.SetTextFont(42)
            lg_rm_D.SetTextSize(0.06)
        lg_rm_D.SetBorderSize(1)
        lg_rm_D.SetLineColor(0)
        lg_rm_D.SetFillColor(0)
        lg_rm_D.SetHeader(str(ecms) + ' MeV')
        frame_rm_D.Draw()
        lg_rm_D.Draw()

        c.cd(2)
        frame_rm_Dmiss = rm_Dmiss.frame(RooFit.Bins(xbins_rm_Dmiss), RooFit.Title('rm_Dmiss'))
        xtitle_rm_Dmiss = 'RM(D^{-}_{miss}) (GeV)'
        content_rm_Dmiss = int((xmax_rm_Dmiss - xmin_rm_Dmiss)/xbins_rm_Dmiss * 1000)
        ytitle_rm_Dmiss = 'Entries/%.1f MeV'%content_rm_Dmiss 
        set_frame_style(frame_rm_Dmiss, xtitle_rm_Dmiss, ytitle_rm_Dmiss)
        combData.plotOn(frame_rm_Dmiss, RooFit.Cut('sample==sample::rm_Dmiss'))
        sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(sample, 'rm_Dmiss'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3))
        sim_pdf.plotOn(frame_rm_Dmiss, RooFit.Slice(sample, 'rm_Dmiss'), RooFit.Components('pdf_D1_2420_rm_Dmiss'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
        combData.plotOn(frame_rm_Dmiss, RooFit.Cut('sample==sample::rm_Dmiss'))

        name = []
        name.append('Data')
        name.append('Total Fit')
        name.append('D_{1}(2420)^{+}D^{-}')

        lg_rm_Dmiss = TLegend(.15, .65, .35, .95)
        for m in xrange(len(name)):
            objName = frame_rm_Dmiss.nameOf(m)
            obj = frame_rm_Dmiss.findObject(objName)
            lg_rm_Dmiss.AddEntry(obj, name[m], 'PL')
            lg_rm_Dmiss.SetTextFont(42)
            lg_rm_Dmiss.SetTextSize(0.06)
        lg_rm_Dmiss.SetBorderSize(1)
        lg_rm_Dmiss.SetLineColor(0)
        lg_rm_Dmiss.SetFillColor(0)
        lg_rm_Dmiss.SetHeader(str(ecms) + ' MeV')
        frame_rm_Dmiss.Draw()
        lg_rm_Dmiss.Draw()

        c.cd(3)
        frame_rm_pipi = rm_pipi.frame(RooFit.Bins(xbins_rm_pipi), RooFit.Title('rm_pipi'))
        xtitle_rm_pipi = 'RM(#pi_{0}^{+}#pi_{0}^{-})(GeV)'
        content_rm_pipi = int((xmax_rm_pipi - xmin_rm_pipi)/xbins_rm_pipi * 1000)
        ytitle_rm_pipi = 'Entries/%.1f MeV'%content_rm_pipi 
        set_frame_style(frame_rm_pipi, xtitle_rm_pipi, ytitle_rm_pipi)
        combData.plotOn(frame_rm_pipi, RooFit.Cut('sample==sample::rm_pipi'))
        sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(3))
        sim_pdf.plotOn(frame_rm_pipi, RooFit.Slice(sample, 'rm_pipi'), RooFit.Components('pdf_D1_2420_rm_pipi'), RooFit.ProjWData(RooArgSet(sample), combData), RooFit.LineColor(kBlack), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
        combData.plotOn(frame_rm_pipi, RooFit.Cut('sample==sample::rm_pipi'))

        name = []
        name.append('Data')
        name.append('Total Fit')
        name.append('D_{1}(2420)^{+}D^{-}')

        lg_rm_pipi = TLegend(.6, .6, .8, .85)
        for m in xrange(len(name)):
            objName = frame_rm_pipi.nameOf(m)
            obj = frame_rm_pipi.findObject(objName)
            lg_rm_pipi.AddEntry(obj, name[m], 'PL')
            lg_rm_pipi.SetTextFont(42)
            lg_rm_pipi.SetTextSize(0.06)
        lg_rm_pipi.SetBorderSize(1)
        lg_rm_pipi.SetLineColor(0)
        lg_rm_pipi.SetFillColor(0)
        lg_rm_pipi.SetHeader(str(ecms) + ' MeV')
        frame_rm_pipi.Draw()
        lg_rm_pipi.Draw()

        # Write necessary info
        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')

        path_out = './txts/IO_num_' + str(ecms) + '_' + method  + '.txt'
        f_out = open(path_out, 'w')
        line = str(n2420.getVal()) + ' ' + str(n2420.getError()) + '\n' 
        f_out.write(line)
        f_out.close()

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    canvas_name = './figs/IO_fit_' + str(ecms) + '_' + method + '.pdf'
    c.SaveAs(canvas_name)

    raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    method = args[1]

    path = []
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_after.root')
    fit(ecms, method, path)

if __name__ == '__main__':
    main()
