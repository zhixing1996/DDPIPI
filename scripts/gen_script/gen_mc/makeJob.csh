#!/bin/tcsh -f

if ($#argv != 1 && $#argv != 2 && $#argv != 3 && $#argv != 4 && $#argv != 5 && $#argv != 6 && $#argv != 7) then
  echo " "
  echo "purpose    : (for real data) you can get jobOptions with certain number rec file in each job automatically. "
  echo "             Also, you can summit the jobs automatically. "
  echo "useage     : ./makeJob.csh jobName [jobN] [fileN] [jobDir] [sampleType] [decayMode] [energy]"
  echo "jobName    : is the name of jobOption you wish"
  echo "             this argument SHOULD NOT be omitted. "
  echo "jobN       : is the largest number of jobs"
  echo "             by default, it will be 20 "
  echo "fileN      : is the smallest of rec file in each jobOption"
  echo "             by default, it will be 2 "
  echo "jobDir     : is the directory where you want the jobOption is"
  echo "             by default, it will be PWD "
  echo "sampleType : is the type of sample you want to deal with, e.g.: signal MC, inclusive MC, data"
  echo "             this argument SHOULD NOT be omitted. "
  echo "decayMode  : is the type of decay mode in your sample"
  echo "             this argument SHOULD NOT be omitted. "
  echo "energy     : is the energy point of your sample"
  echo "             this argument SHOULD NOT be omitted. "
  echo "  "
  echo "SQUESTION  : step one   : please check/modify the 'makeJob.head' "
  echo "             step two   : please check/modify the 'makeJob.tail' "
  echo "             step three : please check 'DataParentPath' in 'makeJob.csh' correct or not"
  exit
endif

# set jobName : the name of job will like "jobName_????.txt" 
set jobName = $argv[1]
echo "jobName : ${jobName}"

# set jobN    : the largest number of jobs" 
if( $#argv >= 2 ) then
    @ jobN=$argv[2]
else
    @ jobN=100
endif
echo "The largest number of jobs : ${jobN}"

# set fileN   : the smallest number of rec file in each jobOption" 
if( $#argv >= 3 ) then
    @ fileN=$argv[3]
else
    @ fileN=2
endif
echo "The smallest number of rec file in each job : ${fileN}"

# input the path as DataParentPath of data
if( $#argv >= 4 ) then
    set jobDir = $argv[4]
else
    set jobDir = $PWD
endif
echo "jobDir  : ${jobDir}"

# set sample
set sample = $argv[5]
echo "sampleType : ${sample}"

# set decay mode
set mode = $argv[6]
echo "decayMode : ${mode}"

# set energypoints
set energy = $argv[7]
echo "energy : ${energy}"

# get all rec file from all child path of the DataParentPath
echo "set data path"
set DataParentPath = /scratchfs/bes/jingmq/bes/DDPIPI/v0.1/${sample}/${mode}/${energy}/dst

# set DataParentPath: where is the real data
echo "DataParentPath : ${DataParentPath}"

if ( -e ${jobDir}/dstlist.txt ) then 
   rm ${jobDir}/dstlist.txt -rf
endif 

if (! -e dstlist.txt )   then 
   find  ${DataParentPath} -name "*.dst" > dstlist.txt

else
   find  ${DataParentPath} -name "*.dst" >> dstlist.txt

endif 

# input the number of total lines of dstlist.txt 
@  nline=`wc -l dstlist.txt | cut -f 1 -d " "`
echo "There are ${nline} rec file totally"

# calculate how much jobs and how much rec file in each job 
@ Ntemp=${fileN} * ${jobN}
if( ${nline} > ${Ntemp} ) then 
  @ fileN=${nline} / ${jobN} + 1
  echo "To make sure there are at most ${jobN} jobs, there will be ${fileN} rec files in each job"
else 
  @ jobN=${nline} / ${fileN} + 1
  echo "To make sure there are at least ${fileN} rec files in each job, there will be ${jobN} jobs"
endif

# make jobOptions with certain rec files in each job
@ iline=1
@ i=0
set ijob=${i}
foreach file ( `cat dstlist.txt` )
# foreach file ( `cat dstlist.txt | sed '1d'` )

        if ( ${iline} % ${fileN} == 1 ) then 
            if ( -e ${jobDir}/${jobName}_${ijob}.txt ) then 
               echo "Just remind: ${jobDir}/${jobName}_${ijob}.txt already exists, and it will be update!"
            endif 
            cp ${jobDir}/makeJob.head  ${jobDir}/${jobName}_${ijob}.txt 
        endif 

        if ( ${iline} % ${fileN} != 0 && ${iline} < ${nline} ) then
	       echo \"${file}\", >>  ${jobDir}/${jobName}_${ijob}.txt
        endif 

        if ( ${iline} % ${fileN} == 0 || ${iline} == ${nline} ) then 
            echo \"${file}\" >>  ${jobDir}/${jobName}_${ijob}.txt
            sed -e s/SAMPLE/${sample}/ -e s/MODE/${mode}/ -e s/ENERGY/${energy}/ -e s/JOB/${jobName}_${ijob}/ ${jobDir}/makeJob.tail >> ${jobDir}/${jobName}_${ijob}.txt

            echo ${jobDir}/${jobName}_${ijob}.txt is finished 

            @ i++
            if ( ${i} < 10 ) then 
               set ijob=${i}
            else
               set ijob=${i}
            endif 
        endif 

        @ iline++
end          
