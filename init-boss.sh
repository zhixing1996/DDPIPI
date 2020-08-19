#!/usr/bin/env bash

# cd besenv/703p01/cmthome
cd besenv/705/cmthome

source setupCVS.csh
source setupCMT.csh
cmt config
source setup.csh

# cd $HOME/bes/DDPIPI/v0.2/besenv/703p01/TestRelease/TestRelease-00-00-86/cmt
cd $HOME/bes/DDPIPI/v0.2/besenv/705/TestRelease/TestRelease-00-00-92/cmt

cmt config
source setup.csh

cd $HOME/bes/DDPIPI/v0.2
