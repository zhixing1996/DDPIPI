#!/usr/bin/env bash

# Main driver to do systerm uncertainties analysis
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2020-02-12 Wed 19:22]

usage() {
    printf "NAME\n\tsubmit.sh - Main driver to do systerm uncertainties analysis\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Pretreatment of data and MC samples]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Get samples -- apply cuts: data"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Get samples -- apply cuts: MC"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Get system uncertainties]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Get shapes -- get D1_2420 shapes"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Get samples -- convert root files"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Fit distributions -- simultaneous fit recoiling mass of D + Dmiss and recoiling mass of pipi"
    printf "\n\t%-9s  %-40s\n" "0.2.4" "Calculate numbers -- calculate cross section of DDpipi and systerm uncertainties"

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
    #  0.1 Pretreatment of data and MC samples
    # ----------------------------------------

    0.1) echo "Pretreating of data and MC samples..."
         echo "--> Samples: data, signal MC, PHSP MC"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03"
         ;;

    0.1.1) echo "Get samples -- applying cuts: data..."
           cd scripts/data
           ./applyCutsData_703p01.sh
           ./applyCutsData_705.sh
           ;;

    0.1.2) echo "Get samples -- applying cuts: MC..."
           cd scripts/mc
           ./applyCutsD1_2420_703p01.sh
           ./applyCutsD1_2420_705.sh
           ./applyCutspsipp_703p01.sh
           ./applyCutspsipp_705.sh
           ./applyCutsD_D_PI_PI_703p01.sh
           ./applyCutsD_D_PI_PI_705.sh
           ;;

    # ------------------------------
    #  0.2 Get systerm uncertainties
    # ------------------------------

    0.2) echo "Getting systerm uncertainties..."
         echo "--> Samples: data, signal MC, PHSP MC"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03"
         ;;

    0.2.1) echo "Get shapes -- getting D1_2420 shapes..."
           cd scripts/ana
           ./getShape_703p01.sh
           ./getShape_705.sh
           ;;

    0.2.2) echo "Get samples -- converting root files..."
           cd scripts/ana
           ./convertROOT_703p01.sh
           ./convertROOT_705.sh
           ;;

    0.2.3) echo "Fit distributions -- simultaneous fitting recoiling mass of D + Dmiss and recoiling mass of pipi..."
           cd scripts/ana
           ./simul_fit_703p01.sh round4
           ./simul_fit_705.sh round4
           ;;

    0.2.4) echo "Calculate numbers -- calculating cross section of DDpipi and systerm uncertainties..."
           cd scripts/ana
           ./calXS_703p01.sh round4
           ./calXS_705.sh round4
           cd -
           ./format_xs.py round4
           ./cal_diff.py round4
           ;;

esac
