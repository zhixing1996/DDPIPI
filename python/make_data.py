#!/usr/bin/env python
"""
Make data analysis jobOptions
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-13 Tue 15:29]"

import sys
import os
from tools import search

def usage():
    sys.stdout.write('''
NAME
    make_data.py 

SYNOPSIS
    ./make_data.py [dst_file_path] [runNo_low] [runNo_up] [energy]

AUTHOR 
    Maoqiang JING <jingmq@ihep.ac.cn> 

DATE
    August 2019 
\n''')

    
def main():
    args = sys.argv[1:]
    if len(args) < 3:
        return usage()
    
    dst_path = args[0]
    runNo_low = args[1]
    runNo_up = args[2]
    energy = args[3]
    sys.stdout.write('Scanning %s...\n' %dst_path)

    for runNo in range(int(runNo_low), int(runNo_up) + 1):
        dst_list = []
        print '***************************************start to search***************************************'
        dst_list = search(dst_list, dst_path, str(runNo))
        print '***************************************searching ending**************************************'
        if dst_list:
            file_name = 'data'+str(runNo)+'.txt'
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
            print 'processing runNo: ' + str(runNo) + ' with ' + str(len(dst_list)) + ' dst files...'
            for dst in dst_list:
                if dst != dst_list[-1]:
                    temp = '"' + dst + '",\n'
                    f.write(temp)
                if dst == dst_list[-1]:
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
            f.write('NTupleSvc.Output = {\"FILE1 DATAFILE=\'/scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/' + energy + '/' + 'data' + str(runNo) + '.root\' OPT=\'NEW\' TYP=\'ROOT\'\"};\n')
            f.close()
        else:
            print 'runNo: ' + str(runNo) + ' is empty, just ignore it!'
    print 'All done!'

if __name__ == '__main__':
    main()
