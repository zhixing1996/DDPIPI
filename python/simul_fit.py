#!/usr/bin/env python
"""
Simultaneous fit of recoiling mass of D and Dmiss
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-30 Sat 06:33]"

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
    simul_fit.py

SYNOPSIS
    ./simul_fit.py

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

def simul_fit(path, shape):
    try:
        f_data_4360 = TFile(path[0], 'READ')
        f_data_4420 = TFile(path[1], 'READ')
        f_data_4600 = TFile(path[2], 'READ')
        f_sideband_4360 = TFile(path[3], 'READ')
        f_sideband_4420 = TFile(path[4], 'READ')
        f_sideband_4600 = TFile(path[5], 'READ')
        f_psipp_4360 = TFile(path[6], 'READ')
        f_psipp_4420 = TFile(path[7], 'READ')
        f_psipp_4600 = TFile(path[8], 'READ')
        t_data_4360 = f_data_4360.Get('save')
        t_data_4420 = f_data_4420.Get('save')
        t_data_4600 = f_data_4600.Get('save')
        t_sideband_4360 = f_sideband_4360.Get('save')
        t_sideband_4420 = f_sideband_4420.Get('save')
        t_sideband_4600 = f_sideband_4600.Get('save')
        t_psipp_4360 = f_psipp_4360.Get('save')
        t_psipp_4420 = f_psipp_4420.Get('save')
        t_psipp_4600 = f_psipp_4600.Get('save')
        entries_data_4360 = t_data_4360.GetEntries()
        entries_data_4420 = t_data_4420.GetEntries()
        entries_data_4600 = t_data_4600.GetEntries()
        entries_sideband_4360 = t_sideband_4360.GetEntries()
        entries_sideband_4420 = t_sideband_4420.GetEntries()
        entries_sideband_4600 = t_sideband_4600.GetEntries()
        entries_psipp_4360 = t_psipp_4360.GetEntries()
        entries_psipp_4420 = t_psipp_4420.GetEntries()
        entries_psipp_4600 = t_psipp_4600.GetEntries()
        logging.info('data(4360) entries :'+str(entries_data_4360))
        logging.info('data(4420) entries :'+str(entries_data_4420))
        logging.info('data(4600) entries :'+str(entries_data_4600))
        logging.info('sideband(4360) entries :'+str(entries_sideband_4360))
        logging.info('sideband(4420) entries :'+str(entries_sideband_4420))
        logging.info('sideband(4600) entries :'+str(entries_sideband_4600))
        logging.info('psipp(4360) entries :'+str(entries_psipp_4360))
        logging.info('psipp(4420) entries :'+str(entries_psipp_4420))
        logging.info('psipp(4600) entries :'+str(entries_psipp_4600))
        f_D1_2420_4360 = TFile(shape[0], 'READ')
        f_D1_2420_4420 = TFile(shape[1], 'READ')
        f_D1_2420_4600 = TFile(shape[2], 'READ')
    except:
        logging.error('Files are invalid!')
        sys.exit()

    xmin_4360 = 2.14
    xmax_4360 = 2.49
    xbins_4360 = 140
    xmin_4420 = 2.14
    xmax_4420 = 2.55
    xbins_4420 = 164
    xmin_4600 = 2.14
    xmax_4600 = 2.72
    xbins_4600 = 232

    rm_D_4360 = RooRealVar('rm_D', 'rm_D', xmin_4360, xmax_4360)
    rm_D_4420 = RooRealVar('rm_D', 'rm_D', xmin_4420, xmax_4420)
    rm_D_4600 = RooRealVar('rm_D', 'rm_D', xmin_4600, xmax_4600)
    n2420_4360 = RooRealVar('n2420_4360', 'n2420_4360', 500, 0, 2000)
    n2420_4420 = RooRealVar('n2420_4420', 'n2420_4420', 3000, 0, 4000)
    n2420_4600 = RooRealVar('n2420_4600', 'n2420_4600', 3000, 0, 4000)
    nsideband_4360 = RooRealVar('nsideband_4360', 'nsideband_4360', 1402)
    nsideband_4420 = RooRealVar('nsideband_4420', 'nsideband_4420', 4359)
    nsideband_4600 = RooRealVar('nsideband_4600', 'nsideband_4600', 3495)
    npsipp_4360 = RooRealVar('npsipp_4360', 'npsipp_4360', 0, 2000)
    npsipp_4420 = RooRealVar('npsipp_4420', 'npsipp_4420', 0, 5000)
    npsipp_4600 = RooRealVar('npsipp_4600', 'npsipp_4600', 0, 4000)

    h_sideband_4360 = TH1F('h_sideband_4360', '', xbins_4360, xmin_4360, xmax_4360)
    h_sideband_4420 = TH1F('h_sideband_4420', '', xbins_4420, xmin_4420, xmax_4420)
    h_sideband_4600 = TH1F('h_sideband_4600', '', xbins_4600, xmin_4600, xmax_4600)
    h_psipp_4360 = TH1F('h_psipp_4360', '', xbins_4360, xmin_4360, xmax_4360)
    h_psipp_4420 = TH1F('h_psipp_4420', '', xbins_4420, xmin_4420, xmax_4420)
    h_psipp_4600 = TH1F('h_psipp_4600', '', xbins_4600, xmin_4600, xmax_4600)

    cut = ''
    t_sideband_4360.Project('h_sideband_4360', 'rm_D', cut)
    t_sideband_4420.Project('h_sideband_4420', 'rm_D', cut)
    t_sideband_4600.Project('h_sideband_4600', 'rm_D', cut)
    t_psipp_4360.Project('h_psipp_4360', 'rm_D', cut)
    t_psipp_4420.Project('h_psipp_4420', 'rm_D', cut)
    t_psipp_4600.Project('h_psipp_4600', 'rm_D', cut)

    set_data_4360 = RooDataSet('set_data_4360', ' set_data_4360', t_data_4360, RooArgSet(rm_D_4360))
    set_data_4420 = RooDataSet('set_data_4420', ' set_data_4420', t_data_4420, RooArgSet(rm_D_4420))
    set_data_4600 = RooDataSet('set_data_4600', ' set_data_4600', t_data_4600, RooArgSet(rm_D_4600))
    hist_sideband_4360 = RooDataHist('hist_sideband_4360', 'hist_sideband_4360', RooArgList(rm_D_4360), h_sideband_4360)
    hist_sideband_4420 = RooDataHist('hist_sideband_4420', 'hist_sideband_4420', RooArgList(rm_D_4420), h_sideband_4420)
    hist_sideband_4600 = RooDataHist('hist_sideband_4600', 'hist_sideband_4600', RooArgList(rm_D_4600), h_sideband_4600)
    hist_psipp_4360 = RooDataHist('hist_psipp_4360', 'hist_psipp_4360', RooArgList(rm_D_4360), h_psipp_4360)
    hist_psipp_4420 = RooDataHist('hist_psipp_4420', 'hist_psipp_4420', RooArgList(rm_D_4420), h_psipp_4420)
    hist_psipp_4600 = RooDataHist('hist_psipp_4600', 'hist_psipp_4600', RooArgList(rm_D_4600), h_psipp_4600)

    pdf_sideband_4360 = RooHistPdf('pdf_sideband_4360', 'pdf_sideband_4360', RooArgSet(rm_D_4360), hist_sideband_4360, 0)
    pdf_sideband_4420 = RooHistPdf('pdf_sideband_4420', 'pdf_sideband_4420', RooArgSet(rm_D_4420), hist_sideband_4420, 0)
    pdf_sideband_4600 = RooHistPdf('pdf_sideband_4600', 'pdf_sideband_4600', RooArgSet(rm_D_4600), hist_sideband_4600, 0)
    pdf_psipp_4360 = RooHistPdf('pdf_psipp_4360', 'pdf_psipp_4360', RooArgSet(rm_D_4360), hist_psipp_4360, 2)
    pdf_psipp_4420 = RooHistPdf('pdf_psipp_4420', 'pdf_psipp_4420', RooArgSet(rm_D_4420), hist_psipp_4420, 2)
    pdf_psipp_4600 = RooHistPdf('pdf_psipp_4600', 'pdf_psipp_4600', RooArgSet(rm_D_4600), hist_psipp_4600, 2)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    path_out = './txts/simul_results.txt'
    f_out = open(path_out, 'w')

    for i in xrange(1):
        for j in xrange(1):
            pdf_name_4360 = 'Covpdf_D1_2420_4360_' + str(i) + '_' + str(j)
            pdf_name_4420 = 'Covpdf_D1_2420_4420_' + str(i) + '_' + str(j)
            pdf_name_4600 = 'Covpdf_D1_2420_4600_' + str(i) + '_' + str(j)
            canvas_name_4360 = './figs/canvas_rm_D_' + str(i) + '_' +str(j) + '_4360.pdf'
            canvas_name_4420 = './figs/canvas_rm_D_' + str(i) + '_' +str(j) + '_4420.pdf'
            canvas_name_4600 = './figs/canvas_rm_D_' + str(i) + '_' +str(j) + '_4600.pdf'

            covpdf_D1_2420_4360 = f_D1_2420_4360.Get(pdf_name_4360)
            covpdf_D1_2420_4420 = f_D1_2420_4420.Get(pdf_name_4420)
            covpdf_D1_2420_4600 = f_D1_2420_4600.Get(pdf_name_4600)

            model_4360 = RooAddPdf('model_4360', 'model_4360', RooArgList(covpdf_D1_2420_4360, pdf_sideband_4360, pdf_psipp_4360), RooArgList(n2420_4360, nsideband_4360, npsipp_4360))
            model_4420 = RooAddPdf('model_4420', 'model_4420', RooArgList(covpdf_D1_2420_4420, pdf_sideband_4420, pdf_psipp_4420), RooArgList(n2420_4420, nsideband_4420, npsipp_4420))
            model_4600 = RooAddPdf('model_4600', 'model_4600', RooArgList(covpdf_D1_2420_4600, pdf_sideband_4600, pdf_psipp_4600), RooArgList(n2420_4600, nsideband_4600, npsipp_4600))

            nl_4360 = model_4360.createNLL(set_data_4360, RooFit.Range(xmin_4360, xmax_4360))
            nl_4420 = model_4420.createNLL(set_data_4420, RooFit.Range(xmin_4420, xmax_4420))
            nl_4600 = model_4600.createNLL(set_data_4600, RooFit.Range(xmin_4600, xmax_4600))

            nll = RooAddition('nll', 'nll', RooArgSet(nl_4360, nl_4420, nl_4600))
            mm = RooMinuit(nll)
            mm.migrad()
            r = mm.save()

            mass2420 = 2.4240 + 0.0001*40
            width2420 = 0.018 + 0.001*8
            n4360 = n2420_4360.getVal()
            n4420 = n2420_4420.getVal()
            n4600 = n2420_4600.getVal()
            npsipp_1 = npsipp_4360.getVal()
            npsipp_2 = npsipp_4420.getVal()
            npsipp_3 = npsipp_4600.getVal()

            line = str(r.minNll()) + ' ' + str(mass2420 + 0.0001*i) + ' ' + str(width2420 + 0.001*j)
            line += ' ' + str(n4360) + ' ' + str(n2420_4360.getError())
            line += ' ' + str(n4420) + ' ' + str(n2420_4420.getError())
            line += ' ' + str(n4600) + ' ' + str(n2420_4600.getError())
            line += ' ' + str(npsipp_1) + ' ' + str(npsipp_4360.getError())
            line += ' ' + str(npsipp_2) + ' ' + str(npsipp_4420.getError())
            line += ' ' + str(npsipp_3) + ' ' + str(npsipp_4600.getError())
            f_out.write(line)

            c_4360 = TCanvas('c_4360', 'c_4360', 800, 600)
            set_canvas_style(c_4360)
            c_4360.cd()

            xframe_4360 = rm_D_4360.frame(RooFit.Bins(xbins_4360), RooFit.Range(xmin_4360, xmax_4360))
            xtitle = 'RM(D^{+}) and RM(D^{-}_{miss})(GeV)'
            content = (xmax_4360 - xmin_4360)/xbins_4360 * 1000
            ytitle = 'Events/%.1f MeV'%content
            set_xframe_style(xframe_4360, xtitle, ytitle)
            set_data_4360.plotOn(xframe_4360, RooFit.MarkerSize(1), RooFit.LineWidth(1))
            model_4360.plotOn(xframe_4360, RooFit.Components('pdf_sideband_4360'), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
            covpdf_name_4360 = 'Covpdf_D1_2420_4360_' + str(i) + '_' + str(j)
            model_4360.plotOn(xframe_4360, RooFit.Components(covpdf_name_4360), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
            model_4360.plotOn(xframe_4360, RooFit.Components('pdf_psipp_4360'), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
            model_4360.plotOn(xframe_4360, RooFit.LineColor(kBlack), RooFit.LineWidth(3))

            name = []
            name.append('Data')
            name.append('Backgrounds')
            name.append('D_{1}(2420)^{+} D^{-}')
            name.append('#psi(3770) #pi^{+} #pi^{-}')

            lg_4360 = TLegend(.2, .6, .4, .85)
            for m in xrange(4):
                objName = xframe_4360.nameOf(m)
                obj = xframe_4360.findObject(objName)
                if m != 1:
                    lg_4360.AddEntry(obj, name[m], 'PL')
                if m == 1:
                    lg_4360.AddEntry(obj, name[m], 'F')
                lg_4360.SetTextFont(42)
                lg_4360.SetTextSize(0.03)
            lg_4360.SetBorderSize(1)
            lg_4360.SetLineColor(0)
            lg_4360.SetFillColor(0)
            xframe_4360.Draw()
            lg_4360.Draw()

            c_4420 = TCanvas('c_4420', 'c_4420', 800, 600)
            set_canvas_style(c_4420)
            c_4420.cd()

            xframe_4420 = rm_D_4420.frame(RooFit.Bins(xbins_4420), RooFit.Range(xmin_4420, xmax_4420))
            xtitle = 'RM(D^{+}) and RM(D^{-}_{miss})(GeV)'
            content = (xmax_4420 - xmin_4420)/xbins_4420 * 1000
            ytitle = 'Events/%.1f MeV'%content
            set_xframe_style(xframe_4420, xtitle, ytitle)
            set_data_4420.plotOn(xframe_4420, RooFit.MarkerSize(1), RooFit.LineWidth(1))
            model_4420.plotOn(xframe_4420, RooFit.Components('pdf_sideband_4420'), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption("F"))
            covpdf_name_4420 = 'Covpdf_D1_2420_4420_' + str(i) + '_' + str(j)
            model_4420.plotOn(xframe_4420, RooFit.Components(covpdf_name_4420), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
            model_4420.plotOn(xframe_4420, RooFit.Components('pdf_psipp_4420'), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
            model_4420.plotOn(xframe_4420, RooFit.LineColor(kBlack), RooFit.LineWidth(3))

            name = []
            name.append('Data')
            name.append('Backgrounds')
            name.append('D_{1}(2420)^{+} D^{-}')
            name.append('#psi(3770) #pi^{+} #pi^{-}')

            lg_4420 = TLegend(.2, .6, .4, .85)
            for m in xrange(4):
                objName_4420 = xframe_4420.nameOf(m)
                obj_4420 = xframe_4420.findObject(objName_4420)
                if m != 1:
                    lg_4420.AddEntry(obj_4420, name[m], 'PL')
                if m == 1:
                    lg_4420.AddEntry(obj_4420, name[m], 'F')
                lg_4420.SetTextFont(42)
                lg_4420.SetTextSize(0.03)
            lg_4420.SetBorderSize(1)
            lg_4420.SetLineColor(0)
            lg_4420.SetFillColor(0)
            xframe_4420.Draw()
            lg_4420.Draw()

            c_4600 = TCanvas('c_4600', 'c_4600', 800, 600)
            set_canvas_style(c_4600)
            c_4600.cd()

            xframe_4600 = rm_D_4600.frame(RooFit.Bins(xbins_4600), RooFit.Range(xmin_4600, xmax_4600))
            xtitle = 'RM(D^{+}) and RM(D^{-}_{miss})(GeV)'
            content = (xmax_4600 - xmin_4600)/xbins_4600 * 1000
            ytitle = 'Events/%.1f MeV'%content
            set_xframe_style(xframe_4600, xtitle, ytitle)
            set_data_4600.plotOn(xframe_4600, RooFit.MarkerSize(1), RooFit.LineWidth(1))
            model_4600.plotOn(xframe_4600, RooFit.Components('pdf_sideband_4600'), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption("F"))
            covpdf_name_4600 = 'Covpdf_D1_2420_4600_' + str(i) + '_' + str(j)
            model_4600.plotOn(xframe_4600, RooFit.Components(covpdf_name_4600), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
            model_4600.plotOn(xframe_4600, RooFit.Components('pdf_psipp_4600'), RooFit.LineColor(kBlue), RooFit.LineWidth(2), RooFit.LineStyle(kDashed))
            model_4600.plotOn(xframe_4600, RooFit.LineColor(kBlack), RooFit.LineWidth(3))

            name = []
            name.append('Data')
            name.append('Backgrounds')
            name.append('D_{1}(2420)^{+} D^{-}')
            name.append('#psi(3770) #pi^{+} #pi^{-}')

            lg_4600 = TLegend(.2, .6, .4, .85)
            for m in xrange(4):
                objName_4600 = xframe_4600.nameOf(m)
                obj_4600 = xframe_4600.findObject(objName_4600)
                if m != 1:
                    lg_4600.AddEntry(obj_4600, name[m], 'PL')
                if m == 1:
                    lg_4600.AddEntry(obj_4600, name[m], 'F')
                lg_4600.SetTextFont(42)
                lg_4600.SetTextSize(0.03)
            lg_4600.SetBorderSize(1)
            lg_4600.SetLineColor(0)
            lg_4600.SetFillColor(0)
            xframe_4600.Draw()
            lg_4600.Draw()

            c_4360.SaveAs(canvas_name_4360)
            c_4420.SaveAs(canvas_name_4420)
            c_4600.SaveAs(canvas_name_4600)

            # delete covpdf_D1_2420_4360
            # delete covpdf_D1_2420_4420
            # delete covpdf_D1_2420_4600
    # f_out.Close()

def main():
    path = []
    shape = []
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4360/data_4360_fit.root')
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4420/data_4420_fit.root')
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4600/data_4600_fit.root')
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4360/data_4360_sideband_fit.root')
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4420/data_4420_sideband_fit.root')
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4600/data_4600_sideband_fit.root')
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_fit.root')
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_fit.root')
    path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_fit.root')
    shape.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_conv_4360.root')
    shape.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_conv_4420.root')
    shape.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_conv_4600.root')
    simul_fit(path, shape)

if __name__ == '__main__':
    main()
