#!/usr/bin/env python
"""
Subject data analysis jobOptions
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-12-09 Mon 21:30]"

import sys
import os
from tools import search, mkdir_p, rm_r
from shutil import copyfile

def usage():
    sys.stdout.write('''
NAME
    make_data.py 

SYNOPSIS
    ./sub_data_703p01.py

AUTHOR 
    Maoqiang JING <jingmq@ihep.ac.cn> 

DATE
    December 2019 
\n''')
    
def main():
    args = sys.argv[1:]
    usage()

    path = os.environ['HOME'] + '/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/DataBase-703-1'
    f = open(path, 'r') 
    lines = f.readlines()
    for line in lines:
        rs = line.rstrip('\n')
        rs = filter(None, rs.split(";")) # 0: int energy point, 1: ruNolow, 2: ruNoup, 3: float energy poit, 4: luminosity, 5: dst path
        PATH = os.environ['HOME'] + '/bes/DDPIPI/v0.2'
        mkdir_p(PATH + '/scripts/data/' + rs[0])
        os.chdir(PATH + '/scripts/data/' + rs[0])
        if not os.path.exists('/scratchfs/bes/' + os.environ['USER'] + '/bes/DDPIPI/v0.2/run/gen_data/data/' + rs[0] + '/jobs_data'):
            mkdir_p('/scratchfs/bes/' + os.environ['USER'] + '/bes/DDPIPI/v0.2/run/gen_data/data/' + rs[0] + '/jobs_data')
            os.symlink('/scratchfs/bes/' + os.environ['USER'] + '/bes/DDPIPI/v0.2/run/gen_data/data/' + rs[0] + '/jobs_data', './jobs_data')
        os.chdir('./jobs_data')
        rm_r('/scratchfs/bes/' + os.environ['USER'] + '/bes/DDPIPI/v0.2/data/' + rs[0])
        mkdir_p('/scratchfs/bes/' + os.environ['USER'] + '/bes/DDPIPI/v0.2/data/' + rs[0])
        copyfile(os.environ['HOME'] + '/bes/DDPIPI/v0.2/python/make_data.py', './make_data.py')
        copyfile(os.environ['HOME'] + '/bes/DDPIPI/v0.2/python/tools.py', './tools.py')
        os.system('python make_data.py ' + rs[5] + ' ' + rs[1] + ' ' + rs[2] + ' ' + rs[0])
        copyfile(os.environ['HOME'] + '/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/subAna.sh', './subAna.sh')
        os.system('sh subAna.sh data')
    
if __name__ == '__main__':
    main()
