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
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Get samples -- extract useful info: raw"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Study cuts]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Draw figures -- study signal region of RM(Dpipi)"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Draw figures -- study mass window of M(Kpipi)"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Get samples -- extract useful info: signal region and sideband region"
    printf "\n\t%-9s  %-40s\n" "0.2.4" "Get samples -- get data sideband samples"
    printf "\n\t%-9s  %-40s\n" "0.2.5" "Draw figures -- compare data, data sideband and signal samples(RM(pipi), raw)"
    printf "\n\t%-9s  %-40s\n" "0.2.6" "Draw figures -- compare data and X(3842) MC(chi2_kf)"
    printf "\n\t%-9s  %-40s\n" "0.2.7" "Draw figures -- compare data, data sideband and signal samples(RM(pipi), cut)"

    printf "\n\t%-9s  %-40s\n" "0.3"   "[Background Study]"
    printf "\n\t%-9s  %-40s\n" "0.3.1" "Get samples -- get topology info"

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
         echo "--> Cross Section: D1_2420: 41.8+/-5.6+/-3.8pb(4360MeV), 65.4+/-3.0+/-5.7pb(4420MeV), 27.7+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Cross Section: psi(3770): 17.3+/-5.4+/-1.5pb(4360MeV), 23.8+/-2.6+/-2.1pb(4420MeV), 7.2+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89pb^{-1}(4420MeV), 566.93pb^{-1}(4600MeV)"
         ;;

    0.1.1) echo "Get samples -- synthesizing root files..."
           cd jobs
           bash synthesize_root
           ;;

    0.1.2) echo "Get samples -- extracting useful info: raw..."
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
           cp $HOME/bes/DDPIPI/v0.2/jobs/get_info_raw .
           hep_sub -g physics get_info_raw -o jobs.out -e jobs.err
           ;;

    # ---------------
    #  0.2 Study cuts
    # ---------------

    0.2) echo "Studying cuts..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC,PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Cross Section: D1(2420): 41.8+/-5.6+/-3.8pb(4360MeV), 65.4+/-3.0+/-5.7pb(4420MeV), 27.7+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Cross Section: psi(3770): 17.3+/-5.4+/-1.5pb(4360MeV), 23.8+/-2.6+/-2.1pb(4420MeV), 7.2+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89pb^{-1}(4420MeV), 566.93pb^{-1}(4600MeV)"
         ;;

    0.2.1) echo "Draw figures -- studying signal region of RM(Dpipi)..."
           cd $HOME/bes/DDPIPI/v0.2/python
           python opt_signal_region.py 4360
           python opt_signal_region.py 4420
           python opt_signal_region.py 4600
           ;;

    0.2.2) echo "Draw figures -- studying mass window of M(Kpipi)..."
           cd $HOME/bes/DDPIPI/v0.2/python
           python opt_mass_window.py 4360
           python opt_mass_window.py 4420
           python opt_mass_window.py 4600
           ;;

    0.2.3) echo "Get samples -- extracting useful info: signal region and sideband region..."
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
           cp $HOME/bes/DDPIPI/v0.2/jobs/get_info_signal .
           cp $HOME/bes/DDPIPI/v0.2/jobs/get_info_sidebandlow .
           cp $HOME/bes/DDPIPI/v0.2/jobs/get_info_sidebandup .
           hep_sub -g physics get_info_signal -o jobs.out -e jobs.err
           hep_sub -g physics get_info_sidebandlow -o jobs.out -e jobs.err
           hep_sub -g physics get_info_sidebandup -o jobs.out -e jobs.err
           ;;

    0.2.4) echo "Get samples -- getting data sideband samples..."
           cd /besfs/users/$USER/bes/DDPIPI/v0.2/data/4360
           rm -rf data_4360_sideband.root
           hadd data_4360_sideband.root data_4360_sideband*.root
           cd /besfs/users/$USER/bes/DDPIPI/v0.2/data/4420
           rm -rf data_4420_sideband.root
           hadd data_4420_sideband.root data_4420_sideband*.root
           cd /besfs/users/$USER/bes/DDPIPI/v0.2/data/4600
           rm -rf data_4600_sideband.root
           hadd data_4600_sideband.root data_4600_sideband*.root
           ;;

    0.2.5) echo "Draw figures -- comparing data, data sideband and signal samples(RM(pipi), raw)..."
           cd $HOME/bes/DDPIPI/v0.2/python
           python plot_rm_pipi.py raw
           ;;

    0.2.6) echo "Draw figures -- comparing data and X(3842) MC(chi2_kf)..."
           cd $HOME/bes/DDPIPI/v0.2/python
           python  plot_chi2_kf.py
           ;;

    0.2.7) echo "Draw figures -- comparing data, data sideband and signal samples(RM(pipi), cut)..."
           cd $HOME/bes/DDPIPI/v0.2/python
           python plot_rm_pipi.py cut
           ;;

    # ---------------------
    #  0.3 Background Study
    # ---------------------

    0.3) echo "Pretreating of data and MC samples..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC,PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Cross Section: D1_2420: 41.8+/-5.6+/-3.8pb(4360MeV), 65.4+/-3.0+/-5.7pb(4420MeV), 27.7+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Cross Section: psi(3770): 17.3+/-5.4+/-1.5pb(4360MeV), 23.8+/-2.6+/-2.1pb(4420MeV), 7.2+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89pb^{-1}(4420MeV), 566.93pb^{-1}(4600MeV)"
         ;;

    0.3.1) echo "Get samples -- getting topology info..."
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
           cp $HOME/bes/DDPIPI/v0.2/jobs/get_info_topo
           hep_sub -g physics get_info_topo -o jobs.out -e jobs.err
           ;;

esac
