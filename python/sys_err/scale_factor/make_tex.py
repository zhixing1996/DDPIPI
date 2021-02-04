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
    with open('./txts/sys_err_scale_factor.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                sample.append(int(fargs[0]*1000))
                sys_err.append(fargs[1])
            except:
                '''
                '''
    
    m_Kpipi_scale = []
    for SAM in sample:
        with open('./txts/scale_factor_m_Kpipi_'+str(SAM)+'.txt') as f:
            lines = f.readlines()
            for line in lines:
                try:
                    fargs = map(float, line.strip('\n').strip().split())
                    m_Kpipi_scale.append(round(fargs[0], 3))
                except:
                    '''
                    '''

    rm_Dpipi_scale = []
    for SAM in sample:
        with open('./txts/scale_factor_rm_Dpipi_'+str(SAM)+'.txt') as f:
            lines = f.readlines()
            for line in lines:
                try:
                    fargs = map(float, line.strip('\n').strip().split())
                    rm_Dpipi_scale.append(round(fargs[0], 3))
                except:
                    '''
                    '''

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')

    with open('./texs/scale_factor.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{$f_{1}$ and $f_{2}$ values.}\n')
        f.write('\t\\begin{tabular}{cc|cc}\n')
        f.write('\t\hline\hline\n')
        f.write('\tData Sample& $(f_{1},\ f_{2})$ & Data Sample& $(f_{1},\ f_{2})$\\\\\n')
        f.write('\t\hline\n')
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[0],  m_Kpipi_scale[0],  rm_Dpipi_scale[0],  sample[16], m_Kpipi_scale[16], rm_Dpipi_scale[16]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[1],  m_Kpipi_scale[1],  rm_Dpipi_scale[1],  sample[17], m_Kpipi_scale[17], rm_Dpipi_scale[17]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[2],  m_Kpipi_scale[2],  rm_Dpipi_scale[2],  sample[18], m_Kpipi_scale[18], rm_Dpipi_scale[18]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[3],  m_Kpipi_scale[3],  rm_Dpipi_scale[3],  sample[19], m_Kpipi_scale[19], rm_Dpipi_scale[19]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[4],  m_Kpipi_scale[4],  rm_Dpipi_scale[4],  sample[20], m_Kpipi_scale[20], rm_Dpipi_scale[20]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[5],  m_Kpipi_scale[5],  rm_Dpipi_scale[5],  sample[21], m_Kpipi_scale[21], rm_Dpipi_scale[21]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[6],  m_Kpipi_scale[6],  rm_Dpipi_scale[6],  sample[22], m_Kpipi_scale[22], rm_Dpipi_scale[22]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[7],  m_Kpipi_scale[7],  rm_Dpipi_scale[7],  sample[23], m_Kpipi_scale[23], rm_Dpipi_scale[23]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[8],  m_Kpipi_scale[8],  rm_Dpipi_scale[8],  sample[24], m_Kpipi_scale[24], rm_Dpipi_scale[24]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[9],  m_Kpipi_scale[9],  rm_Dpipi_scale[9],  sample[25], m_Kpipi_scale[25], rm_Dpipi_scale[25]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[10], m_Kpipi_scale[10], rm_Dpipi_scale[10], sample[26], m_Kpipi_scale[26], rm_Dpipi_scale[26]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[11], m_Kpipi_scale[11], rm_Dpipi_scale[11], sample[27], m_Kpipi_scale[27], rm_Dpipi_scale[27]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[12], m_Kpipi_scale[12], rm_Dpipi_scale[12], sample[28], m_Kpipi_scale[28], rm_Dpipi_scale[28]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[13], m_Kpipi_scale[13], rm_Dpipi_scale[13], sample[29], m_Kpipi_scale[29], rm_Dpipi_scale[29]))
        f.write('\t{:^4}& ({:^5}, {:^5})& {:^4}& ({:^5}, {:^5})\\\\\n'.format(sample[14], m_Kpipi_scale[14], rm_Dpipi_scale[14], sample[30], m_Kpipi_scale[30], rm_Dpipi_scale[30]))
        f.write('\t{:^4}& ({:^5}, {:^5})& -    & -    \\\\\n'.format(sample[15], m_Kpipi_scale[15], rm_Dpipi_scale[15]))
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t\label{table8-3-1}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

    with open('./texs/scale_factor_sys.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Systematic uncertainty caused by $f_{1}$ and $f_{2}$.}\n')
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
        f.write('\t\label{table8-3-2}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

def main():
    make_sys()

if __name__ == '__main__':
    main()
