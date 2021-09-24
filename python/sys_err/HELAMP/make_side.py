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

    xmin, xmax, xbins = -1.1, 1.1, 100
    h_side1 = TH1F('h_side1', '', xbins, xmin, xmax)
    h_side2 = TH1F('h_side2', '', xbins, xmin, xmax)
    h_side3 = TH1F('h_side3', '', xbins, xmin, xmax)
    h_side4 = TH1F('h_side4', '', xbins, xmin, xmax)
    h_side_list = [h_side1, h_side2, h_side3, h_side4]
    for t_side, h_side in zip(t_side_list, h_side_list):
        for ientry in xrange(t_side.GetEntries()):
            t_side.GetEntry(ientry)
            if t_side.m_rm_pipi < 3.79: continue
            if t_side.m_rm_D < 2.4 or t_side.m_rm_D > 2.45: continue
            h_side.Fill(t_side.m_cos_D)
    h_side = TH1F('h_side', '', xbins, xmin, xmax)
    h_side.Add(h_side1)
    h_side.Add(h_side2)
    h_side.Scale(0.5)
    h_side3.Add(h_side4)
    h_side3.Scale(0.25)
    h_side.Add(h_side3, -1)

    print 'filling h_hist histogram of ' + path_out + '...'

    file_out.cd()
    h_side.Write()
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
    path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/HELAMP/shape_side_'+str(ecms)+'.root'
    shape_side(ecms, path_in, path_out)

if __name__ == '__main__':
    main()
