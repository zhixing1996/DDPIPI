#!/usr/bin/env python
"""
Status of D and pi matching
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-10-13 Thu 00:14]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TPaveText
import sys, os
import logging
import math
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

h_match = ROOT.TH1F('hmatch', 'match', 6, 0, 6)
h_match.GetXaxis().SetBinLabel(2, 'not D && not #pi')
h_match.GetXaxis().SetBinLabel(3, 'D && not #pi')
h_match.GetXaxis().SetBinLabel(4, '#pi && not D')
h_match.GetXaxis().SetBinLabel(5, 'D && #pi')

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.04)

def fill(t, entries, MODE):
    for ientry in xrange(entries):
        t.GetEntry(ientry)
        if MODE == 'raw':
            if t.m_matched_D == 0 and t.m_matched_pi == 0:
                h_match.Fill(1)
            if t.m_matched_D == 1 and t.m_matched_pi == 0:
                h_match.Fill(2)
            if t.m_matched_D == 0 and t.m_matched_pi == 1:
                h_match.Fill(3)
            if t.m_matched_D == 1 and t.m_matched_pi == 1:
                h_match.Fill(4)
        if MODE == 'cut1':
            if t.m_n_pi0 == 0 or (t.m_n_pi0 != 0 and t.m_m_Dpi0 > 2.02):
                if t.m_matched_D == 0 and t.m_matched_pi == 0:
                    h_match.Fill(1)
                if t.m_matched_D == 1 and t.m_matched_pi == 0:
                    h_match.Fill(2)
                if t.m_matched_D == 0 and t.m_matched_pi == 1:
                    h_match.Fill(3)
                if t.m_matched_D == 1 and t.m_matched_pi == 1:
                    h_match.Fill(4)
        if MODE == 'cut2':
            if (t.m_n_pi0 == 0 or (t.m_n_pi0 != 0 and t.m_m_Dpi0 > 2.02)) and (t.m_m_pipi < 0.49164 or t.m_m_pipi > 0.50327):
                if t.m_matched_D == 0 and t.m_matched_pi == 0:
                    h_match.Fill(1)
                if t.m_matched_D == 1 and t.m_matched_pi == 0:
                    h_match.Fill(2)
                if t.m_matched_D == 0 and t.m_matched_pi == 1:
                    h_match.Fill(3)
                if t.m_matched_D == 1 and t.m_matched_pi == 1:
                    h_match.Fill(4)
        if MODE == 'cut3':
            if (t.m_n_pi0 == 0 or (t.m_n_pi0 != 0 and t.m_m_Dpi0 > 2.02)) and (t.m_m_pipi < 0.49164 or t.m_m_pipi > 0.50327) and t.m_chi2_vf < 25:
                if t.m_matched_D == 0 and t.m_matched_pi == 0:
                    h_match.Fill(1)
                if t.m_matched_D == 1 and t.m_matched_pi == 0:
                    h_match.Fill(2)
                if t.m_matched_D == 0 and t.m_matched_pi == 1:
                    h_match.Fill(3)
                if t.m_matched_D == 1 and t.m_matched_pi == 1:
                    h_match.Fill(4)
        if MODE == 'cut4':
            if (t.m_n_pi0 == 0 or (t.m_n_pi0 != 0 and t.m_m_Dpi0 > 2.02)) and (t.m_m_pipi < 0.49164 or t.m_m_pipi > 0.50327) and t.m_chi2_vf < 25 and t.m_p_D < 0.675:
                if t.m_matched_D == 0 and t.m_matched_pi == 0:
                    h_match.Fill(1)
                if t.m_matched_D == 1 and t.m_matched_pi == 0:
                    h_match.Fill(2)
                if t.m_matched_D == 0 and t.m_matched_pi == 1:
                    h_match.Fill(3)
                if t.m_matched_D == 1 and t.m_matched_pi == 1:
                    h_match.Fill(4)
        if MODE == 'cut5':
            if (t.m_n_pi0 == 0 or (t.m_n_pi0 != 0 and t.m_m_Dpi0 > 2.02)) and (t.m_m_pipi < 0.49164 or t.m_m_pipi > 0.50327) and t.m_chi2_vf < 25 and t.m_p_D < 0.675 and t.m_m_Dpi < 2.3:
                if t.m_matched_D == 0 and t.m_matched_pi == 0:
                    h_match.Fill(1)
                if t.m_matched_D == 1 and t.m_matched_pi == 0:
                    h_match.Fill(2)
                if t.m_matched_D == 0 and t.m_matched_pi == 1:
                    h_match.Fill(3)
                if t.m_matched_D == 1 and t.m_matched_pi == 1:
                    h_match.Fill(4)

def set_histo_style(h, ytitle):
    h.GetXaxis().SetNdivisions(509)
    h.GetYaxis().SetNdivisions(504)
    h.SetLineWidth(2)
    h.SetStats(0)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetLabelSize(0.04)
    h.GetXaxis().SetTitleOffset(1.4)
    h.GetXaxis().SetLabelOffset(0.01)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetLabelSize(0.04)
    h.GetYaxis().SetTitleOffset(1.8)
    h.GetYaxis().SetLabelOffset(0.01)
    h.GetXaxis().CenterTitle()
    h.GetYaxis().SetTitle(ytitle)
    h.GetYaxis().CenterTitle()
    h.GetYaxis().SetRangeUser(0, 22000)
    h.SetLineColor(1)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)

def plot(incMC_path, leg_title, ecms, MODE):
    try:
        f_incMC = TFile(incMC_path)
        t_incMC = f_incMC.Get('save')
        entries_incMC = t_incMC.GetEntries()
        logging.info('inclusive MC(hadrons) entries :'+str(entries_incMC))
    except:
        logging.error(incMC_path + ' is invalid!')
        sys.exit()

    mbc = TCanvas('mbc', 'mbc', 1200, 800)
    set_canvas_style(mbc)
    ytitle = "Events"

    set_histo_style(h_match, ytitle)
    fill(t_incMC, entries_incMC, MODE)
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    h_match.Draw()

    pt = TPaveText(0.55, 0.6, 0.82, 0.8, "BRNDC")
    set_pavetext(pt)
    pt_1 = 'not D && not #pi: ' + str(h_match.GetBinContent(2))
    pt_2 = 'D && not #pi: ' + str(h_match.GetBinContent(3))
    pt_3 = '#pi && not D: ' + str(h_match.GetBinContent(4))
    pt_4 = '#pi && D: ' + str(h_match.GetBinContent(5))
    pt.AddText(pt_1)
    pt.AddText(pt_2)
    pt.AddText(pt_3)
    pt.AddText(pt_4)
    pt.Draw()

    significance = h_match.GetBinContent(5)/math.sqrt(h_match.GetBinContent(2)+h_match.GetBinContent(3)+h_match.GetBinContent(4)+h_match.GetBinContent(5))
    eff = (h_match.GetBinContent(2)+h_match.GetBinContent(3)+h_match.GetBinContent(4)+h_match.GetBinContent(5))/112500000.
    print 'significance: ' + str(significance)
    print 'efficiency: ' + str(eff)

    mbc.SaveAs('./figs/stat_match_'+str(ecms)+'_'+MODE+'.pdf')

if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        MODE = args[0]
    except:
        logging.error('python plot_stat_match.py [MODE]: MODE = raw or cut')
        sys.exit()

    incMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/hadrons/4360/incMC_hadrons_4360_before.root'
    leg_title = '(a)'
    ecms = 4360
    plot(incMC_path, leg_title, ecms, MODE)

    incMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/hadrons/4420/incMC_hadrons_4420_before.root'
    leg_title = '(b)'
    ecms = 4420
    plot(incMC_path, leg_title, ecms, MODE)

    incMC_path = '/besfs/users/$USER/bes/DDPIPI/v0.2/incMC/hadrons/4600/incMC_hadrons_4600_before.root'
    leg_title = '(c)'
    ecms = 4600
    plot(incMC_path, leg_title, ecms, MODE)
