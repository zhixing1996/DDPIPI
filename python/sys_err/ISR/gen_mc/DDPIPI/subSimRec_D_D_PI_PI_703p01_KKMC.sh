#!/bin/sh
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
    # mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/jobs_sig
    # cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/jobs_sig
    # mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/rtraw
    # mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/dst
    mkdir -p /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/jobs_sig
    cd /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/run/gen_mc/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/jobs_sig
    mkdir -p /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/rtraw
    mkdir -p /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/dst
    rm -rf jobOptions*txt
    rm -rf subSimRec_*.sh
    rm -rf xs_user.dat
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/ISR/gen_mc/DDPIPI/jobOptions_sim_sig_D_D_PI_PI_tempE_703p01_KKMC.sh ./jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/ISR/gen_mc/DDPIPI/xs_user.dat ./xs_user.dat
    sed -i "s/TEMP_0/$PARAM_0/g" jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    sed -i "s/TEMP_1/$PARAM_1/g" jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    sed -i "s/TEMP_2/$PARAM_2/g" jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    sed -i "s/TEMP_3/$PARAM_3/g" jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    thre=4.0205
    PARAM_6=$thre
    sed -i "s/TEMP_6/$PARAM_6/g" jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh
    # rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/rtraw/*.rtraw
    rm -rf /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/rtraw/*.rtraw
    sh jobOptions_sim_sig_D_D_PI_PI_$PARAM_0\.sh 0 9 5000
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/ISR/gen_mc/DDPIPI/jobOptions_rec_sig_D_D_PI_PI_tempE_703p01.sh ./jobOptions_rec_sig_D_D_PI_PI_$PARAM_0\.sh
    sed -i "s/TEMP_0/$PARAM_0/g" jobOptions_rec_sig_D_D_PI_PI_$PARAM_0\.sh
    # rm -rf /scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/dst/*.dst
    rm -rf /besfs/groups/cal/dedx/$USER/bes/DDPIPI/v0.2/sigMC/DDPIPI/$PARAM_0/sys_err/ISR/dst/*.dst
    sh jobOptions_rec_sig_D_D_PI_PI_$PARAM_0\.sh 0 9
    cp -rf $HOME/bes/DDPIPI/v0.2/python/sys_err/ISR/gen_mc/subSimRec.sh ./
    sh subSimRec.sh jobOptions_sim_sig_D_D_PI_PI_$PARAM_0 jobOptions_rec_sig_D_D_PI_PI_$PARAM_0 subSimRec_DDPIPI_$PARAM_0\_703p01 0 9
done
