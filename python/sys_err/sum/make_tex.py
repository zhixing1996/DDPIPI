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

def make_sys():
    sample, sys_err  = [], []
    with open('./txts/sys_err_total.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                sample.append(int(fargs[0]*1000))
                sys_err.append(fargs[1])
            except:
                '''
                '''
    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/total_sys.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Summary of systematic uncertainties.}\n')
        f.write('\t\\begin{tabular}{cc|cc}\n')
        f.write('\t\hline\hline\n')
        f.write('\tData Sample& Systematic Uncertainty(\%) & Data Sample& Systematic Uncertainty(\%)\\\\\n')
        f.write('\t\hline\n')
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[0],  sys_err[0],  sample[19], sys_err[19]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[1],  sys_err[1],  sample[20], sys_err[20]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[2],  sys_err[2],  sample[21], sys_err[21]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[3],  sys_err[3],  sample[22], sys_err[22]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[4],  sys_err[4],  sample[23], sys_err[23]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[5],  sys_err[5],  sample[24], sys_err[24]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[6],  sys_err[6],  sample[25], sys_err[25]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[7],  sys_err[7],  sample[26], sys_err[26]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[8],  sys_err[8],  sample[27], sys_err[27]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[9],  sys_err[9],  sample[28], sys_err[28]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[10], sys_err[10], sample[29], sys_err[29]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[11], sys_err[11], sample[30], sys_err[30]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[12], sys_err[12], sample[31], sys_err[31]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[13], sys_err[13], sample[32], sys_err[32]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[14], sys_err[14], sample[33], sys_err[33]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[15], sys_err[15], sample[34], sys_err[34]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[16], sys_err[16], sample[35], sys_err[35]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[17], sys_err[17], sample[36], sys_err[36]))
        f.write('\t{:^4}& {:^4}& -    & -    \\\\\n'.format(sample[18], sys_err[18]))
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t\label{table8-11}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

def make_draft():
    SAMPLES = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    TYPES = ['scale_factor', 'psipp_shape', 'D1_2420_shape', 'BW', 'omega', 'HELAMP']
    dic = {}
    for SAMPLE in SAMPLES:
        SYS = []
        for TYPE in TYPES:
            f_type = open('../'+TYPE+'/txts/sys_err_'+TYPE+'.txt', 'r')
            lines_type = f_type.readlines()
            for line_type in lines_type:
                rs_type = line_type.rstrip('\n')
                rs_type = filter(None, rs_type.split("\t"))
                ecms = float(rs_type[0])
                sys = float(rs_type[1])
                if ecms == SAMPLE/1000.:
                    SYS.append(sys)
                    dic[SAMPLE] = SYS
                    dic.update({SAMPLE:SYS})

    total = []
    with open('./txts/sys_err_total.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            fargs = map(float, line.strip().split())
            total.append(fargs[1])

    with open('./texs/sys_err_draft.tex', 'w') as f:
        f.write('\\begin{table*}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Systematic uncertainties from scale factors of $f_{1}$ and $f_{2}$, $\psi(3770)$ and $D_{1}(2420)^{+}$ shape, Breit-Wigners in ISR correction, uncertainties of $\omega_{i}$, and decay mode of $e^{+}e^{-}\\rightarrowD_{1}(2420)^{+}D^{-}$ ($\\textsc{HELAMP}$), the last column shows the overall systematic uncertainty obtained by summing all sources of systematic uncertainties in quadrature by assuming they are uncorrelated.}\n')
        # f.write('\t\\resizebox{\\textwidth}{75mm}{\n')
        f.write('\t\\begin{tabular}{ccccccccc}\n')
        f.write('\t\hline\hline\n')
        f.write('\tSample & $f_{1}$ and $f_{2}$ & $\psi(3770)$ shape & $D_{1}(2420)^{+}$ shape & Breit-Wigner & $\omega_{i}$ & $\\textsc{HELAMP}$ & overall &\\\\\n')
        f.write('\t\hline\n')
        count = 0
        for SAMPLE in SAMPLES:
            scale_factor, psipp_shape, D1_2420_shape, BW, omega, HELAMP = dic[SAMPLE]
            f.write('\t{:^4} & {:^3}\% & {:^3}\% & {:^3}\% & {:^3}\% & {:^3}\% & {:^3}\% & {:^3}\% &\\\\\n'.format(SAMPLE, scale_factor, psipp_shape, D1_2420_shape, BW, omega, HELAMP, total[count]))
            count += 1
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        # f.write('\t}\n')
        f.write('\t\label{table2}\n')
        f.write('\end{table*}\n')
        f.write('\n\n')

def main():
    make_sys()
    make_draft()

if __name__ == '__main__':
    main()
