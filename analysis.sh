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

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Study Cuts]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Draw figures -- draw invariant mass of Kpipi"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Draw figures -- study mass window of M(Kpipi)"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Draw figures -- draw recoiling mass of Dpipi"
    printf "\n\t%-9s  %-40s\n" "0.2.4" "Draw figures -- study signal region of RM(Dpipi)"
    printf "\n\t%-9s  %-40s\n" "0.2.5" "Get samples -- extract useful info: signal region and sideband region"
    printf "\n\t%-9s  %-40s\n" "0.2.6" "Get samples -- get data sideband samples"
    printf "\n\t%-9s  %-40s\n" "0.2.7" "Draw figures -- compare data and X(3842) MC(chi2_kf)"
    printf "\n\t%-9s  %-40s\n" "0.2.8" "Draw figures -- study chi2 of Dtag Dmissing pi pi"

    printf "\n\t%-9s  %-40s\n" "0.3"     "[Background Study]"
    printf "\n\t%-9s  %-40s\n" "0.3.1"   "Get samples -- get topology info"
    printf "\n\t%-9s  %-40s\n" "0.3.2"   "Get samples -- apply cuts before background study"
    printf "\n\t%-9s  %-40s\n" "0.3.3"   "Draw figures -- study RM(pipi) before background study"
    printf "\n\t%-9s  %-40s\n" "0.3.4"   "Calculate numbers -- calculate efficiency and significance before background study"
    printf "\n\t%-9s  %-40s\n" "0.3.5"   "Draw figures -- study M(pipi) before background study"
    printf "\n\t%-9s  %-40s\n" "0.3.6"   "Fit distributions -- fit to M(pipi)"
    printf "\n\t%-9s  %-40s\n" "0.3.7"   "Draw figures -- study ctau of pipi before background study"
    printf "\n\t%-9s  %-40s\n" "0.3.8"   "Calculate numbers -- calculate efficiency and significance of cut1"
    printf "\n\t%-9s  %-40s\n" "0.3.9"   "Fit distributions -- fit to M(Dpi0)"
    printf "\n\t%-9s  %-40s\n" "0.3.10"  "Calculate numbers -- calculate efficiency and significance of cut2"
    printf "\n\t%-9s  %-40s\n" "0.3.11"  "Get samples -- apply cuts after background study"
    printf "\n\t%-9s  %-40s\n" "0.3.12"  "Draw figures -- study RM(pipi) after background study"
    printf "\n\t%-9s  %-40s\n" "0.3.13"  "Download software -- download topology"
    printf "\n\t%-9s  %-40s\n" "0.3.14"  "Install software -- install topology"
    printf "\n\t%-9s  %-40s\n" "0.3.15"  "Topo analysis -- apply topology analysis"

    printf "\n\t%-9s  %-40s\n" "0.4"     "[Measurement of Cross Section]"
    printf "\n\t%-9s  %-40s\n" "0.4.1"   "Get samples -- divide samples according to invariant mass of Kpipi"
    printf "\n\t%-9s  %-40s\n" "0.4.2"   "Draw figures -- study RM(pipi) in Kpipi signal region"
    printf "\n\t%-9s  %-40s\n" "0.4.3"   "Fit distributions -- fit to RM(Dpipi)"
    printf "\n\t%-9s  %-40s\n" "0.4.4"   "Draw figures -- study RM(pipi) in fitting region"
    
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
         echo "--> Event Number: 1,000,000(signal MC, PHSP MC, inclusive MC)"
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
         echo "--> Event Number: 1,000,000(signal MC, PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Cross Section: D1(2420): 41.8+/-5.6+/-3.8pb(4360MeV), 65.4+/-3.0+/-5.7pb(4420MeV), 27.7+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Cross Section: psi(3770): 17.3+/-5.4+/-1.5pb(4360MeV), 23.8+/-2.6+/-2.1pb(4420MeV), 7.2+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89pb^{-1}(4420MeV), 566.93pb^{-1}(4600MeV)"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-02(have applied cuts)"
         ;;

    0.2.1) echo "Draw figures -- drawing invariant mass of Kpipi..."
           cd python
           python plot_m_Kpipi.py 4360
           python plot_m_Kpipi.py 4420
           python plot_m_Kpipi.py 4600
           ;;

    0.2.2) echo "Draw figures -- studying mass window of M(Kpipi)..."
           cd python
           python opt_m_Kpipi.py 4360
           python opt_m_Kpipi.py 4420
           python opt_m_Kpipi.py 4600
           ;;

    0.2.3) echo "Draw figures -- drawing recoiling mass of Dpipi..."
           cd python
           python plot_rm_Dpipi.py 4360
           python plot_rm_Dpipi.py 4420
           python plot_rm_Dpipi.py 4600
           ;;

    0.2.4) echo "Draw figures -- studying signal region of RM(Dpipi)..."
           cd python
           python opt_rm_Dpipi.py 4360
           python opt_rm_Dpipi.py 4420
           python opt_rm_Dpipi.py 4600
           ;;

    0.2.5) echo "Get samples -- extracting useful info: signal region and sideband region..."
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

    0.2.6) echo "Get samples -- getting data sideband samples..."
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

    0.2.7) echo "Draw figures -- comparing data and X(3842) MC(chi2_kf)..."
           cd python
           python plot_chi2_kf.py 4360
           python plot_chi2_kf.py 4420
           python plot_chi2_kf.py 4600
           ;;

    0.2.8) echo "Draw figures -- studying chi2 of Dtag Dmissing pi pi..."
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
         echo "--> Event Number: 1,000,000(signal MC, PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Cross Section: D1_2420: 41.8+/-5.6+/-3.8pb(4360MeV), 65.4+/-3.0+/-5.7pb(4420MeV), 27.7+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Cross Section: psi(3770): 17.3+/-5.4+/-1.5pb(4360MeV), 23.8+/-2.6+/-2.1pb(4420MeV), 7.2+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89pb^{-1}(4420MeV), 566.93pb^{-1}(4600MeV)"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03(have applied cuts)"
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

    0.3.2) echo "Get samples -- applying cuts before background study..."
           cd jobs
           bash apply_cuts_before
           ;;

    0.3.3) echo "Draw figures -- studying RM(pipi) before background study..."
           cd python
           python plot_rm_pipi.py 4360 before
           python plot_rm_pipi.py 4420 before
           python plot_rm_pipi.py 4600 before
           ;;

    0.3.4) echo "Calculate numbers -- calculating efficiency and significance before background study..."
           cd python
           python cal.py 4360 raw
           python cal.py 4420 raw
           python cal.py 4600 raw
           ;;

    0.3.5) echo "Draw figures -- studying M(pipi) before background study..."
           cd python
           python plot_m_pipi.py 4360 before
           python plot_m_pipi.py 4420 before
           python plot_m_pipi.py 4600 before
           ;;

    0.3.6) echo "Fit distributions -- fitting to M(pipi)..."
           cd python
           python fit_m_pipi.py 4360
           python fit_m_pipi.py 4420
           python fit_m_pipi.py 4600
           ;;

    0.3.7) echo "Draw figures -- studying ctau of pipi before background study..."
           cd python
           python plot_ctau_pipi.py 4360
           python plot_ctau_pipi.py 4420
           python plot_ctau_pipi.py 4600
           ;;

    0.3.8) echo "Calculate numbers -- calculating efficiency and significance of cut1..."
            cd python
            python cal.py 4360 cut1
            python cal.py 4420 cut1
            python cal.py 4600 cut1
            ;;

    0.3.9) echo "Fit distributions -- fitting to M(Dpi0)..."
           cd python
           python fit_m_Dpi0.py 4360
           python fit_m_Dpi0.py 4420
           python fit_m_Dpi0.py 4600
           ;;

    0.3.10) echo "Calculate numbers -- calculating efficiency and significance of cut2..."
            cd python
            python cal.py 4360 cut2
            python cal.py 4420 cut2
            python cal.py 4600 cut2
            ;;

    0.3.11) echo "Get samples -- applying cuts of background study..."
            cd jobs
            bash apply_cuts_after
            ;;

    0.3.12) echo "Draw figures -- studying RM(pipi) after background study..."
            cd python
            python plot_rm_pipi.py 4360 after
            python plot_rm_pipi.py 4420 after
            python plot_rm_pipi.py 4600 after
            ;;

    0.3.13) echo "Draw figures -- studying M(pipi) after background study..."
            cd python
            python plot_m_pipi.py 4360 after
            python plot_m_pipi.py 4420 after
            python plot_m_pipi.py 4600 after
            ;;

    0.3.14) echo "Download software -- downloading topology..."
            echo "Logout the SL5 environment to download topology v1.9.5!"
            mkdir -p topology
            cd topology
            rm -rf v1.9.5
            git clone https://github.com/zhixing1996/topology.git v1.9.5
            echo "Please login SL5 and set up BOSS6.6.4.p01 environment!"
            ;;

    0.3.15) echo "Install software -- installinging topology..."
            echo "Login SL5 and set up BOSS6.6.4.p01 environment!"
            cd topology/v1.9.5
            ./compile.sh
            echo "Please check how to set up topoana variable environment in its README.md file!"
            ;;

    0.3.16) echo "Topo analysis -- applying topology analysis..."
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
            mkdir -p DD
            cd DD
            rm * -rf
            cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
            sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/DD\/4360\/incMC_DD_4360_topo.root/g" topoana.card
            sed -i "s/NAME/TopoResult_4360_DD/g" topoana.card
            sed -i "s/cut_chi2_kf/15/g" topoana.card
            topoana.exe topoana.card
            cd ..
            mkdir -p qq
            cd qq
            rm * -rf
            cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
            sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/qq\/4360\/incMC_qq_4360_topo.root/g" topoana.card
            sed -i "s/NAME/TopoResult_4360_qq/g" topoana.card
            sed -i "s/cut_chi2_kf/15/g" topoana.card
            topoana.exe topoana.card
            cd ../..
            mkdir -p 4420
            cd 4420
            mkdir -p DD
            cd DD
            rm * -rf
            cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
            sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/DD\/4420\/incMC_DD_4420_topo.root/g" topoana.card
            sed -i "s/NAME/TopoResult_4420_DD/g" topoana.card
            sed -i "s/cut_chi2_kf/15/g" topoana.card
            topoana.exe topoana.card
            cd ..
            mkdir -p qq
            cd qq
            rm * -rf
            cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
            sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/qq\/4420\/incMC_qq_4420_topo.root/g" topoana.card
            sed -i "s/NAME/TopoResult_4420_qq/g" topoana.card
            sed -i "s/cut_chi2_kf/15/g" topoana.card
            topoana.exe topoana.card
            cd ../..
            mkdir -p 4600
            cd 4600
            mkdir -p DD
            cd DD
            rm * -rf
            cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
            sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/DD\/4600\/incMC_DD_4600_topo.root/g" topoana.card
            sed -i "s/NAME/TopoResult_4600_DD/g" topoana.card
            sed -i "s/cut_chi2_kf/15/g" topoana.card
            topoana.exe topoana.card
            cd ..
            mkdir -p qq
            cd qq
            rm * -rf
            cp $HOME/bes/DDPIPI/v0.2/scripts/ana_script/topo/topoana.card . -rf
            sed -i "s/PATH/\/besfs\/users\/$USER\/bes\/DDPIPI\/v0.2\/incMC\/qq\/4600\/incMC_qq_4600_topo.root/g" topoana.card
            sed -i "s/NAME/TopoResult_4600_qq/g" topoana.card
            sed -i "s/cut_chi2_kf/15/g" topoana.card
            topoana.exe topoana.card
            cd ../..
            ;;

    # ---------------------------------
    #  0.4 Measurement of Cross Section
    # ---------------------------------

    0.4) echo "Measurement of cross section..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC, PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Cross Section: D1(2420): 41.8+/-5.6+/-3.8pb(4360MeV), 65.4+/-3.0+/-5.7pb(4420MeV), 27.7+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Cross Section: psi(3770): 17.3+/-5.4+/-1.5pb(4360MeV), 23.8+/-2.6+/-2.1pb(4420MeV), 7.2+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89pb^{-1}(4420MeV), 566.93pb^{-1}(4600MeV)"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03(have applied cuts)"
         ;;

    0.4.1) echo "Get samples -- dividing samples according to invariant mass of Kpipi..."
           cd python
           python divide_samples.py 4360
           python divide_samples.py 4420
           python divide_samples.py 4600
           ;;

    0.4.2) echo "Draw figures -- studying RM(Dpipi) in Kpipi signal and sideband region..."
           cd python
           python plot_rm_Dpipi.py 4360 signal_after
           python plot_rm_Dpipi.py 4420 signal_after
           python plot_rm_Dpipi.py 4600 signal_after
           python plot_rm_Dpipi.py 4360 sideband_after
           python plot_rm_Dpipi.py 4420 sideband_after
           python plot_rm_Dpipi.py 4600 sideband_after
           ;;

    0.4.3) echo "Fit distributions -- fitting to RM(Dpipi)..."
           cd python
           python fit_rm_Dpipi.py 4360 data
           python fit_rm_Dpipi.py 4360 D1_2420
           python fit_rm_Dpipi.py 4360 psipp
           python fit_rm_Dpipi.py 4420 data
           python fit_rm_Dpipi.py 4420 D1_2420
           python fit_rm_Dpipi.py 4420 psipp
           python fit_rm_Dpipi.py 4600 data
           python fit_rm_Dpipi.py 4600 D1_2420
           python fit_rm_Dpipi.py 4600 psipp
           ;;

    0.4.4) echo "Draw figures -- studying RM(pipi) in fitting region..."
           cd python
           python plot_rm_pipi 4360 X_3842
           python plot_rm_pipi 4420 X_3842
           python plot_rm_pipi 4600 X_3842
           ;;

esac
