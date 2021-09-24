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
    with open('./txts/sys_err_HELAMP.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                sample.append(int(fargs[0]*1000))
                sys_err.append(fargs[1])
            except:
                '''
                '''
    R_00, R_10 = [], []
    for sam in sample:
        if sam < 4316:
            R_00.append(0)
            R_10.append(0)
            continue
        with open('./txts/ratio_'+str(sam)+'.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                try:
                    fargs = map(float, line.strip('\n').strip().split())
                    R_00.append(round(fargs[0], 2))
                    R_10.append(round(fargs[1], 2))
                except:
                    '''
                    '''

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/HELAMP_sys.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Systematic uncertainty caused by different parameters of $\\textsc{HELAMP}$ model.}\n')
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
        f.write('\t\label{table8-13-1}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

    with open('./texs/ratio_HELAMP.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Ratio of $\\textsc{HELAMP}\ 1\ 0\ 0\ 0\ 1\ 0$ and $\\textsc{HELAMP}\ 0\ 0\ 1\ 0\ 0\ 0$ conributions.}\n')
        f.write('\t\\resizebox{\\textwidth}{45mm}{\n')
        f.write('\t\\begin{tabular}{cc|cc}\n')
        f.write('\t\hline\hline\n')
        f.write('\tData Sample& $(\\textsc{HELAMP}\ 0\ 0\ 1\ 0\ 0\ 0,\ \\textsc{HELAMP}\ 1\ 0\ 0\ 0\ 1\ 0)$ & Data Sample& $(\\textsc{HELAMP}\ 0\ 0\ 1\ 0\ 0\ 0,\ \\textsc{HELAMP}\ 1\ 0\ 0\ 0\ 1\ 0)$\\\\\n')
        f.write('\t\hline\n')
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[0],  R_00[0],  R_10[0],  sample[19], R_00[19], R_10[19]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[1],  R_00[1],  R_10[1],  sample[20], R_00[20], R_10[20]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[2],  R_00[2],  R_10[2],  sample[21], R_00[21], R_10[21]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[3],  R_00[3],  R_10[3],  sample[22], R_00[22], R_10[22]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[4],  R_00[4],  R_10[4],  sample[23], R_00[23], R_10[23]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[5],  R_00[5],  R_10[5],  sample[24], R_00[24], R_10[24]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[6],  R_00[6],  R_10[6],  sample[25], R_00[25], R_10[25]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[7],  R_00[7],  R_10[7],  sample[26], R_00[26], R_10[26]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[8],  R_00[8],  R_10[8],  sample[27], R_00[27], R_10[27]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[9],  R_00[9],  R_10[9],  sample[28], R_00[28], R_10[28]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[10], R_00[10], R_10[10], sample[29], R_00[29], R_10[29]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[11], R_00[11], R_10[11], sample[30], R_00[30], R_10[30]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[12], R_00[12], R_10[12], sample[31], R_00[31], R_10[31]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[13], R_00[13], R_10[13], sample[32], R_00[32], R_10[32]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[14], R_00[14], R_10[14], sample[33], R_00[33], R_10[33]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[15], R_00[15], R_10[15], sample[34], R_00[34], R_10[34]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[16], R_00[16], R_10[16], sample[35], R_00[35], R_10[35]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[17], R_00[17], R_10[17], sample[36], R_00[36], R_10[36]))
        f.write('\t{:^4}& ({:^5}, {:^5})& -    & -    \\\\\n'.format(sample[18], R_00[18], R_10[18]))
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t}\n')
        f.write('\t\label{table8-13-2}\n')
        f.write('\end{table}\n')
        f.write('\n\n')


def main():
    make_sys()

if __name__ == '__main__':
    main()
