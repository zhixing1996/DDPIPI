#!/usr/bin/env bash

# Main driver to submit simulation and reconstruction jobs as well as generating root files 
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-09-02 Mon 22:17]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit simulation and reconstruction jobs as well as generating root files\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./submit.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" ""      ""
    printf "\n\n"
}

if [[ $# -eq 0 ]]; then
    usage
    echo "Please enter your option: "
    read option
else
    option=$1
fi

case $option in

esac
