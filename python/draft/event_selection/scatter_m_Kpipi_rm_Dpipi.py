#!/usr/bin/env python
"""
Plot scatter plot of M(Kpipi) and RM(Dpipi)
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-12-24 Thu 11:18]"

from ROOT import *
import sys, os
import logging
from array import array
from tools import width, window, position_convert, set_pavetext, set_pub_style, set_prelim_style, format_data_hist, name_axis
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    scatter_m_Kpipi_rm_Dpipi.py

SYNOPSIS
    ./scatter_m_Kpipi_rm_Dpipi.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2020
\n''')

box_cij = [
    [0, 0],  [1, 0],
    [1, -1], [0, -1]
]

def make_box(point0, x_move, y_move):
    box = []
    for cij in box_cij:
        x0, y0 = point0
        c_x, c_y = cij
        x, y = x0 + x_move * c_x, y0 + y_move * c_y
        box.append((x, y))
    box.append(point0)
    return box

def make_matrix(n, m, point0, x_move, x_offset, y_move, y_offset):
    matrix = []
    index_i = range(0, n)
    index_j = list(reversed(range(-m + 1, 1)))
    for j in index_j:
        for i in index_i:
            x0, y0 = point0
            point = (x0 + i * (x_move + x_offset), y0 + j * (y_move + y_offset))
            matrix.append(make_box(point, x_move, y_move))
    return matrix

def fill(t, h):
    for ientry in xrange(int(t.GetEntries())):
        t.GetEntry(ientry)
        h.Fill(t.m_rawm_D, t.m_rrawm_Dpipi)

def plot(path, leg_title, ecms, xmin, xmax, ymin, ymax, bins):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()

    set_pub_style()
    set_prelim_style()
    from ROOT import gStyle
    colors = array('i', 7*[0])
    for i in range(7): colors[i] = 18 - i
    gStyle.SetPalette(7, colors)

    mbc = TCanvas('mbc', 'mbc', 800, 600)
    xtitle = 'M(K^{-}#pi^{+}#pi^{+}) (GeV)/c^{2}'
    ytitle = 'RM(D^{+}#pi_{d}^{+}#pi_{d}^{-}) (GeV)/c^{2}'

    h_data = TH2F('scatter_data', 'scatter plot of M(Kpipi) and Rm(Dpipi)', bins, xmin, xmax, bins, ymin, ymax)
    format_data_hist(h_data)
    name_axis(h_data, xtitle, ytitle)
    fill(t_data, h_data)
    h_data.SetMarkerSize(0.2)
    # h_data.Draw('box')
    h_data.Draw('COLZ')

    x_move = width(ecms)
    y_move = window(ecms)
    x_offset = width(ecms)
    y_offset = window(ecms)
    x0 = 1.86965 - 5/2. * x_move
    y0 = 1.86965 + 5/2. * y_move
    mats = make_matrix(3, 3, (x0, y0), x_move, x_offset, y_move, y_offset)
    VarsManager = locals()
    for i, mat in enumerate(mats):
        x_list = []
        y_list = []
        for point in mat:
            x, y = point
            x_list.append(x)
            y_list.append(y)
        x, y = array('d', x_list), array('d', y_list)
        VarsManager['box_' + str(i)] = TPolyLine(5, x, y)
        if i == 4: color = ROOT.kRed
        else: color = ROOT.kBlue
        VarsManager['box_' + str(i)].SetLineColor(color)
        VarsManager['box_' + str(i)].SetLineWidth(4)
        if i == 1 or i == 3 or i == 5 or i == 7: VarsManager['box_' + str(i)].SetLineStyle(9)
        if i == 0 or i == 2 or i == 6 or i == 8: VarsManager['box_' + str(i)].SetLineStyle(2)
        VarsManager['box_' + str(i)].Draw('same')
        # if i == 0: left, right, bottom, top = position_convert(min(x), xmin, xmax) + 0.0045, position_convert(max(x), xmin, xmax) + 0.025, position_convert(min(y), ymin, ymax) + 0.0045, position_convert(max(y), ymin, ymax) + 0.025
        # elif i == 1 or i == 2: left, right, bottom, top = position_convert(min(x), xmin, xmax), position_convert(max(x), xmin, xmax) + 0.025, position_convert(min(y), ymin, ymax), position_convert(max(y), ymin, ymax) + 0.025
        # elif i == 3: left, right, bottom, top = position_convert(min(x), xmin, xmax) + 0.0045, position_convert(max(x), xmin, xmax), position_convert(min(y), ymin, ymax) + 0.0045, position_convert(max(y), ymin, ymax)
        # elif i == 6: left, right, bottom, top = position_convert(min(x), xmin, xmax) + 0.0045, position_convert(max(x), xmin, xmax) - 0.025, position_convert(min(y), ymin, ymax) + 0.0045, position_convert(max(y), ymin, ymax) - 0.025
        # elif i == 6 or i == 7 or i == 8: left, right, bottom, top = position_convert(min(x), xmin, xmax), position_convert(max(x), xmin, xmax) - 0.025, position_convert(min(y), ymin, ymax), position_convert(max(y), ymin, ymax) - 0.025
        # else: left, right, bottom, top = position_convert(min(x), xmin, xmax), position_convert(max(x), xmin, xmax), position_convert(min(y), ymin, ymax), position_convert(max(y), ymin, ymax)
        # VarsManager['pt_' + str(i)] = TPaveText(left, bottom, right, top, "BRNDC")
        # set_pavetext(VarsManager['pt_' + str(i)])
        # VarsManager['pt_' + str(i)].SetTextSize(0.06)
        # VarsManager['pt_' + str(i)].Draw()
        # if i == 0: VarsManager['pt_' + str(i)].AddText('(-1, 1)')
        # if i == 1: VarsManager['pt_' + str(i)].AddText(' (0, 1) ')
        # if i == 2: VarsManager['pt_' + str(i)].AddText(' (1, 1) ')
        # if i == 3: VarsManager['pt_' + str(i)].AddText('(-1, 0)')
        # if i == 4: VarsManager['pt_' + str(i)].AddText(' (0, 0) ')
        # if i == 5: VarsManager['pt_' + str(i)].AddText(' (1, 0) ')
        # if i == 6: VarsManager['pt_' + str(i)].AddText('(-1, -1)')
        # if i == 7: VarsManager['pt_' + str(i)].AddText(' (0, -1)')
        # if i == 8: VarsManager['pt_' + str(i)].AddText(' (1, -1)')
        # VarsManager['pt_' + str(i)].SetTextColor(color)

    pt = TPaveText(0.75, 0.77, 0.85, 0.87, "BRNDC")
    set_pavetext(pt)
    pt.Draw()
    pt.AddText(leg_title)

    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    mbc.SaveAs('./figs/scatter_m_Kpipi_rm_Dpipi_'+str(ecms)+'.pdf')

    raw_input('Press <Enter> to end...')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw.root')
    leg_title = str(ecms) + ' MeV'
    if ecms == 4230: leg_title = '(a)'
    if ecms == 4420: leg_title = '(b)'
    if ecms == 4680: leg_title = '(c)'
    if ecms == 4230:
        xmin = 1.81
        xmax = 1.93
        ymin = 1.83
        ymax = 1.91
    if ecms == 4420:
        xmin = 1.81
        xmax = 1.93
        ymin = 1.81
        ymax = 1.93
    if ecms == 4680:
        xmin = 1.81
        xmax = 1.93
        ymin = 1.81
        ymax = 1.93
    bins = 80
    plot(path, leg_title, ecms, xmin, xmax, ymin, ymax, bins)
