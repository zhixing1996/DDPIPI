#!/usr/bin/env bash

# Main driver to submit simulation and reconstruction jobs as well as generating root files 
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-09-02 Mon 22:17]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit simulation and reconstruction jobs as well as generating root files\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./submit.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[run on signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[run on signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.3"   "[run on signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.3.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.3.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.4"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.4.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.4.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.5"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.5.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.5.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.6"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4600MeV]" # psi(4415) -> @4600MeV
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

    printf "\n\t%-9s  %-40s\n" "0.10"   "[run on inclusive MC @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.10.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.11"   "[run on inclusive MC @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.11.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.12"   "[run on inclusive MC @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.12.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.13"   "[run on data @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.13.1" "Single D tag -- data sample"

    printf "\n\t%-9s  %-40s\n" "0.14"   "[run on data @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.14.1" "Single D tag -- data sample"

    printf "\n\t%-9s  %-40s\n" "0.15"   "[run on data @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.15.1" "Single D tag -- data sample"

    printf "\n\t%-9s  %-40s\n" "0.16"   "[run on inclusive MC (DDbar) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.16.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.17"   "[run on inclusive MC (DDbar) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.17.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.18"   "[run on inclusive MC (DDbar) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.18.1" "Single D tag -- inclusive MC sample"

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

    # -------------------------------------------------------------------------
    #  0.1 signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4360MeV
    # -------------------------------------------------------------------------
    
    0.1) echo "signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4360MeV..."
         echo "--> Process: psi(4415)->X(3842)PIPI, X(3842)->DD"
         echo "--> E_{CMS}: 4360MeV"
         echo "--> Generation mode: psi(4415)->X(3842)PIPI PHSH; X(3842)->DD VSS; D decay D_DALITZ(assignated mode) or inlusive decay"
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

    # -------------------------------------------------------------------------
    #  0.2 signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4420MeV
    # -------------------------------------------------------------------------
    
    0.2) echo "signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4420MeV..."
         echo "--> Process: psi(4415)->X(3842)PIPI, X(3842)->DD"
         echo "--> E_{CMS}: 4420MeV"
         echo "--> Generation mode: psi(4415)->X(3842)PIPI PHSH; X(3842)->DD VSS; D decay D_DALITZ(assignated mode) or inlusive decay"
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

    # -------------------------------------------------------------------------
    #  0.3 signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4600MeV
    # -------------------------------------------------------------------------
    
    0.3) echo "signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(VSS) @4600MeV..."
         echo "--> Process: psi(4415)->X(3842)PIPI, X(3842)->DD"
         echo "--> E_{CMS}: 4600MeV"
         echo "--> Generation mode: psi(4415)->X(3842)PIPI PHSH; X(3842)->DD VSS; D decay D_DALITZ(assignated mode) or inlusive decay"
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

    # ------------------------------------------------------------------------------
    #  0.4 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(PHSP) @4360MeV
    # ------------------------------------------------------------------------------
    
    0.4) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4360MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4360MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPiPi PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
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
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_PHSP_4360.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_PHSP_4360.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_D1_2420_D_PHSP_4360 jobOptions_rec_sig_D1_2420_D_PHSP_4360 subSimRec 0 99
           ;;

    0.4.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rootfile
           cd scripts/sigMC/D1_2420/4360/jobs_sig
           rm -rf sigMC_D1_2420_D_PHSP_4360_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/dst sigMC D1_2420_D PHSP D1_2420 4360 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4360/rootfile/*root
           ./subAna.sh sigMC_D1_2420_D_PHSP_4360
           ;;

    # ------------------------------------------------------------------------------
    #  0.5 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(PHSP) @4420MeV
    # ------------------------------------------------------------------------------
    
    0.5) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4420MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4420MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPiPi PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
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
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_PHSP_4420.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_PHSP_4420.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_D1_2420_D_PHSP_4420 jobOptions_rec_sig_D1_2420_D_PHSP_4420 subSimRec 0 99
           ;;

    0.5.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rootfile
           cd scripts/sigMC/D1_2420/4420/jobs_sig
           rm -rf sigMC_D1_2420_D_PHSP_4420_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/dst sigMC D1_2420_D PHSP D1_2420 4420 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4420/rootfile/*root
           ./subAna.sh sigMC_D1_2420_D_PHSP_4420
           ;;

    # ------------------------------------------------------------------------------
    #  0.6 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(PHSP) @4600MeV
    # ------------------------------------------------------------------------------
    
    0.6) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4600MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4600MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPiPi PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
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
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_PHSP_4600.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_PHSP_4600.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_D1_2420_D_PHSP_4600 jobOptions_rec_sig_D1_2420_D_PHSP_4600 subSimRec 0 99
           ;;

    0.6.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rootfile
           cd scripts/sigMC/D1_2420/4600/jobs_sig
           rm -rf sigMC_D1_2420_D_PHSP_4600_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/dst sigMC D1_2420_D PHSP D1_2420 4600 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/4600/rootfile/*root
           ./subAna.sh sigMC_D1_2420_D_PHSP_4600
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
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_psipp_PI_PI_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/rtraw/*.rtraw
           ./jobOptions_sim_sig_psipp_PI_PI_PHSP_4360.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_psipp_PI_PI_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/dst/*.dst
           ./jobOptions_rec_sig_psipp_PI_PI_PHSP_4360.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_psipp_PI_PI_PHSP_4360 jobOptions_rec_sig_psipp_PI_PI_PHSP_4360 subSimRec 0 99
           ;;

    0.7.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/rootfile
           cd scripts/sigMC/psipp/4360/jobs_sig
           rm -rf sigMC_psipp_PI_PI_PHSP_4360_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/dst sigMC psipp_PI_PI PHSP psipp 4360 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4360/rootfile/*root
           ./subAna.sh sigMC_psipp_PI_PI_PHSP_4360
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
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_psipp_PI_PI_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/rtraw/*.rtraw
           ./jobOptions_sim_sig_psipp_PI_PI_PHSP_4420.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_psipp_PI_PI_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/dst/*.dst
           ./jobOptions_rec_sig_psipp_PI_PI_PHSP_4420.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_psipp_PI_PI_PHSP_4420 jobOptions_rec_sig_psipp_PI_PI_PHSP_4420 subSimRec 0 99
           ;;

    0.8.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/rootfile
           cd scripts/sigMC/psipp/4420/jobs_sig
           rm -rf sigMC_psipp_PI_PI_PHSP_4420_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/dst sigMC psipp_PI_PI PHSP psipp 4420 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/rootfile/*root
           ./subAna.sh sigMC_psipp_PI_PI_PHSP_4420
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
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_sim_sig_psipp_PI_PI_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/rtraw/*.rtraw
           ./jobOptions_sim_sig_psipp_PI_PI_PHSP_4600.sh 0 99 5000
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/jobOptions_rec_sig_psipp_PI_PI_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/dst/*.dst
           ./jobOptions_rec_sig_psipp_PI_PI_PHSP_4600.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
           ./subSimRec.sh jobOptions_sim_sig_psipp_PI_PI_PHSP_4600 jobOptions_rec_sig_psipp_PI_PI_PHSP_4600 subSimRec 0 99
           ;;

    0.9.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/rootfile
           cd scripts/sigMC/psipp/4600/jobs_sig
           rm -rf sigMC_psipp_PI_PI_PHSP_4600_*txt
           cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
           cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
           ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/dst sigMC psipp_PI_PI PHSP psipp 4600 10
           cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
           rm -rf *boss*
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4600/rootfile/*root
           ./subAna.sh sigMC_psipp_PI_PI_PHSP_4600
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
          echo "--> Event Number: 2,800,000"
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

    # ------------------------------------------
    #  0.16 run on inclusive MC (DDbar) @4360MeV
    # ------------------------------------------

    0.16) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: DDbar"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 500,000"
          echo "--> Cross Section: 1.0nb"
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
            ./make_mc.py /besfs/groups/psip/psipgroup/664p01-MC/4360/res/DD incMC inclusive DD DD 4360 30
            cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
            rm -rf *boss*
            rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/DD/4360/rootfile/*root
            echo "/besfs/groups/psip/psipgroup/664p01-MC/4360/res/DD/raw/2.dst is a bad file, please remove it from jobOption!"
            # ./subAna.sh incMC_inclusive_DD_4360
            ;;

    # ------------------------------------------
    #  0.17 run on inclusive MC (DDbar) @4420MeV
    # ------------------------------------------

    0.17) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: DDbar"
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

    # ------------------------------------------
    #  0.18 run on inclusive MC (DDbar) @4600MeV
    # ------------------------------------------

    0.18) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: DDbar"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 3,100,000"
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

esac
