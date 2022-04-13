#!/usr/bin/env python
"""
Fit cross section
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2021-02-25 Thr 23:47]"

import ROOT
from ROOT import TCanvas, gStyle, TGraphErrors, TGraphAsymmErrors, TGraphErrors
from ROOT import TFile, TH1F, TLegend, TPaveText, TF1, TMath
from array import array
import sys, os
import logging
from math import *
import random
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def usage():
    sys.stdout.write('''
NAME
    fit_xs.py

SYNOPSIS
    ./fit_xs.py [patch] [component1, component2, component3, ...]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    February 2021
\n''')

args = sys.argv[1:]
if len(args)<2:
    usage()
    sys.exit()
patch = args[0]
components = args[1:]
xmin, xmax = 4.0205, 4.9985
GeV_2_sigma = 0.389379

import tools.xs_func_four_body as xs_func_four_body
func = xs_func_four_body.xs_func()

def set_pavetext(pt):
    pt.SetFillStyle(0)
    pt.SetBorderSize(0)
    pt.SetTextAlign(10)
    pt.SetTextSize(0.05)

def read_params():
    ''' read params for function of e+e- --> pipiDD'''
    from tools.Resonances import Resonances
    count_init, count_range = 0, 0
    param_init = []
    param_range = []
    for component in components:
        resonance = Resonances[component]
        if 'BW' in component:
            args = resonance['constant']
            if 'mass' not in args:
                param_init.append(resonance['init']['mass'])
                count_init += 1
                index = count_range
                param_min, param_max = resonance['min_max']['mass']
                param_range.append([index, param_min, param_max])
                count_range += 1
            if 'width' not in args:
                param_init.append(resonance['init']['width'])
                count_init += 1
                index = count_range
                param_min, param_max = resonance['min_max']['width']
                param_range.append([index, param_min, param_max])
                count_range += 1
            if 'BrGam' not in args:
                param_init.append(resonance['init']['BrGam'])
                count_init += 1
                index = count_range
                param_min, param_max = resonance['min_max']['BrGam']
                param_range.append([index, param_min, param_max])
                count_range += 1
            if 'phase' not in args:
                param_init.append(resonance['init']['phase'])
                count_init += 1
                index = count_range
                param_min, param_max = resonance['min_max']['phase']
                param_range.append([index, param_min, param_max])
                count_range += 1
        if 'PHSP' in component:
            param_init.append(resonance['init']['a'])
            index = count_init
            param_min, param_max = resonance['min_max']['a']
            param_range.append([index, param_min, param_max])
            index += 1
            param_init.append(resonance['init']['phase'])
            param_min, param_max = resonance['min_max']['phase']
            param_range.append([index, param_min, param_max])
    return param_init, param_range

par_index = {}
def construct_A2():
    param_init, param_range = read_params()

    def func_DDPIPI(x, par):
        ''' function for correlated breit wigner: e+e- --> pipiDD'''
        from tools.Resonances import Resonances
        global par_index
        xx = x[0]
        resonances = []
        count = 0
        for component in components:
            res = []
            resonance = Resonances[component]
            if 'BW' in component:
                args = resonance['constant']
                if 'mass' not in args:
                    res.append(par[count])
                    par_index[component + '_mass'] = count
                    count += 1
                else:
                    res.append(resonance['init']['mass'])
                if 'width' not in args:
                    res.append(par[count])
                    par_index[component + '_width'] = count
                    count += 1
                else:
                    res.append(resonance['init']['width'])
                if 'BrGam' not in args:
                    res.append(par[count])
                    par_index[component + '_BrGam'] = count
                    count += 1
                else:
                    res.append(resonance['init']['BrGam'])
                if 'phase' not in args:
                    res.append(par[count])
                    par_index[component + '_phase'] = count
                    count += 1
                else:
                    res.append(resonance['init']['phase'])
                resonances.append(res)
            if 'PHSP' in component:
                par_index['phsp_c'] = count
                par_index['phsp_phase'] = count + 1
                phsp = par[count]*func.getExpIPhi(par[count + 1])*sqrt(func.getPHSP(xx))
        bw = func.getCorrelatedBreitWigners(xx, resonances, xmin)
        if 'PHSP' in components: return GeV_2_sigma * pow(abs(bw + phsp), 2)
        else: return GeV_2_sigma * pow(abs(bw), 2)

    param_init = array('d', param_init)
    tfunc = TF1('tfunc', func_DDPIPI, xmin, xmax, len(param_init))
    rand_param = []
    for ilimit, low, high in param_range:
        value = random.uniform(low, high)
        tfunc.SetParameter(ilimit, value)
        tfunc.SetParLimits(ilimit, low, high)
        rand_param.append([ilimit, value])
    tfunc.SetLineColor(2)
    return rand_param, tfunc

def BW_BW(x, par):
    xx = x[0]
    BW = func.getOneBreitWigner(xx, par[0], par[1], par[2], xmin)
    PHI = func.getExpIPhi(par[3])
    return GeV_2_sigma * pow(abs(BW * PHI), 2)

def PHSP_PHSP(x, par):
    xx = x[0]
    phsp = par[0]*func.getExpIPhi(par[1])*sqrt(func.getPHSP(xx))
    return GeV_2_sigma * pow(abs(phsp), 2)

def BW1_BW2(x, par):
    xx = x[0]
    BW1 = func.getOneBreitWigner(xx, par[0], par[1], par[2], xmin)
    PHI1 = func.getExpIPhi(par[3])
    BW2 = func.getOneBreitWigner(xx, par[4], par[5], par[6], xmin)
    PHI2 = func.getExpIPhi(par[7])
    return GeV_2_sigma * 2. * ((BW1 * PHI1).real * (BW2 * PHI2).real + (BW1 * PHI1).imag * (BW2 * PHI2).imag)

def BW_PHSP(x, par):
    xx = x[0]
    BW = func.getOneBreitWigner(xx, par[0], par[1], par[2], xmin)
    PHI = func.getExpIPhi(par[3])
    phsp = par[4]*func.getExpIPhi(par[5])*sqrt(func.getPHSP(xx))
    return GeV_2_sigma * 2. * ((BW * PHI).real * phsp.real + (BW * PHI).imag * phsp.imag)

def set_graph_style(gr, xtitle, ytitle, xmin = 0., xmax = -1):
    gr.GetXaxis().SetNdivisions(509)
    gr.GetYaxis().SetNdivisions(504)
    gr.SetLineWidth(2)
    gr.GetXaxis().SetTitleSize(0.06)
    gr.GetXaxis().SetTitleOffset(1.)
    gr.GetXaxis().SetLabelOffset(0.01)
    gr.GetXaxis().SetLabelSize(0.05)
    gr.GetXaxis().SetRangeUser(4.17, 5.00)
    gr.GetYaxis().SetTitleSize(0.06)
    gr.GetYaxis().SetTitleOffset(1.)
    gr.GetYaxis().SetLabelOffset(0.01)
    gr.GetYaxis().SetLabelSize(0.05)
    if xmax != -1: gr.GetYaxis().SetRangeUser(xmin, xmax)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetXaxis().CenterTitle()
    gr.GetYaxis().SetTitle(ytitle)
    gr.GetYaxis().CenterTitle()
    gr.SetMarkerColor(1)
    gr.SetMarkerStyle(20)

def set_canvas_style(mbc):
    mbc.SetFillColor(0)
    mbc.SetLeftMargin(0.15)
    mbc.SetRightMargin(0.15)
    mbc.SetTopMargin(0.1)
    mbc.SetBottomMargin(0.15)
    mbc.SetGrid()

def set_legend(legend, f, names, funcs, title):
    legend.AddEntry(f, 'Total fit')
    for name, func in zip(names, funcs):
        legend.AddEntry(func, name)
    legend.SetHeader(title)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetTextSize(0.03)

def fit(iround):
    mbc = TCanvas('mbc_' + str(iround), 'mbc_' + str(iround), 800, 600)
    set_canvas_style(mbc)
    mbc.cd()

    ipoint, geexs = 0, TGraphErrors(0)
    path = '../../fit_xs/txts/xs_total_' + patch + '_plot.txt'
    xs_max = 0
    from tools.data_base import ECMS
    for line in open(path):
        try:
            if '#' in line: continue
            fargs = map(float, line.strip().split())
            ecms, xs, xserr = fargs[0], fargs[1], fargs[2]
            geexs.Set(ipoint + 1)
            geexs.SetPoint(ipoint, ECMS(int(ecms*1000)), xs)
            geexs.SetPointError(ipoint, 0.0, xserr)
            if xs > xs_max: xs_max = xs
            ipoint += 1
        except:
            '''
            '''
    xtitle = '#sqrt{s}(GeV)'
    ytitle = '#sigma(e^{+}e^{-}#rightarrow#pi^{+}#pi^{-}D^{+}D^{-})(pb)'
    if 'BW_4230_a' not in components and 'PHSP_a' not in components: set_graph_style(geexs, xtitle, ytitle, xmin = -15., xmax = xs_max * 1.7)
    else: set_graph_style(geexs, xtitle, ytitle, xmin = -5., xmax = xs_max * 1.7)
    geexs.Draw('ap')
    rand_param, tfunc = construct_A2()
    result = geexs.Fit(tfunc, 'S', '')
    flag = 0
    if result.IsValid(): flag = 1
    tfunc.Draw('same')
    _, param_range = read_params()
    for i in range(tfunc.GetNumberFreeParameters()):
        fit_value = tfunc.GetParameter(i)
        ilimit, ilow, ihigh = param_range[i]
        if abs(fit_value - ilow) < 0.001 or abs(fit_value - ihigh) < 0.001:
            flag = 0
    mbc.Update()

    from tools.Resonances import Resonances
    start_param_pos = 0
    param = {}
    for component in components:
        par = []
        len_param = len(Resonances[component]['init']) - len(Resonances[component]['constant'])
        for i in range(start_param_pos, start_param_pos + len_param): 
            par.append(tfunc.GetParameter(i))
        for const in Resonances[component]['constant']:
            if const == 'mass': par.insert(0, Resonances[component]['init']['mass'])
            if const == 'width': par.insert(1, Resonances[component]['init']['width'])
            if const == 'BrGam': par.insert(2, Resonances[component]['init']['BrGam'])
            if const == 'phase': par.insert(3, Resonances[component]['init']['phase'])
        start_param_pos += len_param
        param[component] = par

    used = []
    VarsManager = locals()
    for i, icomponent in enumerate(components):
        for j, jcomponent in enumerate(components):
            if (icomponent, jcomponent) in used or (jcomponent, icomponent) in used: continue
            used.append((icomponent, jcomponent))
            color = 1 + i + j
            if color == 5: color += 1 # not yellow
            if icomponent == jcomponent and 'BW' in icomponent and 'BW' in jcomponent:
                par = param[icomponent]
                VarsManager['f_' + icomponent + '_' + jcomponent] = TF1(icomponent, BW_BW, xmin, xmax, len(par));
                VarsManager['f_' + icomponent + '_' + jcomponent].SetParameters(array('d', par));
                VarsManager['f_' + icomponent + '_' + jcomponent].SetLineColor(color)
                VarsManager['f_' + icomponent + '_' + jcomponent].SetLineStyle(ROOT.kSolid)
                VarsManager['f_' + icomponent + '_' + jcomponent].Draw('same')
            if icomponent == jcomponent and 'PHSP' in icomponent and 'PHSP' in jcomponent:
                par = param[icomponent]
                VarsManager['f_' + icomponent + '_' + jcomponent] = TF1(icomponent, PHSP_PHSP, xmin, xmax, len(par));
                VarsManager['f_' + icomponent + '_' + jcomponent].SetParameters(array('d', par));
                VarsManager['f_' + icomponent + '_' + jcomponent].SetLineColor(color)
                VarsManager['f_' + icomponent + '_' + jcomponent].SetLineStyle(ROOT.kSolid)
                VarsManager['f_' + icomponent + '_' + jcomponent].Draw('same')
            if icomponent != jcomponent and 'BW' in icomponent and 'BW' in jcomponent:
                param_i = param[icomponent]
                param_j = param[jcomponent]
                par = param_i + param_j
                VarsManager['f_' + icomponent + '_' + jcomponent] = TF1(icomponent + '_' + str(jcomponent), BW1_BW2, xmin, xmax, len(par));
                VarsManager['f_' + icomponent + '_' + jcomponent].SetParameters(array('d', par));
                VarsManager['f_' + icomponent + '_' + jcomponent].SetLineColor(color)
                VarsManager['f_' + icomponent + '_' + jcomponent].SetLineStyle(ROOT.kDashed)
                VarsManager['f_' + icomponent + '_' + jcomponent].Draw('same')
            if 'BW' in icomponent and 'PHSP' in jcomponent:
                param_i = param[icomponent]
                param_j = param[jcomponent]
                par = param_i + param_j
                VarsManager['f_' + icomponent + '_' + jcomponent] = TF1(icomponent + '_' + jcomponent, BW_PHSP, xmin, xmax, len(par));
                VarsManager['f_' + icomponent + '_' + jcomponent].SetParameters(array('d', par));
                VarsManager['f_' + icomponent + '_' + jcomponent].SetLineColor(color)
                VarsManager['f_' + icomponent + '_' + jcomponent].SetLineStyle(4)
                VarsManager['f_' + icomponent + '_' + jcomponent].Draw('same')
    funcs = []
    names = []
    for key, value in VarsManager.items():
        if 'f_' in key:
            names.append(value.GetName())
            funcs.append(value)
    mbc.Update()

    if flag != 0:
        chi2 =  tfunc.GetChisquare()
        ndf = tfunc.GetNDF()
        if len(components) == 3 and ('BW_4390' in components and 'BW_4700' in components and 'PHSP' in components): line = '(a) #chi^{2}/ndf = ' + str(round(chi2, 1)) + '/' + str(round(ndf, 1)) + ' = ' + str(round(chi2/ndf, 1))
        elif len(components) == 2 and ('BW_4390' in components and 'BW_4700' in components): line = '(b) #chi^{2}/ndf = ' + str(round(chi2, 1)) + '/' + str(round(ndf, 1)) + ' = ' + str(round(chi2/ndf, 1))
        else: line = '#chi^{2}/ndf = ' + str(round(chi2, 1)) + '/' + str(round(ndf, 1)) + ' = ' + str(round(chi2/ndf, 1))

        label = ''
        for component in components:
            label += '_' + component

        if not os.path.exists('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/txts/'):
            os.makedirs('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/txts/')

        with open('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/txts/fit_result' + label + '_' + str(iround) + '.txt', 'w') as f:
            f.write(str(iround) + ' ' + str(chi2) + ' ')
            for param in rand_param:
                ilimit, par_ini = param
                f.write(str(ilimit) + ' ' + str(par_ini) + ' ')

        with open('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/txts/likelihood' + label + '_' + str(iround) + '.txt', 'w') as f:
            f.write(str(chi2) + '\n' + str(ndf))

        with open('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/txts/params' + label + '_' + str(iround) + '.txt', 'w') as f:
            for key, value in par_index.items():
                out = key + ' ' + str(tfunc.GetParameter(value)) + ' ' + str(tfunc.GetParError(value)) + '\n'
                f.write(out)

        legend = TLegend(0.2, 0.6, 0.5, 0.88)
        set_legend(legend, tfunc, names, funcs, line)
        legend.Draw()

        if not os.path.exists('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/figs/'):
            os.makedirs('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/figs/')

        mbc.SaveAs('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/figs/xs' + label + '_' + str(iround) + '.pdf')

        # raw_input('Enter anything to end...')
    
if __name__ == '__main__':
    for i in range(100):
        fit(i)
