#!/bin/sh
cat psipp_Base_703p01 | while read line
do
    str=$line
    OLD_IFS=$IFS
    IFS=";"
    arr=($str)
    IFS="$OLD_IFS"
    PARAM_0=${arr[0]} # int energy point
    PARAM_1=${arr[1]} # ruNo low
    PARAM_2=${arr[2]} # ruNo up
    PARAM_3=`echo "scale=4; ${arr[3]} / 1000" | bc -l` # float energy poit
    PARAM_4=${arr[4]} # luminosity
    WORKAREA=$HOME"/bes/DDPIPI/v0.2"
    mkdir -p $WORKAREA/scripts/sigMC/psipp/$PARAM_0/sys_err/psipp_shape
    cd $WORKAREA/scripts/sigMC/psipp/$PARAM_0/sys_err/psipp_shape
    if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/jobs_sig" ]; then
        mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/jobs_sig
        ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/jobs_sig ./jobs_sig
    fi
    cd jobs_sig
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/rootfile
    rm -rf sigMC_psipp_PI_PI_VSS_$PARAM_0*txt
    cp -rf $HOME/bes/DDPIPI/v0.2/sys_err/psipp_shape/make_mc.py ./
    cp -rf $HOME/bes/DDPIPI/v0.2/sys_err/psipp_shape/tools.py ./
    ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/dst sigMC psipp_PI_PI VSS psipp $PARAM_0 10
    cp -rf $HOME/bes/DDPIPI/v0.2/sys_err/psipp_shape/scripts/mc/psipp/subAna.sh ./
    rm -rf *boss*
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp/rootfile/*root
    ./subAna.sh sigMC_psipp_PI_PI_VSS_$PARAM_0
done
