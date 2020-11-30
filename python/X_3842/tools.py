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

# ---------------------------------------------
# Function 
# ---------------------------------------------

# range of RM(pipi)
def param_rm_pipi(ecms):
    LOW = 999.
    UP = 999.
    if int(ecms) == 4190:
        LOW = 3.73
        UP = 3.86
    if int(ecms) == 4200:
        LOW = 3.74
        UP = 3.90
    if int(ecms) == 4210:
        LOW = 3.735
        UP = 3.90
    if int(ecms) == 4220:
        LOW = 3.74
        UP = 3.91
    if int(ecms) == 4230:
        LOW = 3.735
        UP = 3.95
    if int(ecms) == 4237:
        LOW = 3.73
        UP = 3.93
    if int(ecms) == 4245:
        LOW = 3.72
        UP = 3.92
    if int(ecms) == 4246:
        LOW = 3.73
        UP = 3.92
    if int(ecms) == 4260:
        LOW = 3.72
        UP = 3.96
    if int(ecms) == 4270:
        LOW = 3.72
        UP = 3.95
    if int(ecms) == 4280:
        LOW = 3.73
        UP = 3.95
    if int(ecms) == 4290:
        LOW = 3.73
        UP = 3.95
    if int(ecms) == 4310:
        LOW = 3.73
        UP = 3.97
    if int(ecms) == 4315:
        LOW = 3.735
        UP = 3.97
    if int(ecms) == 4340:
        LOW = 3.74
        UP = 4.03
    if int(ecms) == 4360:
        LOW = 3.73
        UP = 4.05
    if int(ecms) == 4380:
        LOW = 3.74
        UP = 4.07
    if int(ecms) == 4390:
        LOW = 3.74
        UP = 4.07
    if int(ecms) == 4400:
        LOW = 3.74
        UP = 4.08
    if int(ecms) == 4420:
        LOW = 3.73
        UP = 4.11
    if int(ecms) == 4440:
        LOW = 3.73
        UP = 4.12
    if int(ecms) == 4470:
        LOW = 3.74
        UP = 4.07
    if int(ecms) == 4530:
        LOW = 3.73
        UP = 4.18
    if int(ecms) == 4575:
        LOW = 3.73
        UP = 4.20
    if int(ecms) == 4600:
        LOW = 3.73
        UP = 4.24
    if int(ecms) == 4610:
        LOW = 3.73
        UP = 4.24
    if int(ecms) == 4620:
        LOW = 3.74
        UP = 4.24
    if int(ecms) == 4640:
        LOW = 3.74
        UP = 4.31
    if int(ecms) == 4660:
        LOW = 3.73
        UP = 4.32
    if int(ecms) == 4680:
        LOW = 3.73
        UP = 4.37
    if int(ecms) == 4700:
        LOW = 3.73
        UP = 4.35
    return LOW, UP
