#!/usr/bin/env bash

# Main driver to build programs
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2019-08-06 Tue 21:53]


usage() {
    printf "NAME\n\tbuild.sh - Main driver to build programs\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./build.sh [OPTION]"
    printf "\n\t%-5s  %-40s\n" "1" "Build DDecay analyzer: DDecayAlg-00-00-01: Repeat Yi Zheng's work"
    printf "\n\t%-5s  %-40s\n" "2" "Build DDecay analyzer: DDecayAlg-00-00-02: Add missing D track"
    printf "\n\t%-5s  %-40s\n" "3" "Build DDecay analyzer: DDecayAlg-00-00-02: Background study"
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
       rm -rf Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/x86_*/
       cd Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/cmt
       cmt config
       gmake
       ;;
    2) echo "Building DDecay analyzer: DDecayAlg-00-00-02..."
       rm -rf Analysis/Physics/DDecayAlg/DDecayAlg-00-00-02/x86_*/
       cd Analysis/Physics/DDecayAlg/DDecayAlg-00-00-02/cmt
       cmt config
       gmake
       ;;

    3) echo "Building DDecay analyzer: DDecayAlg-00-00-03..."
       rm -rf Analysis/Physics/DDecayAlg/DDecayAlg-00-00-03/x86_*/
       cd Analysis/Physics/DDecayAlg/DDecayAlg-00-00-03/cmt
       cmt config
       gmake
       ;;

esac
