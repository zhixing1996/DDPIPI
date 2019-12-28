#!/bin/sh
cat Data_Base_665p01 | while read line
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
    mkdir -p $WORKAREA/data/$PARAM_0
    cd $HOME/bes/DDPIPI/v0.2/python
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/*before*.root
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/*after*.root
    PARAM=$(echo $PARAM_0 | sed 's/-Rscan//g')
    echo "Begininning of $PARAM_0!"
    python apply_cuts.py /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_raw.root /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_raw_before.root $PARAM before raw_signal
    echo "STD signal of $PARAM_0 is done!"
    python apply_cuts.py /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_signal.root /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_after.root $PARAM after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"
    ROOT_PATH=/besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    rm -rf $ROOT_PATH/data_$PARAM\_raw_sideband_before.root $ROOT_PATH/data_$PARAM\_raw_sidebandlow_before.root $ROOT_PATH/data_$PARAM\_raw_sidebandup_before.root
    python apply_cuts.py /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_raw_sidebandlow.root /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_raw_sidebandlow_before.root $PARAM before raw_sidebandlow
    python apply_cuts.py /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_raw_sidebandup.root /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_raw_sidebandup_before.root $PARAM before raw_sidebandup
    hadd $ROOT_PATH/data_$PARAM\_raw_sideband_before.root $ROOT_PATH/data_$PARAM\_raw_sidebandlow_before.root $ROOT_PATH/data_$PARAM\_raw_sidebandup_before.root
    echo "STD sideband of $PARAM_0 is done!"
    ROOT_PATH=/besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    rm -rf $ROOT_PATH/data_$PARAM\_sideband.root $ROOT_PATH/data_$PARAM\_STDDmiss_sidebandlow_after.root $ROOT_PATH/data_$PARAM\_STDDmiss_sidebandup_after.root
    python apply_cuts.py /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_sidebandlow.root /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_STDDmiss_sidebandlow_after.root $PARAM after STDDmiss_sidebandlow
    python apply_cuts.py /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_sidebandup.root /besfs/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/data_$PARAM\_STDDmiss_sidebandup_after.root $PARAM after STDDmiss_sidebandup
    hadd $ROOT_PATH/data_$PARAM\_sideband.root $ROOT_PATH/data_$PARAM\_STDDmiss_sidebandlow_after.root $ROOT_PATH/data_$PARAM\_STDDmiss_sidebandup_after.root
    echo "STDDmiss sideband of $PARAM_0 is done!"
    echo "$PARAM_0 is done!"
done
