#!/usr/bin/env python
"""
Sample omega_i according to correlation matrix
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2021-03-24 Wed 19:46]"

import ROOT
from ROOT import TMatrix, gRandom, TH1F, TFile
from array import array
import sys, os
import logging
from math import *
from tools import param_rm_pipi, param_rm_D, luminosity
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    sample.py

SYNOPSIS
    ./sample.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    March 2021
\n''')

Br = 0.0938

def cal_xs(ecms, mode, N, patch):
    xmin_rm_pipi, xmax_rm_pipi = param_rm_pipi(ecms)
    xmin_rm_D, xmax_rm_D, test = param_rm_D(ecms)
    xmin_rm_Dmiss, xmax_rm_Dmiss, test = param_rm_D(ecms)
    lum = luminosity(ecms)
    with open('../../fit_xs/txts/simul_fit_' + str(ecms) + '_' + patch + '.txt') as f_eff:
        lines_eff = f_eff.readlines()
        if mode == 'D1_2420': eff = float(lines_eff[4].split('\\')[0])/100
        if mode == 'psipp': eff = float(lines_eff[5].split('\\')[0])/100
        if mode == 'DDPIPI': eff = float(lines_eff[6].split('\\')[0])/100
    f_factor = open('../../txts/factor_info_' + str(ecms) + '_' + mode + '_' + patch + '.txt', 'r')
    lines = f_factor.readlines()
    for line in lines:
        fargs = map(float, line.strip('\n').strip().split())
        ISR, VP = fargs[0], fargs[1]
    xs = N/2./Br/eff/lum/ISR/VP
    return xs

def cov_gen(C, x, NP):
    z = array('f', NP*[0.])
    for i in xrange(NP):
        z[i] = gRandom.Gaus(0., 1.)
    for i in xrange(NP):
        x[i] = 0
        for j in xrange(NP):
            if j > i: continue
            x[i] += C[i][j] * z[j]

def sqrt_matrix(V, C, NP):
    for i in xrange(NP):
        for j in xrange(NP):
            C[i][j] = 0
    for i in xrange(NP):
        Ck = 0
        for j in xrange(NP):
            if j >= i: continue
            Ck += C[i][j] * C[i][j]
        C[i][i] = sqrt(abs(V[i][i] - Ck))
        for j in xrange(i + 1, NP):
            Ck = 0
            for k in xrange(NP):
                if k >= i: continue
                Ck += C[j][k] * C[j][k]
            C[j][i] = (V[j][i] - Ck)/C[i][i]

def sampling(ecms, patch):
    with open('../../fit_xs/txts/omega_info_' + str(ecms) + '.txt') as f:
        if ecms < 4340:
            Npar = 2
            line = f.readlines()[0]
            fargs = map(float, line.strip().split())
            N = array('f', [fargs[0], fargs[1]])
            N_cov = array('f', [fargs[2], fargs[3], fargs[4], fargs[5]])
        else:
            Npar = 3
            line = f.readlines()[0]
            fargs = map(float, line.strip().split())
            N = array('f', [fargs[0], fargs[1], fargs[2]])
            N_cov = array('f', [fargs[3], fargs[4], fargs[5], fargs[6], fargs[7], fargs[8], fargs[9], fargs[10], fargs[11]])
    matrix_cov = TMatrix(Npar, Npar, N_cov)
    sqrt_cov = TMatrix(Npar, Npar)
    sqrt_matrix(matrix_cov, sqrt_cov, Npar)
    iloop = 0
    Nrand = 500
    N_new = array('f', Npar*[0])
    omega_new = array('f', Npar*[0])
    while (iloop < Nrand):
        cov_gen(sqrt_cov, N_new, Npar)
        for i in xrange(Npar):
            N_new[i] += N[i]
        if ecms < 4316:
            xs_psipp = cal_xs(ecms, 'psipp', N_new[0], patch)
            xs_DDPIPI = cal_xs(ecms, 'DDPIPI', N_new[1], patch)
            xs_total = xs_psipp + xs_DDPIPI
            omega_new[0] = xs_psipp/xs_total
            omega_new[1] = xs_DDPIPI/xs_total
        else:
            xs_D1_2420 = cal_xs(ecms, 'D1_2420', N_new[0], patch)
            xs_psipp = cal_xs(ecms, 'psipp', N_new[1], patch)
            xs_DDPIPI = cal_xs(ecms, 'DDPIPI', N_new[2], patch)
            xs_total = xs_D1_2420 + xs_psipp + xs_DDPIPI
            omega_new[0] = xs_D1_2420/xs_total
            omega_new[1] = xs_psipp/xs_total
            omega_new[2] = xs_DDPIPI/xs_total
        if not os.path.exists('/besfs5/users/$USER/bes/DDPIPI/v0.2/ana/sys_err/omega/' + str(ecms) + '/'):
            os.system('mkdir -p /besfs5/users/$USER/bes/DDPIPI/v0.2/ana/sys_err/omega/' + str(ecms) + '/')
        with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/omega/' + str(ecms) + '/omega_' + str(ecms) + '_' + str(iloop) + '.txt', 'w') as f:
            out = ''
            for i in xrange(Npar):
                out += str(omega_new[i]) + ' '
            f.write(out)
        iloop += 1
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<2:
        usage()
        sys.exit()
    ecms = int(args[0])
    patch = args[1]

    sampling(ecms, patch)
