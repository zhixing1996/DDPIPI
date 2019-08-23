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

def check(t_in, t, t_test, file):
    m_runNo = array('i', [0])
    m_evtNo = array('i', [0])
    m_mode = array('i', [0])
    m_chi2_vf = array('d', [999.])
    m_chi2_kf = array('d', [999.])

    t.Branch('runNo', m_runNo, 'm_runNo/I')
    t.Branch('evtNo', m_evtNo, 'm_evtNo/I')
    t.Branch('mode', m_mode, 'm_mode/I')
    t.Branch('chi2_vf', m_chi2_vf, 'm_chi2_vf/D')
    t.Branch('chi2_kf', m_chi2_kf, 'm_chi2_kf/D')

    print '--> Begin of checking...'
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        rs = line.rstrip('\n')
        nentries = t_in.GetEntries()
        for i in range(nentries):
            t_in.GetEntry(i)
            if t_in.runNo == int(rs.split('/')[0]) and t_in.evtNo == int(rs.split('/')[1]):
                m_runNo[0] = t_in.runNo
                m_evtNo[0] = t_in.evtNo
                m_mode[0] = t_in.mode
                m_chi2_vf[0] = t_in.chi2_vf
                m_chi2_kf[0] = t_in.chi2_kf
                t_test.GetEntry(i)
                print 'RunNo: '+str(t_in.runNo)+', '+'EvtNo: ' + str(t_in.evtNo)
                print '*******************************'
                for iTrk in range(t_test.n_othertrks):
                    print 'rund: ' + str(iTrk)
                    print t_test.rawp4_otherMdcKaltrk[iTrk*6+4]
                    print t_test.rawp4_otherMdcKaltrk[iTrk*6+5]
                print '*******************************'
                t.Fill()
    print '--> End of checking...'

def main():
    args = sys.argv[1:]
    if len(args)<3:
        return usage()

    diff = args[0]
    root_in = args[1]
    root_out = args[2]

    f_in = TFile(root_in)
    t_in = f_in.Get('STD')
    t_test = f_in.Get('otherTrk')

    f_out = TFile(root_out, 'recreate')
    t_out = TTree('save', 'save')

    check(t_in, t_out, t_test, diff)

    f_out.cd()
    t_out.Write()
    f_out.Close()

if __name__ == '__main__':
    main()
