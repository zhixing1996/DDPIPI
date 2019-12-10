#!/usr/bin/env bash

# Main driver to submit simulation and reconstruction jobs as well as generating root files 
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-09-02 Mon 22:17]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit simulation and reconstruction jobs as well as generating root files\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./submit.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[run on signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[run on signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.3"   "[run on signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.3.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.3.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.4"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.4.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.4.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.5"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.5.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.5.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.6"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.6.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.6.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.7"   "[run on signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.7.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.7.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.8"   "[run on signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.8.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.8.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.9"   "[run on signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.9.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.9.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.10"   "[run on inclusive MC (qqbar) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.10.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.11"   "[run on inclusive MC (qqbar) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.11.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.12"   "[run on inclusive MC (qqbar) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.12.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.13"   "[run on data @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.13.1" "Single D tag -- data sample"

    printf "\n\t%-9s  %-40s\n" "0.14"   "[run on data @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.14.1" "Single D tag -- data sample"

    printf "\n\t%-9s  %-40s\n" "0.15"   "[run on data @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.15.1" "Single D tag -- data sample"

    printf "\n\t%-9s  %-40s\n" "0.16"   "[run on inclusive MC (open harm) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.16.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.17"   "[run on inclusive MC (open harm) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.17.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.18"   "[run on inclusive MC (open harm) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.18.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.19"   "[run on inclusive MC (bhabha) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.19.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.20"   "[run on inclusive MC (dimu) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.20.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.21"   "[run on inclusive MC (ditau) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.21.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.22"   "[run on inclusive MC (digamma) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.22.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.23"   "[run on inclusive MC (twogamma) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.23.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.24"   "[run on inclusive MC (ISR) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.24.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.25"   "[run on inclusive MC (gammaXYZ) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.25.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.26"   "[run on inclusive MC (hadrons) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.26.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.27"   "[run on inclusive MC (bhabha) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.27.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.28"   "[run on inclusive MC (dimu) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.28.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.29"   "[run on inclusive MC (ditau) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.29.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.30"   "[run on inclusive MC (digamma) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.30.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.31"   "[run on inclusive MC (bhabha) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.31.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.32"   "[run on inclusive MC (dimu) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.32.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.33"   "[run on inclusive MC (ditau) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.33.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.34"   "[run on inclusive MC (digamma) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.34.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.35"   "[run on inclusive MC (twogamma) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.35.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.36"   "[run on inclusive MC (LL) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.36.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.37"   "[run on signal MC of psi(4415)->D2_(2460)D(PHSP), D2_(2460)->DPIPI(PHSP) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.37.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.37.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.38"   "[run on signal MC of psi(4415)->D2_(2460)D(PHSP), D2_(2460)->DPIPI(PHSP) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.38.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.38.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.39"   "[run on signal MC of psi(4415)->D2_(2460)D(PHSP), D2_(2460)->DPIPI(PHSP) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.39.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.39.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.40"   "[run on signal MC of psi(4415)->DDPIPI(PHSP) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.40.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.40.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.41"   "[run on signal MC of psi(4415)->DDPIPI(PHSP) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.41.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.41.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.42"   "[run on signal MC of psi(4415)->DDPIPI(PHSP) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.42.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.42.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.43"   "[run on signal MC of psi(4415)->D0_(2300)DPI(PHSP), D0_(2300)->DPI(PHSP) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.43.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.43.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.44"   "[run on signal MC of psi(4415)->D0_(2300)DPI(PHSP), D0_(2300)->DPI(PHSP) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.44.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.44.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.45"   "[run on signal MC of psi(4415)->D0_(2300)DPI(PHSP), D0_(2300)->DPI(PHSP) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.45.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.45.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.46"   "[run on data reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.46.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.47"   "[run on signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) reconstructed @703p01]" 
    printf "\n\t%-9s  %-40s\n" "0.47.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.47.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.48"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) reconstructed @703p01]" 
    printf "\n\t%-9s  %-40s\n" "0.48.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.48.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.49"   "[run on signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.49.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.49.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.50"   "[run on signal MC of psi(4415)->DDPIPI(PHSP) reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.50.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.50.2" "Single D tag -- run on signal MC sample"

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

    # --------------------------------------------------------------------------
    #  0.1 signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4360MeV
    # --------------------------------------------------------------------------
    
    0.1) echo "signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4360MeV..."
         echo "--> Process: psi(4415)->X(3842)PIPI, X(3842)->DD"
         echo "--> E_{CMS}: 4360MeV"
         echo "--> Generation mode: psi(4415)->X(3842)PIPI PHSH; X(3842)->DD PHSP; D decay D_DALITZ(assignated mode) or inlusive decay"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 30616~31279"
         ;;

    0.1.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/X_3842/4360
           cd scripts/sigMC/X_3842/4360
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4360/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4360/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4360/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_X_3842_PI_PI_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/rtraw/*.rtraw
           ./jobOptions_sim_sig_X_3842_PI_PI_PHSP_4360.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_X_3842_PI_PI_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/dst/*.dst
           ./jobOptions_rec_sig_X_3842_PI_PI_PHSP_4360.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_X_3842_PI_PI_PHSP_4360 jobOptions_rec_sig_X_3842_PI_PI_PHSP_4360 subSimRec 0 99
           ;;

    0.1.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/rootfile
           cd scripts/sigMC/X_3842/4360/jobs_sig
           rm -rf sigMC_X_3842_PI_PI_PHSP_4360_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/dst sigMC X_3842_PI_PI PHSP X_3842 4360 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4360/rootfile/*root
           ./subAna.sh sigMC_X_3842_PI_PI_PHSP_4360
           ;;

    # --------------------------------------------------------------------------
    #  0.2 signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4420MeV
    # --------------------------------------------------------------------------
    
    0.2) echo "signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4420MeV..."
         echo "--> Process: psi(4415)->X(3842)PIPI, X(3842)->DD"
         echo "--> E_{CMS}: 4420MeV"
         echo "--> Generation mode: psi(4415)->X(3842)PIPI PHSH; X(3842)->DD PHSP; D decay D_DALITZ(assignated mode) or inlusive decay"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 31327~31390, 36773~38140"
         ;;

    0.2.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/X_3842/4420
           cd scripts/sigMC/X_3842/4420
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4420/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4420/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4420/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_X_3842_PI_PI_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/rtraw/*.rtraw
           ./jobOptions_sim_sig_X_3842_PI_PI_PHSP_4420.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_X_3842_PI_PI_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/dst/*.dst
           ./jobOptions_rec_sig_X_3842_PI_PI_PHSP_4420.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_X_3842_PI_PI_PHSP_4420 jobOptions_rec_sig_X_3842_PI_PI_PHSP_4420 subSimRec 0 99
           ;;

    0.2.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/rootfile
           cd scripts/sigMC/X_3842/4420/jobs_sig
           rm -rf sigMC_X_3842_PI_PI_PHSP_4420_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/dst sigMC X_3842_PI_PI PHSP X_3842 4420 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4420/rootfile/*root
           ./subAna.sh sigMC_X_3842_PI_PI_PHSP_4420
           ;;

    # --------------------------------------------------------------------------
    #  0.3 signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4600MeV
    # --------------------------------------------------------------------------
    
    0.3) echo "signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) @4600MeV..."
         echo "--> Process: psi(4415)->X(3842)PIPI, X(3842)->DD"
         echo "--> E_{CMS}: 4600MeV"
         echo "--> Generation mode: psi(4415)->X(3842)PIPI PHSH; X(3842)->DD PHSP; D decay D_DALITZ(assignated mode) or inlusive decay"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 35227~36213"
         ;;

    0.3.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/X_3842/4600
           cd scripts/sigMC/X_3842/4600
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4600/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4600/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/4600/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_X_3842_PI_PI_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/rtraw/*.rtraw
           ./jobOptions_sim_sig_X_3842_PI_PI_PHSP_4600.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_X_3842_PI_PI_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/dst/*.dst
           ./jobOptions_rec_sig_X_3842_PI_PI_PHSP_4600.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_X_3842_PI_PI_PHSP_4600 jobOptions_rec_sig_X_3842_PI_PI_PHSP_4600 subSimRec 0 99
           ;;

    0.3.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/rootfile
           cd scripts/sigMC/X_3842/4600/jobs_sig
           rm -rf sigMC_X_3842_PI_PI_PHSP_4600_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/dst sigMC X_3842_PI_PI PHSP X_3842 4600 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/4600/rootfile/*root
           ./subAna.sh sigMC_X_3842_PI_PI_PHSP_4600
           ;;

    # --------------------------------------------------------------------------------
    #  0.4 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(HELAMP) @4360MeV
    # --------------------------------------------------------------------------------
    
    0.4) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) @4360MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4360MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPIPI HELAMP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 30616~31279"
         ;;

    0.4.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/D1_2420/4360
           cd scripts/sigMC/D1_2420/4360
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4360/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4360/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4360/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_HELAMP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_HELAMP_4360.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_HELAMP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_HELAMP_4360.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_D1_2420_D_HELAMP_4360 jobOptions_rec_sig_D1_2420_D_HELAMP_4360 subSimRec 0 99
           ;;

    0.4.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rootfile
           cd scripts/sigMC/D1_2420/4360/jobs_sig
           rm -rf sigMC_D1_2420_D_HELAMP_4360_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/dst sigMC D1_2420_D HELAMP D1_2420 4360 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rootfile/*root
           ./subAna.sh sigMC_D1_2420_D_HELAMP_4360
           ;;

    # --------------------------------------------------------------------------------
    #  0.5 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(HELAMP) @4420MeV
    # --------------------------------------------------------------------------------
    
    0.5) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) @4420MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4420MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPIPI HELAMP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 31327~31390, 36773~38140"
         ;;

    0.5.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/D1_2420/4420
           cd scripts/sigMC/D1_2420/4420
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4420/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4420/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4420/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_HELAMP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_HELAMP_4420.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_HELAMP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_HELAMP_4420.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_D1_2420_D_HELAMP_4420 jobOptions_rec_sig_D1_2420_D_HELAMP_4420 subSimRec 0 99
           ;;

    0.5.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rootfile
           cd scripts/sigMC/D1_2420/4420/jobs_sig
           rm -rf sigMC_D1_2420_D_HELAMP_4420_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/dst sigMC D1_2420_D HELAMP D1_2420 4420 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rootfile/*root
           ./subAna.sh sigMC_D1_2420_D_HELAMP_4420
           ;;

    # --------------------------------------------------------------------------------
    #  0.6 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(HELAMP) @4600MeV
    # --------------------------------------------------------------------------------
    
    0.6) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) @4600MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4600MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPIPI HELAMP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 35227~36213"
         ;;

    0.6.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/D1_2420/4600
           cd scripts/sigMC/D1_2420/4600
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4600/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4600/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/4600/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_HELAMP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_HELAMP_4600.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_HELAMP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_HELAMP_4600.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_D1_2420_D_HELAMP_4600 jobOptions_rec_sig_D1_2420_D_HELAMP_4600 subSimRec 0 99
           ;;

    0.6.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rootfile
           cd scripts/sigMC/D1_2420/4600/jobs_sig
           rm -rf sigMC_D1_2420_D_HELAMP_4600_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/dst sigMC D1_2420_D HELAMP D1_2420 4600 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rootfile/*root
           ./subAna.sh sigMC_D1_2420_D_HELAMP_4600
           ;;

    # -----------------------------------------------------------------------------
    #  0.7 signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4360MeV
    # -----------------------------------------------------------------------------

    0.7) echo "signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4360MeV..."
         echo "--> Process: psi(4415)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> E_{CMS}: 4360MeV"
         echo "--> Generation mode: psi(4415)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 30616~31279"
         ;;

    0.7.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/psipp/4360
           cd scripts/sigMC/psipp/4360
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4360/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4360/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4360/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_psipp_PI_PI_VSS_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/rtraw/*.rtraw
           ./jobOptions_sim_sig_psipp_PI_PI_VSS_4360.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_psipp_PI_PI_VSS_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/dst/*.dst
           ./jobOptions_rec_sig_psipp_PI_PI_VSS_4360.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_psipp_PI_PI_VSS_4360 jobOptions_rec_sig_psipp_PI_PI_VSS_4360 subSimRec 0 99
           ;;

    0.7.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/rootfile
           cd scripts/sigMC/psipp/4360/jobs_sig
           rm -rf sigMC_psipp_PI_PI_VSS_4360_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/dst sigMC psipp_PI_PI VSS psipp 4360 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/rootfile/*root
           ./subAna.sh sigMC_psipp_PI_PI_VSS_4360
           ;;

    # -----------------------------------------------------------------------------
    #  0.8 signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4420MeV
    # -----------------------------------------------------------------------------

    0.8) echo "signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4420MeV..."
         echo "--> Process: psi(4415)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> E_{CMS}: 4420MeV"
         echo "--> Generation mode: psi(4415)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 31327~31390, 36773~38140"
         ;;

    0.8.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/psipp/4420
           cd scripts/sigMC/psipp/4420
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4420/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4420/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4420/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_psipp_PI_PI_VSS_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/rtraw/*.rtraw
           ./jobOptions_sim_sig_psipp_PI_PI_VSS_4420.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_psipp_PI_PI_VSS_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/dst/*.dst
           ./jobOptions_rec_sig_psipp_PI_PI_VSS_4420.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_psipp_PI_PI_VSS_4420 jobOptions_rec_sig_psipp_PI_PI_VSS_4420 subSimRec 0 99
           ;;

    0.8.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/rootfile
           cd scripts/sigMC/psipp/4420/jobs_sig
           rm -rf sigMC_psipp_PI_PI_VSS_4420_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/dst sigMC psipp_PI_PI VSS psipp 4420 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/rootfile/*root
           ./subAna.sh sigMC_psipp_PI_PI_VSS_4420
           ;;

    # -----------------------------------------------------------------------------
    #  0.9 signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4600MeV
    # -----------------------------------------------------------------------------

    0.9) echo "signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4600MeV..."
         echo "--> Process: psi(4415)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> E_{CMS}: 4600MeV"
         echo "--> Generation mode: psi(4415)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 500,000"
         echo "--> RunNo: 35227~36213"
         ;;

    0.9.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/psipp/4600
           cd scripts/sigMC/psipp/4600
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4600/jobs_sig" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4600/jobs_sig
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/4600/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/dst
           rm -rf jobOptions*txt
           rm -rf subSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_psipp_PI_PI_VSS_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/rtraw/*.rtraw
           ./jobOptions_sim_sig_psipp_PI_PI_VSS_4600.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_psipp_PI_PI_VSS_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/dst/*.dst
           ./jobOptions_rec_sig_psipp_PI_PI_VSS_4600.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_psipp_PI_PI_VSS_4600 jobOptions_rec_sig_psipp_PI_PI_VSS_4600 subSimRec 0 99
           ;;

    0.9.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/rootfile
           cd scripts/sigMC/psipp/4600/jobs_sig
           rm -rf sigMC_psipp_PI_PI_VSS_4600_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/dst sigMC psipp_PI_PI VSS psipp 4600 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/rootfile/*root
           ./subAna.sh sigMC_psipp_PI_PI_VSS_4600
           ;;

    # ------------------------------------------
    #  0.10 run on inclusive MC (qqbar) @4360MeV
    # ------------------------------------------

    0.10) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: qqbar"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 9,400,000"
          echo "--> Cross Section: 17.5nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.10.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/qq/4360
            cd scripts/incMC/qq/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_qq_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/QED/qqbar incMC inclusive qq qq 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/qq/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_qq_4360
            ;;

    # ------------------------------------------
    #  0.11 run on inclusive MC (qqbar) @4420MeV
    # ------------------------------------------

    0.11) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: qqbar"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 14,000,000"
          echo "--> Cross Section: 7.0nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.11.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/qq/4420
            cd scripts/incMC/qq/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4420/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4420/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4420/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_qq_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4420/qqbar incMC inclusive qq qq 4420 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/qq/4420/rootfile/*root
            ./subAna.sh incMC_inclusive_qq_4420
            ;;

    # --------------------------------------------------
    #  0.12 run on inclusive MC (qqbar and ISR) @4600MeV
    # --------------------------------------------------

    0.12) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: qqbar and ISR"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 10,000,000"
          echo "--> Cross Section: 6.0nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.12.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/qq/4600
            cd scripts/incMC/qq/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4600/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4600/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/qq/4600/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_qq_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4600/qqbar incMC inclusive qq qq 4600 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/qq/4600/rootfile/*root
            ./subAna.sh incMC_inclusive_qq_4600
            ;;

    # --------------------------
    #  0.13 run on data @4360MeV
    # --------------------------

    0.13) echo "data @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Luminosity: 539.85pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.13.1) echo "Single D tag -- run on data sample..."
            mkdir -p scripts/data/4360
            cd scripts/data/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4360/jobs_data" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4360/jobs_data
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4360/jobs_data ./jobs_data
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/4360
            cd jobs_data
            rm -rf data*.txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_data.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_data.py /bes3fs/offline/data/664p01/xyz/4360/dst 30616 31279 4360
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/4360/*root
            ./subAna.sh data
            ;;

    # --------------------------
    #  0.14 run on data @4420MeV
    # --------------------------

    0.14) echo "data @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Luminosity: 44.67pb^{-1} + 1028.89pb^{-1}"
          echo "--> RunNo: 31327~31390, 36773~38140"
          ;;

    0.14.1) echo "Single D tag -- run on data sample..."
            mkdir -p scripts/data/4420
            cd scripts/data/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4420/jobs_data" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4420/jobs_data
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4420/jobs_data ./jobs_data
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/4420
            cd jobs_data
            rm -rf data*.txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_data.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_data.py /besfs3/offline/data/664p01/xyz/4360scan/4420/dst 31327 31390 4420
            ./make_data.py /besfs3/offline/data/besfs2/offline/data/664p01/xyz/4420/dst 36773 38140 4420
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/4420/*root
            ./subAna.sh data
            ;;

    # --------------------------
    #  0.15 run on data @4600MeV
    # --------------------------

    0.15) echo "data @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~36213"
          ;;

    0.15.1) echo "Single D tag -- run on data sample..."
            mkdir -p scripts/data/4600
            cd scripts/data/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4600/jobs_data" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4600/jobs_data
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/4600/jobs_data ./jobs_data
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/4600
            cd jobs_data
            rm -rf data*.txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_data.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_data.py /besfs3/offline/data/besfs2/offline/data/664p01/xyz/4600/dst 35227 36213 4600
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/4600/*root
            ./subAna.sh data
            ;;

    # -----------------------------------------------
    #  0.16 run on inclusive MC (open charm) @4360MeV
    # -----------------------------------------------

    0.16) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: open charm"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 17,200,000"
          echo "--> Cross Section: 10.6nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.16.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/DD/4360
            cd scripts/incMC/DD/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_DD_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/665p01-MC/4360/DDbar incMC inclusive DD DD 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/rootfile/*root
            # echo "/besfs/groups/psip/psipgroup/664p01-MC/4360/res/DD/raw/2.dst is a bad file, please remove it from jobOption!"
            ./subAna.sh incMC_inclusive_DD_4360
            ;;

    # -----------------------------------------------
    #  0.17 run on inclusive MC (open charm) @4420MeV
    # -----------------------------------------------

    0.17) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: open charm"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 40,300,000"
          echo "--> Cross Section: 10.2nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.17.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/DD/4420
            cd scripts/incMC/DD/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4420/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4420/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4420/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_DD_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4420/DD incMC inclusive DD DD 4420 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4420/rootfile/*root
            ./subAna.sh incMC_inclusive_DD_4420
            ;;

    # -----------------------------------------------
    #  0.18 run on inclusive MC (open charm) @4600MeV
    # -----------------------------------------------

    0.18) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: open charm"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 12,000,000"
          echo "--> Cross Section: 7.8nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.18.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/DD/4600
            cd scripts/incMC/DD/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4600/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4600/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/DD/4600/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_DD_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4600/DD incMC inclusive DD DD 4600 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4600/rootfile/*root
            ./subAna.sh incMC_inclusive_DD_4600
            ;;

    # -------------------------------------------
    #  0.19 run on inclusive MC (bhabha) @4360MeV
    # -------------------------------------------

    0.19) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: bhabha"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 10,000,000"
          echo "--> Cross Section: 389nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.19.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/bhabha/4360
            cd scripts/incMC/bhabha/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/bhabha/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_bhabha_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/QED/bhabha incMC inclusive bhabha bhabha 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/bhabha/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_bhabha_4360
            ;;

    # -----------------------------------------
    #  0.20 run on inclusive MC (dimu) @4360MeV
    # -----------------------------------------

    0.20) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: dimu"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 2,600,000"
          echo "--> Cross Section: 4.8nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.20.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/dimu/4360
            cd scripts/incMC/dimu/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/dimu/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_dimu_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/QED/dimu incMC inclusive dimu dimu 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/dimu/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_dimu_4360
            ;;

    # ------------------------------------------
    #  0.21 run on inclusive MC (ditau) @4360MeV
    # ------------------------------------------

    0.21) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: ditau"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 5,000,000"
          echo "--> Cross Section: 9.2nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.21.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/ditau/4360
            cd scripts/incMC/ditau/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/ditau/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_ditau_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/QED/ditau incMC inclusive ditau ditau 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/ditau/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_ditau_4360
            ;;

    # --------------------------------------------
    #  0.22 run on inclusive MC (digamma) @4360MeV
    # --------------------------------------------

    0.22) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: digamma"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 10,000,000"
          echo "--> Cross Section: 18.5nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.22.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/digamma/4360
            cd scripts/incMC/digamma/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/digamma/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_digamma_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/QED/digamma incMC inclusive digamma digamma 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/digamma/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_digamma_4360
            ;;

    # ---------------------------------------------
    #  0.23 run on inclusive MC (twogamma) @4360MeV
    # ---------------------------------------------

    0.23) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: twogamma"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 1,000,000"
          echo "--> Cross Section: 1.9nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.23.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/twogamma/4360
            cd scripts/incMC/twogamma/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/twogamma/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/twogamma/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/twogamma/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/twogamma/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_twogamma_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/QED/twogamma incMC inclusive twogamma twogamma 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/twogamma/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_twogamma_4360
            ;;

    # ----------------------------------------
    #  0.24 run on inclusive MC (ISR) @4360MeV
    # ----------------------------------------

    0.24) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: ISR"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 600,000"
          echo "--> Cross Section: 1.11nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.24.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/ISR/4360
            cd scripts/incMC/ISR/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ISR/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ISR/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ISR/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/ISR/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_ISR_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/QED/ISR incMC inclusive ISR ISR 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/ISR/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_ISR_4360
            ;;

    # ---------------------------------------------
    #  0.25 run on inclusive MC (gammaXYZ) @4360MeV
    # ---------------------------------------------

    0.25) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: gammaXYZ"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 33,000"
          echo "--> Cross Section: 41.6pb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.25.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/gammaXYZ/4360
            cd scripts/incMC/gammaXYZ/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/gammaXYZ/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/gammaXYZ/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/gammaXYZ/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/gammaXYZ/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_gammaXYZ_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/res/gammaXYZ incMC inclusive gammaXYZ gammaXYZ 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/gammaXYZ/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_gammaXYZ_4360
            ;;

    # --------------------------------------------
    #  0.26 run on inclusive MC (hadrons) @4360MeV
    # --------------------------------------------

    0.26) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: hadrons"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 190,000"
          echo "--> Cross Section: 249.9pb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.26.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/hadrons/4360
            cd scripts/incMC/hadrons/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/hadrons/4360/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/hadrons/4360/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/hadrons/4360/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/hadrons/4360/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_hadrons_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/res/hadrons incMC inclusive hadrons hadrons 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/hadrons/4360/rootfile/*root
            ./subAna.sh incMC_inclusive_hadrons_4360
            ;;

    # -------------------------------------------
    #  0.27 run on inclusive MC (bhabha) @4420MeV
    # -------------------------------------------

    0.27) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: bhabha"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 38,000,000"
          echo "--> Cross Section: 379.3nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.27.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/bhabha/4420
            cd scripts/incMC/bhabha/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4420/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4420/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4420/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/bhabha/4420/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_bhabha_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4420/bhabha incMC inclusive bhabha bhabha 4420 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/bhabha/4420/rootfile/*root
            ./subAna.sh incMC_inclusive_bhabha_4420
            ;;

    # -----------------------------------------
    #  0.28 run on inclusive MC (dimu) @4420MeV
    # -----------------------------------------

    0.28) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: dimu"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number:6,000,000"
          echo "--> Cross Section: 5.8286nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.28.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/dimu/4420
            cd scripts/incMC/dimu/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4420/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4420/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4420/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/dimu/4420/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_dimu_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4420/mumu incMC inclusive dimu dimu 4420 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/dimu/4420/rootfile/*root
            ./subAna.sh incMC_inclusive_dimu_4420
            ;;

    # ------------------------------------------
    #  0.29 run on inclusive MC (ditau) @4420MeV
    # ------------------------------------------

    0.29) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: ditau"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 7,000,000"
          echo "--> Cross Section: 3.4726nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.29.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/ditau/4420
            cd scripts/incMC/ditau/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4420/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4420/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4420/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/ditau/4420/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_ditau_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4420/tautau incMC inclusive ditau ditau 4420 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/ditau/4420/rootfile/*root
            ./subAna.sh incMC_inclusive_ditau_4420
            ;;

    # --------------------------------------------
    #  0.30 run on inclusive MC (digamma) @4420MeV
    # --------------------------------------------

    0.30) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: digamma"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 18,000,000"
          echo "--> Cross Section: 18.6nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.30.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/digamma/4420
            cd scripts/incMC/digamma/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4420/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4420/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4420/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/digamma/4420/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_digamma_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4420/digamma incMC inclusive digamma digamma 4420 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/digamma/4420/rootfile/*root
            ./subAna.sh incMC_inclusive_digamma_4420
            ;;

    # -------------------------------------------
    #  0.31 run on inclusive MC (bhabha) @4600MeV
    # -------------------------------------------

    0.31) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: bhabha"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 60,000,000"
          echo "--> Cross Section: 350nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.31.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/bhabha/4600
            cd scripts/incMC/bhabha/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4600/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4600/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/bhabha/4600/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/bhabha/4600/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_bhabha_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4600/QED/bhabha incMC inclusive bhabha bhabha 4600 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/bhabha/4600/rootfile/*root
            ./subAna.sh incMC_inclusive_bhabha_4600
            ;;

    # -----------------------------------------
    #  0.32 run on inclusive MC (dimu) @4600MeV
    # -----------------------------------------

    0.32) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: dimu"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 6,600,000"
          echo "--> Cross Section: 4.2nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.32.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/dimu/4600
            cd scripts/incMC/dimu/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4600/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4600/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/dimu/4600/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/dimu/4600/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_dimu_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4600/QED/dimu incMC inclusive dimu dimu 4600 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/dimu/4600/rootfile/*root
            ./subAna.sh incMC_inclusive_dimu_4600
            ;;

    # ------------------------------------------
    #  0.33 run on inclusive MC (ditau) @4600MeV
    # ------------------------------------------

    0.33) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: ditau"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 15,000,000"
          echo "--> Cross Section: 3.4nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.33.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/ditau/4600
            cd scripts/incMC/ditau/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4600/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4600/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/ditau/4600/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/ditau/4600/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_ditau_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4600/QED/ditau incMC inclusive ditau ditau 4600 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/ditau/4600/rootfile/*root
            ./subAna.sh incMC_inclusive_ditau_4600
            ;;

    # --------------------------------------------
    #  0.34 run on inclusive MC (digamma) @4600MeV
    # --------------------------------------------

    0.34) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: digamma"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 30,000,000"
          echo "--> Cross Section: 16.6nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.34.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/digamma/4600
            cd scripts/incMC/digamma/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4600/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4600/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/digamma/4600/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/digamma/4600/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_digamma_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4600/QED/digamma incMC inclusive digamma digamma 4600 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/digamma/4600/rootfile/*root
            ./subAna.sh incMC_inclusive_digamma_4600
            ;;

    # ---------------------------------------------
    #  0.35 run on inclusive MC (twogamma) @4600MeV
    # ---------------------------------------------

    0.35) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: twogamma"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 11,000,000"
          echo "--> Cross Section: 774.1nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.35.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/twogamma/4600
            cd scripts/incMC/twogamma/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/twogamma/4600/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/twogamma/4600/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/twogamma/4600/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/twogamma/4600/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_twogamma_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4600/QED/twogamma incMC inclusive twogamma twogamma 4600 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/twogamma/4600/rootfile/*root
            ./subAna.sh incMC_inclusive_twogamma_4600
            ;;

    # ---------------------------------------
    #  0.36 run on inclusive MC (LL) @4600MeV
    # ---------------------------------------

    0.36) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: LL"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 500,000"
          echo "--> Cross Section: 0.35nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.36.1) echo "Single D tag -- run on inclusive MC sample..."
            mkdir -p scripts/incMC/LL/4600
            cd scripts/incMC/LL/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/LL/4600/jobs_inc" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/LL/4600/jobs_inc
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/LL/4600/jobs_inc ./jobs_inc
            fi
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/LL/4600/rootfile
            cd jobs_inc
            rm -rf incMC_inclusive_LL_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4600/LL incMC inclusive LL LL 4600 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/LL/4600/rootfile/*root
            ./subAna.sh incMC_inclusive_LL_4600
            ;;

    # -------------------------------------------------------------------------------
    #  0.37 signal MC of psi(4415)->D_2(2460)D(PHSP), D_2(2460)->DPIPI(PHSP) @4360MeV
    # -------------------------------------------------------------------------------
    
    0.37) echo "signal MC of psi(4415)->D2_(2460)D(PHSP), D2_(2460)->DPIPI(PHSP) @4360MeV..."
          echo "--> Process: psi(4415)->D2_(2460)D, D2_(2460)->DPIPI"
          echo "--> E_{CMS}: 4360MeV"
          echo "--> Generation mode: psi(4415)->D2_(2460)D PHSH; D2_(2460)->DPIPI PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 30616~31279"
          ;;

    0.37.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/D2_2460/4360
            cd scripts/sigMC/D2_2460/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4360/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4360/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4360/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4360/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4360/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D2_2460_D_PHSP_4360.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4360/rtraw/*.rtraw
            ./jobOptions_sim_sig_D2_2460_D_PHSP_4360.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D2_2460_D_PHSP_4360.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4360/dst/*.dst
            ./jobOptions_rec_sig_D2_2460_D_PHSP_4360.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D2_2460_D_PHSP_4360 jobOptions_rec_sig_D2_2460_D_PHSP_4360 subSimRec 0 99
            ;;

    0.37.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4360/rootfile
            cd scripts/sigMC/D2_2460/4360/jobs_sig
            rm -rf sigMC_D2_2460_D_PHSP_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4360/dst sigMC D2_2460_D PHSP D2_2460 4360 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4360/rootfile/*root
            ./subAna.sh sigMC_D2_2460_D_PHSP_4360
            ;;

    # -------------------------------------------------------------------------------
    #  0.38 signal MC of psi(4415)->D_2(2460)D(PHSP), D_2(2460)->DPIPI(PHSP) @4420MeV
    # -------------------------------------------------------------------------------
    
    0.38) echo "signal MC of psi(4415)->D2_(2460)D(PHSP), D2_(2460)->DPIPI(PHSP) @4420MeV..."
          echo "--> Process: psi(4415)->D2_(2460)D, D2_(2460)->DPIPI"
          echo "--> E_{CMS}: 4420MeV"
          echo "--> Generation mode: psi(4415)->D2_(2460)D PHSH; D2_(2460)->DPIPI PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 31327~31390, 36773~38140"
          ;;

    0.38.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/D2_2460/4420
            cd scripts/sigMC/D2_2460/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4420/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4420/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4420/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4420/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4420/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D2_2460_D_PHSP_4420.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4420/rtraw/*.rtraw
            ./jobOptions_sim_sig_D2_2460_D_PHSP_4420.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D2_2460_D_PHSP_4420.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4420/dst/*.dst
            ./jobOptions_rec_sig_D2_2460_D_PHSP_4420.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D2_2460_D_PHSP_4420 jobOptions_rec_sig_D2_2460_D_PHSP_4420 subSimRec 0 99
            ;;

    0.38.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4420/rootfile
            cd scripts/sigMC/D2_2460/4420/jobs_sig
            rm -rf sigMC_D2_2460_D_PHSP_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4420/dst sigMC D2_2460_D PHSP D2_2460 4420 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4420/rootfile/*root
            ./subAna.sh sigMC_D2_2460_D_PHSP_4420
            ;;

    # -------------------------------------------------------------------------------
    #  0.39 signal MC of psi(4415)->D_2(2460)D(PHSP), D_2(2460)->DPIPI(PHSP) @4600MeV
    # -------------------------------------------------------------------------------
    
    0.39) echo "signal MC of psi(4415)->D2_(2460)D(PHSP), D2_(2460)->DPIPI(PHSP) @4600MeV..."
          echo "--> Process: psi(4415)->D2_(2460)D, D2_(2460)->DPIPI"
          echo "--> E_{CMS}: 4600MeV"
          echo "--> Generation mode: psi(4415)->D2_(2460)D PHSH; D2_(2460)->DPIPI PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 35227~36213"
          ;;

    0.39.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/D2_2460/4600
            cd scripts/sigMC/D2_2460/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4600/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4600/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D2_2460/4600/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4600/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4600/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D2_2460_D_PHSP_4600.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4600/rtraw/*.rtraw
            ./jobOptions_sim_sig_D2_2460_D_PHSP_4600.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D2_2460_D_PHSP_4600.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4600/dst/*.dst
            ./jobOptions_rec_sig_D2_2460_D_PHSP_4600.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D2_2460_D_PHSP_4600 jobOptions_rec_sig_D2_2460_D_PHSP_4600 subSimRec 0 99
            ;;

    0.39.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4600/rootfile
            cd scripts/sigMC/D2_2460/4600/jobs_sig
            rm -rf sigMC_D2_2460_D_PHSP_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4600/dst sigMC D2_2460_D PHSP D2_2460 4600 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D2_2460/4600/rootfile/*root
            ./subAna.sh sigMC_D2_2460_D_PHSP_4600
            ;;

    # ---------------------------------------------------
    #  0.40 signal MC of psi(4415)->DDPIPI(PHSP) @4360MeV
    # ---------------------------------------------------
    
    0.40) echo "signal MC of psi(4415)->DDPIPI(PHSP) @4360MeV..."
          echo "--> Process: psi(4415)->DDPIPI"
          echo "--> E_{CMS}: 4360MeV"
          echo "--> Generation mode: psi(4415)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 30616~31279"
          ;;

    0.40.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/DDPIPI/4360
            cd scripts/sigMC/DDPIPI/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4360/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4360/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4360/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4360/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4360/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D_D_PI_PI_PHSP_4360.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4360/rtraw/*.rtraw
            ./jobOptions_sim_sig_D_D_PI_PI_PHSP_4360.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D_D_PI_PI_PHSP_4360.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4360/dst/*.dst
            ./jobOptions_rec_sig_D_D_PI_PI_PHSP_4360.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D_D_PI_PI_PHSP_4360 jobOptions_rec_sig_D_D_PI_PI_PHSP_4360 subSimRec 0 99
            ;;

    0.40.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4360/rootfile
            cd scripts/sigMC/DDPIPI/4360/jobs_sig
            rm -rf sigMC_D_D_PI_PI_PHSP_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4360/dst sigMC D_D_PI_PI PHSP DDPIPI 4360 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4360/rootfile/*root
            ./subAna.sh sigMC_D_D_PI_PI_PHSP_4360
            ;;

    # ---------------------------------------------------
    #  0.41 signal MC of psi(4415)->DDPIPI(PHSP) @4420MeV
    # ---------------------------------------------------
    
    0.41) echo "signal MC of psi(4415)->DDPIPI(PHSP) @4420MeV..."
          echo "--> Process: psi(4415)->DDPIPI"
          echo "--> E_{CMS}: 4420MeV"
          echo "--> Generation mode: psi(4415)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 31327~31390, 36773~38140"
          ;;

    0.41.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/DDPIPI/4420
            cd scripts/sigMC/DDPIPI/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4420/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4420/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4420/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4420/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4420/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D_D_PI_PI_PHSP_4420.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4420/rtraw/*.rtraw
            ./jobOptions_sim_sig_D_D_PI_PI_PHSP_4420.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D_D_PI_PI_PHSP_4420.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4420/dst/*.dst
            ./jobOptions_rec_sig_D_D_PI_PI_PHSP_4420.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D_D_PI_PI_PHSP_4420 jobOptions_rec_sig_D_D_PI_PI_PHSP_4420 subSimRec 0 99
            ;;

    0.41.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4420/rootfile
            cd scripts/sigMC/DDPIPI/4420/jobs_sig
            rm -rf sigMC_D_D_PI_PI_PHSP_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4420/dst sigMC D_D_PI_PI PHSP DDPIPI 4420 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4420/rootfile/*root
            ./subAna.sh sigMC_D_D_PI_PI_PHSP_4420
            ;;

    # ---------------------------------------------------
    #  0.42 signal MC of psi(4415)->DDPIPI(PHSP) @4600MeV
    # ---------------------------------------------------
    
    0.42) echo "signal MC of psi(4415)->DDPIPI(PHSP) @4600MeV..."
          echo "--> Process: psi(4415)->DDPIPI"
          echo "--> E_{CMS}: 4600MeV"
          echo "--> Generation mode: psi(4415)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 35227~36213"
          ;;

    0.42.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/DDPIPI/4600
            cd scripts/sigMC/DDPIPI/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4600/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4600/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/4600/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D_D_PI_PI_PHSP_4600.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/rtraw/*.rtraw
            ./jobOptions_sim_sig_D_D_PI_PI_PHSP_4600.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D_D_PI_PI_PHSP_4600.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/dst/*.dst
            ./jobOptions_rec_sig_D_D_PI_PI_PHSP_4600.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D_D_PI_PI_PHSP_4600 jobOptions_rec_sig_D_D_PI_PI_PHSP_4600 subSimRec 0 99
            ;;

    0.42.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/rootfile
            cd scripts/sigMC/DDPIPI/4600/jobs_sig
            rm -rf sigMC_D_D_PI_PI_PHSP_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/dst sigMC D_D_PI_PI PHSP DDPIPI 4600 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/4600/rootfile/*root
            ./subAna.sh sigMC_D_D_PI_PI_PHSP_4600
            ;;

    # -------------------------------------------------------------------------------
    #  0.43 signal MC of psi(4415)->D_0(2300)DPI(PHSP), D_0(2300)->DPI(PHSP) @4360MeV
    # -------------------------------------------------------------------------------
    
    0.43) echo "signal MC of psi(4415)->D0_(2300)DPI(PHSP), D0_(2300)->DPI(PHSP) @4360MeV..."
          echo "--> Process: psi(4415)->D0_(2300)DPI, D0_(2300)->DPI"
          echo "--> E_{CMS}: 4360MeV"
          echo "--> Generation mode: psi(4415)->D0_(2300)DPI PHSH; D0_(2300)->DPI PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 30616~31279"
          ;;

    0.43.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/D0_2300/4360
            cd scripts/sigMC/D0_2300/4360
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4360/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4360/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4360/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4360/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4360/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D0_2300_D_PI_PHSP_4360.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4360/rtraw/*.rtraw
            ./jobOptions_sim_sig_D0_2300_D_PI_PHSP_4360.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D0_2300_D_PI_PHSP_4360.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4360/dst/*.dst
            ./jobOptions_rec_sig_D0_2300_D_PI_PHSP_4360.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D0_2300_D_PI_PHSP_4360 jobOptions_rec_sig_D0_2300_D_PI_PHSP_4360 subSimRec 0 99
            ;;

    0.43.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4360/rootfile
            cd scripts/sigMC/D0_2300/4360/jobs_sig
            rm -rf sigMC_D0_2300_D_PI_PHSP_4360_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4360/dst sigMC D0_2300_D_PI PHSP D0_2300 4360 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4360/rootfile/*root
            ./subAna.sh sigMC_D0_2300_D_PI_PHSP_4360
            ;;

    # -------------------------------------------------------------------------------
    #  0.44 signal MC of psi(4415)->D_0(2300)DPI(PHSP), D_0(2300)->DPI(PHSP) @4420MeV
    # -------------------------------------------------------------------------------
    
    0.44) echo "signal MC of psi(4415)->D0_(2300)DPI(PHSP), D0_(2300)->DPI(PHSP) @4420MeV..."
          echo "--> Process: psi(4415)->D0_(2300)DPI, D0_(2300)->DPI"
          echo "--> E_{CMS}: 4420MeV"
          echo "--> Generation mode: psi(4415)->D0_(2300)DPI PHSH; D0_(2300)->DPI PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 31327~31390, 36773~38140"
          ;;

    0.44.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/D0_2300/4420
            cd scripts/sigMC/D0_2300/4420
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4420/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4420/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4420/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4420/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4420/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D0_2300_D_PI_PHSP_4420.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4420/rtraw/*.rtraw
            ./jobOptions_sim_sig_D0_2300_D_PI_PHSP_4420.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D0_2300_D_PI_PHSP_4420.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4420/dst/*.dst
            ./jobOptions_rec_sig_D0_2300_D_PI_PHSP_4420.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D0_2300_D_PI_PHSP_4420 jobOptions_rec_sig_D0_2300_D_PI_PHSP_4420 subSimRec 0 99
            ;;

    0.44.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4420/rootfile
            cd scripts/sigMC/D0_2300/4420/jobs_sig
            rm -rf sigMC_D0_2300_D_PI_PHSP_4420_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4420/dst sigMC D0_2300_D_PI PHSP D0_2300 4420 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4420/rootfile/*root
            ./subAna.sh sigMC_D0_2300_D_PI_PHSP_4420
            ;;

    # -------------------------------------------------------------------------------
    #  0.45 signal MC of psi(4415)->D_0(2300)DPI(PHSP), D_0(2300)->DPI(PHSP) @4600MeV
    # -------------------------------------------------------------------------------
    
    0.45) echo "signal MC of psi(4415)->D0_(2300)DPI(PHSP), D0_(2300)->DPI(PHSP) @4600MeV..."
          echo "--> Process: psi(4415)->D0_(2300)DPI, D0_(2300)->DPI"
          echo "--> E_{CMS}: 4600MeV"
          echo "--> Generation mode: psi(4415)->D0_(2300)DPI PHSH; D0_(2300)->DPI PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          echo "--> Event Number: 500,000"
          echo "--> RunNo: 35227~36213"
          ;;

    0.45.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            mkdir -p scripts/sigMC/D0_2300/4600
            cd scripts/sigMC/D0_2300/4600
            if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4600/jobs_sig" ]; then
                mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4600/jobs_sig
                ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D0_2300/4600/jobs_sig ./jobs_sig
            fi
            cd jobs_sig
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4600/rtraw
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4600/dst
            rm -rf jobOptions*txt
            rm -rf subSimRec_*.sh
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D0_2300_D_PI_PHSP_4600.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4600/rtraw/*.rtraw
            ./jobOptions_sim_sig_D0_2300_D_PI_PHSP_4600.sh 0 99 5000
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D0_2300_D_PI_PHSP_4600.sh ./
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4600/dst/*.dst
            ./jobOptions_rec_sig_D0_2300_D_PI_PHSP_4600.sh 0 99
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
            ./subSimRec.sh jobOptions_sim_sig_D0_2300_D_PI_PHSP_4600 jobOptions_rec_sig_D0_2300_D_PI_PHSP_4600 subSimRec 0 99
            ;;

    0.45.2) echo "Single D tag -- run on signal MC sample..."
            mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4600/rootfile
            cd scripts/sigMC/D0_2300/4600/jobs_sig
            rm -rf sigMC_D0_2300_D_PI_PHSP_4600_*txt
            cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
            cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
            ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4600/dst sigMC D0_2300_D_PI PHSP D0_2300 4600 10
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D0_2300/4600/rootfile/*root
            ./subAna.sh sigMC_D0_2300_D_PI_PHSP_4600
            ;;

    # ---------------------------------------
    #  0.46 run on data reconstructed @703p01
    # ---------------------------------------

    0.46) echo "data reconstructed @703p01..."
          echo "--> Patch: 703p01"
          echo "--> LXSLC: lxslc6"
          ;;

    0.46.1) echo "Single D tag -- run on data sample..."
            cd scripts/gen_script/gen_data
            ./subData_703p01.sh
            ;;

    # ----------------------------------------------------------------------------------------
    #  0.47 signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) reconstructed @703p01
    # ----------------------------------------------------------------------------------------
    
    0.47) echo "signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) reconstructed @703p01..."
          echo "--> Process: psi(4415)->X(3842)PIPI, X(3842)->DD"
          echo "--> Generation mode: psi(4415)->X(3842)PIPI PHSH; X(3842)->DD PHSP; D decay D_DALITZ(assignated mode) or inlusive decay"
          ;;

    0.47.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            cd scripts/gen_script/gen_mc
            ./subSimRec_X_3842_703p01.sh
            ;;

    0.47.2) echo "Single D tag -- run on signal MC sample..."
            ;;

    # ----------------------------------------------------------------------------------------------
    #  0.48 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(HELAMP) reconstructed @703p01
    # ----------------------------------------------------------------------------------------------
    
    0.48) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) reconstructed @703p01..."
          echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
          echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPIPI HELAMP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          ;;

    0.48.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            cd scripts/gen_script/gen_mc
            ./subSimRec_D1_2420_703p01.sh
            ;;

    0.48.2) echo "Single D tag -- run on signal MC sample..."
            ;;

    # -------------------------------------------------------------------------------------------
    #  0.49 signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01
    # -------------------------------------------------------------------------------------------

    0.49) echo "signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01..."
          echo "--> Process: psi(4415)->psi(3770)PIPI, psi(3770)->DD"
          echo "--> Generation mode: psi(4415)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          ;;

    0.49.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            cd scripts/gen_script/gen_mc
            ./subSimRec_psipp_703p01.sh
            ;;

    0.49.2) echo "Single D tag -- run on signal MC sample..."
            ;;

    # ----------------------------------------------------------------
    #  0.50 signal MC of psi(4415)->DDPIPI(PHSP) reconstructed @703p01
    # ----------------------------------------------------------------
    
    0.50) echo "signal MC of psi(4415)->DDPIPI(PHSP) reconstructed @703p01..."
          echo "--> Process: psi(4415)->DDPIPI"
          echo "--> Generation mode: psi(4415)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
          ;;

    0.50.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
            cd scripts/gen_script/gen_mc
            ./subSimRec_D_D_PI_PI_703p01.sh
            ;;

    0.50.2) echo "Single D tag -- run on signal MC sample..."
            ;;

esac
