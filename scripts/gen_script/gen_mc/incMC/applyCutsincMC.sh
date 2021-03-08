#!/bin/sh
cat incMC_Base | while read line
do
    str=$line
    OLD_IFS=$IFS
    IFS=";"
    arr=($str)
    IFS="$OLD_IFS"
    PARAM_0=${arr[0]} # int energy point
    PARAM_1=${arr[1]} # inc MC type
    PARAM_2=${arr[2]} # float energy point
    PARAM_3=${arr[3]} # path
    WORKAREA=/besfs5/users/$USER/bes/DDPIPI/v0.2
    shortbar1="-1"
    shortbar2="-2"
    if [[ $PARAM_0 == *$shortbar1* ]]; then
        PARAM_0=$(echo $PARAM_0 | sed 's/-1//g')
    fi
    if [[ $PARAM_0 == *$shortbar2* ]]; then
        continue
    fi
    mkdir -p $WORKAREA/incMC/$PARAM_1/$PARAM_0
    cd $HOME/bes/DDPIPI/v0.2/python
    SOURCE_PATH=/scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/$PARAM_1/$PARAM_0/rootfile
    ROOT_PATH=/besfs5/users/$USER/bes/DDPIPI/v0.2/incMC/$PARAM_1/$PARAM_0

    echo "Begininning of $PARAM_0!"

    python apply_cuts.py $SOURCE_PATH/incMC_$PARAM_1\_$PARAM_0\_raw.root $ROOT_PATH/incMC_$PARAM_1\_$PARAM_0\_raw_before.root $PARAM_0 before raw_signal
    echo "STD signal of $PARAM_0 is done!"

    python apply_cuts.py $SOURCE_PATH/incMC_$PARAM_1\_$PARAM_0\_signal.root $ROOT_PATH/incMC_$PARAM_1\_$PARAM_0\_before.root $PARAM_0 before STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done! (before bkg suppress)"

    python apply_cuts.py $SOURCE_PATH/incMC_$PARAM_1\_$PARAM_0\_signal.root $ROOT_PATH/incMC_$PARAM_1\_$PARAM_0\_after.root $PARAM_0 after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"

    echo "$PARAM_0 is done!"
done
