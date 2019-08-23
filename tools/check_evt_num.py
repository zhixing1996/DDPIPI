#!/usr/bin/env python
"""
Check events numbers
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-23 Fri 14:20]"

from array import array
import ROOT
from ROOT import TCanvas, gStyle, TLorentzVector, TTree
from ROOT import TFile, TH1F, TLegend, TArrow, TChain
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    check_evt_num.py

SYNOPSIS
    ./check_evt_num.py [file_path] [file_path]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    August 2019
\n''')

def check(t1, t2):
    f1_name = 'myroot.txt'
    f2_name = 'zhengyiroot.txt'
    f3_name = 'diff.txt'
    f1_out = open(f1_name, 'w')
    f2_out = open(f2_name, 'w')
    f3_out = open(f3_name, 'w')
    my_list = []
    other_list = []
    print '--> Begin of checking...'
    for i in range(t1.GetEntries()):
        t1.GetEntry(i)
        # EVT1 = 'runNo: ' + str(t1.m_runNo) + ' evtNo: ' + str(t1.m_evtNo) + '\n'
        EVT1 = str(t1.m_runNo) + '/' + str(t1.m_evtNo) + '\n'
        my_list.append(EVT1)
        f1_out.write(EVT1)
    f1_out.close()
    for i in range(t2.GetEntries()):
        t2.GetEntry(i)
        # EVT2 = 'runNo: ' + str(t2.run) + ' evtNo: ' + str(t2.evt) + '\n'
        EVT2 = str(t2.run) + '/' + str(t2.evt) + '\n'
        other_list.append(EVT2)
        f2_out.write(EVT2)
    f2_out.close()
    num = 0
    for list2 in other_list:
        if list2 not in my_list:
            f3_out.write(list2)
            num += 1
    f3_out.close()
    print 'Number of events in my rootfile: ' + str(len(my_list))
    print 'Number of events in other\'s rootfile: ' + str(len(other_list))
    print 'Number difference: ' + str(len(other_list)-len(my_list))
    print 'Number of recorded different events: ' + str(num)
    print '--> End of checking...'

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()

    file_path1 = args[0]
    file_path2 = args[1]

    f_1 = TFile(file_path1)
    f_2 = TFile(file_path2)
    t_1 = f_1.Get('save')
    t_2 = f_2.Get('save')

    check(t_1, t_2)

if __name__ == '__main__':
    main()
