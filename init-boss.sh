#!/usr/bin/env bash

cd besenv/703p01

source setupCMT.csh
cmt config
source setup.csh

cd $HOME/bes/DDPIPI/v0.2/TestRelease/703p01/TestRelease-00-00-86/cmt

cmt br cmt config

cmt br gmake

cd $HOME/bes/DDPIPI/v0.2
