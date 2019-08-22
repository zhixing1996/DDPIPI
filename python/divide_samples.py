#!/usr/bin/env python
"""
Divide samples into rm_Dpipi signal and sideband region
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-22 Thu 23:38]"

import ROOT
from ROOT import TCanvas, gStyle, TTree, TChain
from ROOT import TFile
import sys, os
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
gStyle.SetOptTitle(0)
gStyle.SetOptTitle(0)

def sel(path, ecms, sample, mode, region):
    print '--> Begin to process file: ' + path
    try:
        chain = TChain('save')
        chain.Add(path)
    except:
        logging.error(path+' is invalid!')
        sys.exit()

    if region == 'signal':
        cut = 'm_rm_Dpipi > 1.855 && m_rm_Dpipi < 1.882'

    if region == 'sideband':
        cut = '( (m_rm_Dpipi > 1.786 && m_rm_Dpipi < 1.84) || (m_rm_Dpipi > 1.897 && m_rm_Dpipi < 1.951) )'

    t = chain.CopyTree(cut)

    path_out = '/besfs/users/jingmq/DDPIPI/v0.1/'+sample+'/'+mode+'/'+str(ecms)+'/'
    t.SaveAs(path_out+sample+'_'+mode+'_'+str(ecms)+'_selected'+'_'+region+'.root')
    print '--> End of processing file: ' + path

if __name__ == '__main__':
    data_path_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected.root'
    sigMC_D1_2420_path_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected.root'
    sigMC_psi_3770_path_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4360/sigMC_psi_3770_4360_selected.root'
    bkgMC_PHSP_path_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/PHSP/4360/bkgMC_PHSP_4360_selected.root'
    incMC_DD_path_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4360/incMC_DD_4360_selected.root'
    incMC_qq_path_4360 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4360/incMC_qq_4360_selected.root'
    ecms_4360 = 4360
    sel(data_path_4360, ecms_4360, 'data', '', 'signal')
    sel(data_path_4360, ecms_4360, 'data', '', 'sideband')
    sel(sigMC_D1_2420_path_4360, ecms_4360, 'sigMC', 'D1_2420', 'signal')
    sel(sigMC_D1_2420_path_4360, ecms_4360, 'sigMC', 'D1_2420', 'sideband')
    sel(sigMC_psi_3770_path_4360, ecms_4360, 'sigMC', 'psi_3770', 'signal')
    sel(sigMC_psi_3770_path_4360, ecms_4360, 'sigMC', 'psi_3770', 'sideband')
    sel(bkgMC_PHSP_path_4360, ecms_4360, 'bkgMC', 'PHSP', 'signal')
    sel(bkgMC_PHSP_path_4360, ecms_4360, 'bkgMC', 'PHSP', 'sideband')
    sel(incMC_DD_path_4360, ecms_4360, 'incMC', 'DD', 'signal')
    sel(incMC_DD_path_4360, ecms_4360, 'incMC', 'DD', 'sideband')
    sel(incMC_qq_path_4360, ecms_4360, 'incMC', 'qq', 'signal')
    sel(incMC_qq_path_4360, ecms_4360, 'incMC', 'qq', 'sideband')

    data_path_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected.root'
    sigMC_D1_2420_path_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected.root'
    sigMC_psi_3770_path_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4420/sigMC_psi_3770_4420_selected.root'
    bkgMC_PHSP_path_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/PHSP/4420/bkgMC_PHSP_4420_selected.root'
    incMC_DD_path_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4420/incMC_DD_4420_selected.root'
    incMC_qq_path_4420 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4420/incMC_qq_4420_selected.root'
    ecms_4420 = 4420
    sel(data_path_4420, ecms_4420, 'data', '', 'signal')
    sel(data_path_4420, ecms_4420, 'data', '', 'sideband')
    sel(sigMC_D1_2420_path_4420, ecms_4420, 'sigMC', 'D1_2420', 'signal')
    sel(sigMC_D1_2420_path_4420, ecms_4420, 'sigMC', 'D1_2420', 'sideband')
    sel(sigMC_psi_3770_path_4420, ecms_4420, 'sigMC', 'psi_3770', 'signal')
    sel(sigMC_psi_3770_path_4420, ecms_4420, 'sigMC', 'psi_3770', 'sideband')
    sel(bkgMC_PHSP_path_4420, ecms_4420, 'bkgMC', 'PHSP', 'signal')
    sel(bkgMC_PHSP_path_4420, ecms_4420, 'bkgMC', 'PHSP', 'sideband')
    sel(incMC_DD_path_4420, ecms_4420, 'incMC', 'DD', 'signal')
    sel(incMC_DD_path_4420, ecms_4420, 'incMC', 'DD', 'sideband')
    sel(incMC_qq_path_4420, ecms_4420, 'incMC', 'qq', 'signal')
    sel(incMC_qq_path_4420, ecms_4420, 'incMC', 'qq', 'sideband')

    data_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected.root'
    sigMC_D1_2420_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected.root'
    sigMC_psi_3770_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4600/sigMC_psi_3770_4600_selected.root'
    bkgMC_PHSP_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/PHSP/4600/bkgMC_PHSP_4600_selected.root'
    incMC_DD_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/DD/4600/incMC_DD_4600_selected.root'
    incMC_qq_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/qq/4600/incMC_qq_4600_selected.root'
    incMC_LL_path_4600 = '/besfs/users/jingmq/DDPIPI/v0.1/incMC/LL/4600/incMC_LL_4600_selected.root'
    ecms_4600 = 4600
    sel(data_path_4600, ecms_4600, 'data', '', 'signal')
    sel(data_path_4600, ecms_4600, 'data', '', 'sideband')
    sel(sigMC_D1_2420_path_4600, ecms_4600, 'sigMC', 'D1_2420', 'signal')
    sel(sigMC_D1_2420_path_4600, ecms_4600, 'sigMC', 'D1_2420', 'sideband')
    sel(sigMC_psi_3770_path_4600, ecms_4600, 'sigMC', 'psi_3770', 'signal')
    sel(sigMC_psi_3770_path_4600, ecms_4600, 'sigMC', 'psi_3770', 'sideband')
    sel(bkgMC_PHSP_path_4600, ecms_4600, 'bkgMC', 'PHSP', 'signal')
    sel(bkgMC_PHSP_path_4600, ecms_4600, 'bkgMC', 'PHSP', 'sideband')
    sel(incMC_DD_path_4600, ecms_4600, 'incMC', 'DD', 'signal')
    sel(incMC_DD_path_4600, ecms_4600, 'incMC', 'DD', 'sideband')
    sel(incMC_qq_path_4600, ecms_4600, 'incMC', 'qq', 'signal')
    sel(incMC_qq_path_4600, ecms_4600, 'incMC', 'qq', 'sideband')
    sel(incMC_LL_path_4600, ecms_4600, 'incMC', 'LL', 'signal')
    sel(incMC_LL_path_4600, ecms_4600, 'incMC', 'LL', 'sideband')
