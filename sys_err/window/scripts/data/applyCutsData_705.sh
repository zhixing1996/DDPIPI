#!/bin/sh
cat Data_Base_705 | while read line
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
    mkdir -p /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/sys_err/window
    cd $HOME/bes/DDPIPI/v0.2/sys_err/window
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/sys_err/window/*before*.root
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/sys_err/window/*after*.root
    ROOT_PATH_RAW=/besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    ROOT_PATH=/besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/sys_err/window
    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $ROOT_PATH_RAW/data_$PARAM_0\_raw.root $ROOT_PATH/data_$PARAM_0\_raw_before.root $PARAM_0 before raw_signal
    echo "STD signal of $PARAM_0 is done!"

    python apply_cuts.py $ROOT_PATH_RAW/data_$PARAM_0\_signal.root $ROOT_PATH/data_$PARAM_0\_after.root $PARAM_0 after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    rm -rf $ROOT_PATH/data_$PARAM_0\_sideband.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_sidebandlow_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_sidebandup_after.root
    python apply_cuts.py $ROOT_PATH_RAW/data_$PARAM_0\_sidebandlow.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_sidebandlow_after.root $PARAM_0 after STDDmiss_sidebandlow
    python apply_cuts.py $ROOT_PATH_RAW/data_$PARAM_0\_sidebandup.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_sidebandup_after.root $PARAM_0 after STDDmiss_sidebandup
    hadd $ROOT_PATH/data_$PARAM_0\_sideband.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_sidebandlow_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_sidebandup_after.root
    echo "STDDmiss sideband of $PARAM_0 is done!"

    rm -rf $ROOT_PATH/data_$PARAM_0\_raw_sideband_before.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_before.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_before.root
    python apply_cuts.py $ROOT_PATH_RAW/data_$PARAM_0\_raw_sidebandlow.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_before.root $PARAM_0 before raw_sidebandlow
    python apply_cuts.py $ROOT_PATH_RAW/data_$PARAM_0\_raw_sidebandup.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_before.root $PARAM_0 before raw_sidebandup
    hadd $ROOT_PATH/data_$PARAM_0\_raw_sideband_before.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_before.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_before.root
    echo "STD sideband of $PARAM_0 is done!"

    echo "$PARAM_0 is done!"
done
