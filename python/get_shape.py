#!/usr/bin/env python
"""
Get signal shape of X(3842) (Breit-Wigner)
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-11-27 Wed 05:40]"

import math
from array import array
import sys, os
import logging
from math import *
from tools import *
from ROOT import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def usage():
    sys.stdout.write('''
NAME
    get_shape.py

SYNOPSIS
    ./get_shape.py [ecms]

AUTHOR
    Maoqiang JING <jingmq@ihep.ac.cn>

DATE
    November 2019
\n''')

def BW(m, M, G):
    s = pow(m, 2)
    bw = 1/(pow((s-M*M),2) + M*M*G*G)
    return bw

def shape(path_out):
    xbins = 2000
    m_min = 3.8
    m_max = 3.9
    file_out = TFile(path_out, 'RECREATE')
    h_mX3842 = TH1F('h_mX3842', 'h_mX3842', xbins, m_min, m_max)
    mass = 3.84271
    width = 0.00279
    for i in xrange(xbins):
        m = m_min + i*(m_max - m_min)/xbins
        XS = BW(m, mass, width)
        h_mX3842.Fill(m, XS)
    h_mX3842.Write()

def main():
    args = sys.argv[1:]
    if len(args)<1:
        return usage()

    path_out = args[0]
    shape(path_out)

if __name__ == '__main__':
    main()
