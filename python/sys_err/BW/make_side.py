#!/usr/bin/env python
"""
Mixing three MC samples
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-03-04 Wed 18:22]"

from array import array
import sys, os
import logging
from math import *
from tools import *
from ROOT import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    mix_mc.py

SYNOPSIS
    ./make_side.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    March 2020
\n''')

def shape_side(ecms, path_in, path_out):
    try:
        f_side1 = TFile(path_in[0])
        t_side1 = f_side1.Get('save')
        entries_side1 = t_side1.GetEntries()
        logging.info('data(side1) entries :'+str(entries_side1))
    except:
        logging.error(path_in[0] + ' is invalid!')
        sys.exit()
    try:
        f_side2 = TFile(path_in[1])
        t_side2 = f_side2.Get('save')
        entries_side2 = t_side2.GetEntries()
        logging.info('data(side2) entries :'+str(entries_side2))
    except:
        logging.error(path_in[1] + ' is invalid!')
        sys.exit()
    try:
        f_side3 = TFile(path_in[2])
        t_side3 = f_side3.Get('save')
        entries_side3 = t_side3.GetEntries()
        logging.info('data(side3) entries :'+str(entries_side3))
    except:
        logging.error(path_in[2] + ' is invalid!')
        sys.exit()
    try:
        f_side4 = TFile(path_in[3])
        t_side4 = f_side4.Get('save')
        entries_side4 = t_side4.GetEntries()
        logging.info('data(side4) entries :'+str(entries_side4))
    except:
        logging.error(path_in[3] + ' is invalid!')
        sys.exit()

    t_side_list = [t_side1, t_side2, t_side3, t_side4]
    file_out = TFile(path_out, 'RECREATE')

    xmin_rm_pipi, xmax_rm_pipi = param_rm_pipi(ecms)
    if ecms < 4470: xbins_rm_pipi = int((xmax_rm_pipi - xmin_rm_pipi)/0.005)
    if ecms >= 4470: xbins_rm_pipi = int((xmax_rm_pipi - xmin_rm_pipi)/0.01)
    h_side1_rm_pipi = TH1F('h_side1_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
    h_side2_rm_pipi = TH1F('h_side2_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
    h_side3_rm_pipi = TH1F('h_side3_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
    h_side4_rm_pipi = TH1F('h_side4_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
    h_side_list = [h_side1_rm_pipi, h_side2_rm_pipi, h_side3_rm_pipi, h_side4_rm_pipi]
    for t_side, h_side in zip(t_side_list, h_side_list):
        for ientry in xrange(t_side.GetEntries()):
            t_side.GetEntry(ientry)
            h_side.Fill(t_side.m_rm_pipi)
    h_side_rm_pipi = TH1F('h_side_rm_pipi', '', xbins_rm_pipi, xmin_rm_pipi, xmax_rm_pipi)
    h_side_rm_pipi.Add(h_side1_rm_pipi)
    h_side_rm_pipi.Add(h_side2_rm_pipi)
    h_side_rm_pipi.Scale(0.5)
    h_side3_rm_pipi.Add(h_side4_rm_pipi)
    h_side3_rm_pipi.Scale(0.25)
    h_side_rm_pipi.Add(h_side3_rm_pipi, -1)

    xmin_rm_D, xmax_rm_D, temp = param_rm_D(ecms)
    if ecms < 4470: xbins_rm_D = int((xmax_rm_D - xmin_rm_D)/0.005)
    if ecms >= 4470: xbins_rm_D = int((xmax_rm_D - xmin_rm_D)/0.01)
    h_side1_rm_D = TH1F('h_side1_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)
    h_side2_rm_D = TH1F('h_side2_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)
    h_side3_rm_D = TH1F('h_side3_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)
    h_side4_rm_D = TH1F('h_side4_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)
    h_side_list = [h_side1_rm_D, h_side2_rm_D, h_side3_rm_D, h_side4_rm_D]
    for t_side, h_side in zip(t_side_list, h_side_list):
        for ientry in xrange(t_side.GetEntries()):
            t_side.GetEntry(ientry)
            h_side.Fill(t_side.m_rm_D)
    h_side_rm_D = TH1F('h_side_rm_D', '', xbins_rm_D, xmin_rm_D, xmax_rm_D)
    h_side_rm_D.Add(h_side1_rm_D)
    h_side_rm_D.Add(h_side2_rm_D)
    h_side_rm_D.Scale(0.5)
    h_side3_rm_D.Add(h_side4_rm_D)
    h_side3_rm_D.Scale(0.25)
    h_side_rm_D.Add(h_side3_rm_D, -1)

    xmin_rm_Dmiss, xmax_rm_Dmiss, temp = param_rm_D(ecms)
    if ecms < 4470: xbins_rm_Dmiss = int((xmax_rm_Dmiss - xmin_rm_Dmiss)/0.005)
    if ecms >= 4470: xbins_rm_Dmiss = int((xmax_rm_Dmiss - xmin_rm_Dmiss)/0.01)
    h_side1_rm_Dmiss = TH1F('h_side1_rm_Dmiss', '', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
    h_side2_rm_Dmiss = TH1F('h_side2_rm_Dmiss', '', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
    h_side3_rm_Dmiss = TH1F('h_side3_rm_Dmiss', '', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
    h_side4_rm_Dmiss = TH1F('h_side4_rm_Dmiss', '', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
    h_side_list = [h_side1_rm_Dmiss, h_side2_rm_Dmiss, h_side3_rm_Dmiss, h_side4_rm_Dmiss]
    for t_side, h_side in zip(t_side_list, h_side_list):
        for ientry in xrange(t_side.GetEntries()):
            t_side.GetEntry(ientry)
            h_side.Fill(t_side.m_rm_Dmiss)
    h_side_rm_Dmiss = TH1F('h_side_rm_Dmiss', '', xbins_rm_Dmiss, xmin_rm_Dmiss, xmax_rm_Dmiss)
    h_side_rm_Dmiss.Add(h_side1_rm_Dmiss)
    h_side_rm_Dmiss.Add(h_side2_rm_Dmiss)
    h_side_rm_Dmiss.Scale(0.5)
    h_side3_rm_Dmiss.Add(h_side4_rm_Dmiss)
    h_side3_rm_Dmiss.Scale(0.25)
    h_side_rm_Dmiss.Add(h_side3_rm_Dmiss, -1)

    print 'filling h_hist histogram of ' + path_out + '...'

    file_out.cd()
    h_side_rm_pipi.Write()
    h_side_rm_D.Write()
    h_side_rm_Dmiss.Write()
    file_out.Close()

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    ecms = int(args[0])

    path_in = []
    path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side1_after.root')
    path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side2_after.root')
    path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side3_after.root')
    path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/data/' + str(ecms) + '/data_' + str(ecms) + '_side4_after.root')
    path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/BW/shape_side_'+str(ecms)+'.root'
    shape_side(ecms, path_in, path_out)

if __name__ == '__main__':
    main()
