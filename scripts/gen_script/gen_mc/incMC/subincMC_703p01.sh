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
    WORKAREA=$HOME"/bes/DDPIPI/v0.2"
    mkdir -p $WORKAREA/scripts/incMC/$PARAM_1/$PARAM_0
    cd $WORKAREA/scripts/incMC/$PARAM_1/$PARAM_0
    if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/$PARAM_1/$PARAM_0/jobs_inc" ]; then
        mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/$PARAM_1/$PARAM_0/jobs_inc
        ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/incMC/$PARAM_1/$PARAM_0/jobs_inc ./jobs_inc
    fi
    cd jobs_inc
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/$PARAM_1/$PARAM_0/rootfile
    rm -rf incMC_inclusive_$PARAM_1\_$PARAM_0*txt
    cp -rf $HOME/bes/DDPIPI/v0.2/python/make_mc.py ./
    cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
    ./make_mc.py $PARAM_3 incMC inclusive $PARAM_1 $PARAM_1 $PARAM_0 $PARAM_2 10
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subAna.sh ./
    rm -rf *boss*
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/incMC/$PARAM_1/$PARAM_0/rootfile/*root
    ./subAna.sh incMC_inclusive_$PARAM_1\_$PARAM_0
done
