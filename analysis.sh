#!/usr/bin/env bash

# Main driver to execute and submit analysis jobs
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-08-21 Wed 10:00]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to execute and submit analysis jobs\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Pretreatment of data and MC samples]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Get samples -- synthesize root files"
    printf "\n\t%-9s  %-40s\n" "0.1.2" ""

    printf "\n\t%-9s  %-40s\n" ""      ""
    printf "\n\n"
}

if [[ $# -eq 0 ]]; then
    usage
    echo "Please enter your option: "
    read option
else
    option=$1
fi

case $option in

    # ----------------------------------------
    #  0.1 pretreatment of data and MC samples
    # ----------------------------------------

    0.1) echo "pretreating of data and MC samples..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC,PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89^{-1}(4420MeV), 566.93^{-1}(4600MeV)"
         ;;

    0.1.1) echo "Getting samples -- synthesize root files..."
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/D1_2420/4360/rootfile
           rm -rf sigMC_D1_2420_4360.root
           hadd sigMC_D1_2420_4360.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/D1_2420/4420/rootfile
           rm -rf sigMC_D1_2420_4420.root
           hadd sigMC_D1_2420_4420.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/D1_2420/4600/rootfile
           rm -rf sigMC_D1_2420_4600.root
           hadd sigMC_D1_2420_4600.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/psi_3770/4360/rootfile
           rm -rf sigMC_psi_3770_4360.root
           hadd sigMC_psi_3770_4360.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/psi_3770/4420/rootfile
           rm -rf sigMC_psi_3770_4420.root
           hadd sigMC_psi_3770_4420.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/psi_3770/4600/rootfile
           rm -rf sigMC_psi_3770_4600.root
           hadd sigMC_psi_3770_4600.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/bkgMC/PHSP/4360/rootfile
           rm -rf bkgMC_PHSP_4360.root
           hadd bkgMC_PHSP_4360.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/bkgMC/PHSP/4420/rootfile
           rm -rf bkgMC_PHSP_4420.root
           hadd bkgMC_PHSP_4420.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/bkgMC/PHSP/4600/rootfile
           rm -rf bkgMC_PHSP_4600.root
           hadd bkgMC_PHSP_4600.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/incMC/DD/4360/rootfile
           rm -rf incMC_DD_4360.root
           hadd incMC_DD_4360.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/incMC/DD/4420/rootfile
           rm -rf incMC_DD_4420.root
           hadd incMC_DD_4420.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/incMC/DD/4600/rootfile
           rm -rf incMC_DD_4600.root
           hadd incMC_DD_4600.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/incMC/qq/4360/rootfile
           rm -rf incMC_qq_4360.root
           hadd incMC_qq_4360.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/incMC/qq/4420/rootfile
           rm -rf incMC_qq_4420.root
           hadd incMC_qq_4420.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/incMC/qq/4600/rootfile
           rm -rf incMC_qq_4600.root
           hadd incMC_qq_4600.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/incMC/LL/4600/rootfile
           rm -rf incMC_LL_4600.root
           hadd incMC_LL_4600.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/data/4360
           rm -rf data_4360.root
           hadd data_4360.root *.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/data/4420
           rm -rf data_4420.root
           hadd data_4420_temp1.root data31*.root
           hadd data_4420_temp2.root data36*.root
           hadd data_4420_temp3.root data37*.root
           hadd data_4420_temp4.root data38*.root
           hadd data_4420.root data_4420_temp*.root
           rm -rf data_4420_temp*.root
           cd /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/data/4600
           rm -rf data_4600.root
           hadd data_4600.root *.root
           ;;

    0.1.2) echo "..."
           ;;

esac
