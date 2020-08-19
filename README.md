# DDPIPI

This is a work about measuring cross sections of DDPIPI

## Install v0.2

> mkdir -p $HOME/bes/DDPIPI

> cd $HOME/bes/DDPIPI

> git clone https://github.com/zhixing1996/DDPIPI.git v0.2

## Initialize BOSS

BOSS version 7.0.3.p01(XYZ data, inclusive MC)

BOSS version 7.0.5(new XYZ data, inclusive MC, data sample above 4600 MeV)

This is only need to be done for the first time after clone the code:

> source init_boss_703p01.sh/init_boss_705.sh

## Setup

> source setup_703p01.sh/setup_705.sh

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
