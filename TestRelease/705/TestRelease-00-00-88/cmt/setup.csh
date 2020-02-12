# echo "setup 705 TestRelease-00-00-88 in /afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/TestRelease"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /afs/ihep.ac.cn/bes3/offline/ExternalLib/SLC6/contrib/CMT/v1r25
endif
source ${CMTROOT}/mgr/setup.csh
set cmt_05tempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set cmt_05tempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt setup -csh -pack=705 -version=TestRelease-00-00-88 -path=/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/TestRelease  -no_cleanup $* >${cmt_05tempfile}
if ( $status != 0 ) then
  echo "${CMTROOT}/mgr/cmt setup -csh -pack=705 -version=TestRelease-00-00-88 -path=/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/TestRelease  -no_cleanup $* >${cmt_05tempfile}"
  set cmtsetupstatus=2
  /bin/rm -f ${cmt_05tempfile}
  unset cmt_05tempfile
  exit $cmtsetupstatus
endif
set cmtsetupstatus=0
source ${cmt_05tempfile}
if ( $status != 0 ) then
  set cmtsetupstatus=2
endif
/bin/rm -f ${cmt_05tempfile}
unset cmt_05tempfile
exit $cmtsetupstatus

