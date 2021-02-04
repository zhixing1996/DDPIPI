#!/usr/bin/env python
"""
Calculate systematic uncertainty
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-12-13 Sun 10:52]"

import ROOT
from ROOT import *
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0) # quench title
gStyle.SetPadTickX(1) # dicide on boxing on or not of x and y axis  
gStyle.SetPadTickY(1) # dicide on boxing on or not of x and y axis

def usage():
    sys.stdout.write('''
NAME
    cal_diff.py

SYNOPSIS
    ./cal_diff.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2020
\n''')

def count(t):
    num = 0
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if t.nMatch == 1 and not t.pid_misid_proton == 1: num += 1
    return num

def cal(path):
    try:
        f_data = TFile(path[0])
        f_KsKpi = TFile(path[1])
        t_data = f_data.Get('vfit')
        t_KsKpi = f_KsKpi.Get('vfit')
        entries_data = t_data.GetEntries('nMatch==1')
        entries_KsKpi = t_KsKpi.GetEntries('nMatch==1')
        logging.info('data entries :'+str(entries_data))
        logging.info('KsKpi entries :'+str(entries_KsKpi))
    except:
        logging.error('File paths are invalid!')
        sys.exit()

    N_data = count(t_data)
    N_KsKpi = count(t_KsKpi)
    
    eff_data = float(N_data)/entries_data
    eff_KsKpi = float(N_KsKpi)/entries_KsKpi
    eff_data_err = sqrt(eff_data*(1 - eff_data)/entries_data)
    eff_KsKpi_err = sqrt(eff_KsKpi*(1 - eff_KsKpi)/entries_KsKpi)
    f = eff_data/eff_KsKpi
    f_err = sqrt(f**2*(eff_data_err**2/eff_data**2 + eff_KsKpi_err**2/eff_KsKpi**2))
    print 'factor K-/->p: ' + str(f) + ', Delta_f/sigma_f: ' + str(abs(1 - f)/f_err)
    sys_err = f_err

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    
    with open('./txts/f_K_p.txt', 'w') as f_out:
        f_out.write(str(f) + '\n')

    ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700]
    with open('./txts/sys_err_K_p.txt', 'w') as f_out:
        for ecm in ecms:
            out = str(ecm/1000.) + '\t' + str(round(sys_err*100, 2)) + '\n'
            f_out.write(out)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path = []
    path.append('/besfs5/groups/cal/dedx/$USER/bes/KsKpi/run/KsKpi/anaroot/data/' + str(ecms) + '/data_' + str(ecms) + '_signal.root')
    path.append('/besfs5/groups/cal/dedx/jingmq/bes/KsKpi/run/KsKpi/anaroot/mc/KsKpi/' + str(ecms) + '/mc_KsKpi_' + str(ecms) + '_signal.root')
    cal(path)
