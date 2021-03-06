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
    omega = array('d', 3*[999.])
    omega_err = array('d', 3*[999.])
    omega_path = '../../fit_xs/txts/omega_' + str(ecms) + '.txt'
    with open(omega_path, 'r') as f:
        lines = f.readlines()
        count = 0
        if len(lines) == 2:
            omega[0] = 0.
            omega_err[0] = 0.
            count = 1
        for line in lines:
            fargs = map(float, line.strip().strip('\n').split())
            omega[count] = fargs[0]
            omega_err[count] = fargs[1]
            count += 1
    omega[0] = omega[0] + omega_err[0]
    omega[1] = omega[1] + omega_err[1]
    omega[2] = omega[2] - omega_err[0] - omega_err[1]

    SUM = 0
    for i in xrange(len(omega)): SUM += omega[i]
    for i in xrange(len(omega)): omega[i] /= SUM

    print '--> Begin to process file: ' + path_out
    f_out = TFile(path_out, 'RECREATE')
    h_shape = TH1F('h_hist', '', xbins, xmin, xmax)
    n = 0
    if ecms <= 4316:
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

def shape_MC_raw(ecms, mode, path_in, path_out, xmin, xmax, xbins):
    file_in = TFile(path_in, 'READ')
    t = file_in.Get('save')
    file_out = TFile(path_out, 'RECREATE')

    # MC information
    h_name = 'h_hist'
    h_hist = TH1F(h_name, '', xbins, xmin, xmax)
    for ientry in xrange(t.GetEntries()):
        if ientry % 10000 == 0:
            print 'processing ' + str(ientry) + 'th event...'
        t.GetEntry(ientry)
        if not (t.matched_D == 1 and t.matched_pi == 1):
            continue
        if mode == 'MC_signal': h_hist.Fill(t.m_rm_Dpipi)
        if mode == 'raw': h_hist.Fill(t.m_rawm_D)
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
            path_in = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/'+process+'/'+str(ecms)+'/sigMC_' + process + '_'+str(ecms)+'_raw_after.root'
            path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_'+process+'_'+str(ecms)+'_signal.root'
        if process == 'DDPIPI':
            path_in = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_raw_after.root'
            path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_D_D_PI_PI_'+str(ecms)+'_signal.root'
        shape_MC_raw(ecms, mode, path_in, path_out, xmin, xmax, xbins)

    if mode == 'MC_mix':
        path_in = []
        path_out = []
        if ecms > 4316:
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_D1_2420_' + str(ecms) + '_signal.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_psipp_' + str(ecms) + '_signal.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_D_D_PI_PI_' + str(ecms) + '_signal.root')
            path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/omega/shape_' + str(ecms) + '_mixed.root'
            mix(path_in, path_out, ecms, xmin, xmax, xbins, patch)
        if ecms <= 4316:
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_psipp_' + str(ecms) + '_signal.root')
            path_in.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_D_D_PI_PI_' + str(ecms) + '_signal.root')
            path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/omega/shape_' + str(ecms) + '_mixed.root'
            mix(path_in, path_out, ecms, xmin, xmax, xbins, patch)

    if mode == 'raw':
        xmin, xmax, xbins = 1.82, 1.92, 100 # M(Kpipi) fit range
        if ecms > 4316:
            path_in = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/'+str(ecms)+'/sigMC_D1_2420_'+str(ecms)+'_raw.root'
            path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_D1_2420_'+str(ecms)+'_raw.root'
            shape_MC_raw(ecms, mode, path_in, path_out, xmin, xmax, xbins)
        path_in = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/'+str(ecms)+'/sigMC_D_D_PI_PI_'+str(ecms)+'_raw.root'
        path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_D_D_PI_PI_'+str(ecms)+'_raw.root'
        shape_MC_raw(ecms, mode, path_in, path_out, xmin, xmax, xbins)
        path_in = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/'+str(ecms)+'/sigMC_psipp_'+str(ecms)+'_raw.root'
        path_out = '/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_psipp_'+str(ecms)+'_raw.root'
        shape_MC_raw(ecms, mode, path_in, path_out, xmin, xmax, xbins)
        path_IN = []
        path_OUT = []
        if ecms > 4316: path_IN.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_D1_2420_' + str(ecms) + '_raw.root')
        path_IN.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_psipp_' + str(ecms) + '_raw.root')
        path_IN.append('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/shape/sys_err/omega/shape_D_D_PI_PI_' + str(ecms) + '_raw.root')
        path_OUT = '/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed/sys_err/omega/shape_' + str(ecms) + '_mixed_raw.root'
        mix(path_IN, path_OUT, ecms, xmin, xmax, xbins, patch)

if __name__ == '__main__':
    main()
