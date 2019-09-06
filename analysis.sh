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
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Get samples -- extract useful info"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Study cuts]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Draw figues -- study chi2 of kinematic fit cuts"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Draw figues -- study mass window"


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
           cd jobs
           bash synthesize_root
           ;;

    0.1.2) echo "Get samples -- extracting useful info..."
           mkdir -p scripts/ana/sel
           cd scripts/ana/sel
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/sel/jobs_ana" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/sel/jobs_ana
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/sel/jobs_ana ./jobs_ana
           fi
           cd jobs_ana
           rm -rf jobs.out
           rm -rf jobs.err
           mkdir jobs.out
           mkdir jobs.err
           cp $HOME/bes/DDPIPI/v0.2/jobs/get_info* .
           hep_sub -g physics get_info_raw -o jobs.out -e jobs.err
           hep_sub -g physics get_info_signal -o jobs.out -e jobs.err
           hep_sub -g physics get_info_sidebandlow -o jobs.out -e jobs.err
           hep_sub -g physics get_info_sidebandup -o jobs.out -e jobs.err
           ;;

    # ---------------
    #  0.2 Study cuts
    # ---------------

    0.2) echo "Studying cuts..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC,PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89^{-1}(4420MeV), 566.93^{-1}(4600MeV)"
         ;;

    0.2.1) echo "Draw figures -- studying chi2 of kinematic fit cuts..."
           cd $HOME/bes/DDPIPI/v0.2/python
           python opt_chi2_kf.py 4360
           python opt_chi2_kf.py 4420
           python opt_chi2_kf.py 4600
           python plot_chi2_kf.py
           ;;

    0.2.2) echo "Draw figures -- studying mass window..."
           cd $HOME/bes/DDPIPI/v0.2/python
           python opt_mass_window.py 4360
           python opt_mass_window.py 4420
           python opt_mass_window.py 4600
           ;;

esac
