#!/bin/sh
cat Data_Base_707 | while read line
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
    WORKAREA=/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    PARAM_3=`echo "scale=4; $PARAM_3 / 1000" | bc -l`
    mkdir -p $WORKAREA/data/$PARAM_0
    cd $HOME/bes/DDPIPI/v0.2/python
    FILE_PATH=/scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    ROOT_PATH=/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/data/$PARAM_0

    echo "Begininning of $PARAM_0!"

    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_signal.root $PARAM_3 STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_raw.root $PARAM_3 raw_signal
    echo "STD signal of $PARAM_0 is done!"

    ROOT_PATH=/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    rm -rf $ROOT_PATH/data_$PARAM_0\_side1_low.root $ROOT_PATH/data_$PARAM_0\_side1_up.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side2_low.root $ROOT_PATH/data_$PARAM_0\_side2_up.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side3_low.root $ROOT_PATH/data_$PARAM_0\_side3_up.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side4_low.root $ROOT_PATH/data_$PARAM_0\_side4_up.root
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_side1_low.root $PARAM_3 STDDmiss_side1_low
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_side1_up.root $PARAM_3 STDDmiss_side1_up
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_side2_low.root $PARAM_3 STDDmiss_side2_low
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_side2_up.root $PARAM_3 STDDmiss_side2_up
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_side3_low.root $PARAM_3 STDDmiss_side3_low
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_side3_up.root $PARAM_3 STDDmiss_side3_up
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_side4_low.root $PARAM_3 STDDmiss_side4_low
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_side4_up.root $PARAM_3 STDDmiss_side4_up
    echo "STDDmiss sideband of $PARAM_0 is done!"

    ROOT_PATH=/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    rm -rf $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup.root
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow.root $PARAM_3 raw_sidebandlow
    python get_info.py $FILE_PATH/data_$PARAM_0\.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup.root $PARAM_3 raw_sidebandup
    echo "STD sideband of $PARAM_0 is done!"

    echo "$PARAM_0 is done!"
done
