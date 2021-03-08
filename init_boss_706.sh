#!/usr/bin/env bash
if [ -f "./besenv/706" ]; then
    echo "Maybe you have already initialized the BOSS environment..."
else 
    mkdir -p besenv/706
    cd besenv/706
    cp /cvmfs/bes3.ihep.ac.cn/bes3sw/cmthome/cmthome-7.0.6-Slc6Centos7Compat ./cmthome -rf
    cd cmthome
    echo "set WorkArea \"/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2\"" >> requirements
    echo "path_remove CMTPATH  \"\${WorkArea}\"" >> requirements
    echo "path_prepend CMTPATH  \"\${WorkArea}\"" >> requirements
    source setupCVS.sh
    source setupCMT.sh
    cmt config
    source setup.sh
    cd ..
    cp /cvmfs/bes3.ihep.ac.cn/bes3sw/Boss/7.0.6/TestRelease . -rf
    cd TestRelease/TestRelease-00-00-95/cmt
    cmt config
    source setup.sh
    cd $HOME/bes/DDPIPI/v0.2
fi
