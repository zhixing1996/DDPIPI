#!/usr/bin/env python
"""
Sample param_i according to correlation matrix
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2021-03-24 Wed 19:46]"

from ROOT import TMatrix, gRandom, TH1F
from array import array
import sys, os
import logging
from math import *

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

def sampling(label_list, iter, Nrand):
    for label in label_list:
        with open('./log/param_cov_' + label + '_' + iter + '.txt', 'r') as f:
            lines = f.readlines()
            Npar = len(lines)
            param_cov = array('f', Npar*Npar*[0.])
            for i in xrange(Npar):
                fargs = map(float, lines[i].strip().split())
                for j in xrange(Npar): param_cov[j + i*Npar] = fargs[j]
        with open('./log/param_' + label + '_' + iter + '.txt', 'r') as f:
            lines = f.readlines()
            param = array('f', Npar*[0.])
            line = lines[0]
            fargs = map(float, line.strip().split())
            for i in xrange(Npar): param[i] = fargs[i]
        matrix_cov = TMatrix(Npar, Npar, param_cov)
        sqrt_cov = TMatrix(Npar, Npar)
        sqrt_matrix(matrix_cov, sqrt_cov, Npar)
        iloop = 0
        param_new = array('f', Npar*[0])
        if not os.path.exists('./txts/'):
            os.makedirs('./txts/')
        with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/param_rand_' + label + '_' + iter + '.txt', 'w') as f:
            while (iloop < Nrand):
                cov_gen(sqrt_cov, param_new, Npar)
                next = False
                for i in xrange(Npar):
                    param_new[i] += param[i]
                    if label == 'D1_2420' and not (param_new[6] > 4. and param_new[6] < 5.) and not abs(param[7]) < 1.:
                        next = True
                    if label == 'psipp' and not param_new[0] > 0.:
                        next = True
                # if next: continue
                out = ''
                for i in xrange(Npar):
                    out += str(param_new[i]) + ' '
                f.write(out + '\n')
                iloop += 1
