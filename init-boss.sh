#!/usr/bin/env bash

cd besenv

source setupCMT.csh

cmt config

cd $HOME/bes/DDPIPI/v0.1/TestRelease/TestRelease-00-00-80/cmt

cmt br cmt config

cmt br gmake

cd $HOME/bes/DDPIPI/v0.1
