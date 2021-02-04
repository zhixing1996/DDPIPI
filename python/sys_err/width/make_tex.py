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
    sample, sys_err, F, Ferr, F_Ferr = [], [], [], [], []
    with open('./txts/sys_err_width.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                sample.append(int(fargs[0]*1000))
                sys_err.append(fargs[1])
                F.append(round(fargs[2], 3))
                Ferr.append(round(fargs[3], 3))
                F_Ferr.append(round(fargs[4], 1))
            except:
                '''
                '''
    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/width_f.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{$f^{M(K^{-}\pi^{+}\pi^{+})}$ and $\\frac{|\Delta f^{M(K^{-}\pi^{+}\pi^{+})}|}{|\sigma_{f^{M(K^{-}\pi^{+}\pi^{+})}}|}$ values.}\n')
        f.write('\t\\begin{tabular}{ccc|ccc}\n')
        f.write('\t\hline\hline\n')
        f.write('\tData Sample& $f^{M(K^{-}\pi^{+}\pi^{+})}$ & $\\frac{|\Delta f^{M(K^{-}\pi^{+}\pi^{+})}|}{|\sigma_{f^{M(K^{-}\pi^{+}\pi^{+})}}|}$ & Data Sample& $f^{M(K^{-}\pi^{+}\pi^{+})}$ & $\\frac{|\Delta f^{M(K^{-}\pi^{+}\pi^{+})}|}{|\sigma_{f^{M(K^{-}\pi^{+}\pi^{+})}}|}$\\\\\n')
        f.write('\t\hline\n')
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[0],  F[0],  Ferr[0],  F_Ferr[0],  sample[16], F[16], Ferr[16], F_Ferr[16]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[1],  F[1],  Ferr[1],  F_Ferr[1],  sample[17], F[17], Ferr[17], F_Ferr[17]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[2],  F[2],  Ferr[2],  F_Ferr[2],  sample[18], F[18], Ferr[18], F_Ferr[18]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[3],  F[3],  Ferr[3],  F_Ferr[3],  sample[19], F[19], Ferr[19], F_Ferr[19]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[4],  F[4],  Ferr[4],  F_Ferr[4],  sample[20], F[20], Ferr[20], F_Ferr[20]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[5],  F[5],  Ferr[5],  F_Ferr[5],  sample[21], F[21], Ferr[21], F_Ferr[21]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[6],  F[6],  Ferr[6],  F_Ferr[6],  sample[22], F[22], Ferr[22], F_Ferr[22]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[7],  F[7],  Ferr[7],  F_Ferr[7],  sample[23], F[23], Ferr[23], F_Ferr[23]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[8],  F[8],  Ferr[8],  F_Ferr[8],  sample[24], F[24], Ferr[24], F_Ferr[24]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[9],  F[9],  Ferr[9],  F_Ferr[9],  sample[25], F[25], Ferr[25], F_Ferr[25]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[10], F[10], Ferr[10], F_Ferr[10], sample[26], F[26], Ferr[26], F_Ferr[26]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[11], F[11], Ferr[11], F_Ferr[11], sample[27], F[27], Ferr[27], F_Ferr[27]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[12], F[12], Ferr[12], F_Ferr[12], sample[28], F[28], Ferr[28], F_Ferr[28]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[13], F[13], Ferr[13], F_Ferr[13], sample[29], F[29], Ferr[29], F_Ferr[29]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& {:^4}& {:^4}$\pm${:^4}& {:^4}\\\\\n'.format(sample[14], F[14], Ferr[14], F_Ferr[14], sample[30], F[30], Ferr[30], F_Ferr[30]))
        f.write('\t{:^4}& {:^4}$\pm${:^4}& {:^4}& -    & -    & -    \\\\\n'.format(sample[15], F[15], Ferr[15], F_Ferr[15]))
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t\label{table8-2-1}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

    with open('./texs/width_sys.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Systematic uncertainty caused by $M(K^{-}\pi^{+}\pi^{+})$ mass window.}\n')
        f.write('\t\\begin{tabular}{cc|cc}\n')
        f.write('\t\hline\hline\n')
        f.write('\tData Sample& Systematic Uncertainty(\%) & Data Sample& Systematic Uncertainty(\%)\\\\\n')
        f.write('\t\hline\n')
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[0], sys_err[0], sample[16], sys_err[16]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[1], sys_err[1], sample[17], sys_err[17]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[2], sys_err[2], sample[18], sys_err[18]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[3], sys_err[3], sample[19], sys_err[19]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[4], sys_err[4], sample[20], sys_err[20]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[5], sys_err[5], sample[21], sys_err[21]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[6], sys_err[6], sample[22], sys_err[22]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[7], sys_err[7], sample[23], sys_err[23]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[8], sys_err[8], sample[24], sys_err[24]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[9], sys_err[9], sample[25], sys_err[25]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[10], sys_err[10], sample[26], sys_err[26]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[11], sys_err[11], sample[27], sys_err[27]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[12], sys_err[12], sample[28], sys_err[28]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[13], sys_err[13], sample[29], sys_err[29]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(sample[14], sys_err[14], sample[30], sys_err[30]))
        f.write('\t{:^4}& {:^4}& -    & -    \\\\\n'.format(sample[15], sys_err[15]))
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t\label{table8-2-2}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

def main():
    make_sys()

if __name__ == '__main__':
    main()
