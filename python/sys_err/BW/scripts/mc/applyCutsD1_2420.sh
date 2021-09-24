#!/bin/sh
cat D1_2420_Base | while read line
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
    WORKAREA=/besfs5/users/$USER/bes/DDPIPI/v0.2
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    mkdir -p $WORKAREA/sigMC/D1_2420/$PARAM_0/sys_err/BW
    cd $HOME/bes/DDPIPI/v0.2/python/sys_err/BW
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/BW/*before*.root
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/BW/*after*.root
    ROOT_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/BW

    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_after.root $PARAM_0 after raw_signal
    echo "STD signal of $PARAM_0 is done!"

    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_signal.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_after.root $PARAM_0 after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    rm -rf $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sideband_after.root
    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow_after.root $PARAM_0 after raw_sidebandlow
    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup_after.root $PARAM_0 after raw_sidebandup
    hadd $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sideband_after.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow_after.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup_after.root
    echo "raw sideband of $PARAM_0 is done! (after bkg suppress)"

    rm -rf $ROOT_PATH/*low* $ROOT_PATH/*up*
    echo "$PARAM_0 is done!"
done
