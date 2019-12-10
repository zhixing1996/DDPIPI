#!/bin/sh

INPUT=$1
UPLIMIT=$2

SEED=3020023
ENERGYPOINT="4420"

DIR_NAME="/scratchfs/bes/$USER/bes/DDPIPI/v0.2/sigMC/psipp/4420/rtraw/"
EVENT_NO=$3

echo "./jobOptions_sim_sig_psipp_PI_PI_VSS_4420.sh [NUM1] [NUM2] [NUM3]"
echo "[NUM1]: the minimum number range of job generated"
echo "[NUM2]: the maximum number range of job generated"
echo "[NUM3]: the number of events in one job"

JOB_NAME="jobOptions_sim_sig_psipp_PI_PI_VSS"
FILE_NAME="Sig_psipp_PI_PI_VSS"

# steer file for simulation
echo "steer file for simulation"

until [ $INPUT -gt $UPLIMIT ]
do

    SIM_NAME=$JOB_NAME"_"$ENERGYPOINT"_"$INPUT".txt"
    OUTPUT_NAME=$FILE_NAME"_"$ENERGYPOINT"_"$INPUT".rtraw"

    touch $SIM_NAME

    echo "#include \"\$OFFLINEEVENTLOOPMGRROOT/share/OfflineEventLoopMgr_Option.txt\"" > $SIM_NAME
    echo "" >> $SIM_NAME
    echo "//**************job options for generator (KKMC)************************" >> $SIM_NAME
    echo "#include \"\$KKMCROOT/share/jobOptions_KKMC.txt\"" >> $SIM_NAME
    echo "KKMC.CMSEnergy = 4.415;" >> $SIM_NAME
    echo "KKMC.BeamEnergySpread=0.00203;" >> $SIM_NAME
    echo "KKMC.NumberOfEventPrinted=10;" >> $SIM_NAME
    echo "KKMC.GeneratePsi4415=true;" >> $SIM_NAME
    echo "KKMC.ParticleDecayThroughEvtGen = true;" >> $SIM_NAME
    echo "KKMC.ThresholdCut = 4.360;" >> $SIM_NAME
    echo "KKMC.RadiationCorrection = 1;" >> $SIM_NAME
    echo "KKMC.TagISR = 1;" >> $SIM_NAME
    echo "KKMC.TagFSR = 1;" >> $SIM_NAME
    echo "" >> $SIM_NAME
    echo "//**************job options for EvtGen************************" >> $SIM_NAME
    echo "#include \"\$BESEVTGENROOT/share/BesEvtGen.txt\"" >> $SIM_NAME
    echo "EvtDecay.userDecayTableName = \"$HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/decay/psi4415_psipp_PI_PI_VSS.dec\";" >> $SIM_NAME
    echo "EvtDecay.PdtTableDir = \"$HOME/bes/DDPIPI/v0.2/scripts/gen_script/gen_mc/decay/pdt_664p01.table\";" >> $SIM_NAME
    echo "EvtDecay.statDecays = true;" >> $SIM_NAME
    echo "" >> $SIM_NAME
    echo "//**************job options for random number************************" >> $SIM_NAME
    echo "BesRndmGenSvc.RndmSeed = $SEED;" >> $SIM_NAME
    echo "" >> $SIM_NAME
    echo "//**************job options for detector simulation******************" >> $SIM_NAME
    echo "#include \"\$BESSIMROOT/share/G4Svc_BesSim.txt\"" >> $SIM_NAME
    echo "" >> $SIM_NAME
    echo "//configure for calibration constants" >> $SIM_NAME
    echo "#include \"\$CALIBSVCROOT/share/calibConfig_sim.txt\"" >> $SIM_NAME
    echo "" >> $SIM_NAME
    echo "// run ID" >> $SIM_NAME
    echo "RealizationSvc.RunIdList = {-31327, 0, -31390, -36773, 0, -38140};" >> $SIM_NAME
    echo "" >> $SIM_NAME
    echo "#include \"\$ROOTIOROOT/share/jobOptions_Digi2Root.txt\"" >> $SIM_NAME
    echo "RootCnvSvc.digiRootOutputFile = \"$DIR_NAME$OUTPUT_NAME\";" >> $SIM_NAME
    echo "" >> $SIM_NAME

    echo "// OUTPUT PRINTOUT LEVEL" >> $SIM_NAME
    echo "// Set output level threshold (2=DEBUG, 3=INFO, 4=WARNING, 5=ERROR, 6=FATAL )" >> $SIM_NAME
    echo "MessageSvc.OutputLevel  = 5;" >> $SIM_NAME
    echo "" >> $SIM_NAME
    echo "// Number of events to be processed (default is 10)" >> $SIM_NAME
    echo "ApplicationMgr.EvtMax = $EVENT_NO;" >> $SIM_NAME
    echo "" >> $SIM_NAME

    echo $SIM_NAME" done!"   

    INPUT=$(($INPUT+1))
    SEED=$(($SEED+1))
  
done

echo "all done!"   
