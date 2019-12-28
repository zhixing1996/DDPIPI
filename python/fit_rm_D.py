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
    simul_fit.py

SYNOPSIS
    ./fit_rm_D.py [ecms]

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

def simul_fit(ecms, path, shape, root):
    try:
        f_data = TFile(path[0], 'READ')
        f_sideband = TFile(path[1], 'READ')
        f_psipp = TFile(path[2], 'READ')
        f_psipp_root = TFile(root[0], 'READ')
        t_data = f_data.Get('save')
        t_sideband = f_sideband.Get('save')
        t_psipp = f_psipp.Get('save')
        t_psipp_root = f_psipp_root.Get('save')
        entries_data = t_data.GetEntries()
        entries_sideband = t_sideband.GetEntries()
        entries_psipp = t_psipp.GetEntries()
        entries_psipp_root = t_psipp_root.GetEntries()
        logging.info('data('+str(ecms)+') entries :'+str(entries_data))
        logging.info('sideband('+str(ecms)+') entries :'+str(entries_sideband))
        logging.info('psipp('+str(ecms)+') entries :'+str(entries_psipp))
        if ecms >= 4290:
            f_D1_2420 = TFile(shape[0], 'READ')
            f_D1_2420_root = TFile(root[1], 'READ')
            t_D1_2420_root = f_D1_2420_root.Get('save')
            entries_D1_2420_root = t_D1_2420_root.GetEntries()
    except:
        logging.error('Files are invalid!')
        sys.exit()

    xmin, xmax, temp = param_rm_D(ecms)
    xbins = int((xmax - xmin)/0.002)

    rm_D = RooRealVar('rm_D', 'rm_D', xmin, xmax)
    if ecms >= 4290:
        n2420 = RooRealVar('n2420', 'n2420', 500, 0, 200000)
    nsideband = RooRealVar('nsideband', 'nsideband', int(entries_sideband/2.))
    npsipp = RooRealVar('npsipp', 'npsipp', 0, 200000)

    h_sideband = TH1F('h_sideband', '', xbins, xmin, xmax)
    h_psipp = TH1F('h_psipp', '', xbins, xmin, xmax)

    cut = ''
    t_sideband.Project('h_sideband', 'rm_D', cut)
    t_psipp.Project('h_psipp', 'rm_D', cut)

    set_data = RooDataSet('set_data', ' set_data', t_data, RooArgSet(rm_D))
    hist_sideband = RooDataHist('hist_sideband', 'hist_sideband', RooArgList(rm_D), h_sideband)
    hist_psipp = RooDataHist('hist_psipp', 'hist_psipp', RooArgList(rm_D), h_psipp)

    pdf_sideband = RooHistPdf('pdf_sideband', 'pdf_sideband', RooArgSet(rm_D), hist_sideband, 0)
    pdf_psipp = RooHistPdf('pdf_psipp', 'pdf_psipp', RooArgSet(rm_D), hist_psipp, 2)

    canvas_name = './figs/canvas_rm_D_' + str(0) + '_' +str(0) + '_' + str(ecms) + '.pdf'
    if ecms >= 4290:
        pdf_name = 'Covpdf_D1_2420_' + str(ecms) + '_' + str(0) + '_' + str(0)
        covpdf_D1_2420 = f_D1_2420.Get(pdf_name)
        model = RooAddPdf('model', 'model', RooArgList(covpdf_D1_2420, pdf_sideband, pdf_psipp), RooArgList(n2420, nsideband, npsipp))
    else:
        model = RooAddPdf('model', 'model', RooArgList(pdf_sideband, pdf_psipp), RooArgList(nsideband, npsipp))
    model.fitTo(set_data)

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_out = './txts/fit_rm_D_' + str(ecms) + '.txt'
    f_out = open(path_out, 'w')
    Br = 0.0938
    temp1, temp2, lum = data_base(ecms)
    n_D1_2420 = 0.
    eff_D1_2420 = 0.
    xs_D1_2420 = 0.
    if ecms >= 4290:
        n_D1_2420 = n2420.getVal()
        if ecms == 4420:
            eff_D1_2420 = entries_D1_2420_root/40000.
        else:
            eff_D1_2420 = entries_D1_2420_root/20000.
        xs_D1_2420 = n_D1_2420/2./2./Br/eff_D1_2420/lum
    if ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420:
        eff_psipp = entries_psipp_root/40000.
    else:
        eff_psipp = entries_psipp_root/20000.
    xs_psipp = npsipp.getVal()/2./2./Br/eff_psipp/lum
    line = '& @' + str(ecms) + 'MeV& ' + str(int(n_D1_2420)) + '& ' + str(int(npsipp.getVal())) + '& ' + str(round(eff_D1_2420*100, 2)) + '\%& ' + str(round(eff_psipp*100, 2)) + '\%& '
    line += str(lum) + '& ' + str(Br*100) + '\%& ' + str(round(xs_D1_2420, 2)) + '& ' + str(round(xs_psipp, 2)) + '& ' + str(round(xs_D1_2420 + xs_psipp, 2)) + '& \\\\\n'
    f_out.write(line)
    f_out.close()

    path_out_read = './txts/fit_rm_D_' + str(ecms) + '_read.txt'
    f_out_read = open(path_out_read, 'w')
    line_read = str(ecms) + ' ' + str(int(n_D1_2420)) + ' ' + str(int(npsipp.getVal())) + ' ' + str(round(eff_D1_2420*100, 2)) + ' ' + str(round(eff_psipp*100, 2)) + ' '
    line_read += str(lum) + ' ' + str(Br*100) + ' ' + str(round(xs_D1_2420, 2)) + ' ' + str(round(xs_psipp, 2)) + ' ' + str(round(xs_D1_2420 + xs_psipp, 2)) + ' \n'
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
    model.plotOn(xframe, RooFit.LineColor(kBlack), RooFit.LineWidth(3))

    name = []
    name.append('Data')
    name.append('Backgrounds')
    if ecms >= 4290:
        name.append('D_{1}(2420)^{+} D^{-}')
    name.append('#psi(3770) #pi^{+} #pi^{-}')

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
    # f_out.close()

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = int(args[0])

    path = []
    shape = []
    root = []
    if ecms >= 4290:
        path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_sideband_fit.root')
        path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_fit.root')
        shape.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_conv_'+str(ecms)+'.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_after.root')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_after.root')
        simul_fit(ecms, path, shape, root)

    if ecms < 4290:
        path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_fit.root')
        path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_sideband_fit.root')
        path.append('/besfs/users/jingmq/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_fit.root')
        shape.append('')
        root.append('/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_after.root')
        simul_fit(ecms, path, shape, root)

if __name__ == '__main__':
    main()
