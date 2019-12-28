# DDPIPI

This is a work of measuring cross section of DDPIPI

## Install v0.2

> mkdir -p $HOME/bes/DDPIPI

> cd $HOME/bes/DDPIPI

> git clone https://github.com/zhixing1996/DDPIPI.git v0.2

## Login container (664p01)

Login with lxslc7 and use hep_container shell SL5 to enter lxslc5

> NOTE: *****Login SL5 after installing as well as pushing codes(git version problem)*****

> source login-container.sh

## Initialize BOSS

BOSS version 6.6.4.p01(topology analysis), 6.6.5.p01(R-scan data), 7.0.3.p01(XYZ data, inclusive MC)

> NOTE: *****When you do simulation and reconstruction under 665p01, the environment has to be set by the way of lig(boss_envirenmet.csh)*****

This is only need to be done for the first time after clone the code:

> source init-boss.sh

## Setup

> source setup.sh

## Build code

> ./build.sh

## Submit Simulation and Reconstruction jobs(MC) and Generate root files(MC and data)

> ./submit.sh

## Execute and submit analysis jobs

> ./analysis.sh

## For developers 
 
- Fork the code with your personal github ID. See [details](https://help.github.com/articles/fork-a-repo/)
 
> git clone https://github.com/zhixing1996/DDPIPI.git
 
- Make your change, commit and push
 
> git commit -a -m "Added feature A, B, C"
 
> git push
 
- Make a pull request. See [details](https://help.github.com/articles/using-pull-requests/)
 
## Some styles to follow 
- Minimize the number of main c++ files
- Keep functions length less than one screen
- Seperate hard-coded cuts into script file                                                                                                                                                              
- Use pull-request mode on git 
- Document well the high-level bash file for work flow 
