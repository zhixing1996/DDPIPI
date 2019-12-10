#!/bin/sh
cat DataBase-703-1 | while read line
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
    WORKAREA=$HOME"/bes/DDPIPI/v0.2"
    mkdir -p $WORKAREA/scripts/data/$PARAM_0
    cd $WORKAREA/scripts/data/$PARAM_0
    if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/$PARAM_0/jobs_data" ]; then
        mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/$PARAM_0/jobs_data
        ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_data/data/$PARAM_0/jobs_data ./jobs_data
    fi
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0
    cd jobs_data
    rm -rf data*txt
    rm -rf *boss*
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/data/$PARAM_0/*root
    cp -rf $HOME/bes/DDPIPI/v0.2/python/make_data.py ./
    chmod u+x make_data.py
    cp -rf $HOME/bes/DDPIPI/v0.2/python/tools.py ./
    python make_data.py $PARAM_5 $PARAM_1 $PARAM_2 $PARAM_0
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_data/subAna.sh ./
    chmod u+x subAna.sh
    sh subAna.sh data
done
