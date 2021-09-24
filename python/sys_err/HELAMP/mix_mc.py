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
    ./mix_mc.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    March 2020
\n''')

def shape_MC_raw(ecms, path_in, path_out, xmin, xmax, xbins):
    file_in = TFile(path_in, 'READ')
    t = file_in.Get('save')
    file_out = TFile(path_out, 'RECREATE')

    # MC information
    h_name = 'h_hist'
    h_hist = TH1F(h_name, '', xbins, xmin, xmax)
    for ientry in xrange(t.GetEntries()):
        if ientry % 10000 == 0:
            print 'processing ' + str(ientry) + 'th event...'
        t.GetEntry(ientry)
        if not (t.matched_D == 1 and t.matched_pi == 1):
            continue
        h_hist.Fill(t.m_rm_Dpipi)
    print 'filling h_hist histogram of ' + path_out + '...'

    file_out.cd()
    h_hist.Write()
    file_out.Close()

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    mode = args[1]

    xmin, xmax, xbins = 1.75, 1.95, 100 # RM(Dpipi) fit range

    path_in = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/'+mode+'/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_raw_after.root'
    path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/HELAMP/shape_'+mode+'_'+str(ecms)+'_signal.root'
    shape_MC_raw(ecms, path_in, path_out, xmin, xmax, xbins)

if __name__ == '__main__':
    main()
