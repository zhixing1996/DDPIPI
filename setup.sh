#!/usr/bin/env bash

cd besenv
source setupCVS.csh
source setupCMT.csh
cmt config
source setup.csh

cd ../TestRelease/TestRelease-00-00-80/cmt
source setup.csh
cd ../../..

source ./Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/cmt/setup.csh
