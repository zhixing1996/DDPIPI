#!/usr/bin/env bash

# Main driver to do systerm uncertainties analysis
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2020-02-12 Wed 19:22]

usage() {
    printf "NAME\n\tsubmit.sh - Main driver to do systerm uncertainties analysis\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Pretreatment of data and MC samples]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Simulation & Reconstruction -- generate D1_2420 MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Simulation & Reconstruction -- generate D1_2420 MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.3" "Single D tag -- run on D1_2420 MC sample(@703p01)"
    printf "\n\t%-9s  %-40s\n" "0.1.4" "Single D tag -- run on D1_2420 MC sample(@705)"
    printf "\n\t%-9s  %-40s\n" "0.1.5" "Get samples -- extracte useful info: signal region, ISR factors"
    printf "\n\t%-9s  %-40s\n" "0.1.6" "Get samples -- apply cuts: D1_2420 MC"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Get system uncertainties]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Fit distributions -- cos theta of tagged D"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Get shapes -- mix MC shapes"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Fit distributions -- fit recoiling mass of Dpipi"
    printf "\n\t%-9s  %-40s\n" "0.2.4" "Calculate numbers -- calculate cross section of DDpipi and systerm uncertainties"

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
         echo "--> Samples: data, D1_2420 MC"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03"
         ;;

    0.1.1) echo "Simulation & Reconstruction -- generating D1_2420 MC sample(@703p01)..."
           cd scripts/mc/D1_2420_001000
           ./subSimRec_D1_2420_703p01_KKMC.sh
           cd $HOME/bes/DDPIPI/v0.2/python/sys_err/HELAMP
           cd scripts/mc/D1_2420_100010
           ./subSimRec_D1_2420_703p01_KKMC.sh
           ;;

    0.1.2) echo "Simulation & Reconstruction -- generating D1_2420 MC sample(@705)..."
           cd scripts/mc/D1_2420_001000
           ./subSimRec_D1_2420_705_KKMC.sh
           cd $HOME/bes/DDPIPI/v0.2/python/sys_err/HELAMP
           cd scripts/mc/D1_2420_100010
           ./subSimRec_D1_2420_705_KKMC.sh
           ;;

    0.1.3) echo "Single D tag -- running on D1_2420 MC sample(@703p01)..."
           cd scripts/mc/D1_2420_001000
           ./subAna_D1_2420_703p01.sh
           cd $HOME/bes/DDPIPI/v0.2/python/sys_err/HELAMP
           cd scripts/mc/D1_2420_100010
           ./subAna_D1_2420_703p01.sh
           ;;

    0.1.4) echo "Single D tag -- running on D1_2420 MC sample(@705)..."
           cd scripts/mc/D1_2420_001000
           ./subAna_D1_2420_705.sh
           cd $HOME/bes/DDPIPI/v0.2/python/sys_err/HELAMP
           cd scripts/mc/D1_2420_100010
           ./subAna_D1_2420_705.sh
           ;;

    0.1.5) echo "Get samples -- extracting useful info: signal region, ISR factors..."
           cd scripts/mc/D1_2420_001000
           ./synthesizeD1_2420_703p01.sh
           ./getInfoD1_2420_703p01.sh
           ./getFactorD1_2420_703p01.sh round3
           ./synthesizeD1_2420_705.sh
           ./getInfoD1_2420_705.sh
           ./getFactorD1_2420_705.sh round3
           cd $HOME/bes/DDPIPI/v0.2/python/sys_err/HELAMP
           cd scripts/mc/D1_2420_100010
           ./synthesizeD1_2420_703p01.sh
           ./getInfoD1_2420_703p01.sh
           ./getFactorD1_2420_703p01.sh round3
           ./synthesizeD1_2420_705.sh
           ./getInfoD1_2420_705.sh
           ./getFactorD1_2420_705.sh round3
           ;;

    0.1.6) echo "Get samples -- applying cuts: D1_2420 MC and data..."
           cd scripts/mc/D1_2420_001000
           ./applyCutsD1_2420_703p01.sh
           ./applyCutsD1_2420_705.sh
           cd $HOME/bes/DDPIPI/v0.2/python/sys_err/HELAMP
           cd scripts/mc/D1_2420_100010
           ./applyCutsD1_2420_703p01.sh
           ./applyCutsD1_2420_705.sh
           cd $HOME/bes/DDPIPI/v0.2/python/sys_err/HELAMP
           cd scripts/ana
           ./applyCuts.sh
           ;;

    # ------------------------------
    #  0.2 Get systerm uncertainties
    # ------------------------------

    0.2) echo "Getting systerm uncertainties..."
         echo "--> Samples: data, D1_2420 MC"
         echo "--> Selection Algorithm Version: DDecayAlg-00-00-03"
         ;;

    0.2.1) echo "Fit distributions -- cos theta of tagged D..."
           cd scripts/ana
           ./fitCosD.sh
           ;;

    0.2.2) echo "Get shapes -- mixing MC shapes..."
           cd scripts/ana
           ./mixMC.sh
           ;;

    0.2.3) echo "Fit distributions -- fitting recoiling mass of Dpipi..."
           cd scripts/ana
           ./fitRMDpipi.sh round3
           ;;

    0.2.5) echo "Calculate numbers -- calculating cross section of DDpipi and systerm uncertainties..."
           cd scripts/ana
           ./calXS.sh round3
           cd -
           ./format_xs.py round3
           ./cal_diff.py round3
           ;;

esac
