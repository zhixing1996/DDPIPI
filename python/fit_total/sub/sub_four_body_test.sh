#!/bin/sh

mkdir -p /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/fit/jobs_ana
cd /scratchfs/bes/$USER/bes/DDPIPI/v0.2/run/ana/fit/jobs_ana

rm -rf jobs.out
mkdir jobs.out
rm -rf jobs.err
mkdir jobs.err

SUB_NAME="Sub_Four_Body_PS_test"
echo "#!/bin/bash" > $SUB_NAME
echo "cd $HOME/bes/DDPIPI/v0.2/python/fit_total" >> $SUB_NAME
echo "python cal_four_test.py" >> $SUB_NAME

chmod u+x $SUB_NAME
# bash $SUB_NAME
hep_sub -g physics $SUB_NAME -o ./jobs.out -e ./jobs.err
# hep_sub -wt long $SUB_NAME -o ./jobs.out -e ./jobs.err
