# echo "Setting DDecayAlg DDecayAlg-00-00-01 in /afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.1"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /afs/ihep.ac.cn/bes3/offline/ExternalLib/contrib/CMT/v1r20p20081118
endif
source ${CMTROOT}/mgr/setup.csh

set tempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set tempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt setup -csh -pack=DDecayAlg -version=DDecayAlg-00-00-01 -path=/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.1/Analysis/Physics/DDecayAlg/DDecayAlg-00-00-01/cmt  -no_cleanup $* >${tempfile}; source ${tempfile}
/bin/rm -f ${tempfile}

