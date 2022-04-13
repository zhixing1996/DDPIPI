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
    PARAM_3=`echo "scale=4; $PARAM_3 / 1000" | bc -l`
    mkdir -p $WORKAREA/sigMC/X_3842/$PARAM_0
    cd $HOME/bes/DDPIPI/v0.2/python
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/*signal*.root
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/*raw*.root
    ROOT_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape
    FILE_PATH=/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sys_err/sigma_shape/rootfile
    mkdir -p $ROOT_PATH
    echo "Begining of $PARAM_0!"

    python get_info.py $FILE_PATH/sigMC_X_3842_$PARAM_0\.root $ROOT_PATH/sigMC_X_3842_$PARAM_0\_signal.root $PARAM_3 STDDmiss_signal
    echo "STDDmiss of $PARAM_0 is done!"

    echo "$PARAM_0 is done!"
done
