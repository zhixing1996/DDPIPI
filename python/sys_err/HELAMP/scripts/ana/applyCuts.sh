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
    WORKAREA=/besfs5/users/$USER/bes/DDPIPI/v0.2
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    mkdir -p $WORKAREA/data/$PARAM_0
    cd $HOME/bes/DDPIPI/v0.2/python/sys_err/HELAMP
    DATA_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    D1_0_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420_001000/$PARAM_0
    D1_1_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420_100010/$PARAM_0
    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $DATA_PATH/data_$PARAM_0\_after.root $DATA_PATH/data_$PARAM_0\_after_angle.root
    python apply_cuts.py $D1_0_PATH/sigMC_D1_2420_$PARAM_0\_after.root $D1_0_PATH/sigMC_D1_2420_$PARAM_0\_after_angle.root
    python apply_cuts.py $D1_1_PATH/sigMC_D1_2420_$PARAM_0\_after.root $D1_1_PATH/sigMC_D1_2420_$PARAM_0\_after_angle.root

    echo "$PARAM_0 is done!"
done
