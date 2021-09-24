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
from tools.fit_xs import fit_xs
from ROOT import TCanvas, TMath, TF1, TChain, TPaveText, TMultiGraph
from math import *

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.05)

if not os.path.exists('./figs/'):
    os.makedirs('./figs/')

if not os.path.exists('./txts/'):
    os.makedirs('./txts/')

'''
Configuration file parser
'''
cp = ConfigParser.SafeConfigParser()
cp.read('weighted_isr.conf')
label_list = cp.get('patch', 'label').strip('[').strip(']').replace(' ', '').split(',')
iter_old = cp.get('patch', 'iter_old')
iter_new = cp.get('patch', 'iter_new')
old_xs_list = [xs.replace('iter_old', iter_old) for xs in cp.get('path', 'xs_old').strip('[').strip(']').replace(' ', '').split(',')]
new_xs_list = [xs.replace('iter_new', iter_new)for xs in cp.get('path', 'xs_new').strip('[').strip(']').replace(' ', '').split(',')]
ini_isr_list = cp.get('path', 'ini_isr').strip('[').strip(']').replace(' ', '').split(',')
xtitle_list = cp.get('draw', 'xtitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
xs_ytitle_list = cp.get('draw', 'xs_ytitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
eff_ytitle_list = cp.get('draw', 'eff_ytitle').strip('[').strip(']').replace(' ', '').replace('\'', '').split(',')
shape_dep_str = cp.get('weight', 'shape_dep')
if shape_dep_str == 'True' or shape_dep_str == 'true':
    shape_dep = True
elif shape_dep_str == 'False' or shape_dep_str == 'false':
    shape_dep = False
else:
    print("WRONG: shape_dep in weighted_isr.conf must be 'True'/'true' or 'False'/'false', now is " + cp.get('weight', 'shape_dep'))
    exit(-1)
if shape_dep:
    root_path_list = cp.get('weight', 'root_path').strip('[').strip(']').replace(' ', '').split(',')
    truth_root_list = cp.get('weight', 'truth_root').strip('[').strip(']').replace(' ', '').split(',')
    event_root_list = cp.get('weight', 'event_root').strip('[').strip(']').replace(' ', '').split(',')
    cut_weight = cp.get('weight', 'cut').replace('\'', '')
    pyroot_fit_str = cp.get('weight', 'pyroot_fit')
    if pyroot_fit_str == 'True' or pyroot_fit_str == 'true':
        pyroot_fit = True
    elif pyroot_fit_str == 'False' or pyroot_fit_str == 'false':
        pyroot_fit = False
    else:
        print("WRONG: pyroot_fit in weighted_isr.conf must be 'True'/'true' or 'False'/'false', now is " + cp.get('weight', 'pyroot_fit'))
        exit(-1)
    manual_update_str = cp.get('weight', 'manual_update')
    if manual_update_str == 'True' or manual_update_str == 'true':
        manual_update = True
    elif manual_update_str == 'False' or manual_update_str == 'false':
        manual_update = False
    else:
        print("WRONG: manual_update in weighted_isr.conf must be 'True'/'true' or 'False'/'false', now is " + cp.get('weight', 'manual_update'))
        exit(-1)
    truth_tree = cp.get('weight', 'truth_tree')
    event_tree = cp.get('weight', 'event_tree')
    weights_out = cp.get('weight', 'weights_out').replace('\'', '')
    # if not os.path.isdir(weights_out):
    #     print('WRONG: ' + weights_out + ' does not exist, please check')
    #     exit(-1)

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
    resonances.append((par[4], par[5], par[0], 0))
    resonances.append((par[6], par[7], par[1], par[2]))
    resonances.append((par[8], par[9], par[10], par[11]))
    bw = func1.getCorrelatedBreitWigners(xx, resonances, xmin_D1_2420)
    return pow(abs(bw), 2) + par[3]
import tools.xs_func_three_body as xs_func_three_body
xmin_psipp, xmax_psipp = 4.0535, 4.9985
func2 = xs_func_three_body.xs_func(100, xmin_psipp, xmax_psipp)
def func_psipp(x, par):
    ''' function for correlated breit wigner: e+e- --> psipp pipi '''
    xx = x[0]
    resonances = []
    resonances.append((par[1], par[2], par[0], 0))
    resonances.append((par[5], par[6], par[7], par[8]))
    bw = func2.getCorrelatedBreitWigners(xx, resonances, xmin_psipp)
    phsp = par[4]*complex(cos(par[3]), sin(par[3]))*sqrt(func2.getPHSP(xx))
    return pow(abs(bw + phsp), 2)
xmin_DDPIPI, xmax_DDPIPI = 4.0205, 4.9985
def func_DDPIPI(x, par):
    ''' function for correlated breit wigner: e+e- --> DDpipi '''
    xx = x[0]
    left = par[2] / xx
    numerator = sqrt(12.0*3.141592653589793*par[3]*par[4])
    denominator = complex(xx*xx-par[2]*par[2], par[2]*par[3])
    middle = numerator/denominator
    bw = left*middle
    return par[0] * pow(xx, -2) * TMath.Exp(-1 * par[1] * (xx - 4.015)) + pow(abs(bw), 2)
# initial parameters of fit functions
par_D1_2420 = array('d', [1.0, 0.1, 0.1, 1.0, 4.42, 0.062, 4.5059, 0.0788, 4.740, 0.134, 0.1, 0.1])
par_psipp = array('d', [0.1, 4.368, 0.096, 0.1, 0.1, 4.740, 0.134, 0.1, 0.1])
par_DDPIPI = array('d', [1.0, -1.0, 4.72, 0.134, 0.1])
# parameters range of fit functions
par_range_D1_2420 = [
    [0, -5.0, 5.0],
    [1, -5.0, 5.0],
    [2, -5.0, 5.0],
    [3, 5.0, 15.0],
    [4, 4.4, 4.425],
    [5, 0.062, 1.],
    [6, 4.4, 4.7],
    [7, 0.02, 1.],
    [8, 4.6, 4.85],
    [9, 0.0, 1.0],
    [10, -10.0, 10.0],
    [11, -10.0, 10.0]
]
par_range_psipp = [
    [0, 0.0, 10.0],
    [1, 4.015, 4.442],
    [2, 0.0, 1.0],
    [3, -10.0, 10.0],
    [4, -10.0, 10.0],
    [5, 4.6, 4.85],
    [6, 0.0, 1.0],
    [7, 0.0, 10.0],
    [8, -10.0, 10.0]
]
par_range_DDPIPI = [
    [0, 0, 50.0],
    [1, -50, 50.0],
    [2, 4.6, 4.76],
    [3, 0.02, 1.],
    [4, .0, 1.0]
]
# of TF1 fit functions
tfunc_D1_2420 = TF1('tfunc_D1_2420', func_D1_2420, xmin_D1_2420, xmax_D1_2420, len(par_D1_2420))
tfunc_psipp = TF1('tfunc_psipp', func_psipp, xmin_psipp, xmax_psipp, len(par_psipp))
tfunc_DDPIPI = TF1('tfunc_DDPIPI', func_DDPIPI, xmin_DDPIPI, xmax_DDPIPI, len(par_DDPIPI))
# necessary list
xmin_list = [xmin_D1_2420, xmin_psipp, xmin_DDPIPI]
xmax_list = [xmax_D1_2420, xmax_psipp, xmax_DDPIPI]
par_list = [par_D1_2420, par_psipp, par_DDPIPI]
par_range_list = [par_range_D1_2420, par_range_psipp, par_range_DDPIPI]
tfunc_list = [tfunc_D1_2420, tfunc_psipp, tfunc_DDPIPI]

'''
} USER DEFINE SECTION
'''

'''
fitting of input cross sections
'''
def FIT_XS():
    is_fit = True
    gaexs_list_fit, geeff_list_fit, gexs_list_fit, func_list = fit_xs(label_list, iter_old, old_xs_list, tfunc_list, par_list, par_range_list, xmin_list, xmax_list, is_fit)
    for f, label, gaexs, geeff, gexs, xtitle, xs_ytitle, eff_ytitle in zip(func_list, label_list, gaexs_list_fit, geeff_list_fit, gexs_list_fit, xtitle_list, xs_ytitle_list, eff_ytitle_list):
        xs_mbc = TCanvas('xs_mbc_' + label + '_' + iter_old + '_fit', '', 700, 600)
        set_canvas_style(xs_mbc)
        xs_mbc.cd()
        if not label == 'DDPIPI':
            set_graph_style(gaexs, xtitle, xs_ytitle)
            gaexs.Draw('ap')
        else:
            set_graph_style(gaexs, xtitle, xs_ytitle)
            set_graph_style(gexs, xtitle, xs_ytitle)
            mg = TMultiGraph()
            mg.Add(gaexs)
            mg.Add(gexs)
            mg.Draw('ap')
        chi2 =  f.GetChisquare()
        if label == 'DDPIPI': ndf = f.GetNDF() + 1
        else: ndf = f.GetNDF()
        pt = TPaveText(0.15, 0.8, 0.55, 0.9, "BRNDC")
        set_pavetext(pt)
        pt.Draw()
        line = '#chi^{2}/ndf = ' + str(round(chi2, 3)) + '/' + str(round(ndf, 3)) + ' = ' + str(round(chi2/ndf, 3))
        with open('./txts/likelihood_' + label + '.txt', 'w') as f:
            f.write(str(chi2) + '\n' + str(ndf))
        pt.AddText(line)
        xs_mbc.SaveAs('./figs/xs_' + label + '_' + iter_old + '_fit.pdf')
    raw_input('Press <Enter> to end...')
    return func_list

def main():
    func_list = FIT_XS()

if __name__ == '__main__':
    main()
