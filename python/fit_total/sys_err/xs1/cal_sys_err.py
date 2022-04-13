#!/usr/bin/env python
"""
Calculate total systematic uncertainty
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2020-04-07 Tue 23:36]"

from array import array
import sys, os
import logging
from math import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    cal_sys_err.py

SYNOPSIS
    ./cal_sys_err.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    April 2020
\n''')

def cal_diff(TYPES, path_sys_err):
    f_sys_err = open(path_sys_err, 'w')

    dic = {}
    ECMS = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    for ECM in ECMS:
        SYS = []
        for TYPE in TYPES:
            f_type = open('../../../sys_err/'+TYPE+'/txts/sys_err_'+TYPE+'.txt', 'r')
            lines_type = f_type.readlines()
            for line_type in lines_type:
                rs_type = line_type.rstrip('\n')
                rs_type = filter(None, rs_type.split("\t"))
                ecms = float(rs_type[0])
                sys = float(rs_type[1])
                if ecms == ECM/1000.:
                    SYS.append(sys)
                    dic[ecms] = SYS
                    dic.update({ecms:SYS})

    dic.items()
    LIST = list(dic.items())
    LIST.sort(key = lambda x:x[0], reverse = False)
    for ecm, sys_errs in LIST:
        sys_err = reduce(lambda x, y: x+y, (map(lambda x: x ** 2, sys_errs)))
        out = str(ecm) + '\t' + str(round(sqrt(sys_err), 1)) + '\n'
        f_sys_err.write(out)
    f_sys_err.close()

if __name__ == '__main__':
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    TYPES = set(['background_shape', 'BW', 'BF', 'D1_2420_shape', 'fit_range', 'IntLum', 'ISR', 'K_p', 'm_pipi', 'omega', 'PID', 'psipp_shape', 'scale_factor', 'tracking', 'VP', 'VrVz', 'width', 'window', 'HELAMP'])
    TYPES_UNCOM = set(['BW', 'D1_2420_shape', 'omega', 'psipp_shape', 'scale_factor', 'HELAMP'])
    path_sys_err_uncom = './txts/sys_err_uncom.txt'
    cal_diff(TYPES_UNCOM, path_sys_err_uncom)
    path_sys_err_com = './txts/sys_err_com.txt'
    cal_diff(TYPES - TYPES_UNCOM, path_sys_err_com)
