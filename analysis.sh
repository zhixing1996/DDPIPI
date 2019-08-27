#!/usr/bin/env bash

# Main driver to execute and submit analysis jobs
# Author Maoqiang Jing <$USER@ihep.ac.cn>
# Created [2019-08-21 Wed 10:00]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to execute and submit analysis jobs\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Pretreatment of data and MC samples]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Get samples -- synthesize root files"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Draw figures -- plot chi2 of kinematic fit of single tagged D"
    printf "\n\t%-9s  %-40s\n" "0.1.3" "Get samples -- apply cuts"

    printf "\n\t%-9s  %-40s\n" "0.2"   "[Signal and background study]"
    printf "\n\t%-9s  %-40s\n" "0.2.1" "Draw figures -- draw recoiling mass of Dpipi"
    printf "\n\t%-9s  %-40s\n" "0.2.2" "Get samples -- divide samples into rm_Dpipi signal region and sideband region"
    printf "\n\t%-9s  %-40s\n" "0.2.3" "Draw figures -- draw recoiling mass of D"
    printf "\n\t%-9s  %-40s\n" "0.2.4" "Draw figures -- background study: draw recoiling mass of D in inclusive MC samples"
    printf "\n\t%-9s  %-40s\n" "0.2.5" "Draw figures -- signal study: draw recoiling mass of D in signal MC samples"
    printf "\n\t%-9s  %-40s\n" "0.2.6" "Draw figures -- signal study: draw recoiling mass of D or mass of Dpipi in signal MC samples"
    printf "\n\t%-9s  %-40s\n" "0.2.7" "Draw figures -- signal study: draw recoiling mass of D vs mass of Dpipi in signal MC samples"

    printf "\n\t%-9s  %-40s\n" "0.3"   "[Simultanous fit]"
    printf "\n\t%-9s  %-40s\n" "0.3.1" "Extract shapes -- get signal shapes"
    printf "\n\t%-9s  %-40s\n" "0.3.2" "Get samples -- apply cuts on control samples"
    printf "\n\t%-9s  %-40s\n" "0.3.3" "Fit distributions -- fit to control samples to get resolutions"
    printf "\n\t%-9s  %-40s\n" "0.3.4" "Extract shapes -- convolve signal shapes with gaussian"
    printf "\n\t%-9s  %-40s\n" "0.3.5" "Extract shapes -- get background shapes"

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
         echo "--> Event Number: 1,000,000(signal MC,PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89^{-1}(4420MeV), 566.93^{-1}(4600MeV)"
         ;;

    0.1.1) echo "Get samples -- synthesizing root files..."
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4360/rootfile
           rm -rf sigMC_D1_2420_4360.root
           hadd sigMC_D1_2420_4360.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4420/rootfile
           rm -rf sigMC_D1_2420_4420.root
           hadd sigMC_D1_2420_4420.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/D1_2420/4600/rootfile
           rm -rf sigMC_D1_2420_4600.root
           hadd sigMC_D1_2420_4600.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4360/rootfile
           rm -rf sigMC_psi_3770_4360.root
           hadd sigMC_psi_3770_4360.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4420/rootfile
           rm -rf sigMC_psi_3770_4420.root
           hadd sigMC_psi_3770_4420.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/sigMC/psi_3770/4600/rootfile
           rm -rf sigMC_psi_3770_4600.root
           hadd sigMC_psi_3770_4600.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4360/rootfile
           rm -rf bkgMC_PHSP_4360.root
           hadd bkgMC_PHSP_4360.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4420/rootfile
           rm -rf bkgMC_PHSP_4420.root
           hadd bkgMC_PHSP_4420.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/bkgMC/PHSP/4600/rootfile
           rm -rf bkgMC_PHSP_4600.root
           hadd bkgMC_PHSP_4600.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/incMC/DD/4360/rootfile
           rm -rf incMC_DD_4360.root
           hadd incMC_DD_4360.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/incMC/DD/4420/rootfile
           rm -rf incMC_DD_4420.root
           hadd incMC_DD_4420.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/incMC/DD/4600/rootfile
           rm -rf incMC_DD_4600.root
           hadd incMC_DD_4600.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/incMC/qq/4360/rootfile
           rm -rf incMC_qq_4360.root
           hadd incMC_qq_4360.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/incMC/qq/4420/rootfile
           rm -rf incMC_qq_4420.root
           hadd incMC_qq_4420.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/incMC/qq/4600/rootfile
           rm -rf incMC_qq_4600.root
           hadd incMC_qq_4600.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/incMC/LL/4600/rootfile
           rm -rf incMC_LL_4600.root
           hadd incMC_LL_4600.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/data/4360
           rm -rf data_4360.root
           hadd data_4360.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/data/4420
           rm -rf data_4420.root
           hadd data_4420_temp1.root data31*.root
           hadd data_4420_temp2.root data36*.root
           hadd data_4420_temp3.root data37*.root
           hadd data_4420_temp4.root data38*.root
           hadd data_4420.root data_4420_temp*.root
           rm -rf data_4420_temp*.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/data/4600
           rm -rf data_4600.root
           hadd data_4600.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/controlMC/DD/4360/rootfile
           rm -rf controlMC_DD_4360.root
           hadd controlMC_DD_4360.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/controlMC/DD/4420/rootfile
           rm -rf controlMC_DD_4420.root
           hadd controlMC_DD_4420.root *.root
           cd /scratchfs/bes/$USER/bes/DDPIPI/v0.1/controlMC/DD/4600/rootfile
           rm -rf controlMC_DD_4600.root
           hadd controlMC_DD_4600.root *.root
           ;;

    0.1.2) echo "Draw figures -- plotting chi2 of kinematic fit of single tagged D..."
           cd python
           python plot_chi2_DKF.py
           ;;

    0.1.3) echo "Get samples -- applying cuts..."
           mkdir -p scripts/ana/sel
           cd scripts/ana/sel
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/sel/jobs_ana" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/sel/jobs_ana
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/sel/jobs_ana ./jobs_ana
           fi
           cd jobs_ana
           rm -rf jobs.out
           rm -rf jobs.err
           mkdir jobs.out
           mkdir jobs.err
           cp $HOME/bes/DDPIPI/v0.1/jobs/apply_cuts . 
           hep_sub -g physics apply_cuts -o jobs.out -e jobs.err
           ;;

    # --------------------------------
    #  0.2 Signal and background study
    # --------------------------------

    0.2) echo "Signal and background study..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC,PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89^{-1}(4420MeV), 566.93^{-1}(4600MeV)"
         ;;

    0.2.1) echo "Draw figures -- drawing recoiling mass of Dpipi..."
           cd python
           python plot_rm_Dpipi.py
           ;;

    0.2.2) echo "Get samples -- dividing samples into rm_Dpipi signal and sideband region..."
           cd python
           python divide_samples.py
           ;;

    0.2.3) echo "Draw figures -- drawing recoiling mass of D..."
           cd python
           python plot_rm_D.py
           ;;

    0.2.4) echo "Draw figures -- background study: drawing recoiling mass of D in inclusive MC samples..."
           cd python
           python plot_rm_D_incMC.py
           ;;

    0.2.5) echo "Draw figures -- signal study: drawing recoiling mass of D in signal MC samples..."
           cd python
           python plot_rm_D_sigMC.py
           ;;
    0.2.6) echo "Draw figures -- signal study: drawing recoiling mass of D or mass of Dpipi in signal MC samples..."
           cd python
           python plot_rm_D_or_m_Dpipi_sigMC.py
           ;;

    0.2.7) echo "Draw figures -- signal study: drawing recoiling mass of D vs mass of Dpipi in signal MC samples..."
           cd python
           python plot_rm_D_vs_m_Dpipi_sigMC.py
           ;;

    # --------------------
    #  0.3 Simultanous fit
    # --------------------

    0.3) echo "Simultanous fit..."
         echo "--> Samples: data, signal MC, PHSP MC, inclusive MC, control sample MC"
         echo "--> E_{CMS}: 4360MeV, 4420MeV, 460MeV"
         echo "--> Event Number: 1,000,000(signal MC,PHSP MC, inclusive MC)"
         echo "--> RunNo: 30616~31279(4360MeV), 31327~31390+36773~38140(4420MeV), 35227~36213(4600MeV)"
         echo "--> Luminosity: 539.84pb^{-1}(4360MeV), 44.67+1028.89^{-1}(4420MeV), 566.93^{-1}(4600MeV)"
         ;;

    0.3.1) echo "Extract shapes -- getting signal shapes..."
           mkdir -p scripts/ana/simu
           cd scripts/ana/simu
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana ./jobs_ana
           fi
           cd jobs_ana
           rm -rf jobs.out
           rm -rf jobs.err
           mkdir jobs.out
           mkdir jobs.err
           mkdir -p /besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360
           mkdir -p /besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420
           mkdir -p /besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600
           cp $HOME/bes/DDPIPI/v0.1/jobs/get_signal_shape_* . 
           hep_sub -g physics get_signal_shape_4360 -o jobs.out -e jobs.err
           hep_sub -g physics get_signal_shape_4420 -o jobs.out -e jobs.err
           hep_sub -g physics get_signal_shape_4600 -o jobs.out -e jobs.err
           ;;

    0.3.2) echo "Get samples -- applying cuts on control samples..."
           mkdir -p scripts/ana/simu
           cd scripts/ana/simu
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana ./jobs_ana
           fi
           cd jobs_ana
           rm -rf jobs.out
           rm -rf jobs.err
           mkdir jobs.out
           mkdir jobs.err
           cp -rf $HOME/bes/DDPIPI/v0.1/jobs/apply_cuts_control .
           hep_sub -g physics apply_cuts_control -o job.out -e job.err
           ;;

    0.3.3) echo "Fit distributions -- fitting to control samples to get resolutions..."
           cd $HOME/bes/DDPIPI/v0.1/simultanous/signalshape/4360
           root -l -q fit_rmD_4360.cxx > result.txt
           cd $HOME/bes/DDPIPI/v0.1/simultanous/signalshape/4420
           root -l -q fit_rmD_4420.cxx > result.txt
           cd $HOME/bes/DDPIPI/v0.1/simultanous/signalshape/4600
           root -l -q fit_rmD_4600.cxx > result.txt
           ;;

    0.3.4) echo "Extract shapes -- convolving signal shapes with gaussian..."
           mkdir -p scripts/ana/simu
           cd scripts/ana/simu
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana ./jobs_ana
           fi
           cd jobs_ana
           rm -rf jobs.out
           rm -rf jobs.err
           mkdir jobs.out
           mkdir jobs.err
           cp $HOME/bes/DDPIPI/v0.1/jobs/signal_shape_cov_gauss . 
           hep_sub -g physics signal_shape_cov_gauss -o jobs.out -e jobs.err
           ;;

    0.3.5) echo "Extract shapes -- getting background shapes..."
           mkdir -p scripts/ana/simu
           cd scripts/ana/simu
           if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana" ]; then
               mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana
               ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.1/run/ana/simu/jobs_ana ./jobs_ana
           fi
           cd jobs_ana
           rm -rf jobs.out
           rm -rf jobs.err
           mkdir jobs.out
           mkdir jobs.err
           cp $HOME/bes/DDPIPI/v0.1/jobs/get_background_shape . 
           hep_sub -g physics get_background_shape -o jobs.out -e jobs.err
           ;;

esac
