echo "Setting DDecayAlg DDecayAlg-00-00-02 in /afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /afs/ihep.ac.cn/bes3/offline/ExternalLib/contrib/CMT/v1r20p20081118
endif
source ${CMTROOT}/mgr/setup.csh

set tempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set tempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt setup -csh -pack=DDecayAlg -version=DDecayAlg-00-00-02 -path=/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/Analysis/Physics  -no_cleanup $* >${tempfile}; source ${tempfile}
/bin/rm -f ${tempfile}

