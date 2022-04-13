#!/usr/bin/env python
"""
Fit of cos theta of Dtag 
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2021-03-28 Sun 22:24]"

import math
from array import array
import sys, os
import logging
from math import *
from ROOT import *
from tools import param_max
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
    fit_cos_D.py

SYNOPSIS
    ./fit_cos_D.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    March 2021
\n''')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.06)

def set_frame_style(frame, xtitle, ytitle, ymax):
    frame.GetXaxis().SetTitle(xtitle)
    frame.GetXaxis().SetTitleSize(0.06)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetXaxis().SetTitleOffset(0.8)
    frame.GetXaxis().SetLabelOffset(0.008)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetXaxis().CenterTitle()
    frame.GetYaxis().SetNdivisions(504)
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleOffset(0.6)
    frame.GetYaxis().SetLabelOffset(0.008)
    frame.GetYaxis().SetTitle(ytitle)
    frame.GetYaxis().CenterTitle()
    frame.GetYaxis().SetRangeUser(0, ymax)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.1)
    mbc.SetRightMargin(0.1)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.14)
    mbc.SetGrid()

def fit(ecms, path):
    try:
        f_data = TFile(path[0], 'READ')
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data('+str(ecms)+') entries :'+str(entries_data))
        f_sideband = TFile(path[1], 'READ')
        h_sideband = f_sideband.Get('h_side')
        entries_sideband = h_sideband.Integral()
        logging.info('sideband('+str(ecms)+') entries :'+str(entries_sideband))
    except:
        logging.error(path[0] + ' or ' + path[1] + ' is invalid!')
        sys.exit()
    try:
        f_001000 = TFile(path[2], 'READ')
        t_001000 = f_001000.Get('save')
        entries_001000 = t_001000.GetEntries()
        logging.info('D1(2420)(001000) ('+str(ecms)+') entries :'+str(entries_001000))
    except:
        logging.error(path[2] + ' is invalid!')
        sys.exit()
    try:
        f_100010 = TFile(path[3], 'READ')
        t_100010 = f_100010.Get('save')
        entries_100010 = t_100010.GetEntries()
        logging.info('D1(2420)(100010) ('+str(ecms)+') entries :'+str(entries_100010))
    except:
        logging.error(path[3] + ' is invalid!')
        sys.exit()
    
    N_001000 = 50000
    N_100010 = 50000
    n001000 = RooRealVar('n001000', 'n001000', 500, 0, N_001000)
    n100010 = RooRealVar('n100010', 'n100010', 500, 0, N_100010)
    nsideband = RooRealVar('nsideband', 'nsideband', int(entries_sideband))

    # model for RM(D)
    xmin, xmax, xbins = -1.1, 1.1, 25
    cos_D = RooRealVar('cos_D', 'cos_D', xmin, xmax)
    cos_D.setRange('signal', xmin, xmax)

    cut = ''
    data = RooDataSet('data', 'data', t_data, RooArgSet(cos_D))
    hist_sideband = RooDataHist('hist_sideband', 'hist_sideband', RooArgList(cos_D), h_sideband)
    pdf_sideband = RooHistPdf('pdf_sideband', 'pdf_sideband', RooArgSet(cos_D), hist_sideband, 0)
    h_001000 = TH1F('h_001000', '', xbins, xmin, xmax)
    t_001000.Project('h_001000', 'cos_D', cut)
    hist_001000 = RooDataHist('hist_001000', 'hist_001000', RooArgList(cos_D), h_001000)
    pdf_001000 = RooHistPdf('pdf_001000', 'pdf_001000', RooArgSet(cos_D), hist_001000, 2)
    h_100010 = TH1F('h_100010', '', xbins, xmin, xmax)
    t_100010.Project('h_100010', 'cos_D', cut)
    hist_100010 = RooDataHist('hist_100010', 'hist_100010', RooArgList(cos_D), h_100010)
    pdf_100010 = RooHistPdf('pdf_100010', 'pdf_100010', RooArgSet(cos_D), hist_100010, 2)
    model = RooAddPdf('model', 'model', RooArgList(pdf_001000, pdf_100010, pdf_sideband), RooArgList(n001000, n100010, nsideband))
    results = model.fitTo(data, RooFit.Save())

    # Draw fitting results
    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)

    # plot results
    xframe = cos_D.frame(RooFit.Bins(xbins), RooFit.Range(xmin, xmax))
    xtitle = 'cos(#theta_{D^{+}})'
    ytitle = 'Entries'
    ymax = param_max(ecms)
    set_frame_style(xframe, xtitle, ytitle, ymax)
    data.plotOn(xframe)
    model.plotOn(xframe, RooFit.LineColor(kBlue), RooFit.LineWidth(3), RooFit.Name('TotFit'))
    model.plotOn(xframe, RooFit.Components('pdf_sideband'), RooFit.LineColor(kGreen), RooFit.FillStyle(1001), RooFit.FillColor(3), RooFit.LineColor(3), RooFit.VLines(), RooFit.DrawOption('F'))
    model.plotOn(xframe, RooFit.Components('pdf_001000'), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(1))
    model.plotOn(xframe, RooFit.Components('pdf_100010'), RooFit.LineColor(kRed), RooFit.LineWidth(2), RooFit.LineStyle(2))
    data.plotOn(xframe, RooFit.Name('Data'))

    name = []
    name.append('Data')
    name.append('Total Fit')
    name.append('Backgrounds')
    name.append('D_{1}(2420)^{+}D^{-}(HELAMP 001000)')
    name.append('D_{1}(2420)^{+}D^{-}(HELAMP 100010)')

    lg = TLegend(.15, .55, .35, .85)
    for m in xrange(len(name)):
        objName = xframe.nameOf(m)
        obj = xframe.findObject(objName)
        if objName == 'model_Norm[cos_D]_Comp[pdf_sideband]':
            lg.AddEntry(obj, name[m], 'F')
        else:
            lg.AddEntry(obj, name[m], 'PL')
        lg.SetTextFont(42)
        lg.SetTextSize(0.06)
    lg.SetBorderSize(1)
    lg.SetLineColor(0)
    lg.SetFillColor(0)
    lg.SetHeader(str(ecms) + ' MeV')
    xframe.Draw()
    lg.Draw()

    curve = xframe.findObject('TotFit')
    histo = xframe.findObject('Data')
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
    pt = TPaveText(0.45, 0.75, 0.6, 0.85, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    n_param = results.floatParsFinal().getSize()
    if not (nbin - n_param -1) == 0: pt_title = '#chi^{2}/ndf = ' + str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1) + '=' + str(round(chi2_tot/(nbin - n_param -1), 2))
    else: pt_title = '#chi^{2}/ndf = ' + str(round(chi2_tot, 2)) + '/' + str(nbin - n_param -1)
    pt.AddText(pt_title)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    canvas_name = './figs/fit_cos_D_' + str(ecms) + '.pdf'
    mbc.SaveAs(canvas_name)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    with open('./txts/ratio_' + str(ecms) + '.txt', 'w') as f:
        f.write(str(n001000.getVal()/(n001000.getVal() + n100010.getVal())) + ' ')
        f.write(str(n100010.getVal()/(n001000.getVal() + n100010.getVal())) + '\n')

    raw_input('Enter anything to end...')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_after_angle.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/HELAMP/shape_side_'+str(ecms)+'.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420_001000/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_after_angle.root')
    path.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420_100010/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_after_angle.root')
    fit(ecms, path)

if __name__ == '__main__':
    main()
