#!/usr/bin/env bash

cd besenv/705
source setupCVS.csh
source setupCMT.csh
cmt config
source setup.csh

cd ../../TestRelease/705/TestRelease-00-00-88/cmt
source setup.csh
cd ../../../..

# source ./Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/cmt/setup.csh
# source ./Analysis/Physics/DDecayAlg/DDecayAlg-00-00-02/cmt/setup.csh
source ./Analysis/Physics/DDecayAlg/DDecayAlg-00-00-03/cmt/setup.csh
