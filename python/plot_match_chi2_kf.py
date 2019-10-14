#!/usr/bin/env python
"""
Plot match chi2 of D kinematic fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-10-14 Mon 10:00]"

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
        if (t.m_n_pi0 == 0 or (t.m_n_pi0 != 0 and t.m_m_Dpi0 > 2.01)) and ((t.m_m_D0 > 0.14 and t.m_m_D0 < 1.8) or t.m_m_D0 > 2.1):
            if t.m_matched_D == 0 and t.m_matched_pi == 0:
                h1.Fill(t.m_chi2_kf)
            if t.m_matched_D == 1 and t.m_matched_pi == 0:
                h2.Fill(t.m_chi2_kf)
            if t.m_matched_D == 0 and t.m_matched_pi == 1:
                h3.Fill(t.m_chi2_kf)
            if t.m_matched_D == 1 and t.m_matched_pi == 1:
                h4.Fill(t.m_chi2_kf)

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

def plot(incMC_path, leg_title, ecms, xmax, arrow_left, arrow_bottom, arrow_right, arrow_top):
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
    xtitle = "#chi^{2}(D^{+}D_{missing}#pi^{+}_{0}#pi^{-}_{0})"
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
    h_unDunpi.Draw('ep')
    h_Dunpi.Draw('samee')
    h_unDpi.Draw('samee')
    h_Dpi.Draw('samee')

    arrow = TArrow(arrow_left, arrow_bottom, arrow_right, arrow_top, 0.01, '<')
    set_arrow(arrow)
    arrow.Draw()

    legend = TLegend(0.45, 0.6, 0.82, 0.8)
    set_legend(legend, h_unDunpi, h_Dunpi, h_unDpi, h_Dpi, leg_title)
    legend.Draw()

    mbc.SaveAs('./figs/matched_chi2_kf_'+str(ecms)+'.pdf')

if __name__ == '__main__':
    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4360/incMC_hadrons_4360_before.root'
    leg_title = '(a)'
    ecms = 4360
    xmax = 47
    arrow_left = 20
    arrow_bottom = 100
    arrow_right = 20
    arrow_top = 4000
    plot(incMC_path, leg_title, ecms, xmax, arrow_left, arrow_bottom, arrow_right, arrow_top)

    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4420/incMC_hadrons_4420_before.root'
    leg_title = '(b)'
    ecms = 4420
    xmax = 47
    arrow_left = 20
    arrow_bottom = 100
    arrow_right = 20
    arrow_top = 4000
    plot(incMC_path, leg_title, ecms, xmax, arrow_left, arrow_bottom, arrow_right, arrow_top)

    incMC_path = '/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4600/incMC_hadrons_4600_before.root'
    leg_title = '(c)'
    ecms = 4600
    xmax = 25
    arrow_left = 20
    arrow_bottom = 100
    arrow_right = 20
    arrow_top = 4000
    plot(incMC_path, leg_title, ecms, xmax, arrow_left, arrow_bottom, arrow_right, arrow_top)
