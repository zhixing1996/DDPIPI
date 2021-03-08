#!/usr/bin/env python
"""
Calculate Correlation Coefficiency
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-12-28 Mon 19:49]"

import sys, os
import logging
from math import *
from sympy import symbols, diff
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    correlation_coefficiency.py

SYNOPSIS
    ./correlation_coefficiency.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2019
\n''')

def cal(ecms):
    if ecms > 4316:
        XS0, XS1, XS2 = symbols('XS0 XS1 XS2', real = True)
        SIGMA0, SIGMA1, SIGMA2 = symbols('SIGMA0 SIGMA1 sigam2', real = True)
        V00, V11, V22 = symbols('V00 V11 V22', real = True)
        V01, V02, V12 = symbols('V01 V02 V12', real = True)
        omega0 = XS0/(XS0 + XS1 + XS2)
        omega1 = XS1/(XS0 + XS1 + XS2)
        omega2 = XS2/(XS0 + XS1 + XS2)
        omega0_XS0 = diff(omega0, XS0)
        omega0_XS1 = diff(omega0, XS1)
        omega0_XS2 = diff(omega0, XS2)
        omega1_XS0 = diff(omega1, XS0)
        omega1_XS1 = diff(omega1, XS1)
        omega1_XS2 = diff(omega1, XS2)
        omega2_XS0 = diff(omega2, XS0)
        omega2_XS1 = diff(omega2, XS1)
        omega2_XS2 = diff(omega2, XS2)
        omega0_err = omega0_XS0*omega0_XS0*V00*SIGMA0*SIGMA0 + omega0_XS1*omega0_XS1*V11*SIGMA1*SIGMA1 + omega0_XS2*omega0_XS2*V22*SIGMA2*SIGMA2 + 2*omega0_XS0*omega0_XS1*V01*SIGMA0*SIGMA1 + 2*omega0_XS0*omega0_XS2*V02*SIGMA0*SIGMA2 + 2*omega0_XS1*omega0_XS2*V12*SIGMA1*SIGMA2
        omega1_err = omega1_XS0*omega1_XS0*V00*SIGMA0*SIGMA0 + omega1_XS1*omega1_XS1*V11*SIGMA1*SIGMA1 + omega1_XS2*omega1_XS2*V22*SIGMA2*SIGMA2 + 2*omega1_XS0*omega1_XS1*V01*SIGMA0*SIGMA1 + 2*omega1_XS0*omega1_XS2*V02*SIGMA0*SIGMA2 + 2*omega1_XS1*omega1_XS2*V12*SIGMA1*SIGMA2
        omega2_err = omega2_XS0*omega2_XS0*V00*SIGMA0*SIGMA0 + omega2_XS1*omega2_XS1*V11*SIGMA1*SIGMA1 + omega2_XS2*omega2_XS2*V22*SIGMA2*SIGMA2 + 2*omega2_XS0*omega2_XS1*V01*SIGMA0*SIGMA1 + 2*omega2_XS0*omega2_XS2*V02*SIGMA0*SIGMA2 + 2*omega2_XS1*omega2_XS2*V12*SIGMA1*SIGMA2
        with open('./txts/correlation_coefficiency_' + str(ecms) + '.txt', 'r') as f:
            for line in f.readlines():
                fargs = line.strip().split(' ')
                xs0, xs1, xs2, sigma0, sigma1, sigma2, v00, v11, v22, v01, v02, v12 = fargs[0], fargs[1], fargs[2], fargs[3], fargs[4], fargs[5], fargs[6], fargs[7], fargs[8], fargs[9], fargs[10], fargs[11]
        with open('./txts/omega_' + str(ecms) + '.txt', 'w') as f:
            OM0 = omega0.subs({XS0:xs0, XS1:xs1, XS2:xs2})
            OM1 = omega1.subs({XS0:xs0, XS1:xs1, XS2:xs2})
            OM2 = omega2.subs({XS0:xs0, XS1:xs1, XS2:xs2})
            OM0_err = omega0_err.subs({XS0:xs0, XS1:xs1, XS2:xs2, SIGMA0:sigma0, SIGMA1:sigma1, SIGMA2:sigma2, V00:v00, V11:v11, V22:v22, V01:v01, V02:v02, V12:v12})
            OM1_err = omega1_err.subs({XS0:xs0, XS1:xs1, XS2:xs2, SIGMA0:sigma0, SIGMA1:sigma1, SIGMA2:sigma2, V00:v00, V11:v11, V22:v22, V01:v01, V02:v02, V12:v12})
            OM2_err = omega2_err.subs({XS0:xs0, XS1:xs1, XS2:xs2, SIGMA0:sigma0, SIGMA1:sigma1, SIGMA2:sigma2, V00:v00, V11:v11, V22:v22, V01:v01, V02:v02, V12:v12})
            f.write(str(OM0) + ' ' + str(sqrt(OM0_err)) + '\n')
            f.write(str(OM1) + ' ' + str(sqrt(OM1_err)) + '\n')
            f.write(str(OM2) + ' ' + str(sqrt(OM2_err)) + '\n')
    else:
        XS0, XS1 = symbols('XS0 XS1', real = True)
        SIGMA0, SIGMA1 = symbols('SIGMA0 SIGMA1', real = True)
        V00, V11 = symbols('V00 V11', real = True)
        V01 = symbols('V01', real = True)
        omega0 = XS0/(XS0 + XS1)
        omega1 = XS1/(XS0 + XS1)
        omega0_XS0 = diff(omega0, XS0)
        omega0_XS1 = diff(omega0, XS1)
        omega1_XS0 = diff(omega1, XS0)
        omega1_XS1 = diff(omega1, XS1)
        omega0_err = omega0_XS0*omega0_XS0*V00*SIGMA0*SIGMA0 + omega0_XS1*omega0_XS1*V11*SIGMA1*SIGMA1 + 2*omega0_XS0*omega0_XS1*V01*SIGMA0*SIGMA1
        omega1_err = omega1_XS0*omega1_XS0*V00*SIGMA0*SIGMA0 + omega1_XS1*omega1_XS1*V11*SIGMA1*SIGMA1 + 2*omega1_XS0*omega1_XS1*V01*SIGMA0*SIGMA1
        with open('./txts/correlation_coefficiency_' + str(ecms) + '.txt', 'r') as f:
            for line in f.readlines():
                fargs = line.strip().split(' ')
                xs0, xs1, sigma0, sigma1, v00, v11, v01 = fargs[0], fargs[1], fargs[2], fargs[3], fargs[4], fargs[5], fargs[6]
        with open('./txts/omega_' + str(ecms) + '.txt', 'w') as f:
            OM0 = omega0.subs({XS0:xs0, XS1:xs1})
            OM1 = omega1.subs({XS0:xs0, XS1:xs1})
            OM0_err = omega0_err.subs({XS0:xs0, XS1:xs1, SIGMA0:sigma0, SIGMA1:sigma1, V00:v00, V11:v11, V01:v01})
            OM1_err = omega1_err.subs({XS0:xs0, XS1:xs1, SIGMA0:sigma0, SIGMA1:sigma1, V00:v00, V11:v11, V01:v01})
            f.write(str(OM0) + ' ' + str(sqrt(OM0_err)) + '\n')
            f.write(str(OM1) + ' ' + str(sqrt(OM1_err)) + '\n')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)<1:
        usage()
        sys.exit()
    ecms = int(args[0])

    cal(ecms)
