#!/usr/bin/env bash

# Main driver to do systerm uncertainties analysis
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2020-02-12 Wed 19:22]

usage() {
    printf "NAME\n\tsubmit.sh - Main driver to do systerm uncertainties analysis\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Get system uncertainties]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Fit distributions -- fit recoiling mass of Dpipi"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Calculate numbers -- calculate cross section of DDpipi and systerm uncertainties"

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

    # ------------------------------
    #  0.1 Get systerm uncertainties
    # ------------------------------

    0.2) echo "Getting systerm uncertainties..."
         echo "--> Samples: data, signal MC, PHSP MC"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03"
         ;;

    0.2.1) echo "Fit distributions -- fitting recoiling mass of Dpipi..."
           cd scripts/ana
           ./fitRMDpipi_703p01.sh round4
           ./fitRMDpipi_705.sh round4
           ;;

    0.2.2) echo "Calculate numbers -- calculating cross section of DDpipi and systerm uncertainties..."
           cd scripts/ana
           ./calXS_703p01.sh round4
           ./calXS_705.sh round4
           cd -
           ./format_xs.py round4
           ./cal_diff.py round4
           ;;

esac
