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
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Simulation & Reconstruction -- generate psipp MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Simulation & Reconstruction -- generate psipp MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.3" "Single D tag -- run on psipp MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.4" "Single D tag -- run on psipp MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.5" "Get samples -- extracte useful info: signal region and sideband region, ISR factors"
    printf "\n\t%-9s  %-40s\n" "0.1.6" "Get samples -- apply cuts: psipp MC"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Get system uncertainties]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Get samples -- convert root files"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Fit distributions -- fit recoiling mass of D + Dmiss"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Get shapes -- mix MC shapes"
    printf "\n\t%-9s  %-40s\n" "0.2.4" "Fit distributions -- fit recoiling mass of Dpipi"
    printf "\n\t%-9s  %-40s\n" "0.2.5" "Calculate numbers -- calculate cross section of DDpipi and systerm uncertainties"

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

    0.1.1) echo "Simulation & Reconstruction -- generating psipp MC sample(@703p01)..."
           cd scripts/mc/psipp
           ./subSimRec_psipp_703p01.sh
           ;;

    0.1.2) echo "Simulation & Reconstruction -- generating psipp MC sample(@705)..."
           cd scripts/mc/psipp
           ./subSimRec_psipp_705.sh
           ;;

    0.1.3) echo "Single D tag -- running on psipp MC sample(@703p01)..."
           cd scripts/mc/psipp
           ./subAna_psipp_703p01.sh
           ;;

    0.1.4) echo "Single D tag -- running on psipp MC sample(@705)..."
           cd scripts/mc/psipp
           ./subAna_psipp_705.sh
           ;;

    0.1.5) echo "Get samples -- extracting useful info: signal region and sideband region, ISR factors..."
           cd scripts/mc
           ./synthesizepsipp_703p01.sh
           ./synthesizepsipp_705.sh
           ./getInfopsipp_703p01.sh
           ./getInfopsipp_705.sh
           ./getFactorpsipp_703p01.sh round4
           ./getFactorpsipp_705.sh round4
           ;;

    0.1.6) echo "Get samples -- applying cuts: psipp MC..."
           cd scripts/mc
           ./applyCutspsipp_703p01.sh
           ./applyCutspsipp_705.sh
           ;;

    # ------------------------------
    #  0.2 Get systerm uncertainties
    # ------------------------------

    0.2) echo "Getting systerm uncertainties..."
         echo "--> Samples: data, signal MC, PHSP MC"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03"
         ;;

    0.2.1) echo "Get samples -- converting root files..."
           cd scripts/ana
           ./convertROOT_703p01.sh
           ./convertROOT_705.sh
           ;;

    0.2.2) echo "Fit distributions -- fitting recoiling mass of D + Dmiss..."
           cd scripts/ana
           ./fitRMD_703p01.sh round4
           ./fitRMD_705.sh round4
           ;;

    0.2.3) echo "Get shapes -- mixing MC shapes..."
           cd scripts/mc
           ./mixMC_703p01.sh round4
           ./mixMC_705.sh round4
           ;;

    0.2.4) echo "Fit distributions -- fitting recoiling mass of Dpipi..."
           cd scripts/ana
           ./fitRMDpipi_703p01.sh round4
           ./fitRMDpipi_705.sh round4
           ;;

    0.2.5) echo "Calculate numbers -- calculating cross section of DDpipi and systerm uncertainties..."
           cd scripts/ana
           ./calXS_703p01.sh round4
           ./calXS_705.sh round4
           cd -
           ./format_xs.py round4
           ./cal_diff.py round4
           ;;

esac
