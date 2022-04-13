#!/usr/bin/env python
"""
Make tables for memo and article
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-12-10 Thu 18:59]"

import sys, os
import logging
from math import *

def usage():
    sys.stdout.write('''
NAME
    make_tex.py

SYNOPSIS
    ./make_tex.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2020
\n''')

def make_draft(s1, s2, s3, s4):
    TARGETS_SPREAD = ['BW_4390_mass', 'BW_4390_width', 'BW_4390_BrGam', 'BW_4700_mass', 'BW_4700_width', 'BW_4700_BrGam', 'BW_4700_phase', 'phsp_phase']
    TARGETS_XS1 = ['BW_4390_mass', 'BW_4390_width', 'BW_4390_BrGam', 'BW_4700_mass', 'BW_4700_width', 'BW_4700_BrGam']
    TARGETS_XS2 = ['BW_4390_BrGam', 'BW_4700_BrGam']

    PATH_SPREAD = '../../fit_total/sys_err/spread/txts/sys_err_spread_' + str(s1) + '.txt'
    sys_spread_s1 = {}
    with open(PATH_SPREAD, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_SPREAD:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_spread_s1[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_spread_s1[TARGET] = round(float(fargs[2]), 1)

    PATH_SPREAD = '../../fit_total/sys_err/spread/txts/sys_err_spread_' + str(s2) + '.txt'
    sys_spread_s2 = {}
    with open(PATH_SPREAD, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_SPREAD:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_spread_s2[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_spread_s2[TARGET] = round(float(fargs[2]), 1)

    PATH_SPREAD = '../../fit_total/sys_err/spread/txts/sys_err_spread_' + str(s3) + '.txt'
    sys_spread_s3 = {}
    with open(PATH_SPREAD, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_SPREAD:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_spread_s3[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_spread_s3[TARGET] = round(float(fargs[2]), 1)

    PATH_SPREAD = '../../fit_total/sys_err/spread/txts/sys_err_spread_' + str(s4) + '.txt'
    sys_spread_s4 = {}
    with open(PATH_SPREAD, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_SPREAD:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_spread_s4[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_spread_s4[TARGET] = round(float(fargs[2]), 1)

    PATH_XS1 = '../../fit_total/sys_err/xs1/txts/sys_err_xs1_' + str(s1) + '.txt'
    sys_xs1_s1 = {}
    with open(PATH_XS1, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_XS1:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_xs1_s1[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_xs1_s1[TARGET] = round(float(fargs[2]), 1)

    PATH_XS1 = '../../fit_total/sys_err/xs1/txts/sys_err_xs1_' + str(s2) + '.txt'
    sys_xs1_s2 = {}
    with open(PATH_XS1, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_XS1:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_xs1_s2[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_xs1_s2[TARGET] = round(float(fargs[2]), 1)

    PATH_XS1 = '../../fit_total/sys_err/xs1/txts/sys_err_xs1_' + str(s3) + '.txt'
    sys_xs1_s3 = {}
    with open(PATH_XS1, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_XS1:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_xs1_s3[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_xs1_s3[TARGET] = round(float(fargs[2]), 1)

    PATH_XS1 = '../../fit_total/sys_err/xs1/txts/sys_err_xs1_' + str(s4) + '.txt'
    sys_xs1_s4 = {}
    with open(PATH_XS1, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_XS1:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_xs1_s4[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_xs1_s4[TARGET] = round(float(fargs[2]), 1)

    PATH_XS2 = '../../fit_total/sys_err/xs2/txts/sys_err_xs2.txt'
    sys_xs2 = {}
    with open(PATH_XS2, 'r') as f:
        for line in f.readlines():
            for TARGET in TARGETS_XS2:
                fargs = line.strip().split()
                if fargs[0] == TARGET:
                    if 'mass' in TARGET or 'width' in TARGET: sys_xs2[TARGET] = round(float(fargs[2]) * 1000, 1)
                    else: sys_xs2[TARGET] = round(float(fargs[2]), 1)

    sys_s1 = {}
    sys_s1['BW_4390_mass'] = round(sqrt(0.8**2 + sys_spread_s1['BW_4390_mass']**2 + sys_xs1_s1['BW_4390_mass']**2), 1)
    sys_s1['BW_4390_width'] = round(sqrt(sys_spread_s1['BW_4390_width']**2 + sys_xs1_s1['BW_4390_width']**2), 1)
    sys_s1['BW_4390_BrGam'] = round(sqrt(sys_spread_s1['BW_4390_BrGam']**2 + sys_xs1_s1['BW_4390_BrGam']**2 + sys_xs2['BW_4390_BrGam']**2), 1)
    sys_s1['BW_4700_mass'] = round(sqrt(0.8**2 + sys_spread_s1['BW_4700_mass']**2 + sys_xs1_s1['BW_4700_mass']**2), 1)
    sys_s1['BW_4700_width'] = round(sqrt(sys_spread_s1['BW_4700_width']**2 + sys_xs1_s1['BW_4700_width']**2), 1)
    sys_s1['BW_4700_BrGam'] = round(sqrt(sys_spread_s1['BW_4700_BrGam']**2 + sys_xs1_s1['BW_4700_BrGam']**2 + sys_xs2['BW_4700_BrGam']**2), 1)
    sys_s1['BW_4700_phase'] = round(sqrt(sys_spread_s1['BW_4700_phase']**2), 1)
    sys_s1['phsp_phase'] = round(sqrt(sys_spread_s1['phsp_phase']**2), 1)

    sys_s2 = {}
    sys_s2['BW_4390_mass'] = round(sqrt(0.8**2 + sys_spread_s2['BW_4390_mass']**2 + sys_xs1_s2['BW_4390_mass']**2), 1)
    sys_s2['BW_4390_width'] = round(sqrt(sys_spread_s2['BW_4390_width']**2 + sys_xs1_s2['BW_4390_width']**2), 1)
    sys_s2['BW_4390_BrGam'] = round(sqrt(sys_spread_s2['BW_4390_BrGam']**2 + sys_xs1_s2['BW_4390_BrGam']**2 + sys_xs2['BW_4390_BrGam']**2), 1)
    sys_s2['BW_4700_mass'] = round(sqrt(0.8**2 + sys_spread_s2['BW_4700_mass']**2 + sys_xs1_s2['BW_4700_mass']**2), 1)
    sys_s2['BW_4700_width'] = round(sqrt(sys_spread_s2['BW_4700_width']**2 + sys_xs1_s2['BW_4700_width']**2), 1)
    sys_s2['BW_4700_BrGam'] = round(sqrt(sys_spread_s2['BW_4700_BrGam']**2 + sys_xs1_s2['BW_4700_BrGam']**2 + sys_xs2['BW_4700_BrGam']**2), 1)
    sys_s2['BW_4700_phase'] = round(sqrt(sys_spread_s2['BW_4700_phase']**2), 1)
    sys_s2['phsp_phase'] = round(sqrt(sys_spread_s1['phsp_phase']**2), 1)

    sys_s3 = {}
    sys_s3['BW_4390_mass'] = round(sqrt(0.8**2 + sys_spread_s3['BW_4390_mass']**2 + sys_xs1_s3['BW_4390_mass']**2), 1)
    sys_s3['BW_4390_width'] = round(sqrt(sys_spread_s3['BW_4390_width']**2 + sys_xs1_s3['BW_4390_width']**2), 1)
    sys_s3['BW_4390_BrGam'] = round(sqrt(sys_spread_s3['BW_4390_BrGam']**2 + sys_xs1_s3['BW_4390_BrGam']**2 + sys_xs2['BW_4390_BrGam']**2), 1)
    sys_s3['BW_4700_mass'] = round(sqrt(0.8**2 + sys_spread_s3['BW_4700_mass']**2 + sys_xs1_s3['BW_4700_mass']**2), 1)
    sys_s3['BW_4700_width'] = round(sqrt(sys_spread_s3['BW_4700_width']**2 + sys_xs1_s3['BW_4700_width']**2), 1)
    sys_s3['BW_4700_BrGam'] = round(sqrt(sys_spread_s3['BW_4700_BrGam']**2 + sys_xs1_s3['BW_4700_BrGam']**2 + sys_xs2['BW_4700_BrGam']**2), 1)
    sys_s3['BW_4700_phase'] = round(sqrt(sys_spread_s3['BW_4700_phase']**2), 1)
    sys_s3['phsp_phase'] = round(sqrt(sys_spread_s1['phsp_phase']**2), 1)

    sys_s4 = {}
    sys_s4['BW_4390_mass'] = round(sqrt(0.8**2 + sys_spread_s4['BW_4390_mass']**2 + sys_xs1_s4['BW_4390_mass']**2), 1)
    sys_s4['BW_4390_width'] = round(sqrt(sys_spread_s4['BW_4390_width']**2 + sys_xs1_s4['BW_4390_width']**2), 1)
    sys_s4['BW_4390_BrGam'] = round(sqrt(sys_spread_s4['BW_4390_BrGam']**2 + sys_xs1_s4['BW_4390_BrGam']**2 + sys_xs2['BW_4390_BrGam']**2), 1)
    sys_s4['BW_4700_mass'] = round(sqrt(0.8**2 + sys_spread_s4['BW_4700_mass']**2 + sys_xs1_s4['BW_4700_mass']**2), 1)
    sys_s4['BW_4700_width'] = round(sqrt(sys_spread_s4['BW_4700_width']**2 + sys_xs1_s4['BW_4700_width']**2), 1)
    sys_s4['BW_4700_BrGam'] = round(sqrt(sys_spread_s4['BW_4700_BrGam']**2 + sys_xs1_s4['BW_4700_BrGam']**2 + sys_xs2['BW_4700_BrGam']**2), 1)
    sys_s4['BW_4700_phase'] = round(sqrt(sys_spread_s4['BW_4700_phase']**2), 1)
    sys_s4['phsp_phase'] = round(sqrt(sys_spread_s1['phsp_phase']**2), 1)

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/sys_err_res.tex', 'w') as f:
        f.write('\\begin{table*}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Systematic uncertainties in the measurement of the resonances parameters. $E_{c.m.}$ represents the systematic uncertainty from the $E_{c.m.}$ measurement. Cross $\\rm{section}_{a(b)}$ represents the systematic uncertainty from the cross section measurements which are uncorrelated (common) in each data sample. The units of $M_{i}$, $\Gamma^{\\rm{tot}_{i}}$, $\Gamma^{\ee}_{j}\mathscr{B}_{j}$, and $\phi_{j}$ are MeV/$c^{2}$, MeV, eV and rad, respectively}\n')
        # f.write('\t\\resizebox{\\textwidth}{75mm}{\n')
        f.write('\t\\begin{tabular}{cccccccccccccc}\n')
        f.write('\t\hline\hline\n')
        f.write('\t& Sources & $M_{0}$ & $\Gamma_{0}$ & $M_{1}$ & $\Gamma_{1}$ & $\Gamma^{\ee}_{0}\mathscr{B}_{0}$ & $\Gamma^{\ee}_{1}\mathscr{B}_{1}$ & $\phi_{0}$ & $\phi_{1}$ &\\\\\n')
        f.write('\t\hline\n')
        f.write('\t\multirow{5}*{Solution \uppercase\expandafter{\\romannumeral1}} & $E_{c.m.}$        & 0.8 & - & 0.8 & - & - & - & - & - &\\\\\n')
        f.write('\t ~                                                              & $E_{c.m.}$ spread & ' + str(sys_spread_s1['BW_4390_mass'])  + ' & ' + 
                                                                                                             str(sys_spread_s1['BW_4390_width']) + ' & ' + 
                                                                                                             str(sys_spread_s1['BW_4700_mass'])  + ' & ' + 
                                                                                                             str(sys_spread_s1['BW_4700_width']) + ' & ' + 
                                                                                                             str(sys_spread_s1['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_spread_s1['BW_4700_BrGam']) + ' & ' + 
                                                                                                             str(sys_spread_s1['BW_4700_phase']) + ' & ' + 
                                                                                                             str(sys_spread_s1['phsp_phase'])    + ' &\\\\\n')
        f.write('\t ~                                                      & Cross $\\rm{Section}_{a}$ & ' + str(sys_xs1_s1['BW_4390_mass'])  + ' & ' + 
                                                                                                             str(sys_xs1_s1['BW_4390_width']) + ' & ' + 
                                                                                                             str(sys_xs1_s1['BW_4700_mass'])  + ' & ' + 
                                                                                                             str(sys_xs1_s1['BW_4700_width']) + ' & ' + 
                                                                                                             str(sys_xs1_s1['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_xs1_s1['BW_4700_BrGam']) + ' & ' + 
                                                                                                             '                                  - & ' + 
                                                                                                             '                                  - &\\\\\n')
        f.write('\t ~                                                      & Cross $\\rm{Section}_{b}$ & ' + ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             str(sys_xs2['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_xs2['BW_4700_BrGam']) + ' & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - &\\\\\n')
        f.write('\t ~                                                              & Overall & ' + str(sys_s1['BW_4390_mass'])  + ' & ' + 
                                                                                                   str(sys_s1['BW_4390_width']) + ' & ' + 
                                                                                                   str(sys_s1['BW_4700_mass'])  + ' & ' + 
                                                                                                   str(sys_s1['BW_4700_width']) + ' & ' + 
                                                                                                   str(sys_s1['BW_4390_BrGam']) + ' & ' + 
                                                                                                   str(sys_s1['BW_4700_BrGam']) + ' & ' + 
                                                                                                   str(sys_s1['BW_4700_phase']) + ' & ' + 
                                                                                                   str(sys_s1['phsp_phase'])    + ' &\\\\\n')
        f.write('\t\hline\n')
        f.write('\t\multirow{5}*{Solution \uppercase\expandafter{\\romannumeral2}} & $E_{c.m.}$        & 0.8 & - & 0.8 & - & - & - & - & - &\\\\\n')
        f.write('\t ~                                                              & $E_{c.m.}$ spread & ' + str(sys_spread_s2['BW_4390_mass'])  + ' & ' + 
                                                                                                             str(sys_spread_s2['BW_4390_width']) + ' & ' + 
                                                                                                             str(sys_spread_s2['BW_4700_mass'])  + ' & ' + 
                                                                                                             str(sys_spread_s2['BW_4700_width']) + ' & ' + 
                                                                                                             str(sys_spread_s2['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_spread_s2['BW_4700_BrGam']) + ' & ' + 
                                                                                                             str(sys_spread_s2['BW_4700_phase']) + ' & ' + 
                                                                                                             str(sys_spread_s2['phsp_phase'])    + ' &\\\\\n')
        f.write('\t ~                                                      & Cross $\\rm{Section}_{a}$ & ' + str(sys_xs1_s2['BW_4390_mass'])  + ' & ' + 
                                                                                                             str(sys_xs1_s2['BW_4390_width']) + ' & ' + 
                                                                                                             str(sys_xs1_s2['BW_4700_mass'])  + ' & ' + 
                                                                                                             str(sys_xs1_s2['BW_4700_width']) + ' & ' + 
                                                                                                             str(sys_xs1_s2['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_xs1_s2['BW_4700_BrGam']) + ' & ' + 
                                                                                                             '                                  - & ' + 
                                                                                                             '                                  - &\\\\\n')
        f.write('\t ~                                                      & Cross $\\rm{Section}_{b}$ & ' + ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             str(sys_xs2['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_xs2['BW_4700_BrGam']) + ' & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - &\\\\\n')
        f.write('\t ~                                                              & Overall & ' + str(sys_s2['BW_4390_mass'])  + ' & ' + 
                                                                                                   str(sys_s2['BW_4390_width']) + ' & ' + 
                                                                                                   str(sys_s2['BW_4700_mass'])  + ' & ' + 
                                                                                                   str(sys_s2['BW_4700_width']) + ' & ' + 
                                                                                                   str(sys_s2['BW_4390_BrGam']) + ' & ' + 
                                                                                                   str(sys_s2['BW_4700_BrGam']) + ' & ' + 
                                                                                                   str(sys_s2['BW_4700_phase']) + ' & ' + 
                                                                                                   str(sys_s2['phsp_phase'])    + ' &\\\\\n')
        f.write('\t\hline\n')
        f.write('\t\multirow{5}*{Solution \uppercase\expandafter{\\romannumeral3}} & $E_{c.m.}$        & 0.8 & - & 0.8 & - & - & - & - & - &\\\\\n')
        f.write('\t ~                                                              & $E_{c.m.}$ spread & ' + str(sys_spread_s3['BW_4390_mass'])  + ' & ' + 
                                                                                                             str(sys_spread_s3['BW_4390_width']) + ' & ' + 
                                                                                                             str(sys_spread_s3['BW_4700_mass'])  + ' & ' + 
                                                                                                             str(sys_spread_s3['BW_4700_width']) + ' & ' + 
                                                                                                             str(sys_spread_s3['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_spread_s3['BW_4700_BrGam']) + ' & ' + 
                                                                                                             str(sys_spread_s3['BW_4700_phase']) + ' & ' + 
                                                                                                             str(sys_spread_s3['phsp_phase'])    + ' &\\\\\n')
        f.write('\t ~                                                      & Cross $\\rm{Section}_{a}$ & ' + str(sys_xs1_s3['BW_4390_mass'])  + ' & ' + 
                                                                                                             str(sys_xs1_s3['BW_4390_width']) + ' & ' + 
                                                                                                             str(sys_xs1_s3['BW_4700_mass'])  + ' & ' + 
                                                                                                             str(sys_xs1_s3['BW_4700_width']) + ' & ' + 
                                                                                                             str(sys_xs1_s3['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_xs1_s3['BW_4700_BrGam']) + ' & ' + 
                                                                                                             '                                  - & ' + 
                                                                                                             '                                  - &\\\\\n')
        f.write('\t ~                                                      & Cross $\\rm{Section}_{b}$ & ' + ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             str(sys_xs2['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_xs2['BW_4700_BrGam']) + ' & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - &\\\\\n')
        f.write('\t ~                                                              & Overall & ' + str(sys_s3['BW_4390_mass'])  + ' & ' + 
                                                                                                   str(sys_s3['BW_4390_width']) + ' & ' + 
                                                                                                   str(sys_s3['BW_4700_mass'])  + ' & ' + 
                                                                                                   str(sys_s3['BW_4700_width']) + ' & ' + 
                                                                                                   str(sys_s3['BW_4390_BrGam']) + ' & ' + 
                                                                                                   str(sys_s3['BW_4700_BrGam']) + ' & ' + 
                                                                                                   str(sys_s3['BW_4700_phase']) + ' & ' + 
                                                                                                   str(sys_s3['phsp_phase'])    + ' &\\\\\n')
        f.write('\t\hline\n')
        f.write('\t\multirow{5}*{Solution \uppercase\expandafter{\\romannumeral4}} & $E_{c.m.}$        & 0.8 & - & 0.8 & - & - & - & - & - &\\\\\n')
        f.write('\t ~                                                              & $E_{c.m.}$ spread & ' + str(sys_spread_s4['BW_4390_mass'])  + ' & ' + 
                                                                                                             str(sys_spread_s4['BW_4390_width']) + ' & ' + 
                                                                                                             str(sys_spread_s4['BW_4700_mass'])  + ' & ' + 
                                                                                                             str(sys_spread_s4['BW_4700_width']) + ' & ' + 
                                                                                                             str(sys_spread_s4['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_spread_s4['BW_4700_BrGam']) + ' & ' + 
                                                                                                             str(sys_spread_s4['BW_4700_phase']) + ' & ' + 
                                                                                                             str(sys_spread_s4['phsp_phase'])    + ' &\\\\\n')
        f.write('\t ~                                                      & Cross $\\rm{Section}_{a}$ & ' + str(sys_xs1_s4['BW_4390_mass'])  + ' & ' + 
                                                                                                             str(sys_xs1_s4['BW_4390_width']) + ' & ' + 
                                                                                                             str(sys_xs1_s4['BW_4700_mass'])  + ' & ' + 
                                                                                                             str(sys_xs1_s4['BW_4700_width']) + ' & ' + 
                                                                                                             str(sys_xs1_s4['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_xs1_s4['BW_4700_BrGam']) + ' & ' + 
                                                                                                             '                                  - & ' + 
                                                                                                             '                                  - &\\\\\n')
        f.write('\t ~                                                      & Cross $\\rm{Section}_{b}$ & ' + ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - & ' + 
                                                                                                             str(sys_xs2['BW_4390_BrGam']) + ' & ' + 
                                                                                                             str(sys_xs2['BW_4700_BrGam']) + ' & ' + 
                                                                                                             ' - & ' + 
                                                                                                             ' - &\\\\\n')
        f.write('\t ~                                                              & Overall & ' + str(sys_s4['BW_4390_mass'])  + ' & ' + 
                                                                                                   str(sys_s4['BW_4390_width']) + ' & ' + 
                                                                                                   str(sys_s4['BW_4700_mass'])  + ' & ' + 
                                                                                                   str(sys_s4['BW_4700_width']) + ' & ' + 
                                                                                                   str(sys_s4['BW_4390_BrGam']) + ' & ' + 
                                                                                                   str(sys_s4['BW_4700_BrGam']) + ' & ' + 
                                                                                                   str(sys_s4['BW_4700_phase']) + ' & ' + 
                                                                                                   str(sys_s4['phsp_phase'])    + ' &\\\\\n')
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        # f.write('\t}\n')
        f.write('\t\label{tableres}\n')
        f.write('\end{table*}\n')
        f.write('\n\n')

    # with open('./texs/sys_err_res.tex', 'w') as f:
    #     f.write('\\begin{table*}[htp]\n')
    #     f.write('\t\centering\n')
    #     f.write('\t\caption{Systematic uncertainties in the measurement of the resonances parameters. $E_{c.m.}$ represents the systematic uncertainty from the $E_{c.m.}$ measurement. Cross $\\rm{section}$ represents the systematic uncertainty from the cross section measurement which are uncorrelated in each data sample. The units of $M_{i}$ and $\Gamma^{\\rm{tot}_{i}}$ are MeV/$c^{2}$ and MeV, respectively.}\n')
    #     # f.write('\t\\resizebox{\\textwidth}{75mm}{\n')
    #     f.write('\t\\begin{tabular}{ccccccccc}\n')
    #     f.write('\t\hline\hline\n')
    #     f.write('\tSources & $M_{0}$ & $\Gamma_{0}$ & $M_{1}$ & $\Gamma_{1}$ &\\\\\n')
    #     f.write('\t\hline\n')
    #     f.write('\t $E_{c.m.}$& 0.8 & - & 0.8 & - &\\\\\n')
    #     f.write('\t $E_{c.m.}$ ' + 'spread & {:^4} & {:^4} & {:^4} & {:^4} &\\\\\n'.format(sys_spread['BW_4390_mass'], sys_spread['BW_4390_width'], sys_spread['BW_4700_mass'], sys_spread['BW_4700_width']))
    #     f.write('\t Cross $\\rm{section}$ ' + '& {:^4} & {:^4} & {:^4} & {:^4} &\\\\\n'.format(sys_xs1['BW_4390_mass'], sys_xs1['BW_4390_width'], sys_xs1['BW_4700_mass'], sys_xs1['BW_4700_width']))
    #     f.write('\t Overall & {:^4} & {:^4} & {:^4} & {:^4} &\\\\\n'.format(sys['BW_4390_mass'], sys['BW_4390_width'], sys['BW_4700_mass'], sys['BW_4700_width']))
    #     f.write('\t\hline\hline\n')
    #     f.write('\t\end{tabular}\n')
    #     # f.write('\t}\n')
    #     f.write('\t\label{tableres}\n')
    #     f.write('\end{table*}\n')
    #     f.write('\n\n')

def main():
    make_draft(8, 12, 26, 28)

if __name__ == '__main__':
    main()
