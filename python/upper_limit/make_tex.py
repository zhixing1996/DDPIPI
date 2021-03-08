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

def make_significance():
    sample, significance  = [], []
    sample_upl, upl = [], []
    with open('../fit_xs/txts/significance_total.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip('@').strip().split())
                sample.append(int(fargs[0]))
                significance.append(round(fargs[1], 1))
                if round(fargs[1], 2) < 5: sample_upl.append(int(fargs[0]))
            except:
                '''
                '''

    for SAM in sample_upl:
        with open('./txts/upl_'+str(SAM)+'.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                try:
                    fargs = map(float, line.strip('\n').strip().split())
                    upl.append(round(fargs[1], 1))
                except:
                    '''
                    '''

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/significance.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Statistical significance of each data sample.}\n')
        f.write('\t\\begin{tabular}{cc|cc}\n')
        f.write('\t\hline\hline\n')
        f.write('\tData Sample& Significance & Data Sample& Significance\\\\\n')
        f.write('\t\hline\n')
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[0], significance[0], sample[16], significance[16]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[1], significance[1], sample[17], significance[17]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[2], significance[2], sample[18], significance[18]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[3], significance[3], sample[19], significance[19]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[4], significance[4], sample[20], significance[20]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[5], significance[5], sample[21], significance[21]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[6], significance[6], sample[22], significance[22]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[7], significance[7], sample[23], significance[23]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[8], significance[8], sample[24], significance[24]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[9], significance[9], sample[25], significance[25]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[10], significance[10], sample[26], significance[26]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[11], significance[11], sample[27], significance[27]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[12], significance[12], sample[28], significance[28]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[13], significance[13], sample[29], significance[29]))
        f.write('\t{:^4}& ${:^4}\sigma$& {:^4}& ${:^4}\sigma$\\\\\n'.format(sample[14], significance[14], sample[30], significance[30]))
        f.write('\t{:^4}& ${:^4}\sigma$& -    & -    \\\\\n'.format(sample[15], significance[15]))
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t\label{table9-1}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/upl.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Upper limits of corresponding data sample.}\n')
        f.write('\t\\begin{tabular}{cc|cc}\n')
        f.write('\t\hline\hline\n')
        f.write('\tData Sample& $\sigma_{\\rm{upl}}(\\rm{pb})$ & Data Sample& $\sigma_{\\rm{upl}}(\\rm{pb})$\\\\\n')
        f.write('\t\hline\n')
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(4190, upl[0], 4270, upl[6]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(4200, upl[1], 4280, upl[7]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(4210, upl[2], 4310, upl[8]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(4220, upl[3], 4530, upl[9]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(4237, upl[4], 4575, upl[10]))
        f.write('\t{:^4}& {:^4}& {:^4}& {:^4}\\\\\n'.format(4245, upl[5], 4610, upl[11]))
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t\label{table9-2}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

def main():
    make_significance()

if __name__ == '__main__':
    main()
