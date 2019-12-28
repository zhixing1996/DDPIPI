#!/usr/bin/env bash

# cd besenv/664p01
# cd besenv/665p01
cd besenv/703p01
source setupCVS.csh
source setupCMT.csh
cmt config
source setup.csh

# cd ../../TestRelease/664p01/TestRelease-00-00-80/cmt
# cd ../../TestRelease/665p01/TestRelease-00-00-81/cmt
cd ../../TestRelease/703p01/TestRelease-00-00-86/cmt
source setup.csh
cd ../../../..

# source ./Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/cmt/setup.csh
# source ./Analysis/Physics/DDecayAlg/DDecayAlg-00-00-02/cmt/setup.csh
source ./Analysis/Physics/DDecayAlg/DDecayAlg-00-00-03/cmt/setup.csh
