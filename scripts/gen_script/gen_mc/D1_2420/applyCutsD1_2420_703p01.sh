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
    PARAM_5=${arr[5]} # dst path
    WORKAREA=/besfs/users/$USER/bes/DDPIPI/v0.2
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    mkdir -p $WORKAREA/sigMC/D1_2420/$PARAM_0
    cd $HOME/bes/DDPIPI/v0.2/python
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/*before*.root
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/*after*.root
    ROOT_PATH=/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0

    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_before.root $PARAM_0 before raw_signal
    echo "STD signal of $PARAM_0 is done!"

    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_signal.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_before.root $PARAM_0 before STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_signal.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_after.root $PARAM_0 after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    rm -rf $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sideband_before.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow_before.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup_before.root
    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow_before.root $PARAM_0 before raw_sidebandlow
    python apply_cuts.py $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup_before.root $PARAM_0 before raw_sidebandup
    hadd $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sideband_before.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow_before.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup_before.root
    echo "raw sideband of $PARAM_0 is done!"

    echo "$PARAM_0 is done!"
done
