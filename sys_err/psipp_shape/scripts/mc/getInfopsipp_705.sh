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
    PARAM_3=${arr[3]} # float energy poit
    PARAM_4=${arr[4]} # luminosity
    PARAM_5=${arr[5]} # dst path
    WORKAREA=/besfs/users/$USER/bes/DDPIPI/v0.2
    PARAM_3=`echo "scale=4; $PARAM_3 / 1000" | bc -l`
    mkdir -p $WORKAREA/sigMC/psipp/$PARAM_0/sys_err/psipp_shape
    cd $HOME/bes/DDPIPI/v0.2/sys_err/psipp_shape
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/*signal*.root
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/*raw*.root
    echo "Begining of $PARAM_0!"
    python get_info.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/rootfile/sigMC_psipp_$PARAM_0\.root /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/sigMC_psipp_$PARAM_0\_signal.root $PARAM_3 STDDmiss_signal
    echo "STDDmiss of $PARAM_0 is done!"
    python get_info.py /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/rootfile/sigMC_psipp_$PARAM_0\.root /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/sigMC_psipp_$PARAM_0\_raw.root $PARAM_3 raw_signal
    echo "STD of $PARAM_0 is done!"
    echo "$PARAM_0 is done!"
done
