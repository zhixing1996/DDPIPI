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

def make_BW_4390_BW_4700():
    S1, S2 = 18, 64
    Labels = [
              [S1, 'Solution \uppercase\expandafter{\\romannumeral1}'],
              [S2, 'Solution \uppercase\expandafter{\\romannumeral2}']
             ]
    Parameters = [
                  '$M_{0}\ (\\rm{MeV}/c^{2})$',
                  '$\Gamma_{0}\ (\\rm{MeV})$',
                  '$M_{1}\ (\\rm{MeV}/c^{2})$',
                  '$\Gamma_{1}\ (\\rm{MeV})$',
                  '$\Gamma^{\ee}_{0}\mathscr{B}_{0}\ (\\rm{eV})$',
                  '$\Gamma^{\ee}_{1}\mathscr{B}_{1}\ (\\rm{eV})$',
                  '$\phi_{1}\ (\\rm{rad})$'
                 ]
    Variables = [
                 'BW_4390_mass',
                 'BW_4390_width',
                 'BW_4390_BrGam',
                 'BW_4700_mass',
                 'BW_4700_width',
                 'BW_4700_BrGam',
                 'BW_4700_phase'
                ]

    Solutions = {}

    for Label in Labels:
        iloop, _ = Label
        Solutions.update({iloop:{}})
        with open('./txts/params_BW_4390_BW_4700_' + str(iloop) + '.txt', 'r') as f:
            for line in f.readlines():
                fargs = line.strip().split()
                for Variable in Variables:
                    if Variable == fargs[0]:
                        if 'mass' in Variable or 'width' in Variable:
                            fargs[1] = float(fargs[1])*1000
                            fargs[2] = float(fargs[2])*1000
                        if 'phase' in fargs[0]:
                            fargs[1] = float(fargs[1])
                            while not (fargs[1] > 0 and fargs[1] < 2 * pi):
                                if fargs[1] > 0.: fargs[1] -= 2 * pi
                                else: fargs[1] += 2 * pi
                        if fargs[0] == 'phsp_c' and fargs[1] < 0: fargs[1] = abs(fargs[1])
                        Solutions[iloop].update({Variable: [round(float(fargs[1]), 1), round(float(fargs[2]), 1)]})

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
        
    with open('./texs/solutions2.tex', 'w') as f:
        f.write('\\begin{table*}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{The fitted parameters of the cross sections of $e^{+}e^{-}\\rightarrow\pi^{+}\pi^{-}D^{+}D^{-}$ with the coherent sum of two Breit-Wigner functions. The uncertainties are statistical.}\n')
        f.write('\t\\begin{tabular}{crrr}\n')
        f.write('\t\hline\hline\n')
        f.write('\tParameters & ' + Labels[0][1] + ' & ' + Labels[1][1] + ' &  \\\\\n')
        f.write('\t\hline\n')
        f.write('\t ' + Parameters[0] + ' & \multicolumn{2}{c}{' + str(Solutions[S1]['BW_4390_mass'][0])  + '$\pm$' + str(Solutions[S1]['BW_4390_mass'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[1] + ' & \multicolumn{2}{c}{' + str(Solutions[S1]['BW_4390_width'][0]) + '$\pm$' + str(Solutions[S1]['BW_4390_width'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[2] + ' & \multicolumn{2}{c}{' + str(Solutions[S1]['BW_4700_mass'][0])  + '$\pm$' + str(Solutions[S1]['BW_4700_mass'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[3] + ' & \multicolumn{2}{c}{' + str(Solutions[S1]['BW_4700_width'][0]) + '$\pm$' + str(Solutions[S1]['BW_4700_width'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[4] + ' & ' + str(Solutions[S1]['BW_4390_BrGam'][0]) + '$\pm$' + str(Solutions[S1]['BW_4390_BrGam'][1]) 
                                      + ' & ' + str(Solutions[S2]['BW_4390_BrGam'][0]) + '$\pm$' + str(Solutions[S2]['BW_4390_BrGam'][1]) 
                                      + ' & \\\\\n')
        f.write('\t ' + Parameters[5] + ' & ' + str(Solutions[S1]['BW_4700_BrGam'][0]) + '$\pm$' + str(Solutions[S1]['BW_4700_BrGam'][1]) 
                                      + ' & ' + str(Solutions[S2]['BW_4700_BrGam'][0]) + '$\pm$' + str(Solutions[S2]['BW_4700_BrGam'][1]) 
                                      + ' & \\\\\n')
        f.write('\t ' + Parameters[6] + ' & ' + str(Solutions[S1]['BW_4700_phase'][0]) + '$\pm$' + str(Solutions[S1]['BW_4700_phase'][1]) 
                                      + ' & ' + str(Solutions[S2]['BW_4700_phase'][0]) + '$\pm$' + str(Solutions[S2]['BW_4700_phase'][1]) 
                                      + ' & \\\\\n')
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t\label{table_solution2}\n')
        f.write('\end{table*}\n')
        f.write('\n\n')

def make_BW_4390_BW_4700_PHSP():
    S1, S2, S3, S4 = 8, 12, 26, 28
    Labels = [[S1, 'Solution \uppercase\expandafter{\\romannumeral1}'],
              [S2, 'Solution \uppercase\expandafter{\\romannumeral2}'],
              [S3, 'Solution \uppercase\expandafter{\\romannumeral3}'],
              [S4, 'Solution \uppercase\expandafter{\\romannumeral4}']]
    Parameters = ['$c\ (\\rm{MeV}^{-3/2})$',
                  '$M_{0}\ (\\rm{MeV}/c^{2})$',
                  '$\Gamma_{0}\ (\\rm{MeV})$',
                  '$M_{1}\ (\\rm{MeV}/c^{2})$',
                  '$\Gamma_{1}\ (\\rm{MeV})$',
                  '$\Gamma^{\ee}_{0}\mathscr{B}_{0}\ (\\rm eV)$',
                  '$\Gamma^{\ee}_{1}\mathscr{B}_{1}\ (\\rm eV)$',
                  '$\phi_{1}\ (\\rm{rad})$',
                  '$\phi_{2}\ (\\rm{rad})$'
                  ]
    Variables = ['BW_4390_mass',
                 'BW_4390_width',
                 'BW_4390_BrGam',
                 'BW_4700_mass',
                 'BW_4700_width',
                 'BW_4700_BrGam',
                 'BW_4700_phase',
                 'phsp_c',
                 'phsp_phase']

    Solutions = {}

    for Label in Labels:
        iloop, _ = Label
        Solutions.update({iloop:{}})
        with open('./txts/params_BW_4390_BW_4700_PHSP_' + str(iloop) + '.txt', 'r') as f:
            for line in f.readlines():
                fargs = line.strip().split()
                for Variable in Variables:
                    if Variable == fargs[0]:
                        if 'mass' in Variable or 'width' in Variable:
                            fargs[1] = float(fargs[1])*1000
                            fargs[2] = float(fargs[2])*1000
                        if 'phase' in fargs[0]:
                            fargs[1] = float(fargs[1])
                            while not (fargs[1] > 0 and fargs[1] < 2 * pi):
                                if fargs[1] > 0.: fargs[1] -= 2 * pi
                                else: fargs[1] += 2 * pi
                        if fargs[0] == 'phsp_c' and fargs[1] < 0: fargs[1] = abs(fargs[1])
                        Solutions[iloop].update({Variable: [round(float(fargs[1]), 1), round(float(fargs[2]), 1)]})

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
        
    with open('./texs/solutions1.tex', 'w') as f:
        f.write('\\begin{table*}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{The fitted parameters of the cross sections of $e^{+}e^{-}\\rightarrow\pi^{+}\pi^{-}D^{+}D^{-}$ with the coherent sum of two Breit-Wigner functions and a phase space term. The uncertainties are statistical.}\n')
        f.write('\t\\begin{tabular}{crrrrr}\n')
        f.write('\t\hline\hline\n')
        f.write('\tParameters & ' + Labels[0][1] + ' & ' + Labels[1][1] + ' & ' + Labels[2][1] + ' & ' + Labels[3][1] + ' &  \\\\\n')
        f.write('\t\hline\n')
        f.write('\t ' + Parameters[0] + ' & \multicolumn{4}{c}{' + str(Solutions[S2]['phsp_c'][0])        + '$\pm$' + str(Solutions[S2]['phsp_c'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[1] + ' & \multicolumn{4}{c}{' + str(Solutions[S2]['BW_4390_mass'][0])  + '$\pm$' + str(Solutions[S2]['BW_4390_mass'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[2] + ' & \multicolumn{4}{c}{' + str(Solutions[S2]['BW_4390_width'][0]) + '$\pm$' + str(Solutions[S2]['BW_4390_width'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[3] + ' & \multicolumn{4}{c}{' + str(Solutions[S2]['BW_4700_mass'][0])  + '$\pm$' + str(Solutions[S2]['BW_4700_mass'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[4] + ' & \multicolumn{4}{c}{' + str(Solutions[S2]['BW_4700_width'][0]) + '$\pm$' + str(Solutions[S2]['BW_4700_width'][1]) + '} & \\\\\n')
        f.write('\t ' + Parameters[5] + ' & ' + str(Solutions[S2]['BW_4390_BrGam'][0]) + '$\pm$' + str(Solutions[S2]['BW_4390_BrGam'][1]) 
                                      + ' & ' + str(Solutions[S2]['BW_4390_BrGam'][0]) + '$\pm$' + str(Solutions[S2]['BW_4390_BrGam'][1]) 
                                      + ' & ' + str(Solutions[S3]['BW_4390_BrGam'][0]) + '$\pm$' + str(Solutions[S3]['BW_4390_BrGam'][1]) 
                                      + ' & ' + str(Solutions[S4]['BW_4390_BrGam'][0]) + '$\pm$' + str(Solutions[S4]['BW_4390_BrGam'][1]) 
                                      + ' & \\\\\n')
        f.write('\t ' + Parameters[6] + ' & ' + str(Solutions[S1]['BW_4700_BrGam'][0]) + '$\pm$' + str(Solutions[S1]['BW_4700_BrGam'][1]) 
                                      + ' & ' + str(Solutions[S2]['BW_4700_BrGam'][0]) + '$\pm$' + str(Solutions[S2]['BW_4700_BrGam'][1]) 
                                      + ' & ' + str(Solutions[S3]['BW_4700_BrGam'][0]) + '$\pm$' + str(Solutions[S3]['BW_4700_BrGam'][1]) 
                                      + ' & ' + str(Solutions[S4]['BW_4700_BrGam'][0]) + '$\pm$' + str(Solutions[S4]['BW_4700_BrGam'][1]) 
                                      + ' & \\\\\n')
        f.write('\t ' + Parameters[7] + ' & ' + str(Solutions[S1]['BW_4700_phase'][0]) + '$\pm$' + str(Solutions[S1]['BW_4700_phase'][1]) 
                                      + ' & ' + str(Solutions[S2]['BW_4700_phase'][0]) + '$\pm$' + str(Solutions[S2]['BW_4700_phase'][1]) 
                                      + ' & ' + str(Solutions[S3]['BW_4700_phase'][0]) + '$\pm$' + str(Solutions[S3]['BW_4700_phase'][1]) 
                                      + ' & ' + str(Solutions[S4]['BW_4700_phase'][0]) + '$\pm$' + str(Solutions[S4]['BW_4700_phase'][1]) 
                                      + ' & \\\\\n')
        f.write('\t ' + Parameters[8] + ' & ' + str(Solutions[S1]['phsp_phase'][0]) + '$\pm$' + str(Solutions[S1]['phsp_phase'][1]) 
                                      + ' & ' + str(Solutions[S2]['phsp_phase'][0]) + '$\pm$' + str(Solutions[S2]['phsp_phase'][1]) 
                                      + ' & ' + str(Solutions[S3]['phsp_phase'][0]) + '$\pm$' + str(Solutions[S3]['phsp_phase'][1]) 
                                      + ' & ' + str(Solutions[S4]['phsp_phase'][0]) + '$\pm$' + str(Solutions[S4]['phsp_phase'][1]) 
                                      + ' & \\\\\n')
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t\label{table_solution1}\n')
        f.write('\end{table*}\n')
        f.write('\n\n')

def main():
    make_BW_4390_BW_4700_PHSP()
    make_BW_4390_BW_4700()

if __name__ == '__main__':
    main()
