#!/bin/sh
cat psipp_Base_707 | while read line
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
    mkdir -p $WORKAREA/scripts/sigMC/psipp/$PARAM_0/sys_err/BW
    cd $WORKAREA/scripts/sigMC/psipp/$PARAM_0/sys_err/BW
    if [ ! -d "/scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/BW/jobs_sig" ]; then
        mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/BW/jobs_sig
        ln -s /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/psipp/$PARAM_0/sys_err/BW/jobs_sig ./jobs_sig
    fi
    cd jobs_sig
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/BW/rtraw
    mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/BW/dst
    rm -rf jobOptions*txt
    rm -rf subSimRec_*.sh
    rm -rf xs_user.dat
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/BW/scripts/mc/psipp/jobOptions_sim_sig_psipp_PI_PI_VSS_tempE_707.sh ./jobOptions_sim_sig_psipp_PI_PI_VSS_$PARAM_0\.sh
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/BW/scripts/mc/psipp/xs_user.dat ./xs_user.dat
    sed -i "s/TEMP_0/$PARAM_0/g" jobOptions_sim_sig_psipp_PI_PI_VSS_$PARAM_0\.sh
    sed -i "s/TEMP_1/$PARAM_1/g" jobOptions_sim_sig_psipp_PI_PI_VSS_$PARAM_0\.sh
    sed -i "s/TEMP_2/$PARAM_2/g" jobOptions_sim_sig_psipp_PI_PI_VSS_$PARAM_0\.sh
    sed -i "s/TEMP_3/$PARAM_3/g" jobOptions_sim_sig_psipp_PI_PI_VSS_$PARAM_0\.sh
    thre=4.0535
    PARAM_6=$thre
    sed -i "s/TEMP_6/$PARAM_6/g" jobOptions_sim_sig_psipp_PI_PI_VSS_$PARAM_0\.sh
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/BW/rtraw/*.rtraw
    sh jobOptions_sim_sig_psipp_PI_PI_VSS_$PARAM_0\.sh 0 9 5000
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/BW/scripts/mc/psipp/jobOptions_rec_sig_psipp_PI_PI_VSS_tempE_707.sh ./jobOptions_rec_sig_psipp_PI_PI_VSS_$PARAM_0\.sh
    sed -i "s/TEMP_0/$PARAM_0/g" jobOptions_rec_sig_psipp_PI_PI_VSS_$PARAM_0\.sh
    rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/$PARAM_0/sys_err/BW/dst/*.dst
    sh jobOptions_rec_sig_psipp_PI_PI_VSS_$PARAM_0\.sh 0 9
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/BW/scripts/mc/psipp/subSimRec.sh ./
    sh subSimRec.sh jobOptions_sim_sig_psipp_PI_PI_VSS_$PARAM_0 jobOptions_rec_sig_psipp_PI_PI_VSS_$PARAM_0 subSimRec_psipp_$PARAM_0\_707 0 9
done
