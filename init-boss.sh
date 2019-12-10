#!/usr/bin/env bash

cd besenv/664p01
# cd besenv/703p01
# cd besenv/704p01

source setupCMT.csh
cmt config
source setup.csh

cd $HOME/bes/DDPIPI/v0.2/TestRelease/664p01/TestRelease-00-00-80/cmt
# cd $HOME/bes/DDPIPI/v0.2/TestRelease/703p01/TestRelease-00-00-86/cmt
# cd $HOME/bes/DDPIPI/v0.2/TestRelease/704p01/TestRelease-00-00-86/cmt

cmt br cmt config

cmt br gmake

cd $HOME/bes/DDPIPI/v0.2
