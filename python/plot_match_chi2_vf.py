#!/usr/bin/env python
"""
Plot mathced chi2 of vertex fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-10-14 Mon 22:32]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TArrow
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def set_arrow(arrow):
    arrow.SetLineWidth(0)
    arrow.SetLineColor(2)
    arrow.SetFillColor(2)

def set_legend(legend, h1, h2, h3, h4, title):
    legend.AddEntry(h1, 'not D && not #pi')
    legend.AddEntry(h2, 'D && not #pi')
    legend.AddEntry(h3, 'not D && #pi')
    legend.AddEntry(h4, 'D && #pi')
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)

def chi2_KF_fill(t, entries, h1, h2, h3, h4):
    for ientry in xrange(entries):
        t.GetEntry(ientry)
        if (t.m_n_pi0 == 0 or (t.m_n_pi0 != 0 and (t.m_m_Dpi0 > 2.01165 or t.m_m_Dpi0 < 2.00871))) and (t.m_m_D0 < 1.80397 or t.m_m_D0 > 1.91843) and (t.m_m_D0 < 2.00117 or t.m_m_D0 > 2.01798) and (t.m_m_pipi < 0.49147 or t.m_m_pipi > 0.50364):
            if t.m_matched_D == 0 and t.m_matched_pi == 0:
                h1.Fill(t.m_chi2_vf)
            if t.m_matched_D == 1 and t.m_matched_pi == 0:
                h2.Fill(t.m_chi2_vf)
            if t.m_matched_D == 0 and t.m_matched_pi == 1:
                h3.Fill(t.m_chi2_vf)
            if t.m_matched_D == 1 and t.m_matched_pi == 1:
                h4.Fill(t.m_chi2_vf)

def set_histo_style(h1, h2, h3, h4, xtitle, ytitle):
    h1.GetXaxis().SetNdivisions(509)
    h1.GetYaxis().SetNdivisions(504)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h3.SetLineWidth(2)
    h4.SetLineWidth(2)
    h1.SetStats(0)
    h2.SetStats(0)
    h3.SetStats(0)
    h4.SetStats(0)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitleOffset(1.4)
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

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(incMC_path, leg_title, ecms, xmax):
    try:
        f_incMC = TFile(incMC_path)
        t_incMC = f_incMC.Get('save')
        entries_incMC = t_incMC.GetEntries()
        logging.info('inclusive MC(hadrons) entries :'+str(entries_incMC))
    except:
        logging.error(incMC_path+' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    set_canvas_style(mbc)
    xmin = 0
    xbins = xmax
    ytitle = "Events"
    xtitle = "#chi^{2}_{vertex}"
    h_unDunpi = TH1F('unDunpi', 'unDunpi', xbins, xmin, xmax)
    h_Dunpi = TH1F('Dunpi', 'Dunpi', xbins, xmin, xmax)
    h_unDpi = TH1F('unDpi', 'unDpi', xbins, xmin, xmax)
    h_Dpi = TH1F('Dpi', 'Dpi', xbins, xmin, xmax)

    set_histo_style(h_unDunpi, h_Dunpi, h_unDpi, h_Dpi, xtitle, ytitle)
    chi2_KF_fill(t_incMC, entries_incMC, h_unDunpi, h_Dunpi, h_unDpi, h_Dpi)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_Dunpi.Scale(h_unDunpi.GetEntries()/h_Dunpi.GetEntries()/2)
    h_unDpi.Scale(h_unDunpi.GetEntries()/h_unDpi.GetEntries()/2)
    h_Dpi.Scale(h_unDunpi.GetEntries()/h_Dpi.GetEntries()/2)
    h_unDunpi.Draw()
    h_Dunpi.Draw('same')
    h_unDpi.Draw('same')
    h_Dpi.Draw('same')

    arrow = TArrow(25, 100, 25, 4000, 0.01, '<')
    set_arrow(arrow)
    arrow.Draw()

    legend = TLegend(0.45, 0.6, 0.82, 0.8)
    set_legend(legend, h_unDunpi, h_Dunpi, h_unDpi, h_Dpi, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/matched_chi2_vf_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4360/data_4360_signal.root'
    sigMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/sigMC_X_3842_4360_signal.root'
    leg_title = '(a)'
    ecms = 4360
    ymax = 1200
    plot(data_path, sigMC_path, leg_title, ecms, ymax)

    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4420/incMC_hadrons_4420_before.root'
    leg_title = '(b)'
    ecms = 4420
    xmax = 100
    plot(incMC_path, leg_title, ecms, xmax)

    data_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/data/4600/data_4600_signal.root'
    sigMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/sigMC_X_3842_4600_signal.root'
    leg_title = '(c)'
    ecms = 4600
    ymax = 3000
    plot(data_path, sigMC_path, leg_title, ecms, ymax)