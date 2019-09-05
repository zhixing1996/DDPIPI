#!/usr/bin/env bash

# Main driver to build programs
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-08-06 Tue 21:53]


usage() {
    printf "NAME\n\tbuild.sh - Main driver to build programs\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./build.sh [OPTION]"
    printf "\n\t%-5s  %-40s\n" "1" "Build DDecay analyzer: DDecayAlg-00-00-01"
    printf "\n\t%-5s  %-40s\n" "2" "Build DDecay analyzer: DDecayAlg-00-00-02"
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
    1) echo "Building DDecay analyzer: DDecayAlg-00-00-01..."
       cd Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/cmt
       gmake
       ;;
    2) echo "Building DDecay analyzer: DDecayAlg-00-00-02..."
       cd Analysis/Physics/DDecayAlg/DDecayAlg-00-00-02/cmt
       gmake
       ;;
esac
