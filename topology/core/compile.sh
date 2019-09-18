#!/bin/bash

#The following two statements set the package path automatically 
pkgPath=`pwd|sed 's/core//g'`
sed -i 's:m_pkgPath=.*:m_pkgPath=\"'$pkgPath'\";:g' topoana.h

cxxfile="topoana.cpp"
exefile="topoana.exe"
ROOTCFLAGS=`root-config --cflags`
# The first method
ROOTLDFLAGS=`root-config --ldflags --glibs`
g++ -g -Wall ${ROOTCFLAGS} ${ROOTLDFLAGS} -lTreePlayer -o ${exefile} ${cxxfile}

# The second method
# This method can't be used with a lower version of ROOT, such as ROOT 5.24.
#ROOTLDFLAGS=`root-config --ldflags --glibs --evelibs` # Note that the argument "--evelibs" is indispensable here; only "--ldflags" and "--glibs" are not enough!
#g++ -g -Wall ${ROOTCFLAGS} ${ROOTLDFLAGS} -o ${exefile} ${cxxfile}

exit 0
