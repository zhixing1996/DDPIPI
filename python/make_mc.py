#!/usr/bin/env python
"""
Make data analysis jobOptions
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-13 Tue 09:29]"

import sys
import os
import math
from tools import search, group_files_by_num

def usage():
    sys.stdout.write('''
NAME
    make_mc.py 

SYNOPSIS
    ./make_mc.py [dst_file_path] [sample] [decay] [mode] [type] [energy] [dst_file_num]
    [dst_file_path]: dst file path
    [sample]: sigMC, incMC, data or others
    [decay]: decay chain, such as X_3842_PI_PI for e+e- -> X(3842)PI+PI-
    [mode]: generation mode
    [type]: X_3842, D1_2420, psi_3770 or others, for inclusive MC the same as mode
    [energy]: energy point
    [dst_file_num]: number of dst files in one jobOption file

AUTHOR 
    Maoqiang JING <jingmq@ihep.ac.cn> 

DATE
    August 2019 
\n''')

    
def main():
    args = sys.argv[1:]
    if len(args) < 7:
        return usage()
    
    dst_path = args[0]
    sample = args[1]
    decay = args[2]
    mode = args[3]
    type = args[4]
    energy = args[5]
    dst_file_num = args[6]
    sys.stdout.write('Scanning %s...\n' %dst_path)

    dst_list = []
    print '***************************************start to search***************************************'
    dst_list = search(dst_list, dst_path, '.dst')
    print '***************************************searching ending**************************************'
    dst_list_groups = group_files_by_num(dst_list, dst_file_num)
    i = 0
    for dst_list_fill in dst_list_groups:
        file_name = sample + '_' + decay + '_' + mode + '_' + energy + '_' + str(i) + '.txt'
        f = open(file_name, 'w')
        f.write('#include "$ROOTIOROOT/share/jobOptions_ReadRec.txt"\n')
        f.write('#include "$MAGNETICFIELDROOT/share/MagneticField.txt"\n')
        f.write('#include "$DTAGALGROOT/share/jobOptions_dTag.txt"\n')
        f.write('#include "$DDECAYALGROOT/share/jobOptions_DDecay.txt"\n')
        f.write('\n')
        f.write('DTag.NeutralDReconstruction  = true;\n')
        f.write('DTag.ChargedDReconstruction  = true;\n')
        f.write('DTag.DsReconstruction        = true;\n')
        f.write('\n')
        f.write('NeutralDSelector.UseMbcCuts       = false;\n')
        f.write('eutralDSelector.UseDeltaECuts     = false;\n')
        f.write('NeutralDSelector.UseDeltaMassCuts = true;\n')
        f.write('\n')
        f.write('ChargedDSelector.UseMbcCuts       = false;\n')
        f.write('ChargedDSelector.UseDeltaECuts    = false;\n')
        f.write('ChargedDSelector.UseDeltaMassCuts = true;\n')
        f.write('\n')
        f.write('DsSelector.UseMbcCuts       = false;\n')
        f.write('DsSelector.UseDeltaECuts    = false;\n')
        f.write('DsSelector.UseDeltaMassCuts = true;\n')
        f.write('\n')
        f.write('// Input REC or DST file name\n')
        f.write('EventCnvSvc.digiRootInputFile = {\n')
        for dst in dst_list_fill:
            if dst != dst_list_fill[-1]:
                temp = '"' + dst + '",\n'
                f.write(temp)
            if dst == dst_list_fill[-1]:
                temp = '"' + dst + '"\n'
                f.write(temp)
        f.write('};\n')
        f.write('\n')
        f.write('// Set output level threshold (2=DEBUG, 3=INFO, 4=WARNING, 5=ERROR, 6=FATAL )\n')
        f.write('MessageSvc.OutputLevel =6;\n')
        f.write('\n')
        f.write('// Number of events to be processed (default is 10)\n')
        f.write('ApplicationMgr.EvtMax = -1;\n')
        f.write('\n')
        f.write('ApplicationMgr.HistogramPersistency = "ROOT";\n')
        f.write('NTupleSvc.Output = {\"FILE1 DATAFILE=\'/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/'+sample+'/'+type+'/'+energy+'/rootfile/'+sample+'_'+decay+'_'+mode+'_'+energy+'_'+str(i)+'.root'+'\' OPT=\'NEW\' TYP=\'ROOT\'\"};\n')
        f.close()
        i = i + 1
    print 'All done!'

if __name__ == '__main__':
    main()