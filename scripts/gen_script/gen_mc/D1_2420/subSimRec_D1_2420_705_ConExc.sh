#!/bin/sh
GEN=$1
cat D1_2420_Base_705 | while read line
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
    mkdir -p $WORKAREA/scripts/sigMC/D1_2420/$PARAM_0
    cd $WORKAREA/scripts/sigMC/D1_2420/$PARAM_0
    if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/$PARAM_0/jobs_sig" ]; then
        mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/$PARAM_0/jobs_sig
        ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/D1_2420/$PARAM_0/jobs_sig ./jobs_sig
    fi
    cd jobs_sig
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/rtraw
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/dst
    rm -rf jobOptions*txt
    rm -rf subSimRec_*.sh
    rm -rf xs_user.txt
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/D1_2420/jobOptions_sim_sig_D1_2420_D_tempE_705_${GEN}.sh ./jobOptions_sim_sig_D1_2420_D_$PARAM_0\.sh
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/decay/${GEN}_D1_2420_D.dec .
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/D1_2420/xs_user.txt ./xs_user.txt
    sed -i "s/TEMP_0/$PARAM_0/g" jobOptions_sim_sig_D1_2420_D_$PARAM_0\.sh
    sed -i "s/TEMP_1/$PARAM_1/g" jobOptions_sim_sig_D1_2420_D_$PARAM_0\.sh
    sed -i "s/TEMP_2/$PARAM_2/g" jobOptions_sim_sig_D1_2420_D_$PARAM_0\.sh
    sed -i "s/ECMS/$PARAM_3/g" ${GEN}_D1_2420_D.dec
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/rtraw/*.rtraw
    sh jobOptions_sim_sig_D1_2420_D_$PARAM_0\.sh 0 9 5000
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/D1_2420/jobOptions_rec_sig_D1_2420_D_tempE_705.sh ./jobOptions_rec_sig_D1_2420_D_$PARAM_0\.sh
    sed -i "s/TEMP_0/$PARAM_0/g" jobOptions_rec_sig_D1_2420_D_$PARAM_0\.sh
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/D1_2420/$PARAM_0/dst/*.dst
    sh jobOptions_rec_sig_D1_2420_D_$PARAM_0\.sh 0 9
    cp -rf $HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/subSimRec.sh ./
    sh subSimRec.sh jobOptions_sim_sig_D1_2420_D_$PARAM_0 jobOptions_rec_sig_D1_2420_D_$PARAM_0 subSimRec_D1_2420_$PARAM_0\_705 0 9
done
