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
    printf "\n\t%-9s  %-40s\n" "0.1.1"  "Single D tag -- run on data"

    printf "\n\t%-9s  %-40s\n" "0.2"    "[run on signal MC of psi(4260)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) reconstructed @703p01]" 
    printf "\n\t%-9s  %-40s\n" "0.2.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.2.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.3"    "[run on signal MC of psi(4260)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.3.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.3.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.4"    "[run on signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.4.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.4.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.5"    "[run on data reconstructed @705]"
    printf "\n\t%-9s  %-40s\n" "0.5.1"  "Single D tag -- data"

    printf "\n\t%-9s  %-40s\n" "0.6"    "[run on signal MC of psi(4260)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) reconstructed @705]" 
    printf "\n\t%-9s  %-40s\n" "0.6.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.6.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.7"    "[run on signal MC of psi(4260)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @705]"
    printf "\n\t%-9s  %-40s\n" "0.7.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.7.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.8"    "[run on signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @705]"
    printf "\n\t%-9s  %-40s\n" "0.8.1"  "Simulation & Reconstruction -- generate signal MC sample"
    printf "\n\t%-9s  %-40s\n" "0.8.2"  "Single D tag -- run on signal MC sample"

    printf "\n\t%-9s  %-40s\n" "0.9"    "[run on inclusive MC reconstructed @703p01]"
    printf "\n\t%-9s  %-40s\n" "0.9.1"  "Single D tag -- inclusive MC"

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
         echo "--> LXSLC: lxslc7"
         ;;

    0.1.1) echo "Single D tag -- run on data sample..."
           cd scripts/gen_script/gen_data
           ./subData_703p01.sh
           ;;

    # ---------------------------------------------------------------------------------------------
    #  0.2 signal MC of psi(4260)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(HELAMP) reconstructed @703p01
    # ---------------------------------------------------------------------------------------------
    
    0.2) echo "signal MC of psi(4260)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) reconstructed @703p01..."
         echo "--> Process: psi(4260)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> Generation mode: psi(4260)->D1_(2420)D PHSH; D1_(2420)->DPIPI HELAMP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 20,000"
         ;;

    0.2.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/D1_2420
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_D1_2420_703p01_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_D1_2420_703p01_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.2.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/D1_2420
           ./subAna_D1_2420_703p01.sh
           ;;

    # ------------------------------------------------------------------------------------------
    #  0.3 signal MC of psi(4260)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01
    # ------------------------------------------------------------------------------------------

    0.3) echo "signal MC of psi(4260)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @703p01..."
         echo "--> Process: psi(4260)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> Generation mode: psi(4260)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 20,000"
         ;;

    0.3.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/psipp
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_psipp_703p01_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_psipp_703p01_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.3.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/psipp
           ./subAna_psipp_703p01.sh
           ;;

    # ---------------------------------------------------------------
    #  0.4 signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @703p01
    # ---------------------------------------------------------------
    
    0.4) echo "signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @703p01..."
         echo "--> Process: psi(4260)->DDPIPI"
         echo "--> Generation mode: psi(4260)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         echo "--> Event Number: 20,000"
         ;;

    0.4.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/DDPIPI
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_D_D_PI_PI_703p01_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_D_D_PI_PI_703p01_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.4.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/DDPIPI
           ./subAna_D_D_PI_PI_703p01.sh
           ;;

    # -----------------------------------
    #  0.5 run on data reconstructed @705
    # -----------------------------------

    0.5) echo "data reconstructed @705..."
         echo "--> Patch: 705"
         echo "--> LXSLC: lxslc7"
         ;;

    0.5.1) echo "Single D tag -- run on data sample..."
           cd scripts/gen_script/gen_data
           ./subData_705.sh
           ;;

    # ------------------------------------------------------------------------------------------
    #  0.6 signal MC of psi(4260)->D_1(2420)D(PHSP), D_1(2420)->DPIPI(HELAMP) reconstructed @705
    # ------------------------------------------------------------------------------------------
    
    0.6) echo "signal MC of psi(4260)->D1_(2420)D(PHSP), D1_(2420)->DPIPI(HELAMP) reconstructed @705..."
         echo "--> Process: psi(4260)->D1_(2420)D, D1_(2420)->DPIPI"
         echo "--> Generation mode: psi(4260)->D1_(2420)D PHSH; D1_(2420)->DPIPI HELAMP; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         ;;

    0.6.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/D1_2420
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_D1_2420_705_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_D1_2420_705_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.6.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/D1_2420
           ./subAna_D1_2420_705.sh
           ;;

    # ---------------------------------------------------------------------------------------
    #  0.7 signal MC of psi(4260)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @705
    # ---------------------------------------------------------------------------------------

    0.7) echo "signal MC of psi(4260)->psi(3770)PIPI(PHSP), psi(3770)->DD(VSS) reconstructed @705..."
         echo "--> Process: psi(4260)->psi(3770)PIPI, psi(3770)->DD"
         echo "--> Generation mode: psi(4260)->psi(3770)PIPI PHSH; psi(3770)->DD VSS; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         ;;

    0.7.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/psipp
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_psipp_705_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_psipp_705_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.7.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/psipp
           ./subAna_psipp_705.sh
           ;;

    # ------------------------------------------------------------
    #  0.8 signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @705
    # ------------------------------------------------------------
    
    0.8) echo "signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @705..."
         echo "--> Process: psi(4260)->DDPIPI"
         echo "--> Generation mode: psi(4260)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         ;;

    0.8.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/DDPIPI
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_D_D_PI_PI_705_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_D_D_PI_PI_705_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.8.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/DDPIPI
           ./subAna_D_D_PI_PI_705.sh
           ;;

    # ----------------------------------------------
    #  0.9 run on inclusive MC reconstructed @703p01
    # ----------------------------------------------

    0.9) echo "inclusive MC reconstructed @703p01..."
         echo "--> Patch: 703p01"
         echo "--> LXSLC: lxslc7"
         ;;

    0.9.1) echo "Single D tag -- run on inclusive MC sample..."
           cd scripts/gen_script/gen_mc/incMC
           ./subincMC_703p01.sh
           ;;

    # -----------------------------------------------------------
    #  0.10 signal MC of psi(4260)->DDPI(PHSP) reconstructed @705
    # -----------------------------------------------------------
    
    0.10) echo "signal MC of psi(4260)->DDPI(PHSP) reconstructed @705..."
         echo "--> Process: psi(4260)->DDPI"
         echo "--> Generation mode: psi(4260)->DDPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         ;;

    0.10.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/DDPI
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_D_D_PI_703p01_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_D_D_PI_703p01_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.10.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/DDPI
           ./subAna_D_D_PI_703p01.sh
           ;;

    # ------------------------------------------------------------
    #  0.11 signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @705
    # ------------------------------------------------------------
    
    0.11) echo "signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @705..."
         echo "--> Process: psi(4260)->DDPIPI"
         echo "--> Generation mode: psi(4260)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         ;;

    0.11.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/DstDPI
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_Dst_D_PI_705_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_Dst_D_PI_703p01_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.11.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/DstDPI
           ./subAna_Dst_D_PI_703p01.sh
           ;;

    # ------------------------------------------------------------
    #  0.12 signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @705
    # ------------------------------------------------------------
    
    0.12) echo "signal MC of psi(4260)->DDPIPI(PHSP) reconstructed @705..."
         echo "--> Process: psi(4260)->DDPIPI"
         echo "--> Generation mode: psi(4260)->DDPIPI PHSH; D decay D_DALITZ(assignated mode) or PHSP(inlusive mode)"
         ;;

    0.12.1) echo "Simulation & Reconstruction -- generate signal MC sample..."
           cd scripts/gen_script/gen_mc/DDPIPIinc
           echo "which type of generator do you want to use?"
           read opt
           if [ $opt == "ConExc" ]; then
               ./subSimRec_D_D_PI_PI_inc_705_ConExc.sh ConExc
           elif [ $opt == "KKMC" ]; then
               ./subSimRec_D_D_PI_PI_inc_703p01_KKMC.sh
           else
               echo "please check the generator you want to use!"
           fi
           ;;

    0.12.2) echo "Single D tag -- run on signal MC sample..."
           cd scripts/gen_script/gen_mc/DDPIPIinc
           ./subAna_D_D_PI_PI_inc_703p01.sh
           ;;

esac
