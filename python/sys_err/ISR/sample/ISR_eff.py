#!/usr/bin/env python
"""
main file of weighted_isr package
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>, inspired by Lianjin Wu <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING, Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

import ConfigParser
import sys, os
from array import array
sys.dont_write_bytecode = True
from tools.setup import set_pub_style, set_graph_style, set_pad_style, set_canvas_style
set_pub_style()
from tools.update_sys import update_sys
from tools.sample import sampling
from ROOT import TCanvas, TMath, TF1, TChain
from math import *

if not os.path.exists('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/'):
    os.makedirs('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/')

'''
Configuration file parser
'''
cp = ConfigParser.SafeConfigParser()
cp.read('weighted_isr_sys.conf')
label_list = cp.get('patch', 'label').strip('[').strip(']').replace(' ', '').split(',')
iter_old = cp.get('patch', 'iter_old')
iter_new = cp.get('patch', 'iter_new')
old_xs_list = [xs.replace('iter_old', iter_old) for xs in cp.get('path', 'xs_old').strip('[').strip(']').replace(' ', '').split(',')]
new_xs_list = [xs.replace('iter_new', iter_new)for xs in cp.get('path', 'xs_new').strip('[').strip(']').replace(' ', '').split(',')]
ini_isr_list = cp.get('path', 'ini_isr').strip('[').strip(']').replace(' ', '').split(',')
xtitle_list = cp.get('draw', 'xtitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
xs_ytitle_list = cp.get('draw', 'xs_ytitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
eff_ytitle_list = cp.get('draw', 'eff_ytitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
sys_err_switch = cp.get('sys_err', 'switch')
Nrand = int(cp.get('sys_err', 'Nrand'))
root_path_list = cp.get('sys_err', 'root_path').strip('[').strip(']').replace(' ', '').split(',')
event_root_list = cp.get('sys_err', 'event_root').strip('[').strip(']').replace(' ', '').split(',')
truth_root_list = cp.get('sys_err', 'truth_root').strip('[').strip(']').replace(' ', '').split(',')
truth_tree = cp.get('sys_err', 'truth_tree')
event_tree = cp.get('sys_err', 'event_tree')
xs_info_sys = cp.get('sys_err', 'xs_info').replace('\'', '')
cut_sys = cp.get('sys_err', 'cut').replace('\'', '')

'''
USER DEFINE SECTION { : fit functions for input cross sections
'''
# formula of fit functions
import tools.xs_func_two_body as xs_func_two_body
xmin_D1_2420, xmax_D1_2420 = 4.2935, 4.9985
m_D1_2420, m_Dm = 2.4232, 1.86965
func1 = xs_func_two_body.xs_func(100, xmin_D1_2420, xmax_D1_2420, m_D1_2420, m_Dm)
def func_D1_2420(x, par):
    ''' function for correlated breit wigner: e+e- --> D1D'''
    xx = x[0]
    resonances = []
    resonances.append((4.420, 0.084, par[0], 0))
    resonances.append((4.530, 0.064, par[1], par[2]))
    bw = func1.getCorrelatedBreitWigners(xx, resonances, xmin_D1_2420)
    return pow(abs(bw), 2) + par[3]
import tools.xs_func_three_body as xs_func_three_body
xmin_psipp, xmax_psipp = 4.0535, 4.9985
func2 = xs_func_three_body.xs_func(100, xmin_psipp, xmax_psipp)
def func_psipp(x, par):
    ''' function for correlated breit wigner: e+e- --> psipp pipi '''
    xx = x[0]
    resonances = []
    resonances.append((4.368, 0.068, par[0], 0))
    resonances.append((4.420, 0.042, par[1], par[2]))
    resonances.append((4.680, 0.032, par[3], par[4]))
    bw = func2.getCorrelatedBreitWigners(xx, resonances, xmin_psipp)
    return pow(abs(bw), 2) + par[5]
xmin_DDPIPI, xmax_DDPIPI = 4.0205, 4.9985
def func_DDPIPI(x, par):
    ''' function for correlated breit wigner: e+e- --> DDpipi '''
    xx = x[0]
    return par[0] * pow(xx, -2) * TMath.Exp(-1 * par[1] * (xx - 4.015)) + par[2] * TMath.Gaus(xx, par[3], par[4])
# initial parameters of fit functions
par_D1_2420 = array('d', [1.0, 0.1, 0.1, 1.0])
par_psipp = array('d', [0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
par_DDPIPI = array('d', [1.0, -1.0, 0., 4.74, 0.05])
# of TF1 fit functions
tfunc_D1_2420 = TF1('tfunc_D1_2420', func_D1_2420, xmin_D1_2420, xmax_D1_2420, len(par_D1_2420))
tfunc_psipp = TF1('tfunc_psipp', func_psipp, xmin_psipp, xmax_psipp, len(par_psipp))
tfunc_DDPIPI = TF1('tfunc_DDPIPI', func_DDPIPI, xmin_DDPIPI, xmax_DDPIPI, len(par_DDPIPI))
# necessary list
xmin_list = [xmin_D1_2420, xmin_psipp, xmin_DDPIPI]
xmax_list = [xmax_D1_2420, xmax_psipp, xmax_DDPIPI]
tfunc_list = [tfunc_D1_2420, tfunc_psipp, tfunc_DDPIPI]

'''
estimate systematic uncertainty caused by line-shape
'''
def CAL():
    sampling(label_list, iter_old, Nrand)
    for iloop in xrange(Nrand):
        print '**************************************************************************************************'
        print str(iloop) + '\'s(' + str(Nrand - 1) + ') simulation is on......'
        func_list = []
        for label, tfunc in zip(label_list, tfunc_list):
            with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/param_rand_' + label + '_' + iter_old + '.txt', 'r') as f:
                lines = f.readlines()
                fargs = map(float, lines[iloop].strip().split())
                Npar = len(fargs)
                par = array('d', Npar*[0.])
                for i in xrange(Npar): par[i] = fargs[i]
            print '------------------------------------------------------'
            print 'Process: ' + label
            print 'Renewed parameters: ' + str(par)
            print '------------------------------------------------------'
            tfunc.SetParameters(par)
            func_list.append(tfunc)
        wisr_dict, weff_dict = update_sys(label_list, old_xs_list, ini_isr_list, func_list, root_path_list, truth_root_list, event_root_list, truth_tree, event_tree, cut_sys)
        D1_2420_isr_eff, DDPIPI_isr_eff, psipp_isr_eff = [], [], []
        D1_2420_isr, DDPIPI_isr, psipp_isr = [], [], []
        D1_2420_eff, DDPIPI_eff, psipp_eff = [], [], []
        for k_wisr, v_wisr in wisr_dict.items():
            if k_wisr == 'D1_2420':
                D1_2420_isr = list(v_wisr)
            if k_wisr == 'psipp':
                psipp_isr = list(v_wisr)
            if k_wisr == 'DDPIPI':
                DDPIPI_isr = list(v_wisr)
        for k_weff, v_weff in weff_dict.items():
            if k_weff == 'D1_2420':
                D1_2420_eff = list(v_weff)
            if k_weff == 'psipp':
                psipp_eff = list(v_weff)
            if k_weff == 'DDPIPI':
                DDPIPI_eff = list(v_weff)
        for i in xrange(len(D1_2420_isr)):
            D1_2420_isr_eff.append(D1_2420_isr[i] * D1_2420_eff[i])
        for i in xrange(len(psipp_isr)):
            psipp_isr_eff.append(psipp_isr[i] * psipp_eff[i])
        for i in xrange(len(DDPIPI_isr)):
            DDPIPI_isr_eff.append(DDPIPI_isr[i] * DDPIPI_eff[i])
        print D1_2420_isr, D1_2420_eff, D1_2420_isr_eff
        print DDPIPI_isr, DDPIPI_eff, DDPIPI_isr_eff
        print psipp_isr, psipp_eff, psipp_isr_eff
        samples = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
        with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/wisr_weff_D1_2420_' + str(iloop) + '.txt', 'w') as f:
            count = 0
            for isr, eff, isr_eff in zip(D1_2420_isr, D1_2420_eff, D1_2420_isr_eff):
                f.write(str(samples[14 + count]) + ' ' + str(isr) + ' ' +str(eff) + ' ' + str(isr_eff) + '\n')
                count += 1
        with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/wisr_weff_psipp_' + str(iloop) + '.txt', 'w') as f:
            for sample, isr, eff, isr_eff in zip(samples, psipp_isr, psipp_eff, psipp_isr_eff):
                f.write(str(sample) + ' ' + str(isr) + ' ' +str(eff) + ' ' + str(isr_eff) + '\n')
        with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/wisr_weff_DDPIPI_' + str(iloop) + '.txt', 'w') as f:
            for sample, isr, eff, isr_eff in zip(samples, DDPIPI_isr, DDPIPI_eff, DDPIPI_isr_eff):
                f.write(str(sample) + ' ' + str(isr) + ' ' +str(eff) + ' ' + str(isr_eff) + '\n')
        with open('/besfs5/users/jingmq/bes/DDPIPI/v0.2/ana/sys_err/ISR/txts/xs_diff_' + str(iloop) + '.txt', 'w') as f_diff:
            for i in xrange(len(samples)):
                sample = samples[i]
                with open(xs_info_sys.replace('SAMPLE', str(sample)), 'r') as f:
                    lines = f.readlines()
                    fargs = map(float, lines[0].strip().split())
                    N_data, N_data_sideband = fargs[1], fargs[3]
                    f_K_p, f_m_pipi, f_VrVz, f_m_Kpipi, f_rm_Dpipi = fargs[5], fargs[6], fargs[7], fargs[8], fargs[9]
                    omega_D1_2420, omega_psipp, omega_DDPIPI = fargs[13], fargs[14], fargs[15]
                    VP, lum, Br, xs_old = fargs[19], fargs[20], fargs[21]/100., fargs[22]
                    if omega_D1_2420 == 0:
                        flag_D1_2420 = 0
                        eff_ISR_VP_D1_2420 = 1
                    else:
                        flag_D1_2420 = 1
                        eff_ISR_VP_D1_2420 = D1_2420_isr_eff[i - 14]*omega_D1_2420*VP*f_K_p*f_m_pipi*f_VrVz*f_m_Kpipi*f_rm_Dpipi
                    if omega_psipp == 0:
                        flag_psipp = 0
                        eff_ISR_VP_psipp = 1
                    else:
                        flag_psipp = 1
                        eff_ISR_VP_psipp = psipp_isr_eff[i]*omega_psipp*VP*f_K_p*f_m_pipi*f_VrVz*f_m_Kpipi*f_rm_Dpipi
                    if omega_DDPIPI == 0:
                        flag_DDPIPI = 0
                        eff_ISR_VP_DDPIPI = 1
                    else:
                        flag_DDPIPI = 1
                        eff_ISR_VP_DDPIPI = DDPIPI_isr_eff[i]*omega_DDPIPI*VP*f_K_p*f_m_pipi*f_VrVz*f_m_Kpipi*f_rm_Dpipi
                    xs_new = (N_data - N_data_sideband/2.)/(2*(flag_D1_2420*eff_ISR_VP_D1_2420 + flag_psipp*eff_ISR_VP_psipp + flag_DDPIPI*eff_ISR_VP_DDPIPI)*Br*lum)
                diff = (xs_old - xs_new)/xs_old
                print str(sample) + ': old cross section: ' + str(xs_old) + ', new cross section: ' + str(xs_new) + ', difference: ' + str(diff)
                f_diff.write(str(sample) + ' ' + str(xs_old) + ' ' + str(xs_new) + ' '  + str(diff) + '\n')
        print '**************************************************************************************************'

def main():
    CAL()

if __name__ == '__main__':
    main()
