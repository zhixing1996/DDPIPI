#!/bin/sh
cat psipp_Base_705 | while read line
do
    str=$line
    OLD_IFS=$IFS
    IFS=";"
    arr=($str)
    IFS="$OLD_IFS"
    PARAM_0=${arr[0]} # int energy point
    PARAM_1=${arr[1]} # ruNo low
    PARAM_2=${arr[2]} # ruNo up
    PARAM_3=${arr[3]} # float energy point
    PARAM_4=${arr[4]} # luminosity
    WORKAREA=$HOME"/bes/DDPIPI/v0.2"
    mkdir -p $WORKAREA/scripts/sigMC/psipp/$PARAM_0/sys_err/BW
    cd $WORKAREA/scripts/sigMC/psipp/$PARAM_0/sys_err/BW
    if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/BW/jobs_sig" ]; then
        mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/BW/jobs_sig
        ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/BW/jobs_sig ./jobs_sig
    fi
    cd jobs_sig
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/BW/rootfile
    rm -rf sigMC_psipp_PI_PI_VSS_$PARAM_0*txt
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/BW/make_mc.py ./
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/BW/tools.py ./
    ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/BW/dst sigMC psipp_PI_PI VSS psipp $PARAM_0 $PARAM_3 2
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/BW/scripts/mc/psipp/subAna.sh ./
    rm -rf *boss*
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/BW/rootfile/*root
    ./subAna.sh sigMC_psipp_PI_PI_VSS_$PARAM_0
done
