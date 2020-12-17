#!/usr/bin/env bash

# Main driver to do systerm uncertainties analysis
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2020-02-12 Wed 19:22]

usage() {
    printf "NAME\n\tsubmit.sh - Main driver to do systerm uncertainties analysis\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"    "[Pretreatment of data and MC samples]"
    printf "\n\t%-9s  %-40s\n" "0.1.1"  "Simulation & Reconstruction -- generate D1_2420 MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.2"  "Simulation & Reconstruction -- generate D1_2420 MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.3"  "Simulation & Reconstruction -- generate psipp MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.4"  "Simulation & Reconstruction -- generate psipp MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.5"  "Simulation & Reconstruction -- generate DDPIPI MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.6"  "Simulation & Reconstruction -- generate DDPIPI MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.7"  "Single D tag -- run on D1_2420 MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.8"  "Single D tag -- run on D1_2420 MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.9"  "Single D tag -- run on psipp MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.10" "Single D tag -- run on psipp MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.11" "Single D tag -- run on DDPIPI MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.12" "Single D tag -- run on DDPIPI MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.13" "Get samples -- extracte useful info && apply cuts: signal region and sideband region, ISR factors -- D1_2420"
    printf "\n\t%-9s  %-40s\n" "0.1.14" "Get samples -- extracte useful info && apply cuts: signal region and sideband region, ISR factors -- psipp"
    printf "\n\t%-9s  %-40s\n" "0.1.15" "Get samples -- extracte useful info && apply cuts: signal region and sideband region, ISR factors -- DDPIPI"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Get system uncertainties]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Fit distributions -- simultaneous fit recoiling mass of D + Dmiss and recoiling mass of pipi"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Get shapes -- mix MC shapes"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Fit distributions -- fit invariant mass of Kpipi"
    printf "\n\t%-9s  %-40s\n" "0.2.4" "Fit distributions -- fit recoiling mass of Dpipi"
    printf "\n\t%-9s  %-40s\n" "0.2.5" "Calculate numbers -- calculate cross section of DDpipi and systerm uncertainties"

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
         echo "--> Samples: data, signal MC, PHSP MC"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03"
         ;;

    0.1.1) echo "Simulation & Reconstruction -- generating D1_2420 MC sample(@703p01)..."
           cd gen_mc/D1_2420
           ./subSimRec_D1_2420_703p01_KKMC.sh
           ;;

    0.1.2) echo "Simulation & Reconstruction -- generating D1_2420 MC sample(@705)..."
           cd gen_mc/D1_2420
           ./subSimRec_D1_2420_705_KKMC.sh
           ;;

    0.1.3) echo "Simulation & Reconstruction -- generating psipp MC sample(@703p01)..."
           cd gen_mc/psipp
           ./subSimRec_psipp_703p01_KKMC.sh
           ;;

    0.1.4) echo "Simulation & Reconstruction -- generating psipp MC sample(@705)..."
           cd gen_mc/psipp
           ./subSimRec_psipp_705_KKMC.sh
           ;;

    0.1.5) echo "Simulation & Reconstruction -- generating DDPIPI MC sample(@703p01)..."
           cd gen_mc/DDPIPI
           ./subSimRec_D_D_PI_PI_703p01_KKMC.sh
           ;;

    0.1.6) echo "Simulation & Reconstruction -- generating DDPIPI MC sample(@705)..."
           cd gen_mc/DDPIPI
           ./subSimRec_D_D_PI_PI_705_KKMC.sh
           ;;

    0.1.7) echo "Single D tag -- running on D1_2420 MC sample(@703p01)..."
           cd gen_mc/D1_2420
           ./subAna_D1_2420_703p01.sh
           ;;

    0.1.8) echo "Single D tag -- running on D1_2420 MC sample(@705)..."
           cd gen_mc/D1_2420
           ./subAna_D1_2420_705.sh
           ;;

    0.1.9) echo "Single D tag -- running on psipp MC sample(@703p01)..."
           cd gen_mc/psipp
           ./subAna_psipp_703p01.sh
           ;;

    0.1.10) echo "Single D tag -- running on psipp MC sample(@705)..."
            cd gen_mc/psipp
            ./subAna_psipp_705.sh
            ;;

    0.1.11) echo "Single D tag -- running on DDPIPI MC sample(@703p01)..."
            cd gen_mc/DDPIPI
            ./subAna_D_D_PI_PI_703p01.sh
            ;;

    0.1.12) echo "Single D tag -- running on DDPIPI MC sample(@705)..."
            cd gen_mc/DDPIPI
            ./subAna_D_D_PI_PI_705.sh
            ;;

    0.1.13) echo "Get samples -- extracting useful info && applying cut -- D1_2420..."
           cd gen_mc/D1_2420
           ./synthesizeD1_2420.sh
           ./getInfoD1_2420.sh
           ./getFactorD1_2420.sh round3
           ./applyCutsD1_2420.sh
           ;;

    0.1.14) echo "Get samples -- extracting useful info && applying cut -- psipp..."
           cd gen_mc/psipp
           ./synthesizepsipp.sh
           ./getInfopsipp.sh
           ./getFactorpsipp.sh round3
           ./applyCutspsipp.sh
           ;;

    0.1.15) echo "Get samples -- extracting useful info && applying cut -- DDPIPI..."
           cd gen_mc/DDPIPI
           ./synthesizeD_D_PI_PI.sh
           ./getInfoD_D_PI_PI.sh
           ./getFactorD_D_PI_PI.sh round3
           ./applyCutsD_D_PI_PI.sh
           ;;

    # ------------------------------
    #  0.2 Get systerm uncertainties
    # ------------------------------

    0.2) echo "Getting systerm uncertainties..."
         echo "--> Samples: data, signal MC, PHSP MC"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03"
         ;;

    0.2.1) echo "Fit distributions -- simultaneous fitting recoiling mass of D + Dmiss and recoiling mass of pipi..."
           cd ana
           ./simul_fit.sh round3
           ;;

    0.2.2) echo "Get shapes -- mixing MC shapes..."
           cd gen_mc/mix
           ./mixMC.sh round3
           cd -
           cd ana
           ./mixROOT.sh round3
           ;;

    0.2.3) echo "Fit distributions -- fitting invariant mass of Kpipi..."
           cd ana
           ./factorMKpipi.sh round3
           ;;

    0.2.4) echo "Fit distributions -- fitting recoiling mass of Dpipi..."
           cd ana
           ./fitRMDpipi.sh round3
           ;;

    0.2.5) echo "Calculate numbers -- calculating cross section of DDpipi and systerm uncertainties..."
           cd ana
           ./calXS.sh round3
           cd -
           ./format_xs.py round3
           ./cal_diff.py round3
           ;;

esac
