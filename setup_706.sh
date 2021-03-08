#!/usr/bin/env bash

cd besenv/706/cmthome
source setupCVS.csh
source setupCMT.csh
cmt config
source setup.csh

cd $HOME/bes/DDPIPI/v0.2/besenv/706/TestRelease/TestRelease-00-00-95/cmt
source setup.csh

# source $HOME/bes/DDPIPI/v0.2/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/cmt/setup.csh
# source $HOME/bes/DDPIPI/v0.2/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-02/cmt/setup.csh
source $HOME/bes/DDPIPI/v0.2/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-03/cmt/setup.csh
# source $HOME/bes/DDPIPI/v0.2/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-04/cmt/setup.csh

cd $HOME/bes/DDPIPI/v0.2
