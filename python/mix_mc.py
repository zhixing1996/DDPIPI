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
    ./mix_mc.py [ecms] [mode] [process] [patch]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    March 2020
\n''')

def mix(path_in, path_out, ecms, xmin, xmax, xbins, patch):
    factor_path = './txts/fit_rm_D_' + str(ecms) + '_read_' + patch + '.txt'
    f_factor = open(factor_path, 'r')
    lines_factor = f_factor.readlines()
    omega = array('d', 3*[999.])
    for line_factor in lines_factor:
        rs_factor = line_factor.rstrip('\n')
        rs_factor = filter(None, rs_factor.split(' '))
        omega[0] = float(rs_factor[1])
        omega[1] = float(rs_factor[2])
        omega[2] = float(rs_factor[3])

    print '--> Begin to process file: ' + path_out
    f_out = TFile(path_out, 'RECREATE')
    h_shape = TH1F('h_hist', '', xbins, xmin, xmax)
    n = 0
    if ecms <= 4311:
        n += 1
    for i in xrange(len(path_in)):
        try:
            f_in = TFile(path_in[i])
            h_hist = f_in.Get('h_hist')
        except:
            logging.error(path_in[i] + ' is invalid!')
            sys.exit()

        h_hist.Scale(omega[n]) 
        h_shape.Add(h_shape, h_hist)
        n += 1

    f_out.cd()
    h_shape.Write()
    f_out.Close()
    print '--> End of processing file: ' + path_out

def shape_MC_hist(ecms, path_signal, path_sideband, path_out, xmin, xmax, xbins, mode, process):
    f_signal = TFile(path_signal)
    f_sideband = TFile(path_sideband)
    if not mode == 'MC_eff':
        f_out = TFile(path_out, 'RECREATE')
    
    h_name = 'h_raw'
    h_signal = f_signal.Get(h_name)
    h_sideband = f_sideband.Get(h_name)
    h_shape = TH1F('h_hist', '', xbins, xmin, xmax)
    h_shape.Add(h_signal, h_sideband, 1, -0.5)

    if mode == 'MC_eff':
        eff = h_shape.Integral() / 50000.
        if (ecms == 4190 or ecms == 4210 or ecms == 4220 or ecms == 4230 or ecms == 4260 or ecms == 4420):
            eff = h_shape.Integral() / 100000.

        print 'MC efficiency is: ' + str(eff) + '...'
        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')
        path_eff = './txts/eff_' + str(ecms) + '_' + process + '.txt'
        f_eff = open(path_eff, 'w')
        out = str(eff)
        f_eff.write(out)
        f_eff.close()

    if not mode == 'MC_eff':
        f_out.cd()
        h_shape.Write()
        f_out.Close()

def shape_MC_raw(ecms, path_in, path_out, xmin, xmax, xbins):
    file_in = TFile(path_in, 'READ')
    t = file_in.Get('save')
    file_out = TFile(path_out, 'RECREATE')

    # MC information
    h_name = 'h_raw'
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
    if len(args)<4:
        return usage()
    ecms = int(args[0])
    mode = args[1]
    process = args[2]
    patch = args[3]

    xmin, xmax, xbins = 1.75, 1.95, 100 # RM(Dpipi) fit range

    if mode == 'MC_signal':
        if not process == 'DDPIPI':
            path_in = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/'+process+'/'+str(ecms)+'/sigMC_' + process + '_'+str(ecms)+'_raw_before.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_'+process+'_'+str(ecms)+'_signal.root'
        if process == 'DDPIPI':
            path_in = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_raw_before.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_'+str(ecms)+'_signal.root'
        shape_MC_raw(ecms, path_in, path_out, xmin, xmax, xbins)

    if mode == 'MC_sideband':
        if not process == 'DDPIPI':
            path_in = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/'+process+'/'+str(ecms)+'/sigMC_' + process + '_'+str(ecms)+'_raw_sideband_before.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_'+process+'_'+str(ecms)+'_sideband.root'
        if process == 'DDPIPI':
            path_in = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_raw_sideband_before.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_'+str(ecms)+'_sideband.root'
        shape_MC_raw(ecms, path_in, path_out, xmin, xmax, xbins)

    if mode == 'MC_shape':
        if not process == 'DDPIPI':
            path_signal = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_'+process+'_'+str(ecms)+'_signal.root'
            path_sideband = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_'+process+'_'+str(ecms)+'_sideband.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_'+process+'_'+str(ecms)+'.root'
        if process == 'DDPIPI':
            path_signal = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_'+str(ecms)+'_signal.root'
            path_sideband = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_'+str(ecms)+'_sideband.root'
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_'+str(ecms)+'.root'
        shape_MC_hist(ecms, path_signal, path_sideband, path_out, xmin, xmax, xbins, mode, process)

    if mode == 'MC_mix':
        path_in = []
        path_out = []
        if ecms > 4311:
            path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D1_2420_' + str(ecms) + '.root')
            path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_psipp_' + str(ecms) + '.root')
            path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_' + str(ecms) + '.root')
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
            mix(path_in, path_out, ecms, xmin, xmax, xbins, patch)
        if ecms <= 4311:
            path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_psipp_' + str(ecms) + '.root')
            path_in.append('/besfs/users/$USER/bes/DDPIPI/v0.2/ana/shape/shape_D_D_PI_PI_' + str(ecms) + '.root')
            path_out = '/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/shape_' + str(ecms) + '_mixed.root'
            mix(path_in, path_out, ecms, xmin, xmax, xbins, patch)

if __name__ == '__main__':
    main()
