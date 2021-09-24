#!/usr/bin/env bash

# Main driver to do systerm uncertainties analysis
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2020-02-12 Wed 19:22]

usage() {
    printf "NAME\n\tsubmit.sh - Main driver to do systerm uncertainties analysis\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Sample omega_i]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Sample -- sample omega_i according to convariance matrix"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Calculate Numbers -- calculate difference between cross sections"
    printf "\n\t%-9s  %-40s\n" "0.1.3" "Convert ROOT -- convert ROOT files"
    printf "\n\t%-9s  %-40s\n" "0.1.4" "Fit Distributions -- fit pulls"
    printf "\n\t%-9s  %-40s\n" "0.1.5" "Calculate Numbers -- calculate systematic uncertainty"

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

    # -------------------
    #  0.1 Sample omega_i
    # -------------------

    0.1) echo "Sample omega_i..."
         ;;

    0.1.1) echo "Sample -- sampling omega_i according to convariance matrix..."
           cd scripts/ana
           ./sampleOmega.sh round2
           ;;

    0.1.2) echo "Calculate Numbers -- calculating difference between cross sections..."
           cd scripts/ana
           ./calDiff.sh round2
           ;;

    0.1.3) echo "Convert ROOT -- converting ROOT files..."
           cd scripts/ana
           ./convertROOT.sh round2
           ;;

    0.1.4) echo "Fit Distributions -- fitting pulls..."
           cd scripts/ana
           ./fitPull.sh
           ;;

    0.1.5) echo "Calculate Numbers -- calculating systematic uncertainty..."
           ./format_diff.py && ./make_tex.py
           ;;

esac
