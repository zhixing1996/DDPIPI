#!/usr/bin/env bash

# Main driver to do systerm uncertainties analysis
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2020-02-12 Wed 19:22]

usage() {
    printf "NAME\n\tsubmit.sh - Main driver to do systerm uncertainties analysis\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Get MC samples with flat cross sections]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Simulation & Reconstruction -- generate samples @703p01"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Simulation & Reconstruction -- generate samples @705"
    printf "\n\t%-9s  %-40s\n" "0.1.3" "Simulation & Reconstruction -- generate samples @707"
    printf "\n\t%-9s  %-40s\n" "0.1.4" "Single D tag -- run on MC samples @703p01"
    printf "\n\t%-9s  %-40s\n" "0.1.5" "Single D tag -- run on MC samples @705"
    printf "\n\t%-9s  %-40s\n" "0.1.6" "Single D tag -- run on MC samples @707"
    printf "\n\t%-9s  %-40s\n" "0.1.7" "Get samples -- extracte useful info: signal region and sideband region, ISR factors"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Sample cross sections 500 times]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Fit distributions -- get fitted cross sections parameters"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Sample -- sample"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Get Info -- get init ISR and m_truth"

    printf "\n\t%-9s  %-40s\n" "0.3"   "[Fit isr*eff distributions]"
    printf "\n\t%-9s  %-40s\n" "0.3.1" "Convert ROOT -- convert ROOT files"
    printf "\n\t%-9s  %-40s\n" "0.3.2" "Fit distributions -- fit isr*eff distributions"
    printf "\n\t%-9s  %-40s\n" "0.3.3" "Calculate numbers -- calculate systerm uncertainties"

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

    0.1.1) echo "Simulation & Reconstruction -- generating MC samples @703p01..."
           cd scripts/mc/D1_2420
           ./subSimRec_D1_2420_703p01.sh
           cd ../DDPIPI
           ./subSimRec_D_D_PI_PI_703p01_KKMC.sh
           cd ../psipp
           ./subSimRec_psipp_703p01_KKMC.sh
           ;;

    0.1.2) echo "Simulation & Reconstruction -- generating MC samples @705..."
           cd scripts/mc/D1_2420
           ./subSimRec_D1_2420_705.sh
           cd ../DDPIPI
           ./subSimRec_D_D_PI_PI_705_KKMC.sh
           cd ../psipp
           ./subSimRec_psipp_705_KKMC.sh
           ;;

    0.1.3) echo "Simulation & Reconstruction -- generating MC samples @707..."
           cd scripts/mc/D1_2420
           ./subSimRec_D1_2420_707.sh
           cd ../DDPIPI
           ./subSimRec_D_D_PI_PI_707_KKMC.sh
           cd ../psipp
           ./subSimRec_psipp_707_KKMC.sh
           ;;

    0.1.4) echo "Single D tag -- running on MC samples @703p01..."
           cd scripts/mc/D1_2420
           ./subAna_D1_2420_703p01.sh
           cd ../DDPIPI
           ./subAna_D_D_PI_PI_703p01.sh
           cd ../psipp
           ./subAna_psipp_703p01.sh
           ;;

    0.1.5) echo "Single D tag -- running on MC samples @705..."
           cd scripts/mc/D1_2420
           ./subAna_D1_2420_705.sh
           cd ../DDPIPI
           ./subAna_D_D_PI_PI_705.sh
           cd ../psipp
           ./subAna_psipp_705.sh
           ;;

    0.1.6) echo "Single D tag -- running on MC samples @707..."
           cd scripts/mc/D1_2420
           ./subAna_D1_2420_707.sh
           cd ../DDPIPI
           ./subAna_D_D_PI_PI_707.sh
           cd ../psipp
           ./subAna_psipp_707.sh
           ;;

    0.1.7) echo "Get samples -- extracting useful info: signal region and sideband region, ISR factors..."
           cd scripts/mc/D1_2420
           ./synthesizeD1_2420_703p01.sh
           ./synthesizeD1_2420_705.sh
           ./synthesizeD1_2420_707.sh
           ./getInfoD1_2420_703p01.sh
           ./getInfoD1_2420_705.sh
           ./getInfoD1_2420_707.sh
           ./getFactorD1_2420_703p01.sh round0
           ./getFactorD1_2420_705.sh round0
           ./getFactorD1_2420_707.sh round0
           cd ../DDPIPI
           ./synthesizeD_D_PI_PI_703p01.sh
           ./synthesizeD_D_PI_PI_705.sh
           ./synthesizeD_D_PI_PI_707.sh
           ./getInfoD_D_PI_PI_703p01.sh
           ./getInfoD_D_PI_PI_705.sh
           ./getInfoD_D_PI_PI_707.sh
           ./getFactorD_D_PI_PI_703p01.sh round0
           ./getFactorD_D_PI_PI_705.sh round0
           ./getFactorD_D_PI_PI_707.sh round0
           cd ../psipp
           ./synthesizepsipp_703p01.sh
           ./synthesizepsipp_705.sh
           ./synthesizepsipp_707.sh
           ./getInfopsipp_703p01.sh
           ./getInfopsipp_705.sh
           ./getInfopsipp_707.sh
           ./getFactorpsipp_703p01.sh round0
           ./getFactorpsipp_705.sh round0
           ./getFactorpsipp_707.sh round0
           ;;

    # ------------------------------------
    #  0.2 Sample cross sections 500 times
    # ------------------------------------

    0.2) echo "Sampling cross sections 500 times..."
         ;;

    0.2.1) echo "Fit distributions -- getting fitted cross sections parameters..."
           cd sample
           python get_param.py
           ;;

    0.2.2) echo "Sample -- sampling..."
           cd sample/sub
           ./sub_ISR_eff.sh
           ;;

    0.2.3) echo "Get Info -- getting init ISR and m_truth..."
           cd sample
           python get_ini_isr.py D1_2420
           python get_ini_isr.py psipp
           python get_ini_isr.py DDPIPI
           cd ../scripts/ana
           ./getMTruthall.sh
           ;;

    # ------------------------------
    #  0.3 Fit isr*eff distributions
    # ------------------------------

    0.3) echo "Fitting isr*eff distributions..."
         ;;

    0.3.1) echo "Convert ROOT -- converting ROOT files..."
           cd scripts/ana
           ./convertROOT.sh round2
           ;;

    0.3.2) echo "Fit distributions -- isr*eff distributions..."
           ./fit_isr_eff.py 4380
           ./fit_isr_eff.py 4390
           ./fit_isr_eff.py 4400
           ./fit_isr_eff.py 4420
           ./fit_isr_eff.py 4440
           ./fit_isr_eff.py 4575
           ;;

    0.3.3) echo "Calculate numbers -- calculating systerm uncertainties..."
           ./format_xs.py
           ./cal_diff.py
           ;;

esac
