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
    cal_diff.py

SYNOPSIS
    ./cal_diff.py

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    April 2020
\n''')

def cal_diff():
    if not os.path.exists('./txts/'):
        os.makedirs('./txts/')
    path_sys_err = './txts/sys_err_total.txt'
    f_sys_err = open(path_sys_err, 'w')

    dic = {}
    TYPES = ['background_shape', 'BW', 'BF', 'D1_2420_shape', 'fit_range', 'IntLum', 'ISR', 'K_p', 'm_pipi', 'omega', 'PID', 'psipp_shape', 'scale_factor', 'tracking', 'VP', 'VrVz', 'width', 'window', 'HELAMP']
    ECMS = [4190, 4200, 4210, 4220, 4230, 4237, 4245, 4246, 4260, 4270, 4280, 4290, 4310, 4315, 4340, 4360, 4380, 4390, 4400, 4420, 4440, 4470, 4530, 4575, 4600, 4610, 4620, 4640, 4660, 4680, 4700, 4740, 4750, 4780, 4840, 4914, 4946]
    for ECM in ECMS:
        SYS = []
        for TYPE in TYPES:
            f_type = open('../'+TYPE+'/txts/sys_err_'+TYPE+'.txt', 'r')
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
    cal_diff()
