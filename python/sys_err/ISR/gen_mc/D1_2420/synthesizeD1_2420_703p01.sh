#!/bin/sh
cat D1_2420_Base_703p01 | while read line
do
    str=$line
    OLD_IFS=$IFS
    IFS=";"
    arr=($str)
    IFS="$OLD_IFS"
    PARAM_0=${arr[0]} # int energy point
    PARAM_1=${arr[1]} # ruNo low
    PARAM_2=${arr[2]} # ruNo up
    PARAM_3=${arr[3]} # float energy poit
    PARAM_4=${arr[4]} # luminosity
    # mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/ISR/rootfile
    # cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/ISR/rootfile
    mkdir -p /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/ISR/rootfile
    cd /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/ISR/rootfile
    rm -rf sigMC_D1_2420_$PARAM_0\.root
    hadd sigMC_D1_2420_$PARAM_0\.root *.root
    cd ../../../..
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        dir=$(echo $PARAM_0 | sed 's/-1//g')/sys_err/ISR/rootfile
        mkdir -p $dir
        # mv /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/ISR/rootfile/sigMC_D1_2420_$PARAM_0\.root ./$dir
        mv /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/ISR/rootfile/sigMC_D1_2420_$PARAM_0\.root ./$dir
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        dir=$(echo $PARAM_0 | sed 's/-2//g')/sys_err/ISR/rootfile
        mkdir -p $dir
        # mv /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/ISR/rootfile/sigMC_D1_2420_$PARAM_0\.root ./$dir
        mv /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/ISR/rootfile/sigMC_D1_2420_$PARAM_0\.root ./$dir
        cd $dir
        VAR=$(echo $PARAM_0 | sed 's/-2//g')
        rm -rf sigMC_D1_2420_$VAR\.root
        hadd sigMC_D1_2420_$VAR\.root sigMC_D1_2420_$VAR-1.root sigMC_D1_2420_$VAR-2.root
    fi
done
