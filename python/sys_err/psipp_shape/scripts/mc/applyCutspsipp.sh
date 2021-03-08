#!/bin/sh
cat ECMS_Base | while read line
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
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    WORKAREA=/besfs5/users/$USER/bes/DDPIPI/v0.2
    mkdir -p $WORKAREA/sigMC/psipp/$PARAM_0/sys_err/psipp_shape
    cd $HOME/bes/DDPIPI/v0.2/python/sys_err/psipp_shape
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/*before*.root
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape/*after*.root
    ROOT_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/psipp_shape

    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw.root $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_after.root $PARAM_0 after raw_signal
    echo "STD signal of $PARAM_0 is done!"

    python apply_cuts.py $ROOT_PATH/sigMC_psipp_$PARAM_0\_signal.root $ROOT_PATH/sigMC_psipp_$PARAM_0\_after.root $PARAM_0 after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    rm -rf $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_sideband_after.root
    python apply_cuts.py $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_sidebandlow.root $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_sidebandlow_after.root $PARAM_0 after raw_sidebandlow
    python apply_cuts.py $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_sidebandup.root $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_sidebandup_after.root $PARAM_0 after raw_sidebandup
    hadd $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_sideband_after.root $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_sidebandlow_after.root $ROOT_PATH/sigMC_psipp_$PARAM_0\_raw_sidebandup_after.root
    # rm -rf $ROOT_PATH/*low* $ROOT_PATH/*up*
    echo "raw sideband of $PARAM_0 is done! (after bkg suppress)"

    echo "$PARAM_0 is done!"
done
