# DDPIPI

This is a work of measuring cross section of DDPIPI

## Install v0.2

> mkdir -p $HOME/bes/DDPIPI

> cd $HOME/bes/DDPIPI

> git clone https://github.com/zhixing1996/DDPIPI.git v0.2

## Initialize BOSS

BOSS version 7.0.3.p01(XYZ data, inclusive MC)

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
