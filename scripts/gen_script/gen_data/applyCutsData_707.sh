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
    cd $HOME/bes/DDPIPI/v0.2/python
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/*before*.root
    rm -rf /besfs5/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/*after*.root
    ROOT_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    SOURCE_PATH=/besfs5/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_raw.root $ROOT_PATH/data_$PARAM_0\_raw_before.root $PARAM_0 before raw_signal
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_raw.root $ROOT_PATH/data_$PARAM_0\_rm_Dpipi_signal.root $PARAM_0 after rm_Dpipi_signal
    echo "STD signal of $PARAM_0 is done! (before bkg suppress)"

    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_raw.root $ROOT_PATH/data_$PARAM_0\_raw_after.root $PARAM_0 after raw_signal
    echo "STD signal of $PARAM_0 is done! (after bkg suppress)"

    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_signal.root $ROOT_PATH/data_$PARAM_0\_before.root $PARAM_0 before STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done! (before bkg suppress)"

    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_signal.root $ROOT_PATH/data_$PARAM_0\_after.root $PARAM_0 after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done! (after bkg suppress)"

    rm -rf $ROOT_PATH/data_$PARAM_0\_side1.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_low_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_up_before.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side1_low.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_low_before.root $PARAM_0 before STDDmiss_side1_low
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side1_up.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_up_before.root $PARAM_0 before STDDmiss_side1_up
    hadd $ROOT_PATH/data_$PARAM_0\_side1_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_low_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_up_before.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side2.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_low_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_up_before.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side2_low.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_low_before.root $PARAM_0 before STDDmiss_side2_low
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side2_up.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_up_before.root $PARAM_0 before STDDmiss_side2_up
    hadd $ROOT_PATH/data_$PARAM_0\_side2_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_low_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_up_before.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side3.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_low_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_up_before.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side3_low.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_low_before.root $PARAM_0 before STDDmiss_side3_low
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side3_up.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_up_before.root $PARAM_0 before STDDmiss_side3_up
    hadd $ROOT_PATH/data_$PARAM_0\_side3_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_low_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_up_before.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side4.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_low_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_up_before.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side4_low.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_low_before.root $PARAM_0 before STDDmiss_side4_low
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side4_up.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_up_before.root $PARAM_0 before STDDmiss_side4_up
    hadd $ROOT_PATH/data_$PARAM_0\_side4_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_low_before.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_up_before.root
    echo "STDDmiss sideband of $PARAM_0 is done! (before bkg suppress)"

    rm -rf $ROOT_PATH/data_$PARAM_0\_side1.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_low_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_up_after.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side1_low.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_low_after.root $PARAM_0 after STDDmiss_side1_low
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side1_up.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_up_after.root $PARAM_0 after STDDmiss_side1_up
    hadd $ROOT_PATH/data_$PARAM_0\_side1_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_low_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side1_up_after.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side2.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_low_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_up_after.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side2_low.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_low_after.root $PARAM_0 after STDDmiss_side2_low
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side2_up.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_up_after.root $PARAM_0 after STDDmiss_side2_up
    hadd $ROOT_PATH/data_$PARAM_0\_side2_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_low_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side2_up_after.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side3.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_low_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_up_after.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side3_low.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_low_after.root $PARAM_0 after STDDmiss_side3_low
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side3_up.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_up_after.root $PARAM_0 after STDDmiss_side3_up
    hadd $ROOT_PATH/data_$PARAM_0\_side3_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_low_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side3_up_after.root
    rm -rf $ROOT_PATH/data_$PARAM_0\_side4.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_low_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_up_after.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side4_low.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_low_after.root $PARAM_0 after STDDmiss_side4_low
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_side4_up.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_up_after.root $PARAM_0 after STDDmiss_side4_up
    hadd $ROOT_PATH/data_$PARAM_0\_side4_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_low_after.root $ROOT_PATH/data_$PARAM_0\_STDDmiss_side4_up_after.root
    echo "STDDmiss sideband of $PARAM_0 is done! (after bkg suppress)"

    rm -rf $ROOT_PATH/data_$PARAM_0\_raw_sideband_before.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_before.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_before.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_raw_sidebandlow.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_before.root $PARAM_0 before raw_sidebandlow
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_raw_sidebandup.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_before.root $PARAM_0 before raw_sidebandup
    hadd $ROOT_PATH/data_$PARAM_0\_raw_sideband_before.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_before.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_before.root
    echo "raw sideband of $PARAM_0 is done! (before bkg suppress)"

    rm -rf $ROOT_PATH/data_$PARAM_0\_raw_sideband_after.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_after.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_after.root
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_raw_sidebandlow.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_after.root $PARAM_0 after raw_sidebandlow
    python apply_cuts.py $SOURCE_PATH/data_$PARAM_0\_raw_sidebandup.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_after.root $PARAM_0 after raw_sidebandup
    hadd $ROOT_PATH/data_$PARAM_0\_raw_sideband_after.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandlow_after.root $ROOT_PATH/data_$PARAM_0\_raw_sidebandup_after.root
    echo "raw sideband of $PARAM_0 is done! (after bkg suppress)"

    rm -rf $ROOT_PATH/*side1_low* $ROOT_PATH/*side1_up*
    rm -rf $ROOT_PATH/*side2_low* $ROOT_PATH/*side2_up*
    rm -rf $ROOT_PATH/*side3_low* $ROOT_PATH/*side3_up*
    rm -rf $ROOT_PATH/*side4_low* $ROOT_PATH/*side4_up*

    echo "$PARAM_0 is done!"
done
