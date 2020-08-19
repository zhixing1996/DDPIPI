#!/bin/sh
GEN=$1
cat DDPIPI_Base_703p01 | while read line
do
    str=$line
    OLD_IFS=$IFS
    IFS=";"
    arr=($str)
    IFS="$OLD_IFS"
    PARAM_0=${arr[0]} # int energy point
    PARAM_1=${arr[1]} # ruNo low
    PARAM_2=${arr[2]} # ruNo up
    PARAM_3=`echo "scale=4; ${arr[3]} / 1000" | bc -l` # float energy poit
    PARAM_4=${arr[4]} # luminosity
    WORKAREA=$HOME/bes/DDPIPI/v0.2
    mkdir -p $WORKAREA/scripts/sigMC/DDPIPI/$PARAM_0
    cd $WORKAREA/scripts/sigMC/DDPIPI/$PARAM_0
    if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/jobs_sig" ]; then
        mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/jobs_sig
        ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/jobs_sig ./jobs_sig
    fi
    cd jobs_sig
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/rtraw
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/dst
    rm -rf jobOptions*txt
    rm -rf subSimRec_*.sh
    rm -rf xs_user.txt
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/DDPIPI/jobOptions_sim_sig_D_D_PI_PI_tempE_703p01_${GEN}.sh ./jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/decay/${GEN}_D_D_PI_PI.dec .
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/DDPIPI/xs_user.txt ./xs_user.txt
    sed -i "s/TEMP_0/$PARAM_0/g" jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    sed -i "s/TEMP_1/$PARAM_1/g" jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    sed -i "s/TEMP_2/$PARAM_2/g" jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    sed -i "s/ECMS/$PARAM_3/g" ${GEN}_D_D_PI_PI.dec
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/rtraw/*.rtraw
    sh jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh 0 9 5000
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/DDPIPI/jobOptions_rec_sig_D_D_PI_PI_tempE_703p01.sh ./jobOptions_rec_sig_D_D_PI_PI_$PARAM_0\.sh
    sed -i "s/TEMP_0/$PARAM_0/g" jobOptions_rec_sig_D_D_PI_PI_$PARAM_0\.sh
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/dst/*.dst
    sh jobOptions_rec_sig_D_D_PI_PI_$PARAM_0\.sh 0 9
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
    sh subSimRec.sh jobOptions_sim_sig_D_D_PI_PI_$PARAM_0 jobOptions_rec_sig_D_D_PI_PI_$PARAM_0 subSimRec_DDPIPI_$PARAM_0\_703p01 0 9
done
