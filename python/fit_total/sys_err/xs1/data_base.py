#!/usr/bin/env python
"""
Common tools 
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-13 Tue 15:05]" 

import sys 
import os, errno
import shutil
import ROOT 

# luminosity
def luminosity(ecms):
    if int(ecms) == 4190:
        LUM = 567.23 # 523.9 + 43.33
    if int(ecms) == 4200:
        LUM = 525.2
    if int(ecms) == 4210:
        LUM = 572.12 # 517.2 + 54.95
    if int(ecms) == 4220:
        LUM = 568 # 513.4 + 54.60
    if int(ecms) == 4230:
        LUM = 1100.94 # 44.54 + 1056.4
    if int(ecms) == 4237:
        LUM = 529.1
    if int(ecms) == 4245:
        LUM = 55.88
    if int(ecms) == 4246:
        LUM = 536.3
    if int(ecms) == 4260:
        LUM = 828.4
    if int(ecms) == 4270:
        LUM = 529.7
    if int(ecms) == 4280:
        LUM = 175.7
    if int(ecms) == 4290:
        LUM = 502.4
    if int(ecms) == 4310:
        LUM = 45.08
    if int(ecms) == 4315:
        LUM = 501.2
    if int(ecms) == 4340:
        LUM = 505.0
    if int(ecms) == 4360:
        LUM = 543.9
    if int(ecms) == 4380:
        LUM = 522.7
    if int(ecms) == 4390:
        LUM = 55.57
    if int(ecms) == 4400:
        LUM = 507.8
    if int(ecms) == 4420:
        LUM = 1090.7 # 46.8 + 1043.9
    if int(ecms) == 4440:
        LUM = 569.9
    if int(ecms) == 4470:
        LUM = 111.1
    if int(ecms) == 4530:
        LUM = 112.1
    if int(ecms) == 4575:
        LUM = 48.9
    if int(ecms) == 4600:
        LUM = 586.9
    if int(ecms) == 4610:
        LUM = 103.83
    if int(ecms) == 4620:
        LUM = 521.52
    if int(ecms) == 4640:
        LUM = 552.41
    if int(ecms) == 4660:
        LUM = 529.63
    if int(ecms) == 4680:
        LUM = 1669.31
    if int(ecms) == 4700:
        LUM = 536.45
    if int(ecms) == 4740:
        LUM = 164.27
    if int(ecms) == 4750:
        LUM = 367.21
    if int(ecms) == 4780:
        LUM = 512.78
    if int(ecms) == 4840:
        LUM = 527.29
    if int(ecms) == 4914:
        LUM = 208.11
    if int(ecms) == 4946:
        LUM = 160.37
    return LUM
