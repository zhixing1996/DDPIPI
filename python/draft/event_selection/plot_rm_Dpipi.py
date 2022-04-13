#!/usr/bin/env python
"""
Plot invariant mass of tagged D without kinematic fit
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-06 Tue 09:14]"

import ROOT
from ROOT import TCanvas, gStyle, TTree, THStack, TArrow
from ROOT import TFile, TH1F, TLegend, TArrow, TPaveText
import sys, os
import logging
from math import *
from tools import width, window, set_pub_style, set_prelim_style, name_axis, format_data_hist, set_arrow, set_pavetext, position_convert, set_legend
from ROOT import gStyle, gROOT
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    plot_m_Kpipi.py

SYNOPSIS
    ./plot_m_Kpipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def rm_Dpipi_fill(t, h, window_low, window_up):
    for ientry in xrange(int(t.GetEntries())):
        t.GetEntry(ientry)
        if fabs(t.m_rawm_D - 1.86965) < width(ecms)/2.:
            h.Fill(t.m_rm_Dpipi)

def plot(data_path, pt_title, ecms, xmin, xmax, xbins, mode):
    try:
        f_data = TFile(data_path)
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    set_pub_style()
    set_prelim_style()

    window_low = 1.86965 - window(ecms)/2.
    window_up = 1.86965 + window(ecms)/2.
    window_side_low_up = window_low - (window_up - window_low)
    window_side_low_low = window_side_low_up - (window_up - window_low)
    window_side_up_low = window_up + (window_up - window_low)
    window_side_up_up = window_side_up_low + (window_up - window_low)

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    content = (xmax - xmin)/xbins * 1000
    ytitle = 'Events/%.1f MeV/c^{2}'%content
    xtitle = 'RM(D^{+}#pi_{d}^{+}#pi_{d}^{-}) (GeV/c^{2})'
    h_data = TH1F('data', 'data', xbins, xmin, float(xmax))
    
    format_data_hist(h_data)
    if ecms == 4420 or ecms == 4680:
        h_data.GetYaxis().SetTitleOffset(1.15)
    h_data.GetXaxis().SetTitleOffset(0.99)
    name_axis(h_data, xtitle, ytitle)
    rm_Dpipi_fill(t_data, h_data, window_low, window_up)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    if mode == 'after' and ecms == 4230: h_data.GetYaxis().SetRangeUser(0, 1.2 * h_data.GetMaximum())
    h_data.Draw('E1')

    if ecms == 4420 and mode == 'before': low = 380
    elif ecms == 4420 and mode == 'after': low = 240
    elif ecms == 4230 and mode == 'before': low = 14
    elif ecms == 4230 and mode == 'after': low = 0
    elif ecms == 4680 and mode == 'before': low = 950
    elif ecms == 4680 and mode == 'after': low = 620
    else: low = 0
    top = h_data.GetMaximum()
    if ecms == 4680: top = top/0.88

    arrow1 = TArrow(window_low, low, window_low, 0.8 * top, 0.02, '<-')
    set_arrow(arrow1, ROOT.kRed)
    arrow1.SetLineStyle(2)
    arrow1.Draw()

    arrow2 = TArrow(window_up, low, window_up, 0.8 * top, 0.02, '<-')
    set_arrow(arrow2, ROOT.kRed)
    arrow2.SetLineStyle(2)
    arrow2.Draw()

    arrow3 = TArrow(window_side_low_low, low, window_side_low_low, 0.8 * top, 0.02, '<-')
    set_arrow(arrow3, ROOT.kBlue)
    arrow3.Draw()

    arrow4 = TArrow(window_side_low_up, low, window_side_low_up, 0.8 * top, 0.02, '<-')
    set_arrow(arrow4, ROOT.kBlue)
    arrow4.Draw()

    arrow5 = TArrow(window_side_up_low, low, window_side_up_low, 0.8 * top, 0.02, '<-')
    set_arrow(arrow5, ROOT.kBlue)
    arrow5.Draw()

    arrow6 = TArrow(window_side_up_up, low, window_side_up_up, 0.8 * top, 0.02, '<-')
    set_arrow(arrow6, ROOT.kBlue)
    arrow6.Draw()

    leg = TLegend(position_convert(0.8 * (xmax - xmin) + xmin, xmin, xmax),
                  position_convert(0.8 * (top - low) + low, low, top),
                  position_convert(0.95 * (xmax - xmin) + xmin, xmin, xmax),
                  position_convert((top - low) + low, low, top),
                  'BRNDC')
    set_legend(leg, h_data, 'Data', pt_title)
    leg.Draw()
    
    h_data.Draw('sameE1')
    mbc.SaveAs('./figs/rm_Dpipi_'+str(ecms)+'_'+mode+'.pdf')

    raw_input('Enter anything to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = int(args[0])
    mode = args[1]

    if mode == 'before': data_path = '/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw.root'
    if mode == 'after': data_path = '/besfs5/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw_after.root'
    if ecms == 4230: pt_title = '(a)'
    elif ecms == 4420: pt_title = '(b)'
    elif ecms == 4680: pt_title = '(c)'
    else: pt_title = str(ecms) + ' MeV'
    xmin = 1.82
    xmax = 1.92
    xbins = int((xmax - xmin)/0.002)
    plot(data_path, pt_title, ecms, xmin, xmax, xbins, mode)
