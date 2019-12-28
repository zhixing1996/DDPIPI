#!/bin/sh
cat ECMS_Base_703p01 | while read line
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
    threshold=4310
    if [[ $PARAM_0 -ge $threshold ]]; then
        echo "Begininning of $PARAM_0!"
        cd $HOME/bes/DDPIPI/v0.2/python
        python get_shape.py $PARAM_0 D1_2420_signal
        python get_shape.py $PARAM_0 D1_2420_sideband
        python get_shape.py $PARAM_0 D1_2420
        python get_shape.py $PARAM_0 D1_2420_conv
        echo "$PARAM_0 is done!"
    fi
done
