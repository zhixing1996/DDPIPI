# DDPIPI

This is a work following Yi Zheng's work(https://hnbes3.ihep.ac.cn/HyperNews/get/paper224.html)

## Install

> mkdir -p $HOME/bes/DDPIPI
> cd $HOME/bes/DDPIPI
> git clone https://github.com/zhixing1996/DDPIPI.git

## Initialize BOSS

BOSS version 6.6.4.p01(Login with lxslc7 and use hep_container shell SL5 to enter lxslc5)

This is only need to be done for the first time after clone the code:

> source init-boss.sh

## For developers 
 
- Fork the code with your personal github ID. See [details](https://help.github.com/articles/fork-a-repo/)
 
> git clone https://github.com/zhixing1996/DDPIPI.git .
 
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
