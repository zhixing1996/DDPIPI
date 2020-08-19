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
    printf "\n\t%-9s  %-40s\n" "0.2.6" "Draw figures -- compare data and X(3842) MC(chi2_kf)"
    printf "\n\t%-9s  %-40s\n" "0.2.7" "Draw figures -- study chi2 of Dtag Dmissing pi pi"

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

    printf "\n\t%-9s  %-40s\n" "0.4"      "[Measurement of DDPIPI Cross Section]"
    printf "\n\t%-9s  %-40s\n" "0.4.1"    "Get samples -- synthesize samples"
    printf "\n\t%-9s  %-40s\n" "0.4.2"    "Get samples -- Get samples -- extract useful info: raw and signal"
    printf "\n\t%-9s  %-40s\n" "0.4.3"    "Get samples -- apply cuts"
    printf "\n\t%-9s  %-40s\n" "0.4.4"    "[D1_2420 & psi(3770)] Draw figures -- study RM(D) in fitting region(RM(Dpipi) signal and sideband region)"
    printf "\n\t%-9s  %-40s\n" "0.4.5"    "[D1_2420 & psi(3770)] Get shape -- get shape of D1(2420)"
    printf "\n\t%-9s  %-40s\n" "0.4.6"    "[D1_2420 & psi(3770)] Get samples -- get samples used for RM(D) fit"
    printf "\n\t%-9s  %-40s\n" "0.4.7"    "[D1_2420 & psi(3770)] Fit distributions -- perform RM(D) and RM(pipi) simultaneous fit"
    printf "\n\t%-9s  %-40s\n" "0.4.8"    "[DDPIPI] Draw figures -- study RM(Dpipi) in Kpipi signal and sideband region"
    printf "\n\t%-9s  %-40s\n" "0.4.9"    "[DDPIPI] Get shape -- mix MC shape"
    printf "\n\t%-9s  %-40s\n" "0.4.10"   "[DDPIPI] Fit distributions -- fit to RM(Dpipi)"
    printf "\n\t%-9s  %-40s\n" "0.4.11"   "[DDPIPI] Fit distributions -- fit to MM(Kpipi)"
    printf "\n\t%-9s  %-40s\n" "0.4.12"   "[DDPIPI] Calculate numbers -- calculate cross sections"
    printf "\n\t%-9s  %-40s\n" "0.4.13"   "[DDPIPI] Calculate numbers -- format cross section outputs"
    printf "\n\t%-9s  %-40s\n" "0.4.14"   "[DDPIPI] Draw figures -- draw cross sections"
    printf "\n\t%-9s  %-40s\n" "0.4.15"   "[ROUND1: D1_2420 & psi(3770)] Get factor -- get ridiative correction and vacuum polarization factors"
    printf "\n\t%-9s  %-40s\n" "0.4.16"   "[ROUND1: D1_2420 & psi(3770)] Get shape -- get shape of D1(2420)"
    printf "\n\t%-9s  %-40s\n" "0.4.17"   "[ROUND1: D1_2420 & psi(3770)] Get samples -- get samples used for RM(D) fit"
    printf "\n\t%-9s  %-40s\n" "0.4.18"   "[ROUND1: D1_2420 & psi(3770)] Fit distributions -- perform RM(D) and RM(pipi) simultaneous fit"
    printf "\n\t%-9s  %-40s\n" "0.4.19"   "[ROUND1: DDPIPI] Get shape -- mix MC shape"
    printf "\n\t%-9s  %-40s\n" "0.4.20"   "[ROUND1: DDPIPI] Fit distributions -- fit to RM(Dpipi)"
    printf "\n\t%-9s  %-40s\n" "0.4.21"   "[ROUND1: DDPIPI] Fit distributions -- fit to MM(Kpipi)"
    printf "\n\t%-9s  %-40s\n" "0.4.22"   "[ROUND1: DDPIPI] Calculate numbers -- calculate cross sections"
    printf "\n\t%-9s  %-40s\n" "0.4.23"   "[ROUND1: DDPIPI] Calculate numbers -- format cross section outputs"
    printf "\n\t%-9s  %-40s\n" "0.4.24"   "[ROUND1: DDPIPI] Draw figures -- draw cross sections"
    printf "\n\t%-9s  %-40s\n" "0.4.25"   "[ROUND1: DDPIPI] Draw figures -- draw cross section differences between iterations"
    printf "\n\t%-9s  %-40s\n" "0.4.26"   "[DDPIPI] Calculate numbers -- calculate significance and upper limit number of total DDPIPI"
    
    printf "\n\t%-9s  %-40s\n" "0.5"      "[Measurement of X(3842) Cross Section]"
    printf "\n\t%-9s  %-40s\n" "0.5.1"    "Get samples -- synthesize samples"
    printf "\n\t%-9s  %-40s\n" "0.5.2"    "Get samples -- Get samples -- extract useful info: raw and signal"
    printf "\n\t%-9s  %-40s\n" "0.5.3"    "Get samples -- apply cuts"
    printf "\n\t%-9s  %-40s\n" "0.5.4"    "Draw figures -- study RM(pipi) in fitting region"
    printf "\n\t%-9s  %-40s\n" "0.5.5"    "Fit distributions -- fit to RM(pipi)(with and without X(3842) signal)"
    printf "\n\t%-9s  %-40s\n" "0.5.6"    "Calculate numbers -- calculate significance and upper limit number of X(3842)"

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

    0.2.6) echo "Draw figures -- comparing data and D1(2420) MC(chi2_kf)..."
           cd python
           python plot_chi2_kf.py 4360 STDDmiss
           python plot_chi2_kf.py 4420 STDDmiss 
           python plot_chi2_kf.py 4600 STDDmiss 
           python plot_chi2_kf.py 4360 STD
           python plot_chi2_kf.py 4420 STD 
           python plot_chi2_kf.py 4600 STD 
           ;;

    0.2.7) echo "Draw figures -- studying chi2 of Dtag Dmissing pi pi..."
           cd python
           python opt_chi2_kf.py 4360 STDDmiss
           python opt_chi2_kf.py 4420 STDDmiss
           python opt_chi2_kf.py 4600 STDDmiss
           python opt_chi2_kf.py 4360 STD
           python opt_chi2_kf.py 4420 STD
           python opt_chi2_kf.py 4600 STD
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

    # ----------------------------------------
    #  0.4 Measurement of DDPIPI Cross Section
    # ----------------------------------------

    0.4) echo "Measurement of DDPIPI cross section..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC, PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Cross Section: D1(2420): 41.8+/-5.6+/-3.8pb(4360MeV), 65.4+/-3.0+/-5.7pb(4420MeV), 27.7+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Cross Section: psi(3770): 17.3+/-5.4+/-1.5pb(4360MeV), 23.8+/-2.6+/-2.1pb(4420MeV), 7.2+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89pb^{-1}(4420MeV), 566.93pb^{-1}(4600MeV)"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03(have applied cuts)"
         ;;

    0.4.1) echo "Get samples -- synthesizing samples..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data
           ./synthesizeData_703p01.sh
           ./synthesizeData_705.sh
           cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc
           cd D1_2420
           ./synthesizeD1_2420_703p01.sh
           ./synthesizeD1_2420_705.sh
           cd ../DDPIPI
           ./synthesizeD_D_PI_PI_703p01.sh
           ./synthesizeD_D_PI_PI_705.sh
           cd ../psipp
           ./synthesizepsipp_703p01.sh
           ./synthesizepsipp_705.sh
           ;;

    0.4.2) echo "Get samples -- extracting useful info: raw and signal..."
           mkdir -p scripts/ana/sel
           cd scripts/ana/sel
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/sel/jobs_ana" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/sel/jobs_ana
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/sel/jobs_ana ./jobs_ana
           fi
           cd jobs_ana
           # rm -rf jobs.out
           # rm -rf jobs.err
           mkdir -p jobs.out
           mkdir -p jobs.err

           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/getInfoData_703p01.sh .
           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/Data_Base_703p01 .
           # echo "#!/bin/bash" > Data_Sub_703p01
           # echo "./getInfoData_703p01.sh" >> Data_Sub_703p01
           # chmod u+x Data_Sub_703p01
           # hep_sub -g physics Data_Sub_703p01 -o jobs.out -e jobs.err

           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/D1_2420/getInfoD1_2420_703p01.sh .
           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/D1_2420/D1_2420_Base_703p01 .
           # echo "#!/bin/bash" > D1_2420_Sub_703p01
           # echo "./getInfoD1_2420_703p01.sh" >> D1_2420_Sub_703p01
           # chmod u+x D1_2420_Sub_703p01
           # hep_sub -g physics D1_2420_Sub_703p01 -o jobs.out -e jobs.err

           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/DDPIPI/getInfoD_D_PI_PI_703p01.sh .
           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/DDPIPI/DDPIPI_Base_703p01 .
           # echo "#!/bin/bash" > D_D_PI_PI_Sub_703p01
           # echo "./getInfoDDPIPI_703p01.sh" >> D_D_PI_PI_Sub_703p01
           # chmod u+x D_D_PI_PI_Sub_703p01
           # hep_sub -g physics D_D_PI_PI_Sub_703p01 -o jobs.out -e jobs.err

           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/psipp/getInfopsipp_703p01.sh .
           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/psipp/psipp_Base_703p01 .
           # echo "#!/bin/bash" > psipp_Sub_703p01
           # echo "./getInfopsipp_703p01.sh" >> psipp_Sub_703p01
           # chmod u+x psipp_Sub_703p01
           # hep_sub -g physics psipp_Sub_703p01 -o jobs.out -e jobs.err

           cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/getInfoData_705.sh .
           cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/Data_Base_705 .
           echo "#!/bin/bash" > Data_Sub_705
           echo "./getInfoData_705.sh" >> Data_Sub_705
           chmod u+x Data_Sub_705
           hep_sub -g physics Data_Sub_705 -o jobs.out -e jobs.err

           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/D1_2420/getInfoD1_2420_705.sh .
           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/D1_2420/D1_2420_Base_705 .
           # echo "#!/bin/bash" > D1_2420_Sub_705
           # echo "./getInfoD1_2420_705.sh" >> D1_2420_Sub_705
           # chmod u+x D1_2420_Sub_705
           # hep_sub -g physics D1_2420_Sub_705 -o jobs.out -e jobs.err

           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/DDPIPI/getInfoD_D_PI_PI_705.sh .
           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/DDPIPI/DDPIPI_Base_705 .
           # echo "#!/bin/bash" > D_D_PI_PI_Sub_705
           # echo "./getInfoDDPIPI_705.sh" >> D_D_PI_PI_Sub_705
           # chmod u+x D_D_PI_PI_Sub_705
           # hep_sub -g physics D_D_PI_PI_Sub_705 -o jobs.out -e jobs.err

           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/psipp/getInfopsipp_705.sh .
           # cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/psipp/psipp_Base_705 .
           # echo "#!/bin/bash" > psipp_Sub_705
           # echo "./getInfopsipp_705.sh" >> psipp_Sub_705
           # chmod u+x psipp_Sub_705
           # hep_sub -g physics psipp_Sub_705 -o jobs.out -e jobs.err
           ;;

    0.4.3) echo "Get samples -- applying cuts..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data
           ./applyCutsData_703p01.sh
           ./applyCutsData_705.sh
           cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc
           cd D1_2420
           ./applyCutsD1_2420_703p01.sh
           ./applyCutsD1_2420_705.sh
           cd ../DDPIPI
           ./applyCutsD_D_PI_PI_703p01.sh
           ./applyCutsD_D_PI_PI_705.sh
           cd ../psipp
           ./applyCutspsipp_703p01.sh
           ./applyCutspsipp_705.sh
           ;;

    0.4.4) echo "[D1_2420 & psi(3770)] Draw figures -- studying RM(D) in fitting region(RM(Dpipi) signal and sideband region)..."
           cd python 
           python plot_rm_D.py 4360
           python plot_rm_D.py 4420
           python plot_rm_D.py 4600
           ;;

    0.4.5) echo "[D1_2420 & psi(3770)] Get shape -- getting shape of D1(2420)..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
           ./getShape_703p01.sh
           ./getShape_705.sh
           ;;

    0.4.6) echo "[D1_2420 & psi(3770)] Get samples -- getting samples used for RM(D) fit..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
           ./convertROOT_703p01.sh
           ./convertROOT_705.sh
           ;;

    0.4.7) echo "[D1_2420 & psi(3770)] Fit distributions -- performing RM(D) and RM(pipi) simultaneous fit..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
           ./simul_fit_703p01.sh round0
           ./simul_fit_705.sh round0
           ;;

    0.4.8) echo "[DDPIPI] Draw figures -- studying RM(Dpipi) in Kpipi signal and sideband region..."
           cd python
           python plot_rm_Dpipi.py 4360 signal
           python plot_rm_Dpipi.py 4420 signal
           python plot_rm_Dpipi.py 4600 signal
           python plot_rm_Dpipi_sideband.py 4360
           python plot_rm_Dpipi_sideband.py 4420
           python plot_rm_Dpipi_sideband.py 4600
           ;;

    0.4.9) echo "[DDPIPI] Get shape -- mixing MC shapes..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc
           cd mix
           ./mixMC_703p01.sh round0
           ./mixMC_705.sh round0
           ;;

    0.4.10) echo "[DDPIPI] Fit distributions -- fitting to RM(Dpipi)..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./fitRMDpipi_703p01.sh round0
            ./fitRMDpipi_705.sh round0
            ;;

    0.4.11) echo "[DDPIPI] Fit distributions -- fitting to M(Kpipi)..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./mixROOT_703p01.sh round0
            ./mixROOT_705.sh round0
            ./factorMKpipi_703p01.sh round0
            ./factorMKpipi_705.sh round0
            ;;

    0.4.12) echo "[DDPIPI] Calculate numbers -- calculating cross sections..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./calXS_703p01.sh round0
            ./calXS_705.sh round0
            ;;

    0.4.13) echo "[DDPIPI] Calculate numbers -- formatting cross section outputs..."
            cd python
            python format_xs.py round0
            ;;

    0.4.14) echo "[DDPIPI] Draw figures -- drawing cross sections..."
            cd python
            python plot_xs.py total round0
            ;;

    0.4.15) echo "[ROUND1: D1_2420 & psi(3770)] Get factor -- getting ridiative correction and vacuum polarization factors..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/D1_2420
            ./getFactorD1_2420_703p01.sh round1
            ./getFactorD1_2420_705.sh round1
            ;;

    0.4.16) echo "[ROUND1: D1_2420 & psi(3770)] Get shape -- getting shape of D1(2420)..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./getShape_703p01.sh
            ./getShape_705.sh
            ;;

    0.4.17) echo "[ROUND1: D1_2420 & psi(3770)] Get samples -- getting samples used for RM(D) fit..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./convertROOT_703p01.sh
            ./convertROOT_705.sh
            ;;

    0.4.18) echo "[ROUND1: D1_2420 & psi(3770)] Fit distributions -- performing RM(D) and RM(pipi) simultaneous fit..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./simul_fit_703p01.sh round1
            ./simul_fit_705.sh round1
            ;;

    0.4.19) echo "[ROUND1: DDPIPI] Get shape -- mixing MC shapes..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc
            cd mix
            ./mixMC_703p01.sh round1
            ./mixMC_705.sh round1
            ;;

    0.4.20) echo "[ROUND1: DDPIPI] Fit distributions -- fitting to RM(Dpipi)..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./fitRMDpipi_703p01.sh round1
            ./fitRMDpipi_705.sh round1
            ;;

    0.4.21) echo "[ROUND1: DDPIPI] Fit distributions -- fitting to M(Kpipi)..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./mixROOT_703p01.sh round1
            ./mixROOT_705.sh round1
            ./factorMKpipi_703p01.sh round1
            ./factorMKpipi_705.sh round1
            ;;

    0.4.22) echo "[ROUND1: DDPIPI] Calculate numbers -- calculating cross sections..."
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./calXS_703p01.sh round1
            ./calXS_705.sh round1
            ;;

    0.4.23) echo "[ROUND1: DDPIPI] Calculate numbers -- formatting cross section outputs..."
            cd python
            python format_xs.py round1
            ;;

    0.4.24) echo "[ROUND1: DDPIPI] Draw figures -- drawing cross sections..."
            cd python
            python plot_xs.py total round1
            ;;

    0.4.25) echo "[ROUND1: DDPIPI] Draw figures -- drawing cross section differences between iterations..."
            cd python
            python plot_xs_diff.py DDPIPI
            python plot_xs_diff.py D1_2420
            python plot_xs_diff.py psipp
            python plot_xs_diff.py total
            ;;

    0.4.26) echo "[DDPIPI] Calculate numbers -- calculating significance and upper limit number of total DDPIPI..."
            rm -rf $HOME/bes/DDPIPI/v0.2/python/txts/significance_*.txt
            rm -rf $HOME/bes/DDPIPI/v0.2/python/txts/upper_limit_likelihood_total_*.txt
            rm -rf $HOME/bes/DDPIPI/v0.2/python/txts/xs_upper_limit_total.txt
            cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
            ./calSignificance_total_703p01.sh round4
            ./calSignificance_total_705.sh round4
            ./calUpperLimit_total_703p01.sh round4
            ;;

    # ----------------------------------------
    #  0.5 Measurement of X(3842) Cross Section
    # ----------------------------------------

    0.5) echo "Measurement of X(3842) cross section..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC, PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Cross Section: D1(2420): 41.8+/-5.6+/-3.8pb(4360MeV), 65.4+/-3.0+/-5.7pb(4420MeV), 27.7+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Cross Section: psi(3770): 17.3+/-5.4+/-1.5pb(4360MeV), 23.8+/-2.6+/-2.1pb(4420MeV), 7.2+/-2.7+/-1.2pb(4600MeV)" 
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89pb^{-1}(4420MeV), 566.93pb^{-1}(4600MeV)"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03(have applied cuts)"
         ;;

    0.5.1) echo "Get samples -- synthesizing samples..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc
           cd X_3842
           ./synthesizeX_3842_703p01.sh
           ;;

    0.5.2) echo "Get samples -- extracting useful info: raw and signal..."
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

           cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/X_3842/getInfoX_3842_703p01.sh .
           cp $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/X_3842/X_3842_Base_703p01 .
           echo "#!/bin/bash" > X_3842_Sub_703p01
           echo "./getInfoX_3842_703p01.sh" >> X_3842_Sub_703p01
           chmod u+x X_3842_Sub_703p01
           hep_sub -g physics X_3842_Sub_703p01 -o jobs.out -e jobs.err
           ;;

    0.5.3) echo "Get samples -- applying cuts..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc
           cd X_3842
           ./applyCutsX_3842_703p01.sh
           ;;

    0.5.4) echo "Draw figures -- studying RM(pipi) in fitting region..."
           cd python
           python plot_rm_pipi.py 4360 X_3842 
           python plot_rm_pipi.py 4420 X_3842
           python plot_rm_pipi.py 4600 X_3842
           ;;

    0.5.5) echo "Fit distributions -- fitting to RM(pipi)(with and without X(3842) signal)..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
           rm -rf $HOME/bes/DDPIPI/v0.2/python/txts/significance_likelihood_4*
           ./fitRMpipi_703p01.sh
           ./fitRMpipi_705.sh
           ;;

    0.5.6) echo "Calculate numbers -- calculating significance and upper limit number of X(3842)..."
           cd $HOME/bes/DDPIPI/v0.2/scripts/ana_script/xs
           ./calSignificance_X_3842_703p01.sh
           ./calUpperLimit_X_3842_703p01.sh
           ./calSignificance_X_3842_705.sh
           ./calUpperLimit_X_3842_705.sh
           ;;

esac
