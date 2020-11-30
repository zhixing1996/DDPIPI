#!/usr/bin/env python
"""
Calculate number of common events between D+ tag and D- tag
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-11-25 Thu 09:11]"

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
    common.py

SYNOPSIS
    ./common.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2020
\n''')

def count(ecms, t):
    Dm_dic = {}
    num = 0
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if not t.m_charm == -1: continue
        Dm_dic[ientry] = (t.runNo, t.evtNo)
        if num % 10000 == 0: print('D- tag: executing {0}/{1}...'.format(num, t.GetEntries('m_charm == -1')))
        num += 1

    Dp_dic = {}
    num = 0
    for ientry in xrange(t.GetEntries()):
        t.GetEntry(ientry)
        if not t.m_charm == 1: continue
        Dp_dic[ientry] = (t.runNo, t.evtNo)
        if num % 10000 == 0: print('D+ tag: executing {0}/{1}...'.format(num, t.GetEntries('m_charm == 1')))
        num += 1

    com = {}
    num = 0
    for Dm_k, Dm_v in Dm_dic.items():
        if num % 1000 == 0: print('find common: executing {0}/{1}...'.format(num, len(Dm_dic)))
        if Dm_v in Dp_dic.values():
            com[Dm_k] = Dm_v
        num += 1

    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')

    with open('./txts/common_'+str(ecms)+'.txt', 'w') as f:
        for k, v in com.items():
            f.write(str(k) + ' ' + str(v[0]) + ' ' + str(v[1]) + '\n')

def common(ecms, path):
    try:
        f_data = TFile(path[0])
        t_data = f_data.Get('save')
        entries_data = t_data.GetEntries()
        logging.info('data entries :'+str(entries_data))
    except:
        logging.error(path[0] + ' is invalid!')
        sys.exit()
    count(ecms, t_data)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    path =[]
    path.append('/besfs/users/$USER/bes/DDPIPI/v0.2/data/'+str(ecms)+'/data_'+str(ecms)+'_raw_before.root')
    common(ecms, path)
