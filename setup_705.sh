#!/usr/bin/env bash

cd besenv/705/cmthome
source setupCVS.csh
source setupCMT.csh
cmt config
source setup.csh

cd $HOME/bes/DDPIPI/v0.2/besenv/705/TestRelease/TestRelease-00-00-92/cmt
source setup.csh

# source $HOME/bes/DDPIPI/v0.2/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/cmt/setup.csh
# source $HOME/bes/DDPIPI/v0.2/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-02/cmt/setup.csh
source $HOME/bes/DDPIPI/v0.2/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-03/cmt/setup.csh
# source $HOME/bes/DDPIPI/v0.2/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-04/cmt/setup.csh

cd $HOME/bes/DDPIPI/v0.2
