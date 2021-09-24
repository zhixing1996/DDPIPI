#!/usr/bin/env python
"""
Update isr factor and efficiency
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>, inspired by Lianjin Wu <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING, Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

import sys, os
import logging
from math import *
from ROOT import TF1, TChain, TH1D, TFile, TTree
import operator
from array import array

def cal_weight(sample, ecms, root, tfunc, label = '', sample_type = 'truth', cut = ''):
    ''' ARGUE: 1. input data sample
               2. input data ecms
               3. input TChain/TTree
               4. input defined TF1
               5. shape depended or not
               6. label of input data
               7. patch number of input data
               8. sample type
               9. cut
               10. output path of weight files
    '''
    wsumtotal, sumtotal = 0., 0.
    with open(root, 'r') as f:
        for line in f.readlines():
            fargs = map(float, line.strip().split())
            winvm = float(tfunc.Eval(fargs[0]))
            wecms = float(tfunc.Eval(ecms))
            w = winvm / wecms
            if not wecms == 0:
                wsumtotal += w
            sumtotal += 1
    return float(wsumtotal), float(sumtotal)

def weight(sample, ecms, truthroot, eventroot, tfunc, label = '', cut = ''):
    ''' ARGUE: 1. input data sample
               2. input data ecms
               3. input TChain/TTree for truth
               4. input TChain/TTree for reconstruct MC (events)
               5. whether mc shape dependent or not
               6. input defined TF1
               7. label of input data
               8. patch number of input data (next)
               9. cut
               10. output path of weight files
    '''
    wsumtru, sumtru = cal_weight(sample, ecms, truthroot, tfunc, label, 'truth', '')
    wsumsig, sumsig = cal_weight(sample, ecms, eventroot, tfunc, label, 'event', cut)
    weff, eff = wsumsig/wsumtru, sumsig/sumtru
    return wsumtru, weff, sumtru, eff

def update_sys(label_list, old_xs_list, ini_isr_list, tfunc_list, root_path_list, truth_root_list, event_root_list, truth_tree, event_tree, cut = ''):
    ''' ARGUE: 1. label list
               2. new iteration tag
               3. old data source file path and name
               4. new data file path and its name, used to store productions
               5. initial parameters for fit function
               6. defined TF1 list
               7. root path
               8. root name of truth
               9. root name of evnets after selecting
               10. tree name of truth
               11. tree name of evnets after selecting
               12. whether mc shape dependent or not
               13. cut
               14. using dedicted pyroot fit or not
               15. output path of weight files
    '''
    if not len(label_list) == len(old_xs_list) == len(ini_isr_list) == len(tfunc_list) == len(root_path_list) == len(truth_root_list) == len(event_root_list):
        print('WRONG: array size of label_list, old_xs, new_xs, ini_isr, tfunc, root_path, truth_path, truth_root and event_root should be the same')
        exit(-1)
    wisr_dict, weff_dict = {}, {}
    for label, old_xs, ini_isr, tfunc, root_path, truth_root, event_root in zip(label_list, old_xs_list, ini_isr_list, tfunc_list, root_path_list, truth_root_list, event_root_list):
        wisr_list, weff_list = [], []
        for line, iniisr in zip(open(old_xs), open(ini_isr)):
            if '#' in line: line = line.replace('#', '')
            try:
                fargs = map(float, line.strip().strip('\n').split())
                fisrs = map(float, iniisr.strip().strip('\n').split())
                sample, ecms, isr_old = fargs[0], fargs[1], fargs[8]
                truthroot, eventroot = root_path + '/' + str(int(sample)) + '/' + truth_root.replace('SAMPLE', str(int(sample))), root_path + '/' + str(int(sample)) + '/' + event_root.replace('SAMPLE', str(int(sample)))
                if not os.path.exists(root_path + '/' + str(int(sample))):
                    wsumtru, wsumeff, sumtru, sumeff, wisr = 0., 0., 0., 0., 0.
                else:
                    print('executing {0} -- {1}'.format(label, str(int(sample))))
                    wsumtru, wsumeff, sumtru, sumeff = weight(sample, ecms, truthroot, eventroot, tfunc, label, cut)
                    wisr = float(fisrs[1]) * wsumtru * pow(sumtru, -1)
                    print('wisr:{:<10.5f}, old isr:{:<10.5f}'.format(wisr, isr_old))
                    print('weff:{:<10.5f}, old eff:{:<10.5f}'.format(wsumeff, sumeff))
                    print('weff*wisr:{:<10.5f}, old eff*old isr:{:<10.5f}'.format(wsumeff*wisr, sumeff*isr_old))
                wisr_list.append(wisr)
                weff_list.append(wsumeff)
                wisr_dict[label] = wisr_list
                weff_dict[label] = weff_list
                wisr_dict.update({label:wisr_list})
                weff_dict.update({label:weff_list})
            except Exception as e:
                print str(e)
                pass
    return wisr_dict, weff_dict
