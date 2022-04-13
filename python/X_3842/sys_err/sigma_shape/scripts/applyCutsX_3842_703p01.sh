#!/bin/sh
cat X_3842_Base_703p01 | while read line
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
    cd $HOME/bes/DDPIPI/v0.2/python
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/*before*.root
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/*after*.root
    ROOT_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape

    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $ROOT_PATH/sigMC_X_3842_$PARAM_0\_signal.root $ROOT_PATH/sigMC_X_3842_$PARAM_0\_after.root $PARAM_0 after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    echo "$PARAM_0 is done!"
done
