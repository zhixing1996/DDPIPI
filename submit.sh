#!/usr/bin/env bash

# Main driver to submit jobs
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-08-10 Sat 08:33]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit jobs\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./submit.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.3"   "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.3.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.3.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.4"   "[run on signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.4.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.4.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.5"   "[run on signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.5.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.5.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.6"   "[run on signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.6.1" "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.6.2" "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.7"   "[run on background MC of psi(4415)->DDPIPI(PHSP) @4360MeV]" # psi(4415) -> @4360MeV
    printf "\n\t%-9s  %-40s\n" "0.7.1" "Simulation & Reconstruction -- generate background MC sample"
    printf "\n\t%-9s  %-40s\n" "0.7.2" "Single D tag -- run on background MC sample"

    printf "\n\t%-9s  %-40s\n" "0.8"   "[run on background MC of psi(4415)->DDPIPI(PHSP) @4420MeV]" # psi(4415) -> @4420MeV
    printf "\n\t%-9s  %-40s\n" "0.8.1" "Simulation & Reconstruction -- generate background MC sample"
    printf "\n\t%-9s  %-40s\n" "0.8.2" "Single D tag -- run on background MC sample"

    printf "\n\t%-9s  %-40s\n" "0.9"   "[run on background MC of psi(4415)->DDPIPI(PHSP) @4600MeV]" # psi(4415) -> @4600MeV
    printf "\n\t%-9s  %-40s\n" "0.9.1" "Simulation & Reconstruction -- generate background MC sample"
    printf "\n\t%-9s  %-40s\n" "0.9.2" "Single D tag -- run on background MC sample"

    printf "\n\t%-9s  %-40s\n" "0.10"   "[run on data @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.10.1" "Single D tag -- data sample"

    printf "\n\t%-9s  %-40s\n" "0.11"   "[run on data @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.11.1" "Single D tag -- data sample"

    printf "\n\t%-9s  %-40s\n" "0.12"   "[run on data @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.12.1" "Single D tag -- data sample"

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

    # ------------------------------------------------------------------------------
    #  0.1 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(PHSP) @4360MeV
    # ------------------------------------------------------------------------------

    0.1) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4360MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4360MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPiPi PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 30616~31279"
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
           rm -rf *boss* 
           ./subjectAna.sh Sig_D1_2420_D_PHSP_4360
           ;;

    # ------------------------------------------------------------------------------
    #  0.2 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(PHSP) @4420MeV
    # ------------------------------------------------------------------------------

    0.2) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4420MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4420MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPiPi PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 31327~31390, 36773~38140"
         ;;

    0.2.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/D1_2420/4420
           cd scripts/sigMC/D1_2420/4420
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4420/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4420/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4420/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4420/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4420/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4420/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_PHSP_4420.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4420/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_PHSP_4420.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_sig_D1_2420_D_PHSP_4420 jobOptions_rec_sig_D1_2420_D_PHSP_4420 subjectSimRec_PHSP 0 99
           ;;

    0.2.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/sigMC/D1_2420/4420
           cd scripts/sigMC/D1_2420/4420/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Sig_D1_2420_D_PHSP_4420 20 20 . sigMC D1_2420 PHSP 4420
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh Sig_D1_2420_D_PHSP_4420
           ;;

    # ------------------------------------------------------------------------------
    #  0.3 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(PHSP) @4600MeV
    # ------------------------------------------------------------------------------

    0.3) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(PHSP) @4600MeV..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> E_{CMS}: 4600MeV"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPiPi PHSP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 35227~36213"
         ;;

    0.3.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/D1_2420/4600
           cd scripts/sigMC/D1_2420/4600
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4600/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4600/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/D1_2420/4600/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4600/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4600/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_sig_D1_2420_D_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4600/rtraw/*.rtraw
           ./jobOptions_sim_sig_D1_2420_D_PHSP_4600.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_sig_D1_2420_D_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4600/dst/*.dst
           ./jobOptions_rec_sig_D1_2420_D_PHSP_4600.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_sig_D1_2420_D_PHSP_4600 jobOptions_rec_sig_D1_2420_D_PHSP_4600 subjectSimRec_PHSP 0 99
           ;;

    0.3.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/sigMC/D1_2420/4600
           cd scripts/sigMC/D1_2420/4600/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Sig_D1_2420_D_PHSP_4600 20 20 . sigMC D1_2420 PHSP 4600
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh Sig_D1_2420_D_PHSP_4600
           ;;

    # -----------------------------------------------------------------------------
    #  0.4 signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4360MeV
    # -----------------------------------------------------------------------------

    0.4) echo "signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4360MeV..."
         echo "--> Process: psi(4415)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> E_{CMS}: 4360MeV"
         echo "--> Generation mode: psi(4415)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 30616~31279"
         ;;

    0.4.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/psi_3770/4360
           cd scripts/sigMC/psi_3770/4360
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4360/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4360/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4360/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4360/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4360/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4360/rtraw/*.rtraw
           ./jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4360.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4360/dst/*.dst
           ./jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4360.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4360 jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4360 subjectSimRec_PHSP 0 99
           ;;

    0.4.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/sigMC/psi_3770/4360
           cd scripts/sigMC/psi_3770/4360/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Sig_psi_3770_PI_PI_PHSP_4360 20 20 . sigMC psi_3770 PHSP 4360
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh Sig_psi_3770_PI_PI_PHSP_4360
           ;;

    # -----------------------------------------------------------------------------
    #  0.5 signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4420MeV
    # -----------------------------------------------------------------------------

    0.5) echo "signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4420MeV..."
         echo "--> Process: psi(4415)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> E_{CMS}: 4420MeV"
         echo "--> Generation mode: psi(4415)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 31327~31390, 36773~38140"
         ;;

    0.5.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/psi_3770/4420
           cd scripts/sigMC/psi_3770/4420
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4420/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4420/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4420/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4420/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4420/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4420/rtraw/*.rtraw
           ./jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4420.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4420/dst/*.dst
           ./jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4420.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4420 jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4420 subjectSimRec_PHSP 0 99
           ;;

    0.5.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/sigMC/psi_3770/4420
           cd scripts/sigMC/psi_3770/4420/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Sig_psi_3770_PI_PI_PHSP_4420 20 20 . sigMC psi_3770 PHSP 4420
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh Sig_psi_3770_PI_PI_PHSP_4420
           ;;

    # -----------------------------------------------------------------------------
    #  0.6 signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4600MeV
    # -----------------------------------------------------------------------------

    0.6) echo "signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) @4600MeV..."
         echo "--> Process: psi(4415)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> E_{CMS}: 4600MeV"
         echo "--> Generation mode: psi(4415)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 35227~36213"
         ;;

    0.6.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           mkdir -p scripts/sigMC/psi_3770/4600
           cd scripts/sigMC/psi_3770/4600
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4600/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4600/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/sigMC/psi_3770/4600/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4600/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4600/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4600/rtraw/*.rtraw
           ./jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4600.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4600/dst/*.dst
           ./jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4600.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_sig_psi_3770_PI_PI_PHSP_4600 jobOptions_rec_sig_psi_3770_PI_PI_PHSP_4600 subjectSimRec_PHSP 0 99
           ;;

    0.6.2) echo "Single D tag -- run on signal MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/sigMC/psi_3770/4600
           cd scripts/sigMC/psi_3770/4600/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Sig_psi_3770_PI_PI_PHSP_4600 20 20 . sigMC psi_3770 PHSP 4600
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh Sig_psi_3770_PI_PI_PHSP_4600
           ;;

    # ------------------------------------------
    #  0.7 background MC of PHSP DDPIPI @4360MeV
    # ------------------------------------------

    0.7) echo "background MC of PHSP DDPIPI @4360MeV..."
         echo "--> Process: psi(4415)->DDPIPI"
         echo "--> E_{CMS}: 4360MeV"
         echo "--> Generation mode: psi(4415)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or default pdt.table mode"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 30616~31279"
         ;;

    0.7.1) echo "Simulation & Reconstruction -- generate background MC sample..."
           mkdir -p scripts/bkgMC/PHSP/4360
           cd scripts/bkgMC/PHSP/4360
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4360/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4360/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4360/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4360/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4360/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_bkg_PHSP_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4360/rtraw/*.rtraw
           ./jobOptions_sim_bkg_PHSP_PHSP_4360.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_bkg_PHSP_PHSP_4360.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4360/dst/*.dst
           ./jobOptions_rec_bkg_PHSP_PHSP_4360.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_bkg_PHSP_PHSP_4360 jobOptions_rec_bkg_PHSP_PHSP_4360 subjectSimRec_PHSP 0 99
           ;;

    0.7.2) echo "Single D tag -- run on background MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/bkgMC/PHSP/4360
           cd scripts/bkgMC/PHSP/4360/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Bkg_PHSP_PHSP_4360 20 20 . bkgMC PHSP PHSP 4360
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh Bkg_PHSP_PHSP_4360
           ;;

    # ------------------------------------------
    #  0.8 background MC of PHSP DDPIPI @4420MeV
    # ------------------------------------------

    0.8) echo "background MC of PHSP DDPIPI @4420MeV..."
         echo "--> Process: psi(4415)->DDPIPI"
         echo "--> E_{CMS}: 4420MeV"
         echo "--> Generation mode: psi(4415)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or default pdt.table mode"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 31327~31390, 36773~38140"
         ;;

    0.8.1) echo "Simulation & Reconstruction -- generate background MC sample..."
           mkdir -p scripts/bkgMC/PHSP/4420
           cd scripts/bkgMC/PHSP/4420
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4420/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4420/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4420/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4420/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4420/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_bkg_PHSP_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4420/rtraw/*.rtraw
           ./jobOptions_sim_bkg_PHSP_PHSP_4420.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_bkg_PHSP_PHSP_4420.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4420/dst/*.dst
           ./jobOptions_rec_bkg_PHSP_PHSP_4420.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_bkg_PHSP_PHSP_4420 jobOptions_rec_bkg_PHSP_PHSP_4420 subjectSimRec_PHSP 0 99
           ;;

    0.8.2) echo "Single D tag -- run on background MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/bkgMC/PHSP/4420
           cd scripts/bkgMC/PHSP/4420/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Bkg_PHSP_PHSP_4420 20 20 . bkgMC PHSP PHSP 4420
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh Bkg_PHSP_PHSP_4420
           ;;

    # ------------------------------------------
    #  0.9 background MC of PHSP DDPIPI @4600MeV
    # ------------------------------------------

    0.9) echo "background MC of PHSP DDPIPI @4600MeV..."
         echo "--> Process: psi(4415)->DDPIPI"
         echo "--> E_{CMS}: 4600MeV"
         echo "--> Generation mode: psi(4415)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or default pdt.table mode"
         echo "--> Event Number: 1,000,000"
         echo "--> RunNo: 35227~36213"
         ;;

    0.9.1) echo "Simulation & Reconstruction -- generate background MC sample..."
           mkdir -p scripts/bkgMC/PHSP/4600
           cd scripts/bkgMC/PHSP/4600
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4600/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4600/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_mc/bkgMC/PHSP/4600/jobs_sig ./jobs_sig
           fi
           cd jobs_sig
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4600/rtraw
           mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4600/dst
           rm -rf jobOptions*txt
           rm -rf subjectSimRec_*.sh
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_sim_bkg_PHSP_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4600/rtraw/*.rtraw
           ./jobOptions_sim_bkg_PHSP_PHSP_4600.sh 0 99 10000
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/jobOptions_rec_bkg_PHSP_PHSP_4600.sh ./
           rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4600/dst/*.dst
           ./jobOptions_rec_bkg_PHSP_PHSP_4600.sh 0 99
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectSimRec.sh ./
           ./subjectSimRec.sh jobOptions_sim_bkg_PHSP_PHSP_4600 jobOptions_rec_bkg_PHSP_PHSP_4600 subjectSimRec_PHSP 0 99
           ;;

    0.9.2) echo "Single D tag -- run on background MC sample..."
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/bkgMC/PHSP/4600
           cd scripts/bkgMC/PHSP/4600/jobs_sig
           rm -rf dstlist.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/makeJob* ./
           ./makeJob.csh Bkg_PHSP_PHSP_4600 20 20 . bkgMC PHSP PHSP 4600
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_mc/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh Bkg_PHSP_PHSP_4600
           ;;

    # --------------------------
    #  0.10 run on data @4360MeV
    # --------------------------

    0.10) echo "data @4600MeV..."
         echo "--> E_{CMS}: 4358.260MeV"
         echo "--> Energy Spread: 1.97MeV"
         echo "--> Luminosity: 55.18pb^{-1}"
         echo "--> RunNo: 30616~31279"
         ;;

    0.10.1) echo "Single D tag -- run on data sample..."
           mkdir -p scripts/data/4360
           cd scripts/data/4360
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4360/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4360/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4360/jobs_sig ./jobs_sig
           fi
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/data/4360
           cd jobs_sig
           rm -rf data*.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/python/make_data.py ./
           cp -rf $HOME/bes/DDPIPI/v0.1/python/tools.py ./
           ./make_data.py /bes3fs/offline/data/664p01/xyz/4360/dst 30616 31279 4360
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_data/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh data
           ;;

    # --------------------------
    #  0.11 run on data @4420MeV
    # --------------------------

    0.11) echo "data @4420MeV..."
         echo "--> E_{CMS}: 4415.580MeV"
         echo "--> Energy Spread: 2.03MeV"
         echo "--> Luminosity: 44.67pb^{-1} + 1028.89pb^{-1}"
         echo "--> RunNo: 31327~31390, 36773~38140"
         ;;

    0.11.1) echo "Single D tag -- run on data sample..."
           mkdir -p scripts/data/4420
           cd scripts/data/4420
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4420/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4420/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4420/jobs_sig ./jobs_sig
           fi
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/data/4420
           cd jobs_sig
           rm -rf data*.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/python/make_data.py ./
           cp -rf $HOME/bes/DDPIPI/v0.1/python/tools.py ./
           ./make_data.py /besfs3/offline/data/664p01/xyz/4360scan/4420/dst 31327 31390 4420
           ./make_data.py /besfs3/offline/data/besfs2/offline/data/664p01/xyz/4420/dst 36773 38140 4420
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_data/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh data
           ;;

    # --------------------------
    #  0.12 run on data @4600MeV
    # --------------------------

    0.12) echo "data @4600MeV..."
         echo "--> E_{CMS}: 4599.530MeV"
         echo "--> Energy Spread: 2.20MeV"
         echo "--> Luminosity: 566.93pb^{-1}"
         echo "--> RunNo: 35227~36213"
         ;;

    0.12.1) echo "Single D tag -- run on data sample..."
           mkdir -p scripts/data/4600
           cd scripts/data/4600
           if [ ! -d "/besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4600/jobs_sig" ]; then
               mkdir -p /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4600/jobs_sig
               ln -s /besfs/groups/tauqcd/$USER/bes/DDPIPI/v0.1/run/gen_data/data/4600/jobs_sig ./jobs_sig
           fi
           mkdir -p /besfs/users/$USER/DDPIPI/v0.1/data/4600
           cd jobs_sig
           rm -rf data*.txt
           cp -rf $HOME/bes/DDPIPI/v0.1/python/make_data.py ./
           cp -rf $HOME/bes/DDPIPI/v0.1/python/tools.py ./
           ./make_data.py /besfs3/offline/data/besfs2/offline/data/664p01/xyz/4600/dst 35227 36213 4600
           cp -rf $HOME/bes/DDPIPI/v0.1/scripts/gen_script/gen_data/subjectAna.sh ./
           rm -rf *boss* 
           ./subjectAna.sh data
           ;;

esac
