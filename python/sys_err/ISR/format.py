#!/usr/bin/env python
"""
Format systematic uncertainty at each energy point
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-20 Fri 21:03]"

import ROOT
from ROOT import TCanvas, gStyle
from ROOT import TFile, TH1F, TLegend, TPaveText
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    format_diff.py

SYNOPSIS
    ./format_diff.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def format(mode, variable):
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    file_path = '/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/' + mode + '/rand/'
    if not mode == 'D1_2420': ecms = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    if mode == 'D1_2420': ecms = [4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    for ecm in ecms:
        path_diff = '/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/'+mode+'_'+variable+'_'+str(ecm)+'.txt'
        f_diff = open(path_diff, 'w')

        file_num = len(os.listdir(file_path))
        for i in range(file_num):
            f = open(file_path+'/wisr_weff_'+str(mode)+'_'+str(i)+'.txt')
            for line in f.readlines():
                fargs = map(float, line.strip().split())
                if int(fargs[0]) == ecm:
                    if variable == 'isr': diff = fargs[1]
                    if variable == 'eff': diff = fargs[2]
                    if variable == 'isr_eff': diff = fargs[3]
                    f_diff.write(str(diff) + '\n')
        f_diff.close()
   
def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    mode = args[0]
    variable = args[1]
    
    format(mode, variable)

if __name__ == '__main__':
    main()
