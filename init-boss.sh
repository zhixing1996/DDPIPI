#!/usr/bin/env bash

# cd besenv/703p01
# cd besenv/703
cd besenv/705

source setupCMT.csh
cmt config
source setup.csh

# cd $HOME/bes/DDPIPI/v0.2/TestRelease/703p01/TestRelease-00-00-86/cmt
# cd $HOME/bes/DDPIPI/v0.2/TestRelease/703/TestRelease-00-00-86/cmt
cd $HOME/bes/DDPIPI/v0.2/TestRelease/705/TestRelease-00-00-88/cmt

cmt br cmt config

cmt br gmake

cd $HOME/bes/DDPIPI/v0.2
