#!/usr/bin/env python
"""
Get signal shape of D1(2420) (Breit-Wigner + MCTruth shape), X(3842) (Breit-Wigner)
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-27 Wed 05:40]"

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
    get_shape.py

SYNOPSIS
    ./get_shape.py [ecms] [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def num_sim(m, h_in):
    # when mass = m, find the bin number at this time
    bin = h_in.FindBin(m)
    # return this bin's event number, when find this bin
    return h_in.GetBinContent(bin)

def BW(m, M, G):
    s = pow(m, 2)
    bw = 1/(pow((s-M*M),2) + M*M*G*G)
    return bw

def shape_D1_2420_final(path_signal, path_sideband, path_out):
    f_signal = TFile(path_signal)
    f_sideband = TFile(path_sideband)
    f_out = TFile(path_out, 'RECREATE')
    
    print 'test1'
    for i in xrange(80):
        for j in xrange(20):
            h_name = 'h_' + str(i) + '_' + str(j)
            h_signal = f_signal.Get(h_name)
            h_sideband = f_sideband.Get(h_name)
            h_shape = TH1F(h_name, '', 320, 2.0, 2.8)
            h_shape.Add(h_signal, h_sideband, 1, -0.5)
            h_shape.Write()

def shape_D1_2420(path_in, path_out, ecms, cms, mode):
    file_in = TFile(path_in, 'READ')
    t = file_in.Get('STDDmiss')
    file_out = TFile(path_out, 'RECREATE')

    h_mDstst = TH1F('h_mDstst', 'h_mDstst', 320, 2.0, 2.8)

    # get mass of Dstst MC Truth
    for i in xrange(t.GetEntries()):
        if i % 100000 == 0:
            print 'processing ' + str(i) + 'th event...'
        t.GetEntry(i)
        Dstst = TLorentzVector(0, 0, 0, 0)
        Dstst.SetPxPyPzE(t.p4_Dstst[0], t.p4_Dstst[1], t.p4_Dstst[2], t.p4_Dstst[3])
        mDstst = Dstst.M()
        # get the initial Dstst histogram from MC truth
        h_mDstst.Fill(mDstst)

    h_list = []
    # MC information
    for i in xrange(80):
        for j in xrange(20):
            h_name = 'h_' + str(i) + '_' + str(j)
            h_list.append(TH1F(h_name, '', 320, 2.0, 2.8))
            MASS = 2.4240 + 0.0001*i
            WIDTH = 0.018 + 0.001*j
            for ientry in xrange(t.GetEntries()):
                if ientry % 10000 == 0:
                    print 'processing ' + str(ientry) + 'th event...'
                t.GetEntry(ientry)
                if t.mode != 200:
                    continue
                Dstst = TLorentzVector(0,0,0,0)
                Dstst.SetPxPyPzE(t.p4_Dstst[0], t.p4_Dstst[1], t.p4_Dstst[2], t.p4_Dstst[3])
                mDstst = Dstst.M()
                #  when mass = Dstst_th, get the event number in h_mZ(MCtruth)
                w1 = num_sim(mDstst, h_mDstst)
                # build the relativistic Breit-wigner distribution
                # when Dstst = mass the probability of BW-PDF is maxium
                w2 = BW(mDstst, MASS, WIDTH)
                # define the wight
                if w1 < 0.000001:
                    continue
                wight = w2/w1
                # prepare variables used for cuts
                pD = TLorentzVector(0,0,0,0)
                pD_raw = TLorentzVector(0,0,0,0)
                for m in xrange(t.n_trkD):
                    ptrack = TLorentzVector(0,0,0,0)
                    ptrack_raw = TLorentzVector(0,0,0,0)
                    ptrack.SetPxPyPzE(t.p4_Dtrk[m*4+0], t.p4_Dtrk[m*4+1], t.p4_Dtrk[m*4+2], t.p4_Dtrk[m*4+3])
                    ptrack_raw.SetPxPyPzE(t.rawp4_Dtrk[m*6+0], t.rawp4_Dtrk[m*6+1], t.rawp4_Dtrk[m*6+2], t.rawp4_Dtrk[m*6+3])
                    pD += ptrack
                    pD_raw += ptrack_raw
                for m in xrange(t.n_shwD):
                    print t.n_shwD
                    pshower = TLorentzVector(0,0,0,0)
                    pshower_raw = TLorentzVector(0,0,0,0)
                    pshower.SetPxPyPzE(t.p4_Dshw[m*4+0], t.p4_Dshw[m*4+1], t.p4_Dshw[m*4+2], t.p4_Dshw[m*4+3])
                    pshower_raw.SetPxPyPzE(t.rawp4_Dshw[m*4+0], t.rawp4_Dshw[m*4+1], t.rawp4_Dshw[m*4+2], t.rawp4_Dshw[m*4+3])
                    pD += pshower
                    pD_raw += pshower_raw
                pDmiss = TLorentzVector(0, 0, 0, 0)
                pPip = TLorentzVector(0, 0, 0, 0)
                pPim = TLorentzVector(0, 0, 0, 0)
                pPi0 = TLorentzVector(0, 0, 0, 0)
                pDmiss.SetPxPyPzE(t.p4_Dmiss[0], t.p4_Dmiss[1], t.p4_Dmiss[2], t.p4_Dmiss[3])
                pPip.SetPxPyPzE(t.p4_piplus[0], t.p4_piplus[1], t.p4_piplus[2], t.p4_piplus[3])
                pPim.SetPxPyPzE(t.p4_piminus[0], t.p4_piminus[1], t.p4_piminus[2], t.p4_piminus[3])
                pPi0.SetPxPyPzE(t.p4_pi0_save[0], t.p4_pi0_save[1], t.p4_pi0_save[2], t.p4_pi0_save[3])
                rm_D = (cms-pD).M()
                rm_Dmiss = (cms-pD).M()
                rawm_D = pD_raw.M()
                rm_Dpipi = t.rm_Dpipi
                CHI2_KF = t.chi2_kf
                m_pipi = (pPip + pPim).M()
                ctau_svf = t.ctau_svf
                m_Dpi0 = pD.M()
                if pPi0.M() > 0:
                    m_Dpi0 = (pD + pPi0).M()
                # apply cuts
                signal_low = 1.86965 - width(ecms)/2.
                signal_up = 1.86965 + width(ecms)/2.
                window_low = 1.86965 - window(ecms)/2.
                window_up = 1.86965 + window(ecms)/2.
                windowlow_up = window_low - (window_up - window_low)
                windowlow_low = windowlow_up - (window_up - window_low)
                windowup_low = window_up + (window_up - window_low)
                windowup_up = windowup_low + (window_up - window_low)
                if not (rawm_D > signal_low and rawm_D < signal_up):
                    continue
                if mode == 'D1_2420_signal':
                    if not (rm_Dpipi > window_low and rm_Dpipi < window_up):
                        continue
                if mode == 'D1_2420_sideband':
                    if not ((rm_Dpipi > windowlow_low and rm_Dpipi < windowlow_up) or (rm_Dpipi > windowup_low and rm_Dpipi < windowup_up)):
                        continue
                if not (CHI2_KF < chi2_kf(ecms)):
                    continue
                if (m_pipi > 0.491036 and m_pipi < 0.503471 and ctau_svf > 0.5):
                    continue
                if (m_Dpi0 > 2.0082 and m_Dpi0 < 2.01269):
                    continue
                h_list[i+j].Fill(rm_D, wight)
                h_list[i+j].Fill(rm_Dmiss, wight)
            print 'filling ' + str(i + j) + 'th histogram of D1(2420)...'
            h_list[i+j].Write()

def shape_X3842(path_out):
    xbins = 2000
    m_min = 3.8
    m_max = 3.9
    file_out = TFile(path_out, 'RECREATE')
    h_mX3842 = TH1F('h_mX3842', 'h_mX3842', xbins, m_min, m_max)
    MASS = 3.84271
    WIDTH = 0.00279
    for i in xrange(xbins):
        m = m_min + i*(m_max - m_min)/xbins
        XS = BW(m, MASS, WIDTH)
        h_mX3842.Fill(m, XS)
    h_mX3842.Write()

def main():
    args = sys.argv[1:]
    if len(args)<2:
        return usage()
    ecms = int(args[0])
    mode = args[1]

    if ecms == 4360:
        cms = TLorentzVector(0.011*4.358, 0, 0, 4.358)
        if mode == 'X_3842':
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_X3842.root'
            shape_X3842(path_out)
        if mode == 'D1_2420_signal':
            path_in = '/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rootfile/sigMC_D1_2420_4360.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4360_signal.root'
            shape_D1_2420(path_in, path_out, ecms, cms, mode)
        if mode == 'D1_2420_sideband':
            path_in = '/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rootfile/sigMC_D1_2420_4360.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4360_sideband.root'
            shape_D1_2420(path_in, path_out, ecms, cms, mode)
        if mode == 'D1_2420':
            path_signal = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4360_signal.root'
            path_sideband = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4360_sideband.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4360.root'
            shape_D1_2420_final(path_signal, path_sideband, path_out)

    if ecms == 4420:
        cms = TLorentzVector(0.011*4.416, 0, 0, 4.416)
        if mode == 'X_3842':
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_X3842.root'
            shape_X3842(path_out)
        if mode == 'D1_2420_signal':
            path_in = '/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rootfile/sigMC_D1_2420_4420.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4420_signal.root'
            shape_D1_2420(path_in, path_out, ecms, cms, mode)
        if mode == 'D1_2420_sideband':
            path_in = '/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rootfile/sigMC_D1_2420_4420.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4420_sideband.root'
            shape_D1_2420(path_in, path_out, ecms, cms, mode)
        if mode == 'D1_2420':
            path_signal = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4420_signal.root'
            path_sideband = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4420_sideband.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4420.root'
            shape_D1_2420_final(path_signal, path_sideband, path_out)

    if ecms == 4600:
        cms = TLorentzVector(0.011*4.600, 0, 0, 4.600)
        if mode == 'X_3842':
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_X3842.root'
            shape_X3842(path_out)
        if mode == 'D1_2420_signal':
            path_in = '/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rootfile/sigMC_D1_2420_4600.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4600_signal.root'
            shape_D1_2420(path_in, path_out, ecms, cms, mode)
        if mode == 'D1_2420_sideband':
            path_in = '/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rootfile/sigMC_D1_2420_4600.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4600_sideband.root'
            shape_D1_2420(path_in, path_out, ecms, cms, mode)
        if mode == 'D1_2420':
            path_signal = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4600_signal.root'
            path_sideband = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4600_sideband.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_4600.root'
            shape_D1_2420_final(path_signal, path_sideband, path_out)

if __name__ == '__main__':
    main()
