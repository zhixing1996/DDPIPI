#!/usr/bin/env python
"""
Get M(truthall)
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2021-04-25 Sun 04:57]"

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
    get_m_truth.py

SYNOPSIS
    ./get_m_truth.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    April 2021
\n''')

def get_m(path_in, path_out, type):
    file_in = TFile(path_in, 'READ')
    if type == 'truth': t = file_in.Get('truth')
    if type == 'raw_after': t = file_in.Get('save')

    with open(path_out, 'w') as f:
        for ientry in xrange(t.GetEntries()):
            if ientry % 10000 == 0:
                print 'processing ' + str(ientry) + 'th event...'
            t.GetEntry(ientry)
            if type == 'raw_after' and not (t.matched_D == 1 and t.matched_pi == 1):
                continue
            f.write(str(t.m_m_truthall)+'\n')
    print path_out + ' is finished...'

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    mode = args[1]
    type = args[2]

    if not mode == 'DDPIPI':
        path_in = '/besfs5/groups/psip/psipgroup/user/$USER/bes/DDPIPI/v0.2/sigMC/'+mode+'/'+str(ecms)+'/sigMC_'+mode+'_'+str(ecms)+'_'+type+'.root'
        path_out = '/besfs5/groups/psip/psipgroup/user/jingmq/bes/DDPIPI/v0.2/sigMC/'+mode+'/'+str(ecms)+'/sigMC_'+mode+'_'+str(ecms)+'_'+type+'.txt'
    else:
        path_in = '/besfs5/groups/psip/psipgroup/user/$USER/bes/DDPIPI/v0.2/sigMC/'+mode+'/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_'+type+'.root'
        path_out = '/besfs5/groups/psip/psipgroup/user/jingmq/bes/DDPIPI/v0.2/sigMC/'+mode+'/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_'+type+'.txt'
    get_m(path_in, path_out, type)

if __name__ == '__main__':
    main()
