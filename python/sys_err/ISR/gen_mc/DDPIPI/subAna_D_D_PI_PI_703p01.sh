#!/bin/sh
cat DDPIPI_Base_703p01 | while read line
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
    # mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/jobs_sig
    # cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/jobs_sig
    # mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/rootfile
    mkdir -p /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/jobs_sig
    cd /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/jobs_sig
    mkdir -p /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/rootfile
    rm -rf sigMC_D_D_PI_PI_PHSP_$PARAM_0*txt
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/ISR/make_mc.py ./
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/ISR/tools.py ./
    # ./make_mc.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/dst sigMC D_D_PI_PI PHSP DDPIPI $PARAM_0 $PARAM_3 2
    ./make_mc.py /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/dst sigMC D_D_PI_PI PHSP DDPIPI $PARAM_0 $PARAM_3 2
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/ISR/gen_mc/subAna.sh ./
    rm -rf *boss*
    # rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/rootfile/*root
    rm -rf /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/rootfile/*root
    ./subAna.sh sigMC_D_D_PI_PI_PHSP_$PARAM_0
done
