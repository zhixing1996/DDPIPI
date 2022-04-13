#!/usr/bin/env python
"""
Common tools 
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-13 Tue 15:05]" 

import sys 
import os, errno
import shutil
import ROOT 

# ---------------------------------------------
# Function 
# ---------------------------------------------

# width for M(Kpipi)
def width(ecms):
    WIDTH = 999.
    if int(ecms) < 4300:
        WIDTH = 0.011*2
    elif int(ecms) >= 4300 and int(ecms) < 4500:
        WIDTH = 0.011*2
    if int(ecms) >= 4500:
        WIDTH = 0.011*2
    return WIDTH

# signal window for RM(Dpipi)
def window(ecms):
    WINDOW = 999.
    if int(ecms) < 4300:
        WINDOW = 0.006*2
    elif int(ecms) >= 4300 and int(ecms) < 4500:
        WINDOW = 0.009*2
    if int(ecms) >= 4500:
        WINDOW = 0.009*2
    return WINDOW

def format_data_hist(hist):
    hist.SetStats(0)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(1)
    hist.SetLineWidth(2)
    hist.SetLineColor(1)

    hist.GetXaxis().SetNdivisions(509)
    hist.GetYaxis().SetNdivisions(504)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetXaxis().SetTitleSize(0.07)
    hist.GetXaxis().SetTitleOffset(1.04)
    hist.GetXaxis().SetLabelOffset(0.01)
    hist.GetXaxis().SetLabelSize(0.07)
    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetTitleSize(0.07)
    hist.GetYaxis().SetTitleOffset(1.055)
    hist.GetYaxis().SetLabelOffset(0.01)
    hist.GetYaxis().SetLabelSize(0.07)

def format_data_graph(graph):
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1)
    graph.SetLineWidth(2)

def name_axis(hist_graph, xname = '', yname = ''):
    if xname:
        hist_graph.GetXaxis().SetTitle(xname)
        hist_graph.GetXaxis().CenterTitle()
    if yname:
        hist_graph.GetYaxis().SetTitle(yname)
        hist_graph.GetYaxis().CenterTitle()

def format_mc_hist(h_mc, color):
    h_mc.SetLineColor(color)
    h_mc.SetFillColor(color)
    h_mc.SetLineWidth(2)
    h_mc.SetFillStyle(3001)

def set_pub_style():
    from ROOT import gStyle
    # No Canvas Border
    gStyle.SetCanvasBorderMode(0)
    gStyle.SetCanvasBorderSize(0)
    # White BG
    gStyle.SetCanvasColor(10)
    # Format for axes
    gStyle.SetLabelFont(42, 'xyz')
    gStyle.SetLabelSize(0.05, 'xyz')
    gStyle.SetLabelOffset(0.01, 'xyz')
    # gStyle->SetNdivisions(510, 'xyz')
    gStyle.SetTitleFont(42, 'xyz')
    gStyle.SetTitleColor(1, 'xyz')
    gStyle.SetTitleSize(0.06, 'xyz')
    gStyle.SetTitleOffset(1.25, 'xyz')
    # No pad borders
    gStyle.SetPadBorderMode(0)
    gStyle.SetPadBorderSize(0)
    # White BG
    gStyle.SetPadColor(10)
    # Margins for labels etc.
    gStyle.SetPadLeftMargin(0.155)
    gStyle.SetPadBottomMargin(0.155)
    gStyle.SetPadRightMargin(0.15)
    gStyle.SetPadTopMargin(0.1)
    # No error bars in x direction
    gStyle.SetErrorX(0)
    # Format legend
    gStyle.SetLegendBorderSize(0)

def set_prelim_style():
    from ROOT import gStyle
    gStyle.SetOptDate(0)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetOptTitle(0)

def set_meeting_style():
    from ROOT import gStyle
    gStyle.SetOptDate(0)
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(1111)
    gStyle.SetStatBorderSize(1)
    gStyle.SetStatColor(10)
    gStyle.SetStatFont(42)
    gStyle.SetStatFontSize(0.03)
    gStyle.SetOptFit(1111)

def set_arrow(arr, color):
    arr.SetLineWidth(4)
    arr.SetLineColor(color)
    arr.SetFillColor(color)
    arr.SetLineStyle(6)

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.07)

def position_convert(x, xmin, xmax):
    pos = 0.15 + 0.7 * (x - xmin) / (xmax - xmin)
    return pos

def set_legend(legend, h, name, title):
    legend.SetHeader(title)
    legend.AddEntry(h, name)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.07)
