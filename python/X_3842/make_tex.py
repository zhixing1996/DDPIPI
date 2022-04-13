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
from tools import *

def usage():
    sys.stdout.write('''
NAME
    make_tex.py

SYNOPSIS
    ./make_tex.py [mode]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    December 2020
\n''')

def make_total(patch):
    sample, N_sig, N_side, N_sig_err, N_side_err = [], [], [], [], []
    lum, xs, xs_err, eff, ISR = [], [], [], [], []
    SAMPLES = [4190, 4200, 4210, 4220, 4230, 4237, 4246, 4260, 4270, 4290, 4315, 4340, 4360, 4380, 4400, 4420, 4440, 4600, 4620, 4640, 4660, 4680, 4700, 4750, 4780, 4840, 4914, 4946]
    for SAMPLE in SAMPLES:
        with open('./txts/xs_info_'+str(SAMPLE)+'_read_'+patch+'.txt', 'r') as f:
            for line in f.readlines():
                fargs = map(float, line.strip('\n').strip().split())
                sample.append(int(fargs[0]))
                N_sig.append(int(fargs[1]))
                N_sig_err.append(int(fargs[2]))
                eff.append(round(float(fargs[8]), 1))
                ISR.append(float(fargs[9]))
                lum.append(round(fargs[11], 1))
                xs.append(round(fargs[13], 1))
                xs_err.append(round(fargs[14], 1))
    xs_sys_err = []
    with open('./sys_err/sum/txts/sys_err_total.txt', 'r') as f:
        count = 0
        for line in f.readlines():
            fargs = map(float, line.strip('\n').strip().split())
            xs_sys_err.append(abs(round(xs[count]*fargs[1]/100., 1)))
            count += 1
    sample_upl, significance = [], []
    with open('./txts/significance.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip('@').strip().split())
                significance.append(round(fargs[1], 1))
                if round(fargs[1], 3) < 5: sample_upl.append(int(fargs[0]))
            except:
                '''
                '''

    # upl = {}
    upl = []
    for SAM in sample_upl:
        with open('./txts/upl_'+str(SAM)+'.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                try:
                    fargs = map(float, line.strip('\n').strip().split())
                    # upl[SAM] = round(fargs[1], 1)
                    upl.append(round(fargs[1], 1))
                except:
                    '''
                    '''

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/xs_X_3842.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Results of $e^{+}e^{-}\\rightarrow \\rightarrow \pi^{+}\pi^{-}X(3842)\\rightarrow\pi^{+}\pi^{-}D^{+}D^{-}$, the first uncertainty is statistical and the second systematic. The negative significance means that the fitted signal number is negative. $\sigma$ and $\sigma_{\\rm ul}$ are the criss section of $\ee\\rightarrow\pi^{+}\pi^{-}X(3842)\\rightarrow\pi^{+}\pi^{-}D^{+}D^{-}$ process and the upper limit of cross section at 90\% confidence level. For the estimation of significance, only statistical uncertainty is considered.}\n')
        f.write('\t% \\resizebox{\\textwidth}{55mm}{\n')
        f.write('\t\\begin{tabular}{c c c c r@{$\pm$}l r@{$\pm$}c@{$\pm$}l c c}\n')
        f.write('\t\\toprule\n')
        f.write('\t\hline\hline\n')
        f.write('$\sqrt{s}$ (MeV) & $\epsilon (\%)$ & $(1+\delta)$ & $\mathscr{L}$ ($\\rm{pb}^{-1}$) & \multicolumn{2}{c}{$N$} & \multicolumn{3}{c}{$\sigma\ (\\rm{pb})$} & Significance & $\sigma_{\\rm{ul}}$ (\\rm{pb}) \\\\\n')
        f.write('\t\hline\n')
        f.write('\t\midrule\n')
        count = 0
        for SAM in sample:
            f.write('\t{:^7} & {:^3} & {:^4} & {:^6}  & {:^4} & {:^4} & {:^4} & {:^4} & {:^4} & ${:^4}\sigma$ & {:^4} \\\\\n'.format(ECMS(SAM)*1000, eff[count], ISR[count], lum[count], N_sig[count], N_sig_err[count], xs[count], xs_err[count], xs_sys_err[count], significance[count], upl[count]))
            count += 1
        f.write('\t\hline\hline\n')
        f.write('\t\\bottomrule\n')
        f.write('\t\end{tabular}\n')
        f.write('\t% }\n')
        f.write('\t\label{tableapp11-1}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    patch = args[0]

    make_total(patch)

if __name__ == '__main__':
    main()
