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
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Draw figures -- study mass window of M(Kpipi)"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Draw figures -- study signal region of RM(Dpipi)"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Get samples -- extract useful info: signal region and sideband region"
    printf "\n\t%-9s  %-40s\n" "0.2.4" "Get samples -- get data sideband samples"
    printf "\n\t%-9s  %-40s\n" "0.2.5" "Draw figures -- compare data and X(3842) MC(chi2_kf)"
    printf "\n\t%-9s  %-40s\n" "0.2.6" "Draw figures -- study chi2 of Dtag Dmissing pi pi"

    printf "\n\t%-9s  %-40s\n" "0.3"    "[Background Study]"
    printf "\n\t%-9s  %-40s\n" "0.3.1"  "Get samples -- get topology info"
    printf "\n\t%-9s  %-40s\n" "0.3.2"  "Download software -- download topology"
    printf "\n\t%-9s  %-40s\n" "0.3.3"  "Install software -- install topology"
    printf "\n\t%-9s  %-40s\n" "0.3.4"  "Topo analysis -- apply topology analysis"
    printf "\n\t%-9s  %-40s\n" "0.3.5"  "Get samples -- apply cuts before background study"
    printf "\n\t%-9s  %-40s\n" "0.3.6"  "Draw figures -- study status of matching before background study"
    printf "\n\t%-9s  %-40s\n" "0.3.7"  "Fit distributions -- fit to M(Dpi0)"
    printf "\n\t%-9s  %-40s\n" "0.3.8"  "Draw figures -- study status of matching on cut1"
    printf "\n\t%-9s  %-40s\n" "0.3.9"  "Fit distributions -- fit to M(pipi)"
    printf "\n\t%-9s  %-40s\n" "0.3.10" "Draw figures -- study status of matching on cut2"
    printf "\n\t%-9s  %-40s\n" "0.3.11" "Draw figures -- compare chi2 of vertex fit between types of matching status"
    printf "\n\t%-9s  %-40s\n" "0.3.12" "Draw figures -- study status of matching on cut3"
    printf "\n\t%-9s  %-40s\n" "0.3.13" "Draw figures -- cpmpare momentum of D between data and signal MC"
    printf "\n\t%-9s  %-40s\n" "0.3.14" "Draw figures -- study status of matching on cut4"
    printf "\n\t%-9s  %-40s\n" "0.3.15" "Draw figures -- compare invariant mass of M(Dpi) between data and signal MC"
    printf "\n\t%-9s  %-40s\n" "0.3.16" "Draw figures -- study status of matching on cut5"
    printf "\n\t%-9s  %-40s\n" "0.3.17" "Get samples -- apply cuts after background study"
    printf "\n\t%-9s  %-40s\n" "0.3.18" "Draw figures -- study RM(pipi)"
    printf "\n\t%-9s  %-40s\n" "0.3.19" "Draw figures -- study M(Dpipi)"

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
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-01(haven't applied cuts)"
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
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-02(have applied cuts)"
         ;;

    0.2.1) echo "Draw figures -- studying mass window of M(Kpipi)..."
           cd python
           python opt_mass_Kpipi.py 4360
           python opt_mass_Kpipi.py 4420
           python opt_mass_Kpipi.py 4600
           ;;

    0.2.2) echo "Draw figures -- studying signal region of RM(Dpipi)..."
           cd python
           python opt_signal_region.py 4360
           python opt_signal_region.py 4420
           python opt_signal_region.py 4600
           ;;

    0.2.3) echo "Get samples -- extracting useful info: signal region and sideband region..."
           echo "Please run selection algorithm codes again with M(Kpipi) and RM(Dpipi) cuts"
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

    0.2.5) echo "Draw figures -- comparing data and X(3842) MC(chi2_kf)..."
           cd python
           python plot_chi2_kf.py
           ;;

    0.2.6) echo "Draw figures -- studying chi2 of Dtag Dmissing pi pi..."
           cd python
           python opt_chi2_kf.py 4360
           python opt_chi2_kf.py 4420
           python opt_chi2_kf.py 4600
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
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-02(have applied cuts)"
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
           cp $HOME/bes/DDPIPI/v0.2/jobs/get_info_topo .
           hep_sub -g physics get_info_topo -o jobs.out -e jobs.err
           ;;

    0.3.2) echo "Download software -- downloading topology..."
           echo "Logout the SL5 environment to download topology v1.9.5!"
           mkdir -p topology
           cd topology
           rm -rf v1.9.5
           git clone https://github.com/zhixing1996/topology.git v1.9.5
           echo "Please login SL5 and set up BOSS6.6.4.p01 environment!"
           ;;

    0.3.3) echo "Install software -- installinging topology..."
           echo "Login SL5 and set up BOSS6.6.4.p01 environment!"
           cd topology/v1.9.5
           ./compile.sh
           echo "Please check how to set up topoana variable environment in its README.md file!"
           ;;

    0.3.4) echo "Topo analysis -- applying topology analysis..."
           echo "Must be executed in bash shell mode and set up topoana environment!"
           mkdir -p scripts/ana/topo
           cd scripts/ana/topo
           if [ ! -d "/besfs/users/$USER/bes/DDPIPI/v0.2/ana/topo" ]; then
               mkdir -p /besfs/users/$USER/bes/DDPIPI/v0.2/ana/topo
               ln -s /besfs/users/$USER/bes/DDPIPI/v0.2/ana/topo ./ana_topo
           fi
           cd ana_topo
           mkdir -p 4360
           cd 4360
           rm * -rf
           cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
           sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/DD\/4360\/incMC_DD_4360_topo.root/g" topoana.card
           sed -i "s/NAME/TopoResult_4360/g" topoana.card
           sed -i "s/cut_chi2_kf/20/g" topoana.card
           topoana.exe topoana.card
           cd ..
           mkdir -p 4420
           cd 4420
           rm * -rf
           cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
           sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/hadrons\/4420\/incMC_hadrons_4420_topo.root/g" topoana.card
           sed -i "s/NAME/TopoResult_4420/g" topoana.card
           sed -i "s/cut_chi2_kf/10/g" topoana.card
           topoana.exe topoana.card
           cd ..
           mkdir -p 4600
           cd 4600
           rm * -rf
           cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
           sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/DD\/4600\/incMC_DD_4600_topo.root/g" topoana.card
           sed -i "s/NAME/TopoResult_4600/g" topoana.card
           sed -i "s/cut_chi2_kf/25/g" topoana.card
           topoana.exe topoana.card
           ;;

    0.3.5) echo "Get samples -- applying cuts before background study..."
           cd jobs
           bash apply_cuts_before
           ;;

    0.3.6) echo "Draw figures -- studying status of matching before background study..."
           cd python
           python plot_stat_match.py raw
           ;;

    0.3.7) echo "Fit distributions -- fitting to M(Dpi0)..."
           cd cxx
           root -l -q fit_m_Dpi0_4420.cxx
           ;;

    0.3.8) echo "Draw figures -- studying status of matching on cut1..."
           cd python
           python plot_stat_match.py cut1
           ;;

    0.3.9) echo "Fit distributions -- fitting to M(pipi)..."
           cd cxx
           root -l -q fit_mKS_4420.cxx
           ;;

    0.3.10) echo "Draw figures -- studying status of matching on cut2..."
            cd python
            python plot_stat_match.py cut2
            ;;

    0.3.11) echo "Draw figures -- comparing chi2 of vertex fit between types of matching status..."
            cd python
            python plot_match_chi2_vf.py
            ;;

    0.3.12) echo "Draw figures -- studying status of matching on cut3..."
            cd python
            python plot_stat_match.py cut3
            ;;

    0.3.13) echo "Draw figures -- cpmparing momentum of D between data and signal MC..."
            cd python
            python plot_p_D.py
            ;;

    0.3.14) echo "Draw figures -- studying status of matching on cut4..."
            cd python
            python plot_stat_match.py cut4
            ;;

    0.3.15) echo "Draw figures -- comparing invariant mass of M(Dpi) between data and signal MC..."
            cd python
            python plot_m_Dpi.py
            ;;

    0.3.16) echo "Draw figures -- studying status of matching on cut5..."
            cd python
            python plot_stat_match.py cut5
            ;;

    0.3.17) echo "Get samples -- applying cuts of background study..."
            cd jobs
            bash apply_cuts_after
            ;;

    0.3.18) echo "Draw figures -- studying RM(pipi)..."
            cd python
            python plot_rm_pipi.py
            ;;

    0.3.19) echo "Draw figures -- studying M(Dpipi)..."
            cd python
            python plot_m_Dpipi.py
            ;;

esac
