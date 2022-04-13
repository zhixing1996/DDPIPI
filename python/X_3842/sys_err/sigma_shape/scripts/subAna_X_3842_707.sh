#!/bin/sh
cat X_3842_Base_707 | while read line
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
    mkdir -p $WORKAREA/scripts/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape
    cd $WORKAREA/scripts/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape
    if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/jobs_sig" ]; then
        mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/jobs_sig
        ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/jobs_sig ./jobs_sig
    fi
    cd jobs_sig
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/rootfile
    rm -rf sigMC_Sigma_X_3842_VSS_$PARAM_0*txt
    cp -rf $HOME/bes/DDPIPI/v0.2/python/X_3842/sys_err/sigma_shape/make_mc.py ./
    cp -rf $HOME/bes/DDPIPI/v0.2/python/X_3842/sys_err/sigma_shape/tools.py ./
    ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/dst sigMC Sigma_X_3842 VSS X_3842 $PARAM_0 $PARAM_3 2
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
    rm -rf *boss*
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/rootfile/*root
    ./subAna.sh sigMC_Sigma_X_3842_VSS_$PARAM_0
done
