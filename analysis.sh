#!/usr/bin/env bash

# Main driver to execute and submit analysis jobs
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-09-02 Mon 21:42]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to execute and submit analysis jobs\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Pretreatment of data and MC samples]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Get samples -- synthesize root files"

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
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC,PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89^{-1}(4420MeV), 566.93^{-1}(4600MeV)"
         ;;

    0.1.1) echo "Get samples -- synthesizing root files..."
           ;;

esac
