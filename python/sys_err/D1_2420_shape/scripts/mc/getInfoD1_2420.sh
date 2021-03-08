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
    PARAM_3=`echo "scale=4; $PARAM_3 / 1000" | bc -l`
    WORKAREA=/besfs5/users/$USER/bes/DDPIPI/v0.2
    mkdir -p $WORKAREA/sigMC/D1_2420/$PARAM_0/sys_err/D1_2420_shape
    cd $HOME/bes/DDPIPI/v0.2/python/sys_err/D1_2420_shape
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/D1_2420_shape/*signal*.root
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/D1_2420_shape/*raw*.root
    ROOT_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/D1_2420_shape
    FILE_PATH=/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/sys_err/D1_2420_shape/rootfile
    echo "Begining of $PARAM_0!"

    python get_info.py $FILE_PATH/sigMC_D1_2420_$PARAM_0\.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_signal.root $PARAM_3 STDDmiss_signal
    echo "STDDmiss of $PARAM_0 is done!"

    python get_info.py $FILE_PATH/sigMC_D1_2420_$PARAM_0\.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw.root $PARAM_3 raw_signal
    echo "STD of $PARAM_0 is done!"

    rm -rf $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup.root
    python get_info.py $FILE_PATH/sigMC_D1_2420_$PARAM_0\.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandlow.root $PARAM_3 raw_sidebandlow
    python get_info.py $FILE_PATH/sigMC_D1_2420_$PARAM_0\.root $ROOT_PATH/sigMC_D1_2420_$PARAM_0\_raw_sidebandup.root $PARAM_3 raw_sidebandup
    echo "STD sideband of $PARAM_0 is done!"

    echo "$PARAM_0 is done!"
done
