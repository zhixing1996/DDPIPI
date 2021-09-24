#!/bin/sh

mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/sel/jobs_ana
cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/sel/jobs_ana

rm -rf jobs.out
mkdir jobs.out
rm -rf jobs.err
mkdir jobs.err

SUB_NAME="Sub_ISR_eff"
echo "#!/bin/bash" > $SUB_NAME
echo "cd $HOME/bes/DDPIPI/v0.2/python/sys_err/ISR/sample" >> $SUB_NAME
echo "python ISR_eff.py" >> $SUB_NAME

chmod u+x $SUB_NAME
hep_sub -g physics $SUB_NAME -o ./jobs.out -e ./jobs.err
