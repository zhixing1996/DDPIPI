#!/usr/bin/env python
"""
Convert txt file toy ROOT file
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-08-12 Wed 16:47]"

import sys, os
import logging
from math import *
from array import array
from ROOT import TFile, TTree
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    convert_root.py

SYNOPSIS
    ./convert_root.py [var]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    August 2020
\n''')

def convert(ecms, save):
    pull = array('d', [999.])
    save.Branch('pull', pull, 'pull/D')
    f_txt = open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/isr_eff_' + str(ecms) + '.txt', 'r')
    for line in f_txt.readlines():
        rs = line.rstrip('\n')
        pull[0] = float(rs)
        save.Fill()
    f_txt.close()

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    if not os.path.exists('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/sys_err/ISR/' + str(ecms) + '/'):
        os.system('mkdir -p /besfs5/users/$USER/bes/DDPIPI/v0.2/ana/sys_err/ISR/' + str(ecms) + '/')
    f_root = TFile('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/sys_err/ISR/' + str(ecms) + '/isr_eff_' + str(ecms) + '.root', 'RECREATE')
    save = TTree('save', 'save')
    convert(ecms, save)
    f_root.cd()
    save.Write()
    f_root.Close()
