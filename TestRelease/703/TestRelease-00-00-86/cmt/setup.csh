# echo "setup 703 TestRelease-00-00-86 in /afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/TestRelease"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /afs/ihep.ac.cn/bes3/offline/ExternalLib/SLC6/contrib/CMT/v1r25
endif
source ${CMTROOT}/mgr/setup.csh
set cmt_03tempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set cmt_03tempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt setup -csh -pack=703 -version=TestRelease-00-00-86 -path=/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/TestRelease  -no_cleanup $* >${cmt_03tempfile}
if ( $status != 0 ) then
  echo "${CMTROOT}/mgr/cmt setup -csh -pack=703 -version=TestRelease-00-00-86 -path=/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/TestRelease  -no_cleanup $* >${cmt_03tempfile}"
  set cmtsetupstatus=2
  /bin/rm -f ${cmt_03tempfile}
  unset cmt_03tempfile
  exit $cmtsetupstatus
endif
set cmtsetupstatus=0
source ${cmt_03tempfile}
if ( $status != 0 ) then
  set cmtsetupstatus=2
endif
/bin/rm -f ${cmt_03tempfile}
unset cmt_03tempfile
exit $cmtsetupstatus

