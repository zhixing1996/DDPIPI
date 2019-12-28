#!/bin/sh
cat X_3842_Base_665p01 | while read line
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
    ECMS=$(echo $PARAM_0 | sed 's/-Rscan//g')
    mkdir -p $WORKAREA/sigMC/X_3842/$PARAM_0
    cd $HOME/bes/DDPIPI/v0.2/python
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/*before*.root
    rm -rf /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/*after*.root
    echo "Begininning of $PARAM_0!"
    python apply_cuts.py /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sigMC_X_3842_$PARAM_0\_raw.root /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sigMC_X_3842_$PARAM_0\_raw_before.root $ECMS before raw_signal
    echo "STD signal of $PARAM_0 is done!"
    python apply_cuts.py /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sigMC_X_3842_$PARAM_0\_signal.root /besfs/users/$USER/bes/DDPIPI/v0.2/sigMC/X_3842/$PARAM_0/sigMC_X_3842_$PARAM_0\_after.root $ECMS after STDDmiss_signal
    echo "STDDmiss signal of $PARAM_0 is done!"
    echo "$PARAM_0 is done!"
done
