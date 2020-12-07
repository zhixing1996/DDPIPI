#!/bin/sh
cat DDPIPI_Base_705 | while read line
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
    mkdir -p $WORKAREA/sigMC/DDPIPI/$PARAM_0
    cd $HOME/bes/DDPIPI/v0.2/python
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/*before*.root
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/*after*.root
    ROOT_PATH=/besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0

    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $ROOT_PATH/sigMC_D_D_PI_PI_$PARAM_0\_raw.root $ROOT_PATH/sigMC_D_D_PI_PI_$PARAM_0\_raw_before.root $PARAM_0 before raw_signal
    echo "STD signal of $PARAM_0 is done!"

    python apply_cuts.py $ROOT_PATH/sigMC_D_D_PI_PI_$PARAM_0\_signal.root $ROOT_PATH/sigMC_D_D_PI_PI_$PARAM_0\_before.root $PARAM_0 before STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    python apply_cuts.py $ROOT_PATH/sigMC_D_D_PI_PI_$PARAM_0\_signal.root $ROOT_PATH/sigMC_D_D_PI_PI_$PARAM_0\_after.root $PARAM_0 after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    echo "$PARAM_0 is done!"
done
