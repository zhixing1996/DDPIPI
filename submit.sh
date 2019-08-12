#!/usr/bin/env bash

# Main driver to submit jobs
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-08-10 Sat 08:33]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit jobs\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./submit.sh [OPTION]"
    printf "\nOPTIONS\n"
    printf "\n\t%-9s  %-40s\n" "0.1"   "[run on signal MC of psi(4415)->D1_(2420)D, D1_(2420)->DPIPI @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Single D tag -- run on signal MC sample"
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

    # --------------------------------------------------------------------------
    #  0.1 signal MC of psi(4415)->D_1(2420)D, D_1(2420)->DPIPI @4360MeV
    # --------------------------------------------------------------------------

case $option in
    0.1) echo "signal MC of psi(4415)->D1_(2420)D, D1_(2420)->DPIPI @4360MeV..."
         ;;

    0.1.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/D1_2420/4360
           cd scripts/sigMC/D1_2420/4360
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4360/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4360/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4360/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4360/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4360/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4360/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_PHSP_4360.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4360/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_PHSP_4360.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_sig_D1_2420_D_PHSP_4360 jobOptions_rec_sig_D1_2420_D_PHSP_4360 subjectSimRec_PHSP 0 99
           ;;

    0.1.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/sigMC/D1_2420/4360
           cd scripts/sigMC/D1_2420/4360/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Sig_D1_2420_D_PHSP_4360 20 20 . sigMC D1_2420 PHSP 4360
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           ./subjectAna.sh Sig_D1_2420_D_PHSP_4360 0 99
           ;;

esac
