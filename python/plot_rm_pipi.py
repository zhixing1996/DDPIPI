#!/usr/bin/env python
"""
Plot recoiling mass of selected piplus and piminus
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-09-11 Wed 19:35]"

import ROOT
from ROOT import TCanvas, gStyle, TTree
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
import math
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def set_legend(legend, h1, h2, h3, h4, h5, title):
    legend.AddEntry(h1, 'data')
    legend.AddEntry(h2, 'data: RM(D^{+}#pi^{+}#pi^{-}) sideband')
    legend.AddEntry(h3, 'D_{1}(2420)D')
    legend.AddEntry(h4, '#psi(3770)#pi^{+}#pi^{-}')
    legend.AddEntry(h5, 'X(3842)#pi^{+}#pi^{-}')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def rm_pipi_fill(t1, t2, t3, t4, t5, h1, h2, h3, h4, h5, chi2_cut):
    for ientry1 in xrange(t1.GetEntries()):
        t1.GetEntry(ientry1)
        h1.Fill(t1.m_rm_pipi)
    for ientry2 in xrange(t2.GetEntries()):
        t2.GetEntry(ientry2)
        if t2.m_m_pipi > 0.28 and t2.m_chi2_kf < chi2_cut and (t2.m_n_pi0 == 0 or (t2.m_n_pi0 != 0 and t2.m_m_Dpi0 > 2.02)) and (t2.m_m_pipi < 0.49164 or t2.m_m_pipi > 0.50327) and t2.m_chi2_vf < 25 and t2.m_p_D < 0.675 and t2.m_m_Dpi < 2.3:
            h2.Fill(t2.m_rm_pipi)
    for ientry3 in xrange(t3.GetEntries()):
        t3.GetEntry(ientry3)
        h3.Fill(t3.m_rm_pipi)
    for ientry4 in xrange(t4.GetEntries()):
        t4.GetEntry(ientry4)
        h4.Fill(t4.m_rm_pipi)
    for ientry5 in xrange(t5.GetEntries()):
        t5.GetEntry(ientry5)
        h5.Fill(t5.m_rm_pipi)

def set_histo_style(h1, h2, h3, h4, h5, xtitle, ytitle):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitleOffset(1.3)
    h1.GetXaxis().SetLabelOffset(0.01)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetTitleOffset(1.5)
    h1.GetYaxis().SetLabelOffset(0.01)
    h1.GetXaxis().SetTitle(xtitle)
    h1.GetXaxis().CenterTitle()
    h1.GetYaxis().SetTitle(ytitle)
    h1.GetYaxis().CenterTitle()
    h1.SetLineColor(1)
    h2.SetLineColor(2)
    h3.SetLineColor(3)
    h4.SetLineColor(4)
    h5.SetLineColor(6)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(data_path, data_sideband_path, sigMC1_path, sigMC2_path, sigMC3_path, leg_title, ecms, scale, scale1, scale2, scale3, xmax, chi2_cut):
    try:
        f_data = TFile(data_path)
        f_data_sideband = TFile(data_sideband_path)
        f_sigMC1 = TFile(sigMC1_path)
        f_sigMC2 = TFile(sigMC2_path)
        f_sigMC3 = TFile(sigMC3_path)
        t_data = f_data.Get('save')
        t_data_sideband = f_data_sideband.Get('save')
        t_sigMC1 = f_sigMC1.Get('save')
        t_sigMC2 = f_sigMC2.Get('save')
        t_sigMC3 = f_sigMC3.Get('save')
        entries_data = t_data.GetEntries()
        entries_data_sideband = t_data_sideband.GetEntries()
        entries_sigMC1 = t_sigMC1.GetEntries()
        entries_sigMC2 = t_sigMC2.GetEntries()
        entries_sigMC3 = t_sigMC3.GetEntries()
        logging.info('data entries :'+str(entries_data))
        logging.info('data sideband entries :'+str(entries_data_sideband))
        logging.info('signal MC(D1(2420)) entries :'+str(entries_sigMC1))
        logging.info('signal MC(psi(3770)) entries :'+str(entries_sigMC2))
        logging.info('signal MC(X(3842)) entries :'+str(entries_sigMC3))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 3.7
    xbins = 75
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV'%content
    xtitle = 'RM(#pi^{+}_{0}#pi^{-}_{0})(GeV)'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    h_data_sideband = TH1F('data_sideband', 'data sideband', xbins, xmin, float(xmax))
    h_sigMC1 = TH1F('sigMC1', 'signal MC: D1(2420)', xbins, xmin, float(xmax))
    h_sigMC2 = TH1F('sigMC2', 'signal MC: psi(3770)', xbins, xmin, float(xmax))
    h_sigMC3 = TH1F('sigMC3', 'signal MC: X(3842)', xbins, xmin, float(xmax))

    set_histo_style(h_data, h_data_sideband, h_sigMC1, h_sigMC2, h_sigMC3, xtitle, ytitle)
    rm_pipi_fill(t_data, t_data_sideband, t_sigMC1, t_sigMC2, t_sigMC3, h_data, h_data_sideband, h_sigMC1, h_sigMC2, h_sigMC3, chi2_cut)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_data_sideband.Scale(scale)
    h_sigMC1.Scale(scale1)
    h_sigMC2.Scale(scale2)
    h_sigMC3.Scale(scale3)
    h_data.Draw('ep')
    h_data_sideband.Draw('same')
    h_sigMC1.Draw('same')
    h_sigMC2.Draw('same')
    h_sigMC3.Draw('same')

    legend = TLegend(0.55, 0.6, 0.8, 0.75)
    set_legend(legend, h_data, h_data_sideband, h_sigMC1, h_sigMC2, h_sigMC3, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/rm_pipi_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_after.root'
    data_sideband_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_sideband.root'
    sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/sigMC_D1_2420_4360_after.root'
    sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/sigMC_psipp_4360_after.root'
    sigMC3_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/sigMC_X_3842_4360_after.root'
    leg_title = '(a)'
    ecms = 4360
    scale = 0.5
    scale1 = 0.003125
    scale2 = 0.003125
    scale3 = 0.00065
    xmax = 4.1
    chi2_cut = 999
    plot(data_path, data_sideband_path, sigMC1_path, sigMC2_path, sigMC3_path, leg_title, ecms, scale, scale1, scale2, scale3, xmax, chi2_cut)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_after.root'
    data_sideband_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4420/data_4420_sideband.root'
    sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/sigMC_D1_2420_4420_after.root'
    sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/sigMC_psipp_4420_after.root'
    sigMC3_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/sigMC_X_3842_4420_after.root'
    leg_title = '(b)'
    ecms = 4420
    scale = 0.5
    scale1 = 1073.56*65.4*0.0938/500000
    scale2 = 1073.56*23.8*0.0938/500000
    scale3 = 0.0015
    xmax = 4.1
    chi2_cut = 20
    plot(data_path, data_sideband_path, sigMC1_path, sigMC2_path, sigMC3_path, leg_title, ecms, scale, scale1, scale2, scale3, xmax, chi2_cut)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_after.root'
    data_sideband_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_sideband.root'
    sigMC1_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/sigMC_D1_2420_4600_after.root'
    sigMC2_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/sigMC_psipp_4600_after.root'
    sigMC3_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/sigMC_X_3842_4600_after.root'
    leg_title = '(c)'
    ecms = 4600
    scale = 0.5
    scale1 = 0.003125
    scale2 = 0.001625
    scale3 = 0.0009
    xmax = 4.35
    chi2_cut = 999
    plot(data_path, data_sideband_path, sigMC1_path, sigMC2_path, sigMC3_path, leg_title, ecms, scale, scale1, scale2, scale3, xmax, chi2_cut)
