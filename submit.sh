#!/usr/bin/env bash

# Main driver to submit simulation and reconstruction jobs as well as generating root files 
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-09-02 Mon 22:17]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit simulation and reconstruction jobs as well as generating root files\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./submit.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"    "[run on data reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.1.1"  "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.2"    "[run on signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) reconstructed @703p01]" 
    printf "\n\t%-9s  %-40s\n" "0.2.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.2.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.3"    "[run on signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) reconstructed @703p01]" 
    printf "\n\t%-9s  %-40s\n" "0.3.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.3.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.4"    "[run on signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.4.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.4.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.5"    "[run on signal MC of psi(4415)->DDPIPI(PHSP) reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.5.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.5.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.6"    "[run on inclusive MC (qqbar) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.6.1"  "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.7"    "[run on inclusive MC (qqbar) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.7.1"  "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.8"    "[run on inclusive MC (qqbar) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.8.1"  "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.9"    "[run on inclusive MC (open harm) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.9.1"  "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.10"   "[run on inclusive MC (open harm) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.10.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.11"   "[run on inclusive MC (open harm) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.11.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.12"   "[run on inclusive MC (bhabha) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.12.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.13"   "[run on inclusive MC (dimu) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.13.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.14"   "[run on inclusive MC (ditau) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.14.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.15"   "[run on inclusive MC (digamma) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.15.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.16"   "[run on inclusive MC (twogamma) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.16.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.17"   "[run on inclusive MC (ISR) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.17.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.18"   "[run on inclusive MC (gammaXYZ) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.18.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.19"   "[run on inclusive MC (hadrons) @4360MeV]"
    printf "\n\t%-9s  %-40s\n" "0.19.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.20"   "[run on inclusive MC (bhabha) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.20.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.21"   "[run on inclusive MC (dimu) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.21.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.22"   "[run on inclusive MC (ditau) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.22.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.23"   "[run on inclusive MC (digamma) @4420MeV]"
    printf "\n\t%-9s  %-40s\n" "0.23.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.24"   "[run on inclusive MC (bhabha) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.24.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.25"   "[run on inclusive MC (dimu) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.25.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.26"   "[run on inclusive MC (ditau) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.26.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.27"   "[run on inclusive MC (digamma) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.27.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.28"   "[run on inclusive MC (twogamma) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.28.1" "Single D tag -- inclusive MC sample"

    printf "\n\t%-9s  %-40s\n" "0.29"   "[run on inclusive MC (LL) @4600MeV]"
    printf "\n\t%-9s  %-40s\n" "0.29.1" "Single D tag -- inclusive MC sample"

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

    # --------------------------------------
    #  0.1 run on data reconstructed @703p01
    # --------------------------------------

    0.1) echo "data reconstructed @703p01..."
         echo "--> Patch: 703p01"
         echo "--> LXSLC: lxslc6"
         ;;

    0.1.1) echo "Single D tag -- run on data sample..."
           cd scripts/gen_script/gen_data
           ./subData_703p01.sh
           ;;

    # ---------------------------------------------------------------------------------------
    #  0.2 signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) reconstructed @703p01
    # ---------------------------------------------------------------------------------------
    
    0.2) echo "signal MC of psi(4415)->X(3842)PIPI(PHSP), X(3842)->DD(PHSP) reconstructed @703p01..."
         echo "--> Process: psi(4415)->X(3842)PIPI, X(3842)->DD"
         echo "--> Generation mode: psi(4415)->X(3842)PIPI PHSH; X(3842)->DD PHSP; D decay D_DALITZ(assignated mode) or inlusive decay"
         echo "--> Event Number: 20,000"
         ;;

    0.2.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc
           ./subSimRec_X_3842_703p01.sh
           ;;

    0.2.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc
           ./subAna_X_3842_703p01.sh
           ;;

    # ---------------------------------------------------------------------------------------------
    #  0.3 signal MC of psi(4415)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(HELAMP) reconstructed @703p01
    # ---------------------------------------------------------------------------------------------
    
    0.3) echo "signal MC of psi(4415)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) reconstructed @703p01..."
         echo "--> Process: psi(4415)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> Generation mode: psi(4415)->D1_(2420)D PHSH; D1_(2420)->DPIPI HELAMP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 20,000"
         ;;

    0.3.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc
           ./subSimRec_D1_2420_703p01.sh
           ;;

    0.3.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc
           ./subAna_D1_2420_703p01.sh
           ;;

    # ------------------------------------------------------------------------------------------
    #  0.4 signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01
    # ------------------------------------------------------------------------------------------

    0.4) echo "signal MC of psi(4415)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01..."
         echo "--> Process: psi(4415)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> Generation mode: psi(4415)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 20,000"
         ;;

    0.4.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc
           ./subSimRec_psipp_703p01.sh
           ;;

    0.4.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc
           ./subAna_psipp_703p01.sh
           ;;

    # ---------------------------------------------------------------
    #  0.5 signal MC of psi(4415)->DDPIPI(PHSP) reconstructed @703p01
    # ---------------------------------------------------------------
    
    0.5) echo "signal MC of psi(4415)->DDPIPI(PHSP) reconstructed @703p01..."
         echo "--> Process: psi(4415)->DDPIPI"
         echo "--> Generation mode: psi(4415)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 20,000"
         ;;

    0.5.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc
           ./subSimRec_D_D_PI_PI_703p01.sh
           ;;

    0.5.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc
           ./subAna_D_D_PI_PI_703p01.sh
           ;;

    # -----------------------------------------
    #  0.6 run on inclusive MC (qqbar) @4360MeV
    # -----------------------------------------

    0.6) echo "inclusive MC @4360MeV..."
         echo "--> E_{CMS}: 4358.260MeV"
         echo "--> Mode: qqbar"
         echo "--> Energy Spread: 1.97MeV"
         echo "--> Event Number: 9,400,000"
         echo "--> Cross Section: 17.5nb"
         echo "--> Luminosity: 539.84pb^{-1}"
         echo "--> RunNo: 30616~31279"
         ;;

    0.6.1) echo "Single D tag -- run on inclusive MC sample..."
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

    # -----------------------------------------
    #  0.7 run on inclusive MC (qqbar) @4420MeV
    # -----------------------------------------

    0.7) echo "inclusive MC @4420MeV..."
         echo "--> E_{CMS}: 4415.580MeV"
         echo "--> Mode: qqbar"
         echo "--> Energy Spread: 2.03MeV"
         echo "--> Event Number: 14,000,000"
         echo "--> Cross Section: 7.0nb"
         echo "--> Luminosity: 1028.89pb^{-1}"
         echo "--> RunNo: 36773~38140"
         ;;

    0.7.1) echo "Single D tag -- run on inclusive MC sample..."
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

    # -------------------------------------------------
    #  0.8 run on inclusive MC (qqbar and ISR) @4600MeV
    # -------------------------------------------------

    0.8) echo "inclusive MC @4600MeV..."
         echo "--> E_{CMS}: 4599.530MeV"
         echo "--> Mode: qqbar and ISR"
         echo "--> Energy Spread: 2.20MeV"
         echo "--> Event Number: 10,000,000"
         echo "--> Cross Section: 6.0nb"
         echo "--> Luminosity: 566.93pb^{-1}"
         echo "--> RunNo: 35227~35743"
         ;;

    0.8.1) echo "Single D tag -- run on inclusive MC sample..."
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

    # ----------------------------------------------
    #  0.9 run on inclusive MC (open charm) @4360MeV
    # ----------------------------------------------

    0.9) echo "inclusive MC @4360MeV..."
         echo "--> E_{CMS}: 4358.260MeV"
         echo "--> Mode: open charm"
         echo "--> Energy Spread: 1.97MeV"
         echo "--> Event Number: 17,200,000"
         echo "--> Cross Section: 10.6nb"
         echo "--> Luminosity: 539.84pb^{-1}"
         echo "--> RunNo: 30616~31279"
         ;;

    0.9.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.10 run on inclusive MC (open charm) @4420MeV
    # -----------------------------------------------

    0.10) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: open charm"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 40,300,000"
          echo "--> Cross Section: 10.2nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.10.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.11 run on inclusive MC (open charm) @4600MeV
    # -----------------------------------------------

    0.11) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: open charm"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 12,000,000"
          echo "--> Cross Section: 7.8nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.11.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.12 run on inclusive MC (bhabha) @4360MeV
    # -------------------------------------------

    0.12) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: bhabha"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 10,000,000"
          echo "--> Cross Section: 389nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.12.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.13 run on inclusive MC (dimu) @4360MeV
    # -----------------------------------------

    0.13) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: dimu"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 2,600,000"
          echo "--> Cross Section: 4.8nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.13.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.14 run on inclusive MC (ditau) @4360MeV
    # ------------------------------------------

    0.14) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: ditau"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 5,000,000"
          echo "--> Cross Section: 9.2nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.14.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.15 run on inclusive MC (digamma) @4360MeV
    # --------------------------------------------

    0.15) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: digamma"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 10,000,000"
          echo "--> Cross Section: 18.5nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.15.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.16 run on inclusive MC (twogamma) @4360MeV
    # ---------------------------------------------

    0.16) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: twogamma"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 1,000,000"
          echo "--> Cross Section: 1.9nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.16.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.17 run on inclusive MC (ISR) @4360MeV
    # ----------------------------------------

    0.17) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: ISR"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 600,000"
          echo "--> Cross Section: 1.11nb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.17.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.18 run on inclusive MC (gammaXYZ) @4360MeV
    # ---------------------------------------------

    0.18) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: gammaXYZ"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 33,000"
          echo "--> Cross Section: 41.6pb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.18.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.19 run on inclusive MC (hadrons) @4360MeV
    # --------------------------------------------

    0.19) echo "inclusive MC @4360MeV..."
          echo "--> E_{CMS}: 4358.260MeV"
          echo "--> Mode: hadrons"
          echo "--> Energy Spread: 1.97MeV"
          echo "--> Event Number: 190,000"
          echo "--> Cross Section: 249.9pb"
          echo "--> Luminosity: 539.84pb^{-1}"
          echo "--> RunNo: 30616~31279"
          ;;

    0.19.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.20 run on inclusive MC (bhabha) @4420MeV
    # -------------------------------------------

    0.20) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: bhabha"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 38,000,000"
          echo "--> Cross Section: 379.3nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.20.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.21 run on inclusive MC (dimu) @4420MeV
    # -----------------------------------------

    0.21) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: dimu"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number:6,000,000"
          echo "--> Cross Section: 5.8286nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.21.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.22 run on inclusive MC (ditau) @4420MeV
    # ------------------------------------------

    0.22) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: ditau"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 7,000,000"
          echo "--> Cross Section: 3.4726nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.22.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.23 run on inclusive MC (digamma) @4420MeV
    # --------------------------------------------

    0.23) echo "inclusive MC @4420MeV..."
          echo "--> E_{CMS}: 4415.580MeV"
          echo "--> Mode: digamma"
          echo "--> Energy Spread: 2.03MeV"
          echo "--> Event Number: 18,000,000"
          echo "--> Cross Section: 18.6nb"
          echo "--> Luminosity: 1028.89pb^{-1}"
          echo "--> RunNo: 36773~38140"
          ;;

    0.23.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.24 run on inclusive MC (bhabha) @4600MeV
    # -------------------------------------------

    0.24) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: bhabha"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 60,000,000"
          echo "--> Cross Section: 350nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.24.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.25 run on inclusive MC (dimu) @4600MeV
    # -----------------------------------------

    0.25) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: dimu"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 6,600,000"
          echo "--> Cross Section: 4.2nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.25.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.26 run on inclusive MC (ditau) @4600MeV
    # ------------------------------------------

    0.26) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: ditau"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 15,000,000"
          echo "--> Cross Section: 3.4nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.26.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.27 run on inclusive MC (digamma) @4600MeV
    # --------------------------------------------

    0.27) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: digamma"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 30,000,000"
          echo "--> Cross Section: 16.6nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.27.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.28 run on inclusive MC (twogamma) @4600MeV
    # ---------------------------------------------

    0.28) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: twogamma"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 11,000,000"
          echo "--> Cross Section: 774.1nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.28.1) echo "Single D tag -- run on inclusive MC sample..."
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
    #  0.29 run on inclusive MC (LL) @4600MeV
    # ---------------------------------------

    0.29) echo "inclusive MC @4600MeV..."
          echo "--> E_{CMS}: 4599.530MeV"
          echo "--> Mode: LL"
          echo "--> Energy Spread: 2.20MeV"
          echo "--> Event Number: 500,000"
          echo "--> Cross Section: 0.35nb"
          echo "--> Luminosity: 566.93pb^{-1}"
          echo "--> RunNo: 35227~35743"
          ;;

    0.29.1) echo "Single D tag -- run on inclusive MC sample..."
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

esac
