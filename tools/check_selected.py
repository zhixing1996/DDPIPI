#!/usr/bin/env python
"""
Select events using cuts
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-21 Wed 14:41]"

from array import array
# import numpy as np
import ROOT
from ROOT import TCanvas, gStyle, TLorentzVector, TTree
from ROOT import TFile, TH1F, TLegend, TArrow, TChain
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    sel_events.py

SYNOPSIS
    ./sel_events.py [infile_path] [outfile_path] [Ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    August 2019
\n''')

def check(t1, t2, t):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_mode = array('i', [0])
    m_charm = array('i', [0])
    m_rawm_D = array('d', [999.])
    m_rm_D = array('d', [999.])
    # m_rm_pipi = array('d', [999.])
    m_m_Dpi = array('d', [999.])
    m_m_Dpipi = array('d', [999.])
    m_rm_Dpipi = array('d', [999.])
    m_chi2_vf = array('d', [999.])
    m_chi2_kf = array('d', [999.])

    t.Branch('runNo', m_runNo, 'm_runNo/I')
    t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
    t.Branch('mode', m_mode, 'm_mode/I')
    t.Branch('charm', m_charm, 'm_charm/I')
    t.Branch('rawm_D', m_rawm_D, 'm_rawm_D/D')
    t.Branch('rm_D', m_rm_D, 'm_rm_D/D')
    # t.Branch('rm_pipi', m_rm_pipi, 'm_rm_pipi/D')
    t.Branch('m_Dpi', m_m_Dpi, 'm_m_Dpi/D')
    t.Branch('m_Dpipi', m_m_Dpipi, 'm_m_Dpipi/D')
    t.Branch('rm_Dpipi', m_rm_Dpipi, 'm_rm_Dpipi/D')
    t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
    t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')

    my_list = []
    other_list = []
    print '--> Begin of checking...'
    f1_name = 'my.txt'
    f2_name = 'other.txt'
    f3_name = 'diff.txt'
    f1_out = open(f1_name, 'w')
    f2_out = open(f2_name, 'w')
    f3_out = open(f3_name, 'w')
    my_list = []
    other_list = []
    myrun_list = []
    otherrun_list = []
    myevt_list = []
    otherevt_list = []
    print '--> Begin of checking...'
    for i in range(t1.GetEntries()):
        t1.GetEntry(i)
        EVT1 = 'runNo: ' + str(t1.m_runNo) + ' evtNo: ' + str(t1.m_evtNo) + '\n'
        my_list.append([EVT1, i])
        myrun_list.append(t1.m_runNo)
        myevt_list.append(t1.m_evtNo)
        f1_out.write(EVT1)
    f1_out.close()
    for i in range(t2.GetEntries()):
        t2.GetEntry(i)
        EVT2 = 'runNo: ' + str(t2.run) + ' evtNo: ' + str(t2.evt) + '\n'
        other_list.append([EVT2, i])
        otherrun_list.append(t2.run)
        otherevt_list.append(t2.evt)
        f2_out.write(EVT2)
    f2_out.close()
    for [list2, num] in other_list:
        if [list2, num] not in my_list:
            t2.GetEntry(num)
            m_runNo[0] = t2.run                        
            m_evtNo[0] = t2.evt
            m_mode[0] = t2.mode
            m_charm[0] = t2.charm
            m_rawm_D[0] = t2.mD
            m_rm_D[0] = t2.rmD_3
            # m_rm_pipi[0] = t2.rmpipi
            m_m_Dpi[0] = t2.mDpi
            m_m_Dpipi[0] = t2.mDpipi
            m_rm_Dpipi[0] = t2.rmDpipi
            m_chi2_vf[0] = t2.VFchi2
            m_chi2_kf[0] = t2.KFchi2
            t.Fill()
            f3_out.write(list2)
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

    path_1 = args[0]
    path_2 = args[1]
    path_out = args[2]

    f1 = TFile(path_1)
    t1 = f1.Get('save')
    f2 = TFile(path_2)
    t2 = f2.Get('save')

    f_out = TFile(path_out, 'recreate')
    t_out = TTree('save', 'save')

    check(t1, t2, t_out)

    f_out.cd()
    t_out.Write()
    f_out.Close()

if __name__ == '__main__':
    main()
