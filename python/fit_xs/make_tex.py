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
    lum, xs, xs_err = [], [], []
    SAMPLES = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700]
    for SAMPLE in SAMPLES:
        with open('./txts/xs_info_'+str(SAMPLE)+'_read_'+patch+'.txt', 'r') as f:
            for line in f.readlines():
                fargs = map(float, line.strip('\n').strip().split())
                sample.append(int(fargs[0]))
                N_sig.append(int(fargs[1]))
                N_sig_err.append(int(fargs[2]))
                N_side.append(int(fargs[3]))
                N_side_err.append(int(fargs[4]))
                lum.append(round(fargs[20], 2))
                xs.append(round(fargs[22], 1))
                xs_err.append(round(fargs[23], 1))
    xs_sys_err = []
    with open('../sys_err/sum/txts/sys_err_total.txt', 'r') as f:
        count = 0
        for line in f.readlines():
            fargs = map(float, line.strip('\n').strip().split())
            xs_sys_err.append(round(xs[count]*fargs[1]/100., 1))
            count += 1
    sample_upl, significance = [], []
    with open('./txts/significance_total.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip('@').strip().split())
                significance.append(round(fargs[1], 1))
                if round(fargs[1], 2) < 5: sample_upl.append(int(fargs[0]))
            except:
                '''
                '''

    upl = {}
    for SAM in sample_upl:
        with open('../upper_limit/txts/upl_'+str(SAM)+'.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                try:
                    fargs = map(float, line.strip('\n').strip().split())
                    upl[SAM] = round(fargs[1], 1)
                except:
                    '''
                    '''

    with open('./texs/xs_total.tex', 'w') as f:
        f.write('\\begin{table}[htp]\n')
        f.write('\t\centering\n')
        f.write('\t\caption{Born cross section of $e^{+}e^{-}\\rightarrow\pi^{+}\pi^{-}D^{+}D^{-}$, the first uncertainties are statistical and the second systematic.}\n')
        f.write('\t\\resizebox{\\textwidth}{65mm}{\n')
        f.write('\t\\begin{tabular}{ccccccccc}\n')
        f.write('\t\hline\hline\n')
        f.write('Sample & $\sqrt{s}$ (MeV) & $\mathscr{L}$ ($\\rm{pb}^{-1}$) & $N_{\\rm{signal}}$ & $N_{\\rm{sideband}}$ & $\sigma\ (\\rm{pb})$ & Statistical Significance & $\sigma_{\\rm{upl}}$ (\\rm{pb}) &\\\\\n')
        f.write('\t\hline\n')
        count = 0
        for SAM in sample:
            if SAM in sample_upl:
                f.write('\t{:^4}& {:^7} & {:^6}  & ${:^4} \pm {:^4}$ & ${:^4} \pm {:^4}$  & ${:^4} \pm {:^4} \pm {:^4}$ & ${:^4}\sigma$ & {:^4} &\\\\\n'.format(SAM, ECMS(SAM)*1000, lum[count], N_sig[count], N_sig_err[count], N_side[count], N_side_err[count], xs[count], xs_err[count], xs_sys_err[count], significance[count], upl[SAM]))
            else:
                f.write('\t{:^4}& {:^7} & {:^6}  & ${:^4} \pm {:^4}$ & ${:^4} \pm {:^4}$  & ${:^4} \pm {:^4} \pm {:^4}$ & ${:^4}\sigma$ & -     &\\\\\n'.format(SAM, ECMS(SAM)*1000, lum[count], N_sig[count], N_sig_err[count], N_side[count], N_side_err[count], xs[count], xs_err[count], xs_sys_err[count], significance[count]))
            count += 1
        f.write('\t\hline\hline\n')
        f.write('\t\end{tabular}\n')
        f.write('\t}\n')
        f.write('\t\label{table10-1}\n')
        f.write('\end{table}\n')
        f.write('\n\n')

def make_xs(patch):
    N_sig, N_side, eff0, eff1, eff2, one_del0, one_del1, one_del2, VP, lum = [], [], [], [], [], [], [], [], [], []
    sample, N_sig_err, N_side_err, xs, xs_err = [], [], [], [], []
    F_K_p, F_m_pipi, F_VrVz, F_m_Kpipi, F_rm_Dpipi = [], [], [], [], []
    SAMPLES = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700]
    for SAMPLE in SAMPLES:
        with open('./txts/xs_info_'+str(SAMPLE)+'_read_'+patch+'.txt', 'r') as f:
            for line in f.readlines():
                fargs = map(float, line.strip('\n').strip().split())
                sample.append(int(fargs[0]))
                N_sig.append(int(fargs[1]))
                N_sig_err.append(int(fargs[2]))
                N_side.append(int(fargs[3]))
                N_side_err.append(int(fargs[4]))
                F_K_p.append(round(fargs[5], 2))
                F_m_pipi.append(round(fargs[6], 2))
                F_VrVz.append(round(fargs[7], 2))
                F_m_Kpipi.append(round(fargs[8], 2))
                F_rm_Dpipi.append(round(fargs[9], 2))
                eff0.append(round(fargs[10], 1))
                eff1.append(round(fargs[11], 1))
                eff2.append(round(fargs[12], 1))
                one_del0.append(fargs[16])
                one_del1.append(fargs[17])
                one_del2.append(fargs[18])
                VP.append(fargs[19])
                lum.append(round(fargs[20], 2))
                xs.append(round(fargs[22], 1))
                xs_err.append(round(fargs[23], 1))

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/xs_info.tex', 'w') as f:
        for i in xrange(6):
            if not i == 5:
                f.write('\\begin{table}[htp]\n')
                f.write('\t\centering\n')
                f.write('\t\caption{Cross sections of $e^{+}e^{-}\\rightarrow \pi^{+}\pi^{-}D^{+}D^{-}$.}\n')
                f.write('\t\\begin{tabular}{ccccccc}\n')
                f.write('\t\hline\hline\n')
                f.write('\tData Sample& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(sample[0+i*5], sample[1+i*5], sample[2+i*5], sample[3+i*5], sample[4+i*5]))
                f.write('\t\hline\n')
                f.write('\t$N'+'_{\\rm{signal}}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N_sig[0+i*5], N_sig_err[0+i*5], N_sig[1+i*5], N_sig_err[1+i*5], N_sig[2+i*5], N_sig_err[2+i*5], N_sig[3+i*5], N_sig_err[3+i*5], N_sig[4+i*5], N_sig_err[4+i*5]))
                f.write('\t$N'+'_{\\rm{sideband}}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N_side[0+i*5], N_side_err[0+i*5], N_side[1+i*5], N_side_err[1+i*5], N_side[2+i*5], N_side_err[2+i*5], N_side[3+i*5], N_side_err[3+i*5], N_side[4+i*5], N_side_err[4+i*5]))
                f.write('\t$'+'f^{K\\nrightarrow}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_K_p[0+i*5], F_K_p[1+i*5], F_K_p[2+i*5], F_K_p[3+i*5], F_K_p[4+i*5]))
                f.write('\t$'+'f^{M(\pi^{+}\pi^{-})}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_m_pipi[0+i*5], F_m_pipi[1+i*5], F_m_pipi[2+i*5], F_m_pipi[3+i*5], F_m_pipi[4+i*5]))
                f.write('\t$'+'f^{V_{xy, z}}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_VrVz[0+i*5], F_VrVz[1+i*5], F_VrVz[2+i*5], F_VrVz[3+i*5], F_VrVz[4+i*5]))
                f.write('\t$'+'f^{M(K^{-}\pi^{+}\pi^{+})}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_m_Kpipi[0+i*5], F_m_Kpipi[1+i*5], F_m_Kpipi[2+i*5], F_m_Kpipi[3+i*5], F_m_Kpipi[4+i*5]))
                f.write('\t$'+'f^{RM(D^{+}\pi_{0}^{+}\pi_{0}^{-})}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_rm_Dpipi[0+i*5], F_rm_Dpipi[1+i*5], F_rm_Dpipi[2+i*5], F_rm_Dpipi[3+i*5], F_rm_Dpipi[4+i*5]))
                f.write('\t$\epsilon'+'_{0}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff0[0+i*5], eff0[1+i*5], eff0[2+i*5], eff0[3+i*5], eff0[4+i*5]))
                f.write('\t$\epsilon'+'_{1}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff1[0+i*5], eff1[1+i*5], eff1[2+i*5], eff1[3+i*5], eff1[4+i*5]))
                f.write('\t$\epsilon'+'_{2}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff2[0+i*5], eff2[1+i*5], eff2[2+i*5], eff2[3+i*5], eff2[4+i*5]))
                f.write('\t$'+'\mathscr{L}(\\rm{pb}^{-1})'+'$ & {:^6}& {:^6}& {:^6}& {:^6}& {:^6}&\\\\\n'.format(lum[0+i*5], lum[1+i*5], lum[2+i*5], lum[3+i*5], lum[4+i*5]))
                f.write('\t$(1+\delta)'+'_{0}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del0[0+i*5], one_del0[1+i*5], one_del0[2+i*5], one_del0[3+i*5], one_del0[4+i*5]))
                f.write('\t$(1+\delta)'+'_{1}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del1[0+i*5], one_del1[1+i*5], one_del1[2+i*5], one_del1[3+i*5], one_del1[4+i*5]))
                f.write('\t$(1+\delta)'+'_{2}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del2[0+i*5], one_del2[1+i*5], one_del2[2+i*5], one_del2[3+i*5], one_del2[4+i*5]))
                f.write('\t$\\frac'+'{1}{|1-\Pi|^{2}}_{i}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(VP[0+i*5], VP[1+i*5], VP[2+i*5], VP[3+i*5], VP[4+i*5]))
                f.write('\t$\mathscr{B}(D^{+}\\rightarrow K^{-}\pi^{+}\pi^{+})$ & 9.38\%& 9.38\%& 9.38\%& 9.38\%& 9.38\%&\\\\\n')
                f.write('\t$\sigma(\\rm{pb})$ '+'& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(xs[0+i*5], xs_err[0+i*5], xs[1+i*5], xs_err[1+i*5], xs[2+i*5], xs_err[2+i*5], xs[3+i*5], xs_err[3+i*5], xs[4+i*5], xs_err[4+i*5]))
                f.write('\t\hline\hline\n')
                f.write('\t\end{tabular}\n')
                f.write('\t\label{table6-'+str(2+i+8)+'}\n')
                f.write('\end{table}\n')
                f.write('\n\n')
            if i == 5:
                f.write('\\begin{table}[htp]\n')
                f.write('\t\centering\n')
                f.write('\t\caption{Cross sections of $e^{+}e^{-}\\rightarrow \pi^{+}\pi^{-}D^{+}D^{-}$.}\n')
                f.write('\t\\resizebox{\\textwidth}{45mm}{\n')
                f.write('\t\\begin{tabular}{cccccccc}\n')
                f.write('\t\hline\hline\n')
                f.write('\tData Sample& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(sample[0+i*5], sample[1+i*5], sample[2+i*5], sample[3+i*5], sample[4+i*5], sample[5+i*5]))
                f.write('\t\hline\n')
                f.write('\t$N'+'_{\\rm{signal}}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N_sig[0+i*5], N_sig_err[0+i*5], N_sig[1+i*5], N_sig_err[1+i*5], N_sig[2+i*5], N_sig_err[2+i*5], N_sig[3+i*5], N_sig_err[3+i*5], N_sig[4+i*5], N_sig_err[4+i*5], N_sig[5+i*5], N_sig_err[5+i*5]))
                f.write('\t$N'+'_{\\rm{sideband}}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N_side[0+i*5], N_side_err[0+i*5], N_side[1+i*5], N_side_err[1+i*5], N_side[2+i*5], N_side_err[2+i*5], N_side[3+i*5], N_side_err[3+i*5], N_side[4+i*5], N_side_err[4+i*5], N_side[5+i*5], N_side_err[5+i*5]))
                f.write('\t$'+'f^{K\\nrightarrow}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_K_p[0+i*5], F_K_p[1+i*5], F_K_p[2+i*5], F_K_p[3+i*5], F_K_p[4+i*5], F_K_p[5+i*5]))
                f.write('\t$'+'f^{M(\pi^{+}\pi^{-})}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_m_pipi[0+i*5], F_m_pipi[1+i*5], F_m_pipi[2+i*5], F_m_pipi[3+i*5], F_m_pipi[4+i*5], F_m_pipi[5+i*5]))
                f.write('\t$'+'f^{V_{xy, z}}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_VrVz[0+i*5], F_VrVz[1+i*5], F_VrVz[2+i*5], F_VrVz[3+i*5], F_VrVz[4+i*5], F_VrVz[5+i*5]))
                f.write('\t$'+'f^{M(K^{-}\pi^{+}\pi^{+})}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_m_Kpipi[0+i*5], F_m_Kpipi[1+i*5], F_m_Kpipi[2+i*5], F_m_Kpipi[3+i*5], F_m_Kpipi[4+i*5], F_m_Kpipi[5+i*5]))
                f.write('\t$'+'f^{RM(D^{+}\pi_{0}^{+}\pi_{0}^{-})}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(F_rm_Dpipi[0+i*5], F_rm_Dpipi[1+i*5], F_rm_Dpipi[2+i*5], F_rm_Dpipi[3+i*5], F_rm_Dpipi[4+i*5], F_rm_Dpipi[5+i*5]))
                f.write('\t$\epsilon'+'_{0}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff0[0+i*5], eff0[1+i*5], eff0[2+i*5], eff0[3+i*5], eff0[4+i*5], eff0[5+i*5]))
                f.write('\t$\epsilon'+'_{1}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff1[0+i*5], eff1[1+i*5], eff1[2+i*5], eff1[3+i*5], eff1[4+i*5], eff1[5+i*5]))
                f.write('\t$\epsilon'+'_{2}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff2[0+i*5], eff2[1+i*5], eff2[2+i*5], eff2[3+i*5], eff2[4+i*5], eff2[5+i*5]))
                f.write('\t$'+'\mathscr{L}(\\rm{pb}^{-1})'+'$ & {:^6}& {:^6}& {:^6}& {:^6}& {:^6}& {:^6}&\\\\\n'.format(lum[0+i*5], lum[1+i*5], lum[2+i*5], lum[3+i*5], lum[4+i*5], lum[5+i*5]))
                f.write('\t$(1+\delta)'+'_{0}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del0[0+i*5], one_del0[1+i*5], one_del0[2+i*5], one_del0[3+i*5], one_del0[4+i*5], one_del0[5+i*5]))
                f.write('\t$(1+\delta)'+'_{1}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del1[0+i*5], one_del1[1+i*5], one_del1[2+i*5], one_del1[3+i*5], one_del1[4+i*5], one_del1[5+i*5]))
                f.write('\t$(1+\delta)'+'_{2}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del2[0+i*5], one_del2[1+i*5], one_del2[2+i*5], one_del2[3+i*5], one_del2[4+i*5], one_del2[5+i*5]))
                f.write('\t$\\frac'+'{1}{|1-\Pi|^{2}}_{i}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(VP[0+i*5], VP[1+i*5], VP[2+i*5], VP[3+i*5], VP[4+i*5], VP[5+i*5]))
                f.write('\t$\mathscr{B}(D^{+}\\rightarrow K^{-}\pi^{+}\pi^{+})$ & 9.38\%& 9.38\%& 9.38\%& 9.38\%& 9.38\%& 9.38\%&\\\\\n')
                f.write('\t$\sigma(\\rm{pb})$ '+'& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(xs[0+i*5], xs_err[0+i*5], xs[1+i*5], xs_err[1+i*5], xs[2+i*5], xs_err[2+i*5], xs[3+i*5], xs_err[3+i*5], xs[4+i*5], xs_err[4+i*5], xs[5+i*5], xs_err[5+i*5]))
                f.write('\t\hline\hline\n')
                f.write('\t\end{tabular}\n')
                f.write('\t}\n')
                f.write('\t\label{table6-'+str(2+i+8)+'}\n')
                f.write('\end{table}\n')
                f.write('\n\n')

def make_simul():
    xs0, xs1, xs2 = [], [], []
    with open('./txts/xs_D1_2420_round3.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                xs0.append(fargs[4])
            except:
                '''
                '''
    with open('./txts/xs_psipp_round3.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                xs1.append(fargs[4])
            except:
                '''
                '''
    with open('./txts/xs_DDPIPI_round3.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                xs2.append(fargs[4])
            except:
                '''
                '''
    N0, N1, N2, eff0, eff1, eff2, one_del0, one_del1, one_del2, VP = [], [], [], [], [], [], [], [], [], []
    sample, lum, omega0, omega1, omega2, N0_err, N1_err, N2_err = [], [], [], [], [], [], [], []
    with open('./txts/xs_D1_2420_round3_num.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                N0.append(int(fargs[4]))
                N0_err.append(int(sqrt(3)*fargs[5]))
                eff0.append(round(fargs[7], 3))
                one_del0.append(round(fargs[8], 2))
            except:
                '''
                '''
    with open('./txts/xs_psipp_round3_num.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                sample.append(int(fargs[0]))
                lum.append(round(fargs[2], 2))
                N1.append(int(fargs[4]))
                N1_err.append(int(sqrt(3)*fargs[5]))
                eff1.append(round(fargs[7], 3))
                one_del1.append(round(fargs[8], 2))
                VP.append(round(fargs[9], 2))
            except:
                '''
                '''
    with open('./txts/xs_DDPIPI_round3_num.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                fargs = map(float, line.strip('\n').strip().split())
                N2.append(int(fargs[4]))
                N2_err.append(int(sqrt(3)*fargs[5]))
                eff2.append(round(fargs[7], 3))
                one_del2.append(round(fargs[8], 2))
            except:
                '''
                '''
    omega0, omega1, omega2 = [], [], []
    omega0_err, omega1_err, omega2_err = [], [], []
    num = 0
    for SAM in sample:
        with open('./txts/omega_' + str(SAM) + '.txt') as f:
            lines = f.readlines()
            if SAM > 4316:
                D1_2420_args = map(float, lines[0].strip().split())
                psipp_args = map(float, lines[1].strip().split())
                DDPIPI_args = map(float, lines[2].strip().split())
            else:
                psipp_args = map(float, lines[0].strip().split())
                DDPIPI_args = map(float, lines[1].strip().split())
        if SAM > 4316: omega0.append(round(D1_2420_args[0], 3))
        omega1.append(round(psipp_args[0], 3))
        omega2.append(round(DDPIPI_args[0], 3))
        if SAM > 4316: omega0_err.append(round(D1_2420_args[1], 3))
        omega1_err.append(round(psipp_args[1], 3))
        omega2_err.append(round(DDPIPI_args[1], 3))
        num += 1

    if not os.path.exists('./texs/'):
        os.makedirs('./texs/')
    with open('./texs/simul_fit.tex', 'w') as f:
        for i in xrange(6):
            if sample[0+i*5] > 4316: N00, N00_err = N0[0+i*5-14], N0_err[0+i*5-14]
            else: N00, N00_err = 0, 0
            if sample[1+i*5] > 4316: N01, N01_err = N0[1+i*5-14], N0_err[1+i*5-14]
            else: N01, N01_err = 0, 0
            if sample[2+i*5] > 4316: N02, N02_err = N0[2+i*5-14], N0_err[2+i*5-14]
            else: N02, N02_err = 0, 0
            if sample[3+i*5] > 4316: N03, N03_err = N0[3+i*5-14], N0_err[3+i*5-14]
            else: N03, N03_err = 0, 0
            if sample[4+i*5] > 4316: N04, N04_err = N0[4+i*5-14], N0_err[4+i*5-14]
            else: N04, N04_err = 0, 0
            if sample[0+i*5] > 4316: eff00 = eff0[0+i*5-14]*100
            else: eff00 = 0.
            if sample[1+i*5] > 4316: eff01 = eff0[1+i*5-14]*100
            else: eff01 = 0.
            if sample[2+i*5] > 4316: eff02 = eff0[2+i*5-14]*100
            else: eff02 = 0.
            if sample[3+i*5] > 4316: eff03 = eff0[3+i*5-14]*100
            else: eff03 = 0.
            if sample[4+i*5] > 4316: eff04 = eff0[4+i*5-14]*100
            else: eff04 = 0.
            if sample[0+i*5] > 4316: one_del00 = one_del0[0+i*5-14]
            else: one_del00 = 0.
            if sample[1+i*5] > 4316: one_del01 = one_del0[1+i*5-14]
            else: one_del01 = 0.
            if sample[2+i*5] > 4316: one_del02 = one_del0[2+i*5-14]
            else: one_del02 = 0.
            if sample[3+i*5] > 4316: one_del03 = one_del0[3+i*5-14]
            else: one_del03 = 0.
            if sample[4+i*5] > 4316: one_del04 = one_del0[4+i*5-14]
            else: one_del04 = 0.
            if sample[0+i*5] > 4316: omega00 = omega0[0+i*5-14]
            else: omega00 = 0.
            if sample[1+i*5] > 4316: omega01 = omega0[1+i*5-14]
            else: omega01 = 0.
            if sample[2+i*5] > 4316: omega02 = omega0[2+i*5-14]
            else: omega02 = 0.
            if sample[3+i*5] > 4316: omega03 = omega0[3+i*5-14]
            else: omega03 = 0.
            if sample[4+i*5] > 4316: omega04 = omega0[4+i*5-14]
            else: omega04 = 0.
            if sample[0+i*5] > 4316: omega00 = omega0[0+i*5-14]
            else: omega00 = 0.
            if sample[0+i*5] > 4316: omega00_err = omega0_err[0+i*5-14]
            else: omega00_err = 0.
            if sample[1+i*5] > 4316: omega01_err = omega0_err[1+i*5-14]
            else: omega01_err = 0.
            if sample[2+i*5] > 4316: omega02_err = omega0_err[2+i*5-14]
            else: omega02_err = 0.
            if sample[3+i*5] > 4316: omega03_err = omega0_err[3+i*5-14]
            else: omega03_err = 0.
            if sample[4+i*5] > 4316: omega04_err = omega0_err[4+i*5-14]
            else: omega04_err = 0.
            if i == 5:
                if sample[5+i*5] > 4316: N05, N05_err = N0[5+i*5-14], N0_err[5+i*5-14]
                else: N05, N05_err = 0, 0
                if sample[5+i*5] > 4316: eff05 = eff0[5+i*5-14]
                else: eff05 = 0.
                if sample[5+i*5] > 4316: one_del05 = one_del0[5+i*5-14]
                else: one_del05 = 0.
                if sample[5+i*5] > 4316: omega05 = omega0[5+i*5-14]
                else: omega05 = 0.
                if sample[5+i*5] > 4316: omega05_err = omega0_err[5+i*5-14]
                else: omega05_err = 0.
            if not i == 5:
                f.write('\\begin{table}[htp]\n')
                f.write('\t\centering\n')
                f.write('\t\caption{Fractions of $e^{+}e^{-}\\rightarrow D_{1}(2420)^{+}D^{-}$, $e^{+}e^{-}\\rightarrow\pi^{+}\pi^{-}\psi(3770)$, and $e^{+}e^{-}\\rightarrow\pi^{+}\pi^{-}D^{+}D^{-}(\sc{PHSP})$.}\n')
                f.write('\t\\begin{tabular}{ccccccc}\n')
                f.write('\t\hline\hline\n')
                f.write('\tData Sample& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(sample[0+i*5], sample[1+i*5], sample[2+i*5], sample[3+i*5], sample[4+i*5]))
                f.write('\t\hline\n')
                f.write('\t$N'+'_{0}^{\'}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N00, N00_err, N01, N01_err, N02, N02_err, N03, N03_err, N04, N04_err))
                f.write('\t$N'+'_{1}^{\'}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N1[0+i*5], N1_err[0+i*5], N1[1+i*5], N1_err[1+i*5], N1[2+i*5], N1_err[2+i*5], N1[3+i*5], N1_err[3+i*5], N1[4+i*5], N1_err[4+i*5]))
                f.write('\t$N'+'_{2}^{\'}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N2[0+i*5], N2_err[0+i*5], N2[1+i*5], N2_err[1+i*5], N2[2+i*5], N2_err[2+i*5], N2[3+i*5], N2_err[3+i*5], N2[4+i*5], N2_err[4+i*5]))
                f.write('\t$\epsilon'+'_{0}^{\'}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff00, eff01, eff02, eff03, eff04))
                f.write('\t$\epsilon'+'_{1}^{\'}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff1[0+i*5]*100, eff1[1+i*5]*100, eff1[2+i*5]*100, eff1[3+i*5]*100, eff1[4+i*5]*100))
                f.write('\t$\epsilon'+'_{2}^{\'}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff2[0+i*5]*100, eff2[1+i*5]*100, eff2[2+i*5]*100, eff2[3+i*5]*100, eff2[4+i*5]*100))
                f.write('\t$(1+\delta)'+'_{0}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del00, one_del01, one_del02, one_del03, one_del04))
                f.write('\t$(1+\delta)'+'_{1}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del1[0+i*5], one_del1[1+i*5], one_del1[2+i*5], one_del1[3+i*5], one_del1[4+i*5]))
                f.write('\t$(1+\delta)'+'_{2}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del2[0+i*5], one_del2[1+i*5], one_del2[2+i*5], one_del2[3+i*5], one_del2[4+i*5]))
                f.write('\t$\\frac'+'{1}{|1-\Pi|^{2}}_{i}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(VP[0+i*5], VP[1+i*5], VP[2+i*5], VP[3+i*5], VP[4+i*5]))
                f.write('\t$\mathscr{B}(D^{+}\\rightarrow K^{-}\pi^{+}\pi^{+})$ & 9.38\%& 9.38\%& 9.38\%& 9.38\%& 9.38\%&\\\\\n')
                f.write('\t$'+'\mathscr{L}(\\rm{pb}^{-1})'+'$ & {:^6}& {:^6}& {:^6}& {:^6}& {:^6}&\\\\\n'.format(lum[0+i*5], lum[1+i*5], lum[2+i*5], lum[3+i*5], lum[4+i*5]))
                f.write('\t$\omega'+'_{0}'+'$ & ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$&\\\\\n'.format(omega00, omega00_err, omega01, omega01_err, omega02, omega02_err, omega03, omega03_err, omega04, omega04_err))
                f.write('\t$\omega'+'_{1}'+'$ & ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$&\\\\\n'.format(omega1[0+i*5], omega1_err[0+i*5], omega1[1+i*5], omega1_err[1+i*5], omega1[2+i*5], omega1_err[2+i*5], omega1[3+i*5], omega1_err[3+i*5], omega1[4+i*5], omega1_err[4+i*5]))
                f.write('\t$\omega'+'_{2}'+'$ & ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$&\\\\\n'.format(omega2[0+i*5], omega2_err[0+i*5], omega2[1+i*5], omega2_err[1+i*5], omega2[2+i*5], omega2_err[2+i*5], omega2[3+i*5], omega2_err[3+i*5], omega2[4+i*5], omega2_err[4+i*5]))
                f.write('\t\hline\hline\n')
                f.write('\t\end{tabular}\n')
                f.write('\t\label{table6-'+str(2+i)+'}\n')
                f.write('\end{table}\n')
                f.write('\n\n')
            if i == 5:
                f.write('\\begin{table}[htp]\n')
                f.write('\t\centering\n')
                f.write('\t\caption{Fractions of $e^{+}e^{-}\\rightarrow D_{1}(2420)^{+}D^{-}$, $e^{+}e^{-}\\rightarrow\pi^{+}\pi^{-}\psi(3770)$, and $e^{+}e^{-}\\rightarrow\pi^{+}\pi^{-}D^{+}D^{-}(\sc{PHSP})$.}\n')
                f.write('\t\\resizebox{\\textwidth}{41mm}{\n')
                f.write('\t\t\\begin{tabular}{cccccccc}\n')
                f.write('\t\t\hline\hline\n')
                f.write('\t\tData Sample& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(sample[0+i*5], sample[1+i*5], sample[2+i*5], sample[3+i*5], sample[4+i*5], sample[5+i*5]))
                f.write('\t\t\hline\n')
                f.write('\t\t$N'+'_{0}^{\'}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N00, N00_err, N01, N01_err, N02, N02_err, N03, N03_err, N04, N04_err, N05, N05_err))
                f.write('\t\t$N'+'_{1}^{\'}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N1[0+i*5], N1_err[0+i*5], N1[1+i*5], N1_err[1+i*5], N1[2+i*5], N1_err[2+i*5], N1[3+i*5], N1_err[3+i*5], N1[4+i*5], N1_err[4+i*5], N1[5+i*5], N1_err[5+i*5]))
                f.write('\t\t$N'+'_{2}^{\'}'+'$ & {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}& {:^4}$\pm${:^4}&\\\\\n'.format(N2[0+i*5], N2_err[0+i*5], N2[1+i*5], N2_err[1+i*5], N2[2+i*5], N2_err[2+i*5], N2[3+i*5], N2_err[3+i*5], N2[4+i*5], N2_err[4+i*5], N2[5+i*5], N2_err[5+i*5]))
                f.write('\t\t$\epsilon'+'_{0}^{\'}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff00, eff01, eff02, eff03, eff04, eff05))
                f.write('\t\t$\epsilon'+'_{1}^{\'}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff1[0+i*5]*100, eff1[1+i*5]*100, eff1[2+i*5]*100, eff1[3+i*5]*100, eff1[4+i*5]*100, eff1[5+i*5]*100))
                f.write('\t\t$\epsilon'+'_{2}^{\'}'+'$ & ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$& ${:^4}\%$&\\\\\n'.format(eff2[0+i*5]*100, eff2[1+i*5]*100, eff2[2+i*5]*100, eff2[3+i*5]*100, eff2[4+i*5]*100, eff2[5+i*5]*100))
                f.write('\t\t$(1+\delta)'+'_{0}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del00, one_del01, one_del02, one_del03, one_del04, one_del05))
                f.write('\t\t$(1+\delta)'+'_{1}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del1[0+i*5], one_del1[1+i*5], one_del1[2+i*5], one_del1[3+i*5], one_del1[4+i*5], one_del1[5+i*5]))
                f.write('\t\t$(1+\delta)'+'_{2}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(one_del2[0+i*5], one_del2[1+i*5], one_del2[2+i*5], one_del2[3+i*5], one_del2[4+i*5], one_del1[5+i*5]))
                f.write('\t\t$\\frac'+'{1}{|1-\Pi|^{2}}_{i}'+'$ & {:^4}& {:^4}& {:^4}& {:^4}& {:^4}& {:^4}&\\\\\n'.format(VP[0+i*5], VP[1+i*5], VP[2+i*5], VP[3+i*5], VP[4+i*5], VP[5+i*5]))
                f.write('\t\t$\mathscr{B}(D^{+}\\rightarrow K^{-}\pi^{+}\pi^{+})$ & 9.38\%& 9.38\%& 9.38\%& 9.38\%& 9.38\%& 9.38\%&\\\\\n')
                f.write('\t\t$'+'\mathscr{L}(\\rm{pb}^{-1})'+'$ & {:^6}& {:^6}& {:^6}& {:^6}& {:^6}& {:^6}&\\\\\n'.format(lum[0+i*5], lum[1+i*5], lum[2+i*5], lum[3+i*5], lum[4+i*5], lum[5+i*5]))
                f.write('\t\t$\omega'+'_{0}'+'$ & ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$ &\\\\\n'.format(omega00, omega00_err, omega01, omega01_err, omega02, omega02_err, omega03, omega03_err, omega04, omega04_err, omega05, omega05_err))
                f.write('\t\t$\omega'+'_{1}'+'$ & ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$ &\\\\\n'.format(omega1[0+i*5], omega1_err[0+i*5], omega1[1+i*5], omega1_err[1+i*5], omega1[2+i*5], omega1_err[2+i*5], omega1[3+i*5], omega1_err[3+i*5], omega1[4+i*5], omega1_err[4+i*5], omega1[5+i*5], omega1_err[5+i*5]))
                f.write('\t\t$\omega'+'_{2}'+'$ & ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$& ${:^4}\pm{:^4}$ &\\\\\n'.format(omega2[0+i*5], omega2_err[0+i*5], omega2[1+i*5], omega2_err[1+i*5], omega2[2+i*5], omega2_err[2+i*5], omega2[3+i*5], omega2_err[3+i*5], omega2[4+i*5], omega2_err[4+i*5], omega2[5+i*5], omega2_err[5+i*5]))
                f.write('\t\t\hline\hline\n')
                f.write('\t\t\end{tabular}\n')
                f.write('\t}\n')
                f.write('\t\label{table6-'+str(2+i)+'}\n')
                f.write('\end{table}\n')
                f.write('\n\n')

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()
    patch = args[0]

    make_simul()
    make_xs(patch)
    make_total(patch)

if __name__ == '__main__':
    main()
