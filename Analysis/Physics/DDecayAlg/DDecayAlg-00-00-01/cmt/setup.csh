# echo "setup DDecayAlg DDecayAlg-00-00-01 in /afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/Analysis/Physics"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /afs/ihep.ac.cn/bes3/offline/ExternalLib/SLC6/contrib/CMT/v1r25
endif
source ${CMTROOT}/mgr/setup.csh
set cmtDDecayAlgtempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set cmtDDecayAlgtempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt setup -csh -pack=DDecayAlg -version=DDecayAlg-00-00-01 -path=/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/Analysis/Physics  -no_cleanup $* >${cmtDDecayAlgtempfile}
if ( $status != 0 ) then
  echo "${CMTROOT}/mgr/cmt setup -csh -pack=DDecayAlg -version=DDecayAlg-00-00-01 -path=/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/Analysis/Physics  -no_cleanup $* >${cmtDDecayAlgtempfile}"
  set cmtsetupstatus=2
  /bin/rm -f ${cmtDDecayAlgtempfile}
  unset cmtDDecayAlgtempfile
  exit $cmtsetupstatus
endif
set cmtsetupstatus=0
source ${cmtDDecayAlgtempfile}
if ( $status != 0 ) then
  set cmtsetupstatus=2
endif
/bin/rm -f ${cmtDDecayAlgtempfile}
unset cmtDDecayAlgtempfile
exit $cmtsetupstatus

