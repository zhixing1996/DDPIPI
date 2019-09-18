#include "topoana.h"
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <algorithm>
#include <sstream>
#include <iomanip>
#include "TFile.h"
#include "TChain.h"
#include "TChainElement.h"
#include "TTree.h"
#include "TBranch.h"
#include <ctime>
#include "TTreeFormula.h"
#include <cmath>

string & topoana::trim(string & line)
{
  if(line.empty())
    {
      return line;
    }
  line.erase(0,line.find_first_not_of(" "));
  line.erase(line.find_last_not_of(" ")+1);
  line.erase(0,line.find_first_not_of("\t"));
  line.erase(line.find_last_not_of("\t")+1);
  return line;
}

void topoana::mkPidTxtPnmMap()
{
  m_pidTxtPnmMap.clear();
  int pid;string txtpnm;
  string pidTxtPnmDatFlNm=m_pkgPath+"core/pid_txtpnm.dat";
  ifstream fin(pidTxtPnmDatFlNm.c_str(),ios::in);
  if(!fin)
    {
      cerr<<"Error: Can't open the data file \""<<pidTxtPnmDatFlNm<<"\"!"<<endl;
      cerr<<"Infor: Please check it."<<endl;
      exit(11);
    }
  while(fin>>pid>>txtpnm)
    {
      m_pidTxtPnmMap[pid]=txtpnm;
      //cout<<pid<<"\t"<<m_pidTxtPnmMap[pid]<<endl;
    }
}

void topoana::mkPid3PchrgMap()
{
  m_pid3PchrgMap.clear();
  int pid,i3pchrg; // The character "i" in the variable name "i3pchrg" is inserted specially for avoiding the mistake of starting a variable name with a number.
  string pid3PchrgDatFlNm=m_pkgPath+"core/pid_3pchrg.dat";
  ifstream fin(pid3PchrgDatFlNm.c_str(),ios::in);
  if(!fin)
    {
      cerr<<"Error: Can't open the data file \""<<pid3PchrgDatFlNm<<"\"!"<<endl;
      cerr<<"Infor: Please check it."<<endl;
      exit(12);           
    }
  while(fin>>pid>>i3pchrg)
    {
      m_pid3PchrgMap[pid]=i3pchrg;
      //cout<<pid<<"\t"<<m_pid3PchrgMap[pid]<<endl;
    }
}

int topoana::getPidFromTxtPnm(string pnm)
{
  int pid;
  bool inTheMap=false;
  map<int,string>::iterator misit;
  for(misit=m_pidTxtPnmMap.begin();misit!=m_pidTxtPnmMap.end();misit++)
    {
      if((misit->second)==pnm)
        {
          pid=(misit->first);
          inTheMap=true;
          break;
        }
    }
  if(inTheMap)
    {
      return pid;
    }
  else
    {
      string pidTxtPnmDatFlNm=m_pkgPath+"core/pid_txtpnm.dat";
      string evtPdlFlNm=m_pkgPath+"doc/evt.pdl";
      cerr<<"Error: The Pid for the TxtPnm \""<<pnm<<"\" does not exist in the data file \""<<pidTxtPnmDatFlNm<<"\"!"<<endl;
      cerr<<"Infor: Please check whether the TxtPnm \""<<pnm<<"\" is right. If yes, please refer to the pdl file \""<<evtPdlFlNm<<"\", find the Pid for the TxtPnm \""<<pnm<<"\", and add the pair of Pid to TxtPnm in the data file \""<<pidTxtPnmDatFlNm<<"\". If no, please correct it to the right one."<<endl;
      exit(41);
    }
}

void topoana::optErrInfOnPid3PchrgMap(int pid)
{
  string pid3PchrgDatFlNm=m_pkgPath+"core/pid_3pchrg.dat";
  string evtPdlFlNm=m_pkgPath+"doc/evt.pdl";
  cerr<<"Error: The 3Pchrg for Pid \""<<pid<<"\" does not exist in the data file \""<<pid3PchrgDatFlNm<<"\"!"<<endl;
  cerr<<"Infor: Please refer to the pdl file \""<<evtPdlFlNm<<"\", find the 3Pchrg for the Pid \""<<pid<<"\", and add the pair of Pid to 3Pchrg in the data file \""<<pid3PchrgDatFlNm<<"\"."<<endl<<endl;
}

void topoana::optPnmFromPid(ostream & out,string pnmType,int pid)
{
  if(pnmType=="TxtPnm")
    {
      if(m_pidTxtPnmMap.find(pid)!=m_pidTxtPnmMap.end())
        { 
          out<<" "<<m_pidTxtPnmMap[pid];
        }
      else
        {
          out<<" "<<"??";
          string pidTxtPnmDatFlNm=m_pkgPath+"core/pid_txtpnm.dat";
          string evtPdlFlNm=m_pkgPath+"doc/evt.pdl";
          cerr<<"Error: The TxtPnm for the Pid \""<<pid<<"\" does not exist in the data file \""<<pidTxtPnmDatFlNm<<"\"!"<<endl;
          cerr<<"Infor: please refer to the pdl file \""<<evtPdlFlNm<<"\", find the TxtPnm for the Pid \""<<pid<<"\", and add the pair of Pid to TxtPnm in the data file \""<<pidTxtPnmDatFlNm<<"\"."<<endl<<endl;
        }
    }
  else if(pnmType=="TexPnm")
    {
      if(m_pidTexPnmMap.find(pid)!=m_pidTexPnmMap.end())
        {
          out<<m_pidTexPnmMap[pid]<<" ";
        }
      else
        {
          out<<"{\\color{red}{??}}"<<" ";
          string pidTexPnmDatFlNm=m_pkgPath+"core/pid_texpnm.dat";
          string pidPsymbPdfFlNm=m_pkgPath+"doc/pid_psymb.pdf";
          cerr<<"Error: The TexPnm for the Pid \""<<pid<<"\" does not exist in the data file \""<<pidTexPnmDatFlNm<<"\"!"<<endl;
          cerr<<"Infor: please refer to the pdf file \""<<pidPsymbPdfFlNm<<"\", find the TexPnm for the Pid \""<<pid<<"\", and add the pair of Pid to TexPnm in the data file \""<<pidTexPnmDatFlNm<<"\"."<<endl<<endl;
        }
    }
  else
    {
      cerr<<"Error: The pnmType \""<<pnmType<<"\" does not exist!"<<endl;
      cerr<<"Infor: Please check it in the cpp source file \"topoana.cpp\"."<<endl;
      exit(42);
    }
}

void topoana::sortByPidAndPchrg(vector<int> &via,vector<int> &vib,vector<int> &vic,vector<int> &vid)
{
  if(via.size()!=vib.size()||vib.size()!=vic.size())
    {
      cerr<<"Error: The three vectors have different sizes!"<<endl;
      cerr<<"Infor: The size of the first vector is "<<via.size()<<"."<<endl;
      cerr<<"Infor: The size of the second vector is "<<vib.size()<<"."<<endl;
      cerr<<"Infor: The size of the third vector is "<<vic.size()<<"."<<endl;
      cerr<<"Infor: Please check them."<<endl;
      exit(61);
    }
  if(via.size()==0)
    {
      cerr<<"Infor: The sizes of the three vectors are zero!"<<endl<<endl;
      return;
    }

  /*cout<<"Before sort:"<<endl;
  for(unsigned int i=0;i<via.size();i++)
    { 
      if(i<(via.size()-1)) cout<<via[i]<<" ";
      else cout<<via[i]<<endl;
    }
  for(unsigned int i=0;i<vib.size();i++)
    {
      if(i<(vib.size()-1)) cout<<vib[i]<<" ";
      else cout<<vib[i]<<endl;
    }*/

  int iaTmp,ibTmp,icTmp;
  for(unsigned int i=0;i<(via.size()-1);i++)
    for(unsigned int j=i+1;j<via.size();j++)
      {
        if(abs(via[i])>abs(via[j]))
          {
            if(abs(via[j])!=22)
              {
                iaTmp=via[i];
                via[i]=via[j];
                via[j]=iaTmp;
                ibTmp=vib[i];
                vib[i]=vib[j];
                vib[j]=ibTmp;
                icTmp=vic[i];
                vic[i]=vic[j];
                vic[j]=icTmp;
              }
          }
        else if(abs(via[i])==abs(via[j]))
          {
            if(m_pid3PchrgMap.find(via[i])!=m_pid3PchrgMap.end()&&m_pid3PchrgMap.find(via[j])!=m_pid3PchrgMap.end())
              {              
                if(m_pid3PchrgMap[via[i]]<m_pid3PchrgMap[via[j]])
                  {
                    iaTmp=via[i];
                    via[i]=via[j];
                    via[j]=iaTmp;
                    ibTmp=vib[i];
                    vib[i]=vib[j];
                    vib[j]=ibTmp;
                    icTmp=vic[i];
                    vic[i]=vic[j];
                    vic[j]=icTmp;
                  }
                else if(m_pid3PchrgMap[via[i]]==m_pid3PchrgMap[via[j]])
                  {
                    if(via[i]<via[j])
                      {
                        iaTmp=via[i];
                        via[i]=via[j];
                        via[j]=iaTmp;
                        ibTmp=vib[i];
                        vib[i]=vib[j];
                        vib[j]=ibTmp;
                        icTmp=vic[i];
                        vic[i]=vic[j];
                        vic[j]=icTmp;
                      }  
                  }
              }
            else
              {
                if(m_pid3PchrgMap.find(via[i])==m_pid3PchrgMap.end()) optErrInfOnPid3PchrgMap(via[i]);
                if(m_pid3PchrgMap.find(via[j])==m_pid3PchrgMap.end()) optErrInfOnPid3PchrgMap(via[j]);
              }
          }
        else
          {
            if(abs(via[i])==22)
              {
                iaTmp=via[i];
                via[i]=via[j];
                via[j]=iaTmp;
                ibTmp=vib[i];
                vib[i]=vib[j];
                vib[j]=ibTmp;
                icTmp=vic[i];
                vic[i]=vic[j];
                vic[j]=icTmp;
              }
          }
      }


  /*cout<<"After sort:"<<endl;
  for(unsigned int i=0;i<via.size();i++)
    {
      if(i<(via.size()-1)) cout<<via[i]<<" ";
      else cout<<via[i]<<endl;
    }
  for(unsigned int i=0;i<vib.size();i++)
    {
      if(i<(vib.size()-1)) cout<<vib[i]<<" ";
      else cout<<vib[i]<<endl;
    }*/

  vid.clear();
  int nSmPids;
  for(unsigned int i=0;i<via.size();i++)
    {
      nSmPids=count(via.begin(),via.end(),via[i]);
      vid.push_back(nSmPids);
      i=i+(nSmPids-1);
    }
  /*for(unsigned int i=0;i<vid.size();i++)
    {
      if(i<(vid.size()-1)) cout<<vid[i]<<" ";
      else cout<<vid[i]<<endl;
    }*/
}

void topoana::sortBySzPidAndPchrg(vector< vector<int> > &vVia,vector< vector<int> > &vVib,vector< vector<int> >&vVic,vector< vector<int> > &vVid)
{
  if(vVia.size()!=vVib.size()||vVib.size()!=vVic.size()||vVic.size()!=vVid.size())
    { 
      cerr<<"Error: The four vectors have different sizes!"<<endl;
      cerr<<"Infor: The size of the first vector is "<<vVia.size()<<"."<<endl;
      cerr<<"Infor: The size of the second vector is "<<vVib.size()<<"."<<endl;
      cerr<<"Infor: The size of the third vector is "<<vVic.size()<<"."<<endl;
      cerr<<"Infor: The size of the fourth vector is "<<vVid.size()<<"."<<endl;
      cerr<<"Infor: Please check them."<<endl;
      exit(62);
    }
  if(vVia.size()==0)
    { 
      cerr<<"Infor: The sizes of the four vectors are zero!"<<endl<<endl;
      return;
    }

  /*cout<<"Before sort:"<<endl;
  for(unsigned int i=0;i<vVia.size();i++)
    for(unsigned int j=0;j<vVia[i].size();j++)
      {
        if(j<(vVia[i].size()-1)) cout<<vVia[i][j]<<" ";
        else cout<<vVia[i][j]<<endl; 
      }*/

  bool exchOrd;
  vector<int> viaTmp,vibTmp,vicTmp,vidTmp;
  int ibTmp;
  for(unsigned int i=0;i<(vVia.size()-1);i++)
    for(unsigned int j=i+1;j<vVia.size();j++)
      {
        exchOrd=false;
        if(vVia[i].size()>vVia[j].size()) exchOrd=true;
        else if(vVia[i].size()==vVia[j].size())
          {
            for(unsigned int k=0;k<vVia[i].size();k++)
              {
                if(abs(vVia[i][k])>abs(vVia[j][k]))
                  {
                    if(abs(vVia[j][k])!=22)
                      {                    
                        exchOrd=true;
                        break;
                      }
                    else
                      {
                        break;
                      }
                  }
                else if(abs(vVia[i][k])==abs(vVia[j][k]))
                  {
                    if(m_pid3PchrgMap.find(vVia[i][k])!=m_pid3PchrgMap.end()&&m_pid3PchrgMap.find(vVia[j][k])!=m_pid3PchrgMap.end())
                      {              
                        if(m_pid3PchrgMap[vVia[i][k]]<m_pid3PchrgMap[vVia[j][k]])
                          {
                            exchOrd=true;        
                            break;
                          }
                        else if(m_pid3PchrgMap[vVia[i][k]]>m_pid3PchrgMap[vVia[j][k]])
                          {
                            break;
                          }
                        else
                          {
                            if(vVia[i][k]<vVia[j][k])
                              {
                                exchOrd=true;
                                break;
                              }
                            else if(vVia[i][k]>vVia[j][k])
                              {
                                break;
                              }
                          }                        
                      }
                    else
                      {
                        if(m_pid3PchrgMap.find(vVia[i][k])==m_pid3PchrgMap.end()) optErrInfOnPid3PchrgMap(vVia[i][k]);
                        if(m_pid3PchrgMap.find(vVia[j][k])==m_pid3PchrgMap.end()) optErrInfOnPid3PchrgMap(vVia[j][k]);
                      }                    
                  }
                else // Please don't forget this part of the if statement.
                  { 
                    if(abs(vVia[i][k])==22)
                      {
                        exchOrd=true;
                        break;
                      }
                    else
                      {
                        break;
                      }
                  }
              }
          }
        if(exchOrd==true)
          {
            viaTmp=vVia[i];
            vVia[i]=vVia[j];
            vVia[j]=viaTmp;

            ibTmp=vVib[i][0];
            for(unsigned int k=0;k<vVib[i].size();k++) vVib[i][k]=vVib[j][0];
            for(unsigned int k=0;k<vVib[j].size();k++) vVib[j][k]=ibTmp;

            vibTmp=vVib[i];
            vVib[i]=vVib[j];
            vVib[j]=vibTmp;

            vicTmp=vVic[i];
            vVic[i]=vVic[j];
            vVic[j]=vicTmp;

            vidTmp=vVid[i];
            vVid[i]=vVid[j];
            vVid[j]=vidTmp;             
          }        
      }
  
  /*cout<<"After sort:"<<endl;
  for(unsigned int i=0;i<vVia.size();i++)
    for(unsigned int j=0;j<vVia[i].size();j++)
      { 
        if(j<(vVia[i].size()-1)) cout<<vVia[i][j]<<" ";
        else cout<<vVia[i][j]<<endl;
      }*/
}

void topoana::sortPs(vector<int> & vPid,vector<int> & vMidx)
{
  if(vPid.size()!=vMidx.size())
    {
      cerr<<"Error: The two vectors vPid and vMidx have different sizes!"<<endl;
      cerr<<"Infor: The size of the vector vPid is "<<vPid.size()<<"."<<endl;
      cerr<<"Infor: The size of the vector vMidx is "<<vMidx.size()<<"."<<endl;
      cerr<<"Infor: Please check them."<<endl;
      exit(63);
    }

  /*cout<<"Before sort:"<<endl;
  for(unsigned int i=0;i<vPid.size();i++)
    {
      cout<<"Pid: "<<vPid[i]<<"\t"<<"Midx: "<<vMidx[i]<<endl;
    }*/

  vector<int> vPidFnl,vMidxFnl,vIdxFnl;
  vector<int> vPidOld,vMidxOld,vIdxOld,vNSmPidsOld;
  for(unsigned int i=0;i<vPid.size();i++)
    {
      //if(((unsigned int) vMidx[i])==i) Sometimes, users may set Midx[i] at -1 rather than i when the pid of the mother of the partilce i does not appear in the array Pid. Note that the arrays Pid and Midx are the branches stored in the tree of the input root files. In order to make the program can handle such cases as well, this statement is revised to be the following one.
      if((((unsigned int) vMidx[i])==i)||(vMidx[i]==-1))
	{
	  vPidOld.push_back(vPid[i]);
	  //vMidxOld.push_back(vMidx[i]); Sometimes, users may set Midx[i] at -1 rather than i when the pid of the mother of the partilce i does not appear in the array Pid. Note that the arrays Pid and Midx are the branches stored in the tree of the input root files. In order to make the program can handle such cases as well, this statement is revised to be the following one. Then, the following parts of the program do not have to change any more.
          vMidxOld.push_back(i);
	  vIdxOld.push_back(i);
	}
    }
  sortByPidAndPchrg(vPidOld,vMidxOld,vIdxOld,vNSmPidsOld);
  for(unsigned int i=0;i<vPidOld.size();i++)
    {
      vPidFnl.push_back(vPidOld[i]);
      vMidxFnl.push_back(vMidxOld[i]);
      vIdxFnl.push_back(vIdxOld[i]);
    }

  unsigned int nCmltSmPids;
  vector<int> vIdxYng,vNSmPidsYng;
  vector< vector<int> > vVPidYngSbst,vVMidxYngSbst,vVIdxYngSbst,vVNSmPidsYngSbst;
  vector<int> vPidYngSbst,vMidxYngSbst,vIdxYngSbst,vNSmPidsYngSbst;
  while(vIdxOld.size()!=0)
    {
      nCmltSmPids=0;
      vIdxYng.clear();
      vNSmPidsYng.clear();
      for(unsigned int i=0;i<vNSmPidsOld.size();i++)
        {
          vVPidYngSbst.clear();
          vVMidxYngSbst.clear();
          vVIdxYngSbst.clear();
          vVNSmPidsYngSbst.clear();
          for(unsigned int j=0;j<((unsigned int) vNSmPidsOld[i]);j++)
            {
              vPidYngSbst.clear();
              vMidxYngSbst.clear();
              vIdxYngSbst.clear();
              vNSmPidsYngSbst.clear();
              for(unsigned int k=0;k<vPid.size();k++)
	        {
                  //if((((unsigned int) vMidx[k])!=k)&&vMidx[k]==vIdxOld[nCmltSmPids+j]) Sometimes, users may set Midx[i] at -1 rather than i when the pid of the mother of the partilce i does not appear in the array Pid. Note that the arrays Pid and Midx are the branches stored in the tree of the input root files. In order to make the program can handle such cases as well, this statement is revised to be the following one.
                  if(((((unsigned int) vMidx[k])!=k)&&(vMidx[k]!=-1))&&vMidx[k]==vIdxOld[nCmltSmPids+j])
	            {
	              vPidYngSbst.push_back(vPid[k]);
	              vMidxYngSbst.push_back(vMidx[k]);
	              vIdxYngSbst.push_back(k);
	            }
	        }
              if(vPidYngSbst.size()>0)
                {
                  sortByPidAndPchrg(vPidYngSbst,vMidxYngSbst,vIdxYngSbst,vNSmPidsYngSbst);
                  // The following four statements should be put in the scope of the if statement, or empty vectors might be pushed back to these vectors of vector. 
                  vVPidYngSbst.push_back(vPidYngSbst);
                  vVMidxYngSbst.push_back(vMidxYngSbst);
                  vVIdxYngSbst.push_back(vIdxYngSbst);
                  vVNSmPidsYngSbst.push_back(vNSmPidsYngSbst);
                }
            }
        if(vVPidYngSbst.size()>1) sortBySzPidAndPchrg(vVPidYngSbst,vVMidxYngSbst,vVIdxYngSbst,vVNSmPidsYngSbst);
        for(unsigned int j=0;j<vVPidYngSbst.size();j++)
          {
            for(unsigned int k=0;k<vVPidYngSbst[j].size();k++)
	      {
	        vPidFnl.push_back(vVPidYngSbst[j][k]);
	        vMidxFnl.push_back(vVMidxYngSbst[j][k]);
                vIdxFnl.push_back(vVIdxYngSbst[j][k]);
	        vIdxYng.push_back(vVIdxYngSbst[j][k]);
	      }
            for(unsigned int k=0;k<vVNSmPidsYngSbst[j].size();k++)
              {
                vNSmPidsYng.push_back(vVNSmPidsYngSbst[j][k]);
              }            
          }
        nCmltSmPids=nCmltSmPids+vNSmPidsOld[i];
      }
      vIdxOld.clear();
      vIdxOld=vIdxYng;
      vNSmPidsOld.clear();
      vNSmPidsOld=vNSmPidsYng;
    }

  for(unsigned int i=0;i<vMidxFnl.size();i++)
    {
      for(unsigned int j=0;j<vMidxFnl.size();j++)
        {
          if(vIdxFnl[j]==vMidxFnl[i])
            {
              vMidxFnl[i]=j;
              break;
            }
        }
    }
  vPid.clear();
  vMidx.clear();
  vPid=vPidFnl;
  vMidx=vMidxFnl;

  /*cout<<"After sort:"<<endl;
  for(unsigned int i=0;i<vPid.size();i++)
    {
      cout<<"Pid: "<<vPid[i]<<"\t"<<"Midx: "<<vMidx[i]<<endl; 
    }*/
}

void topoana::getEvtTr(vector<int> vPid, vector<int> vMidx, vector< list<int> > & evtTr)
{
  evtTr.clear();
  list<int> evtBr;
  evtBr.clear();
  for(unsigned int i=0;i<vPid.size();i++)
    {
      if(((unsigned int) vMidx[i])==i) evtBr.push_back(vPid[i]);
    }
  evtBr.push_front(11);
  evtBr.push_front(-11);
  evtTr.push_back(evtBr);
  evtBr.clear();
  for(unsigned int i=0;i<vPid.size();i++)
    {
      for(unsigned int j=i+1;j<vPid.size();j++)
        {
          if(((unsigned int) vMidx[j])==i) evtBr.push_back(vPid[j]); 
        }
      if(evtBr.size()==0) continue; 
      if(abs(vPid[i])!=1&&abs(vPid[i])!=2&&abs(vPid[i])!=3&&abs(vPid[i])!=4&&abs(vPid[i])!=5&&abs(vPid[i])!=6)
        {
          evtBr.push_front(vPid[i]);
        }
      else
        {
          evtBr.push_front(-abs(vPid[i]));
          evtBr.push_front(abs(vPid[i]));    
        }
      evtTr.push_back(evtBr);
      evtBr.clear();
    }
}

void topoana::getEvtTr(vector<int> vPid, vector<int> vMidx, vector< list<int> > & evtTr, vector <int> & vIdxOfHead, vector<int> & vMidxOfHead)
{
  evtTr.clear();
  vIdxOfHead.clear();
  vMidxOfHead.clear();
  list<int> evtBr;
  evtBr.clear();
  for(unsigned int i=0;i<vPid.size();i++)
    {
      if(((unsigned int) vMidx[i])==i) evtBr.push_back(vPid[i]);
    }
  evtBr.push_front(11);
  evtBr.push_front(-11);
  evtTr.push_back(evtBr);
  vIdxOfHead.push_back(-1);
  vMidxOfHead.push_back(-1);
  evtBr.clear();
  for(unsigned int i=0;i<vPid.size();i++)
    {
      for(unsigned int j=i+1;j<vPid.size();j++)
        {
          if(((unsigned int) vMidx[j])==i) evtBr.push_back(vPid[j]); 
        }
      if(evtBr.size()==0) continue; 
      if(abs(vPid[i])!=1&&abs(vPid[i])!=2&&abs(vPid[i])!=3&&abs(vPid[i])!=4&&abs(vPid[i])!=5&&abs(vPid[i])!=6)
        {
          evtBr.push_front(vPid[i]);
        }
      else
        {
          evtBr.push_front(-abs(vPid[i]));
          evtBr.push_front(abs(vPid[i]));    
        }
      evtTr.push_back(evtBr);
      vIdxOfHead.push_back(i);
      vMidxOfHead.push_back(vMidx[i]);
      evtBr.clear();
    }
}

// Note that this algorithm does not necessarily preserve the original sequence orders of the particles of same identifications.
void topoana::sortByPidAndPchrg(list<int> &lia)
{
  if(lia.size()==0)
    {
      cerr<<"Infor: The size of the list is zero."<<endl<<endl;
      return;
    }
  int iaTmp;
  list<int>::iterator liait1;
  list<int>::iterator liait2;
  list<int>::iterator liaitLastButOne=lia.end();liaitLastButOne--;
  for(liait1=lia.begin();liait1!=liaitLastButOne;liait1++)
    for(liait2=liait1,liait2++;liait2!=lia.end();liait2++)
      {
        if(abs((*liait1))>abs((*liait2)))
          {
            if(abs((*liait2))!=22)
              {
                iaTmp=(*liait1);
                (*liait1)=(*liait2);
                (*liait2)=iaTmp;
              }
          }
        else if(abs((*liait1))==abs((*liait2)))
          {
            if(m_pid3PchrgMap.find((*liait1))!=m_pid3PchrgMap.end()&&m_pid3PchrgMap.find((*liait2))!=m_pid3PchrgMap.end())
              {
                if(m_pid3PchrgMap[(*liait1)]<m_pid3PchrgMap[(*liait2)])
                  {
                    iaTmp=(*liait1);
                    (*liait1)=(*liait2);
                    (*liait2)=iaTmp;
                  }
                else if(m_pid3PchrgMap[(*liait1)]==m_pid3PchrgMap[(*liait2)])
                  {
                    if((*liait1)<(*liait2))
                      {
                        iaTmp=(*liait1);
                        (*liait1)=(*liait2);
                        (*liait2)=iaTmp;
                      }
                  }
              }
            else
              {
                if(m_pid3PchrgMap.find((*liait1))==m_pid3PchrgMap.end()) optErrInfOnPid3PchrgMap((*liait1)); 
                if(m_pid3PchrgMap.find((*liait2))==m_pid3PchrgMap.end()) optErrInfOnPid3PchrgMap((*liait2));
              }
          }
        else
          {
            if(abs((*liait1))==22)
              {
                iaTmp=(*liait1);
                (*liait1)=(*liait2);
                (*liait2)=iaTmp;
              }
          }
      }
}

void  topoana::getEvtIFSts(vector<int> & vPid,vector<int> & vMidx,list<int> & evtIFSts)
{
  evtIFSts.clear();
  bool fsp;
  for(unsigned int i=0;i<vPid.size();i++)
    {
      fsp=true;
      for(unsigned int j=i+1;j<vPid.size();j++)
        {
          if(((unsigned int) vMidx[j])==i)
            {
              fsp=false;
              break;
	    }
        }
      if(fsp&&abs(vPid[i])!=1&&abs(vPid[i])!=2&&abs(vPid[i])!=3&&abs(vPid[i])!=4&&abs(vPid[i])!=5&&abs(vPid[i])!=6) evtIFSts.push_back(vPid[i]);
    }
  sortByPidAndPchrg(evtIFSts);
  evtIFSts.push_front(11);
  evtIFSts.push_front(-11);
}

unsigned int topoana::countPFSts(vector<int> & vPid,vector<int> & vMidx, list<int> pFSts)
{
  unsigned int nCount=0;
  list<int> pFStsTmp;
  vector<int> vIdx;
  vIdx.clear();
  list<int>::iterator liit=pFSts.begin();
  for(unsigned int i=0;i<vPid.size();i++)
    {
      if(vPid[i]==(*liit)) vIdx.push_back(i);
    }
  for(unsigned int i=0;i<vIdx.size();i++)
    {
      pFStsTmp.clear();
      for(unsigned int j=vIdx[i]+1;j<vPid.size();j++)
        {
          bool specifiedP=false;
          for(liit++;liit!=pFSts.end();liit++)
            {
              if(vPid[j]==(*liit)) specifiedP=true;
              break;
            }
          liit=pFSts.begin();
          bool fsp=true;
          if(specifiedP==false)
            {
              for(unsigned int k=j+1;k<vPid.size();k++)
                {
                  if(((unsigned int) vMidx[k])==j)
                    {
                      fsp=false;
                      break;
                    }
                }
            }
          bool descendantOfOneSpecifiedP=false;
          for(liit++;liit!=pFSts.end();liit++)
            {
              int k=j;
              while(1)
                {                     
                  if(vPid[vMidx[k]]==(*liit))
                    {
                      descendantOfOneSpecifiedP=true;
                      break;
                    }
                  else if(vMidx[k]==k||vMidx[k]==-1)
                    {
                      break;
                    }
                  else
                    {
                      k=vMidx[k];
                    }
                }
              if(descendantOfOneSpecifiedP==true) break;
            }
          liit=pFSts.begin();
          if((specifiedP==true||fsp==true)&&(descendantOfOneSpecifiedP==false))
            {
              bool fromTheP=false;
              int k=j;
              while(1)
                {
                  if(vMidx[k]==vIdx[i])
                    {
                      fromTheP=true;
                      break;
                    }
                  else if(vMidx[k]==k||vMidx[k]==-1)
                    {
                      break;
                    }
                  else
                    {
                      k=vMidx[k];
                    }
                }
              // The following condition "vPid[j]!=22" is exerted specially for the comparison without final state photons.
              if(fromTheP==true&&vPid[j]!=22) pFStsTmp.push_back(vPid[j]);
            } 
        }
     if(pFStsTmp.size()>0)
       {
         sortByPidAndPchrg(pFStsTmp);
         pFStsTmp.push_front((*liit));
         if(pFStsTmp==pFSts) nCount++;
       }
    }
  return nCount;
}

void topoana::readOpenCurly(ifstream & fin, string & line, string prompt)
{
  line="";
  while(!fin.eof())
    {
      getline(fin,line);
      trim(line);
      if(!line.empty()&&line[0]!='#') break;
    }
  if(line!="{")
   {
     cerr<<"Error: The open curly \"{\" related to the prompt \""<<prompt<<"\" is missing!"<<endl;
     exit(112);
   } 
}

void topoana::read1stLineOrCloseCurly(ifstream & fin, string & line, bool essential=true, string errinforprompt="")
{
  line="";
  while(!fin.eof())
    {
      getline(fin,line);
      trim(line);
      if(!line.empty()&&line[0]!='#') break;
    }       
  if(essential==true)
    {
      if(line.empty()||line[0]=='#'||line=="}"||line.substr(0,2)=="% ")
        {
          cerr<<"Error: "<<errinforprompt<<"\"!"<<endl;
          exit(111);
        }
    }  
  else
    {
      if(line.empty()||line[0]=='#'||line.substr(0,2)=="% ")
        {
          cerr<<"Error: The close curly \"}\" related to the prompt \""<<errinforprompt<<"\" is missing!"<<endl;
        }
    }
}

void topoana::readExtraLinesOrCloseCurly(ifstream & fin, string & line, string prompt)
{
  line="";
  while(!fin.eof())
    {
      getline(fin,line);
      trim(line);
      if(!line.empty()&&line[0]!='#') break;
    }
  if(line.empty()||line[0]=='#'||line.substr(0,2)=="% ")
    {
      cerr<<"Error: The close curly \"}\" related to the prompt \""<<prompt<<"\" is missing!"<<endl;
      exit(112);
    }
}

void topoana::readCloseCurly(ifstream & fin, string & line, string prompt)
{
  line="";
  while(!fin.eof())
    {
      getline(fin,line);
      trim(line);
      if(!line.empty()&&line[0]!='#') break;
    }
  if(line!="}")
    {
      cerr<<"Error: The close curly bracket \"}\" related to the prompt \""<<prompt<<"\" is missing!"<<endl;
      exit(114);
    }
}

void topoana::readCard(string topoAnaCardFlNm)
{
  m_nmsOfIptRootFls.clear();
  m_vSigPid.clear();
  m_vVSigPid2.clear();
  m_vVSigMidx2.clear();
  m_vVSigPid4.clear();
  m_vVSigMidx4.clear();
  m_vVSigPid5.clear();

  ifstream fin(topoAnaCardFlNm.c_str(),ios::in);
  if(!fin)
    {
      cerr<<"Error: Can't open the card file \""<<topoAnaCardFlNm<<"\"!"<<endl;
      if(topoAnaCardFlNm=="topoana.card")
        {
          cerr<<"Infor: The card file name is the default one."<<endl;
          cerr<<"Infor: Do you forget to append the name of your own card file to the end of the executable?"<<endl;
          cerr<<"Infor: If yes, please specify it along with the executable by the command line \"pathOfTheExecutable/topoana.exe nameOfyourOwnCardFile\""<<endl;
        }
      else
        {
          cerr<<"Infor: Please check it."<<endl;
        }
      exit(13);
    }  
  string line="";
  while(!fin.eof())      
    {
      while(!fin.eof())
        {
          getline(fin,line);
          trim(line);
          if(!line.empty()&&line[0]!='#') break;
        }
      if(line.empty()||line[0]=='#')
        {
          break;
        }
      else if(line=="% Names of input root files")
        {
          readOpenCurly(fin,line,"% Names of input root files");
          read1stLineOrCloseCurly(fin,line,true,"There are not root file names related to the prompt \"% Names of input root files");
          m_nmsOfIptRootFls.push_back(line);
          while(1)
            {
              readExtraLinesOrCloseCurly(fin,line,"% Names of input root files");
              if(line=="}")
                {
                  break;
                }
              else 
                {
                  m_nmsOfIptRootFls.push_back(line);
                }
            }
	}
      else if(line=="% Tree name")
        {
          readOpenCurly(fin,line,"% Tree name");
          read1stLineOrCloseCurly(fin,line,true,"There is not a tree name related to the prompt \"% Tree name");
          m_trNm=line;
          readCloseCurly(fin,line,"% Tree name");
        }
      else if(line=="% Branch name of the number of particles")
        {
          readOpenCurly(fin,line,"% Branch name of the number of particles");
          read1stLineOrCloseCurly(fin,line,true,"There is not a branch name of the number of particles related to the prompt \"% Branch name of the number of particles");
          m_brNmOfNps=line;
          readCloseCurly(fin,line,"% Branch name of the number of particles");
        }
      else if(line=="% Branch name of the array of particle identifications")
        {
          readOpenCurly(fin,line,"% Branch name of the array of particle identifications");
          read1stLineOrCloseCurly(fin,line,true,"There is not a branch name of the array of particle identifications related to the prompt \"% Branch name of the array of particle identifications");
          m_brNmOfPid=line;
          readCloseCurly(fin,line,"% Branch name of the array of particle identifications");     
        }
      else if(line=="% Branch name of the array of the mother indeces of particles")
        {
          readOpenCurly(fin,line,"% Branch name of the array of the mother indeces of particles");
          read1stLineOrCloseCurly(fin,line,true,"There is not a branch name of the array of the mother indeces of particles related to the prompt \"% Branch name of the array of the mother indeces of particles");
          m_brNmOfMidx=line;
          readCloseCurly(fin,line,"% Branch name of the array of the mother indeces of particles");  
        }
      else if(line=="% Main name of output files")
        {
          readOpenCurly(fin,line,"% Main name of output files");
          read1stLineOrCloseCurly(fin,line,true,"There is not a main file name related to the prompt \"% Main name of output files");
          m_mainNmOfOptFls=line;
          readCloseCurly(fin,line,"% Main name of output files");
        }
      else if(line=="% Signal particles")
        {
          readOpenCurly(fin,line,"% Signal particles");
          read1stLineOrCloseCurly(fin,line,false,"% Signal particles");
          if(line!="}")
            {
              int sigPid=getPidFromTxtPnm(line);
              m_vSigPid.push_back(sigPid);
              while(1)
                {
                  readExtraLinesOrCloseCurly(fin,line,"% Signal particles");
                  if(line=="}")
                    {
                      break;
                    }
                  else 
                    {
                      sigPid=getPidFromTxtPnm(line);
                      m_vSigPid.push_back(sigPid);
                    }
                }
            }
	}      
      else if(line=="% Signal inclusive event branches")
        {
          readOpenCurly(fin,line,"% Signal inclusive event branches");
          read1stLineOrCloseCurly(fin,line,false,"% Signal inclusive event branches");
          if(line!="}")
            {
              istringstream iss;
              iss.clear();
              int sigIdx1;
              vector<int> vSigPid1;
              vSigPid1.clear();
              string sigTxtPnm1;
              int sigPid1;
              iss.str(line);
              iss>>sigIdx1>>sigTxtPnm1;
              sigPid1=getPidFromTxtPnm(sigTxtPnm1);
              vSigPid1.push_back(sigPid1);
              iss.clear();
              while(1)
                {
                  readExtraLinesOrCloseCurly(fin,line,"% Signal inclusive event branches");
                  if(line=="}")
                    {
                      m_vVSigPid1.push_back(vSigPid1);
                      vSigPid1.clear();
                      break;
                    }
                  else
                    {
                      iss.str(line);
                      iss>>sigIdx1>>sigTxtPnm1;
                      if(sigIdx1==0)
                        {
                          m_vVSigPid1.push_back(vSigPid1);
                          vSigPid1.clear();
                        }
                      sigPid1=getPidFromTxtPnm(sigTxtPnm1);
                      vSigPid1.push_back(sigPid1);
                      iss.clear();
                    }
                }
            }
	}
      else if(line=="% Signal sequential event branches")
        {
          readOpenCurly(fin,line,"% Signal sequential event branches");
          read1stLineOrCloseCurly(fin,line,false,"% Signal sequential event branches");
          if(line!="}")
            {
              istringstream iss;
              iss.clear();
              int sigIdx2;
              vector<int> vSigPid2;
              vSigPid2.clear();
              string sigTxtPnm2;
              int sigPid2;
              vector<int> vSigMidx2;
              vSigMidx2.clear();
              int sigMidx2;
              iss.str(line);
              iss>>sigIdx2>>sigTxtPnm2>>sigMidx2;
              sigPid2=getPidFromTxtPnm(sigTxtPnm2);
              vSigPid2.push_back(sigPid2);
              vSigMidx2.push_back(sigMidx2);
              iss.clear();
              while(1)
                {
                  readExtraLinesOrCloseCurly(fin,line,"% Signal sequential event branches");
                  if(line=="}")
                    {
                      m_vVSigPid2.push_back(vSigPid2);
                      vSigPid2.clear();
                      m_vVSigMidx2.push_back(vSigMidx2);
                      vSigMidx2.clear();
                      break;
                    }
                  else
                    {
                      iss.str(line);
                      iss>>sigIdx2>>sigTxtPnm2>>sigMidx2;
                      if(sigIdx2==0)
                        {
                          m_vVSigPid2.push_back(vSigPid2);
                          vSigPid2.clear();
                          m_vVSigMidx2.push_back(vSigMidx2);
                          vSigMidx2.clear();
                        }
                      sigPid2=getPidFromTxtPnm(sigTxtPnm2);
                      vSigPid2.push_back(sigPid2);
                      vSigMidx2.push_back(sigMidx2);
                      iss.clear();
                    }
                }
            }
	}
      else if(line=="% Signal particle final states")
        {
          readOpenCurly(fin,line,"% Signal particle final states");          
          read1stLineOrCloseCurly(fin,line,false,"% Signal particle final states");
          if(line!="}")
            {
              istringstream iss;
              iss.clear();
              int sigIdx3;
              vector<int> vSigPid3;
              vSigPid3.clear();
              string sigTxtPnm3;
              int sigPid3;
              iss.str(line);
              iss>>sigIdx3>>sigTxtPnm3;
              sigPid3=getPidFromTxtPnm(sigTxtPnm3);
              vSigPid3.push_back(sigPid3);
              iss.clear();
              while(1)
                {
                  readExtraLinesOrCloseCurly(fin,line,"% Signal particle final states");
                  if(line=="}")
                    {
                      m_vVSigPid3.push_back(vSigPid3);
                      vSigPid3.clear();
                      break;
                    }
                  else
                    {
                      iss.str(line);
                      iss>>sigIdx3>>sigTxtPnm3;
                      if(sigIdx3==0)
                        {
                          m_vVSigPid3.push_back(vSigPid3);
                          vSigPid3.clear();
                        }
                      sigPid3=getPidFromTxtPnm(sigTxtPnm3);
                      vSigPid3.push_back(sigPid3);
                      iss.clear();
                    }
                }
            }
	}
      else if(line=="% Signal event trees")
        {
          readOpenCurly(fin,line,"% Signal event trees");
          read1stLineOrCloseCurly(fin,line,false,"% Signal event trees");
          if(line!="}")
            {
              istringstream iss;
              iss.clear();
              int sigIdx4;
              vector<int> vSigPid4;
              vSigPid4.clear();
              string sigTxtPnm4;
              int sigPid4;
              vector<int> vSigMidx4;
              vSigMidx4.clear();
              int sigMidx4;
              iss.str(line);
              iss>>sigIdx4>>sigTxtPnm4>>sigMidx4;
              sigPid4=getPidFromTxtPnm(sigTxtPnm4);
              vSigPid4.push_back(sigPid4);
              vSigMidx4.push_back(sigMidx4);
              iss.clear();
              while(1)
                {
                  readExtraLinesOrCloseCurly(fin,line,"% Signal event trees");
                  if(line=="}")
                    {
                      m_vVSigPid4.push_back(vSigPid4);
                      vSigPid4.clear();
                      m_vVSigMidx4.push_back(vSigMidx4);
                      vSigMidx4.clear();
                      break;
                    }
                  else
                    {
                      iss.str(line);
                      iss>>sigIdx4>>sigTxtPnm4>>sigMidx4;
                      if(sigIdx4==0)
                        {
                          m_vVSigPid4.push_back(vSigPid4);
                          vSigPid4.clear();
                          m_vVSigMidx4.push_back(vSigMidx4);
                          vSigMidx4.clear();
                        }
                      sigPid4=getPidFromTxtPnm(sigTxtPnm4);
                      vSigPid4.push_back(sigPid4);
                      vSigMidx4.push_back(sigMidx4);
                      iss.clear();
                    }
                }
            }
	}
      else if(line=="% Signal event final states")
        {
          readOpenCurly(fin,line,"% Signal event final states");
          read1stLineOrCloseCurly(fin,line,false,"% Signal event final states");
          if(line!="}")
            {
              istringstream iss;
              iss.clear();
              int sigIdx5;
              vector<int> vSigPid5;
              vSigPid5.clear();
              string sigTxtPnm5;
              int sigPid5;
              iss.str(line);
              iss>>sigIdx5>>sigTxtPnm5;
              sigPid5=getPidFromTxtPnm(sigTxtPnm5);
              vSigPid5.push_back(sigPid5);
              iss.clear();
              while(1)
                {
                  readExtraLinesOrCloseCurly(fin,line,"% Signal event final states");
                  if(line=="}")
                    {
                      m_vVSigPid5.push_back(vSigPid5);
                      vSigPid5.clear();
                      break;
                    }
                  else
                    {
                      iss.str(line);
                      iss>>sigIdx5>>sigTxtPnm5;
                      if(sigIdx5==0)
                        {
                          m_vVSigPid5.push_back(vSigPid5);
                          vSigPid5.clear();
                        }
                      sigPid5=getPidFromTxtPnm(sigTxtPnm5);
                      vSigPid5.push_back(sigPid5);
                      iss.clear();
                    }
                }
            }
	}
      else if(line=="% Maximum number of events to be processed")
        {
          readOpenCurly(fin,line,"% Maximum number of events to be processed");
          read1stLineOrCloseCurly(fin,line,false,"% Maximum number of events to be processed");
          if(line!="}")
            {
              istringstream iss;
              iss.clear();
              iss.str(line);
              iss>>m_nEvtsMax;
              readCloseCurly(fin,line,"% Maximum number of events to be processed");
            }
        }
      else if(line=="% Cut to select events")
        {
          readOpenCurly(fin,line,"% Cut to select events");
          read1stLineOrCloseCurly(fin,line,false,"% Cut to select events");
          if(line!="}")
            {
              m_cut=line;
              readCloseCurly(fin,line,"% Cut to select events");
            }
        }
      else
        {
          cerr<<"Error: The input line "<<line<<"\" is invalid!"<<endl;
          exit(135);
        }
    }

  cout<<"The parameters set in the card file \""<<topoAnaCardFlNm<<"\" are as follows:"<<endl<<endl;

  if(m_nmsOfIptRootFls.size()==0)
    {
      cerr<<"Error: The names of input root files do not exist!"<<endl;
      exit(136);
    }
  else
    {
      cout<<"Names of input root files:"<<endl<<endl;
      for(unsigned int i=0;i<m_nmsOfIptRootFls.size();i++)
        {
          cout<<"  "<<m_nmsOfIptRootFls[i]<<endl;
        }
      cout<<endl;

      bool hasWildcards=false;
      TString * nmOfIptRootFl;
      for(unsigned int i=0;i<m_nmsOfIptRootFls.size();i++)
        {
          nmOfIptRootFl=new TString(m_nmsOfIptRootFls[i]);
          if(nmOfIptRootFl->MaybeWildcard())
            {
              hasWildcards=true;
              delete nmOfIptRootFl;
              break;
            }
          else
            {
              delete nmOfIptRootFl;
            }
        }
      if(hasWildcards==true)
        {
          cout<<"With the wildcards parsed:"<<endl<<endl;
          TChain * chn=new TChain(m_trNm.c_str());
          for(unsigned int i=0;i<m_nmsOfIptRootFls.size();i++)
            {
              chn->Add(m_nmsOfIptRootFls[i].c_str());
            }
          TObjArray * objArray=chn->GetListOfFiles();
          TIter next(objArray);
          TChainElement * chnElmt=0;
          unsigned int nCmltFls=0;
          while((chnElmt=(TChainElement *) next()))
            {
              cout<<"  "<<chnElmt->GetTitle()<<endl;
              nCmltFls++;
            }
          if(nCmltFls>0)
            {
              cout<<endl<<"In total, "<<nCmltFls<<" files match the names listed above."<<endl<<endl;
            }
          else
            {
              cerr<<"Error: No valid input root files match the names listed above!"<<endl;
              exit(137);
            }
        }
    }

  if(m_trNm.empty())
    {
      cerr<<"Error: The tree name is empty!"<<endl;
      exit(138);
    }
  else
    {
      cout<<"Tree name: "<<m_trNm<<endl<<endl;
    }

  if(m_brNmOfNps.empty())
    {
      cerr<<"Error: The branch name of the number of particles is empty!"<<endl;
      exit(139);
    }
  else
    {
      cout<<"Branch name of the number of particles: "<<m_brNmOfNps<<endl<<endl;
    }

  if(m_brNmOfPid.empty())
    {
      cerr<<"Error: The branch name of the array of particle identifications is empty!"<<endl;
      exit(140);
    }
  else
    {
      cout<<"Branch name of the array of particle identifications: "<<m_brNmOfPid<<endl<<endl;
    }

  if(m_brNmOfMidx.empty())
    {
      cerr<<"Error: The branch name of the array of the mother indeces of particles is empty!"<<endl;
      exit(141);
    }
  else
    {
      cout<<"Branch name of the array of the mother indeces of particles: "<<m_brNmOfMidx<<endl<<endl;
    }

  TChain * chn=new TChain(m_trNm.c_str());
  for(unsigned int i=0;i<m_nmsOfIptRootFls.size();i++)
    {
      chn->Add(m_nmsOfIptRootFls[i].c_str());
    }

  bool allIptsAreOK=true;
  TObjArray * objArray=chn->GetListOfFiles();
  TIter next(objArray);
  TChainElement * chnElmt=0;
  while((chnElmt=(TChainElement *) next()))
    {
      TFile * fl=new TFile(chnElmt->GetTitle());
      if(fl->IsZombie())
        {
          cerr<<"Error: The input root file \""<<chnElmt->GetTitle()<<"\" is zombie!"<<endl<<endl;
          allIptsAreOK=false;
        }
      else
        {
          TTree * tr=(TTree *) fl->Get(m_trNm.c_str());
          if(!tr)
            {
              cerr<<"Error: The input root file \""<<chnElmt->GetTitle()<<"\" does not contain a tree named \""<<m_trNm<<"\"!"<<endl<<endl;
              allIptsAreOK=false;
            }
          else
            {
              TBranch * br0=tr->FindBranch(m_brNmOfNps.c_str());
              if(!br0)
                {
                  cerr<<"Error: The tree \""<<m_trNm<<"\" in the input root file \""<<chnElmt->GetTitle()<<"\" does not contain a branch named \""<<m_brNmOfNps<<"\"!"<<endl<<endl;
                  allIptsAreOK=false;
                }
              TBranch * br1=tr->FindBranch(m_brNmOfPid.c_str());
              if(!br1)
                {
                  cerr<<"Error: The tree \""<<m_trNm<<"\" in the input root file \""<<chnElmt->GetTitle()<<"\" does not contain a branch named \""<<m_brNmOfPid<<"\"!"<<endl<<endl;
                  allIptsAreOK=false;
                }
              TBranch * br2=tr->FindBranch(m_brNmOfMidx.c_str());
              if(!br2)
                {
                  cerr<<"Error: The tree \""<<m_trNm<<"\" in the input root file \""<<chnElmt->GetTitle()<<"\" does not contain a branch named \""<<m_brNmOfMidx<<"\"!"<<endl<<endl;
                  allIptsAreOK=false;
                }
            }
          delete fl;
        }
    }
  if(!allIptsAreOK) exit(142);
  delete chn;

  if(m_mainNmOfOptFls.empty())
    {
      cerr<<"Error: The main name of output files is empty!"<<endl;
      exit(143);
    }
  else
    {
      cout<<"Main name of output files: "<<m_mainNmOfOptFls<<endl<<endl;
    }

  if(m_vSigPid.size()==0)
    {
      cout<<"There are not signal particles."<<endl<<endl;
    }
  else
    {
      cout<<"Signal particles:"<<endl<<endl;
      for(unsigned int i=0;i<m_vSigPid.size();i++)
        {
          cout<<" ";
          optPnmFromPid(cout,"TxtPnm",m_vSigPid[i]);
          cout<<endl;
        }
      cout<<endl;

      m_vISigP.clear();
      m_vNSigP.clear();
      for(unsigned int i=0;i<m_vSigPid.size();i++)
        { 
          m_vISigP.push_back(i);
          m_vNSigP.push_back(0);
        }
    }

  if(m_vVSigPid1.size()==0)
    {
      cout<<"There are not signal inclusive event branches."<<endl<<endl;
    }
  else
    {
      cout<<"Signal inclusive event branches:"<<endl<<endl;
      for(unsigned int i=0;i<m_vVSigPid1.size();i++)
	{
          for(unsigned int j=0;j<m_vVSigPid1[i].size();j++)
	    {
	      cout<<"  "<<j<<"\t";
              optPnmFromPid(cout,"TxtPnm",m_vVSigPid1[i][j]);
              cout<<endl;
	    }
          cout<<endl;
	}

      m_vSigIncEvtBr.clear();
      list<int> sigIncEvtBr;
      m_vISigIncEvtBr.clear();
      m_vNSigIncEvtBr.clear();
      for(unsigned int i=0;i<m_vVSigPid1.size();i++)
        {
          sigIncEvtBr.clear();
          for(unsigned int j=1;j<m_vVSigPid1[i].size();j++) sigIncEvtBr.push_back(m_vVSigPid1[i][j]);
          sortByPidAndPchrg(sigIncEvtBr);
          sigIncEvtBr.push_front(m_vVSigPid1[i][0]);

          string ordNumSufi="th";
          string ordNumSufj="th";
          for(unsigned int j=0;j<m_vSigIncEvtBr.size();j++)
            {
              if(sigIncEvtBr==m_vSigIncEvtBr[j])
                {
                  if(i==0) ordNumSufi="st"; else if(i==1) ordNumSufi="nd"; else if(i==2) ordNumSufi="rd";
                  if(j==0) ordNumSufj="st"; else if(j==1) ordNumSufj="nd"; else if(j==2) ordNumSufj="rd";
                  cerr<<"Error: The "<<i+1<<ordNumSufi<<" signal inclusive event branch is same as the "<<j+1<<ordNumSufj<<" signal inclusive event branch!"<<endl;
                  cerr<<"Infor: Please check the input card and remove one of them."<<endl;
                  exit(146);
                }
            }
          m_vSigIncEvtBr.push_back(sigIncEvtBr);
          m_vISigIncEvtBr.push_back(m_vSigIncEvtBr.size()-1);
          m_vNSigIncEvtBr.push_back(0);
        }

      cout<<"i.e.:"<<endl<<endl;
      for(unsigned int i=0;i<m_vSigIncEvtBr.size();i++)
        {
          sigIncEvtBr.clear();
          sigIncEvtBr=m_vSigIncEvtBr[i];
          cout<<" ";
          list<int>::iterator liit=sigIncEvtBr.begin();
          optPnmFromPid(cout,"TxtPnm",(*liit));
          cout<<" -->";
          for(liit++;liit!=sigIncEvtBr.end();liit++) optPnmFromPid(cout,"TxtPnm",(*liit));
          cout<<" + anything";
          cout<<endl<<endl;
        }
    }

  if(m_vVSigPid2.size()==0)
    {
      cout<<"There are not signal sequential event branches."<<endl<<endl;
    }
  else
    {
      cout<<"Signal sequential event branches:"<<endl<<endl;
      for(unsigned int i=0;i<m_vVSigPid2.size();i++)
	{
          for(unsigned int j=0;j<m_vVSigPid2[i].size();j++)
	    {
	      cout<<"  "<<j<<"\t";
              optPnmFromPid(cout,"TxtPnm",m_vVSigPid2[i][j]);
              if(m_pidTxtPnmMap[m_vVSigPid2[i][j]].size()<7)  cout<<"\t\t\t";
              else if(m_pidTxtPnmMap[m_vVSigPid2[i][j]].size()<15) cout<<"\t\t";
              else cout<<"\t";
              cout<<setiosflags(ios::right)<<setw(3)<<m_vVSigMidx2[i][j]<<resetiosflags(ios::adjustfield)<<endl;
	    }
          cout<<endl;
	}

      m_vSigSeqEvtBrs.clear();
      vector< list<int> > sigSeqEvtBrs;
      m_vVSigIdxOfHead.clear();
      vector<int> vSigIdxOfHead;
      m_vVSigMidxOfHead.clear();
      vector<int> vSigMidxOfHead;
      m_vISigSeqEvtBrs.clear();
      m_vNSigSeqEvtBrs.clear();
      for(unsigned int i=0;i<m_vVSigPid2.size();i++)
        {
          sortPs(m_vVSigPid2[i],m_vVSigMidx2[i]);
          sigSeqEvtBrs.clear();      
          vSigIdxOfHead.clear();
          vSigMidxOfHead.clear();
          getEvtTr(m_vVSigPid2[i],m_vVSigMidx2[i],sigSeqEvtBrs,vSigIdxOfHead,vSigMidxOfHead);
          sigSeqEvtBrs.erase(sigSeqEvtBrs.begin());
          vSigIdxOfHead.erase(vSigIdxOfHead.begin());
          vSigMidxOfHead.erase(vSigMidxOfHead.begin());
          string ordNumSufi="th";
          string ordNumSufj="th";
          for(unsigned int j=0;j<m_vSigSeqEvtBrs.size();j++)
            {
              if(sigSeqEvtBrs==m_vSigSeqEvtBrs[j])
                {
                  if(i==0) ordNumSufi="st"; else if(i==1) ordNumSufi="nd"; else if(i==2) ordNumSufi="rd";
                  if(j==0) ordNumSufj="st"; else if(j==1) ordNumSufj="nd"; else if(j==2) ordNumSufj="rd";
                  cerr<<"Error: The "<<i+1<<ordNumSufi<<" signal sequential event branches is same as the "<<j+1<<ordNumSufj<<" signal sequential event branches!"<<endl;
                  cerr<<"Infor: Please check the input card and remove one of them."<<endl;
                  exit(144);    
                }
            }
          m_vSigSeqEvtBrs.push_back(sigSeqEvtBrs);
          m_vVSigIdxOfHead.push_back(vSigIdxOfHead);
          m_vVSigMidxOfHead.push_back(vSigMidxOfHead);
          m_vISigSeqEvtBrs.push_back(m_vSigSeqEvtBrs.size()-1);
          m_vNSigSeqEvtBrs.push_back(0);
        }

      cout<<"i.e.:"<<endl<<endl;
      list<int> sigEvtBr;
      for(unsigned int i=0;i<m_vSigSeqEvtBrs.size();i++)
        { 
          sigSeqEvtBrs.clear();
          sigSeqEvtBrs=m_vSigSeqEvtBrs[i];
          for(unsigned int j=0;j<sigSeqEvtBrs.size();j++)
            {
              sigEvtBr.clear();
              sigEvtBr=sigSeqEvtBrs[j];
              cout<<" ";
              list<int>::iterator liit=sigEvtBr.begin();
              optPnmFromPid(cout,"TxtPnm",(*liit));
              cout<<" -->";
              for(liit++;liit!=sigEvtBr.end();liit++) optPnmFromPid(cout,"TxtPnm",(*liit));
              cout<<endl;
            }
          cout<<endl;
        }
    }

  if(m_vVSigPid3.size()==0)
    {
      cout<<"There are not signal particle final states."<<endl<<endl;
    }
  else
    {
      cout<<"Signal particle final states:"<<endl<<endl;
      for(unsigned int i=0;i<m_vVSigPid3.size();i++)
	{
          for(unsigned int j=0;j<m_vVSigPid3[i].size();j++)
	    {
	      cout<<"  "<<j<<"\t";
              optPnmFromPid(cout,"TxtPnm",m_vVSigPid3[i][j]);
              cout<<endl;
	    }
          cout<<endl;
	}

      m_vSigPFSts.clear();
      list<int> sigPFSts;
      m_vISigPFSts.clear();
      m_vNSigPFSts.clear();
      for(unsigned int i=0;i<m_vVSigPid3.size();i++)
        {
          sigPFSts.clear();
          for(unsigned int j=1;j<m_vVSigPid3[i].size();j++) sigPFSts.push_back(m_vVSigPid3[i][j]);
          sortByPidAndPchrg(sigPFSts);
          sigPFSts.push_front(m_vVSigPid3[i][0]);

          string ordNumSufi="th";
          string ordNumSufj="th";
          for(unsigned int j=0;j<m_vSigPFSts.size();j++)
            {
              if(sigPFSts==m_vSigPFSts[j])
                {
                  if(i==0) ordNumSufi="st"; else if(i==1) ordNumSufi="nd"; else if(i==2) ordNumSufi="rd";
                  if(j==0) ordNumSufj="st"; else if(j==1) ordNumSufj="nd"; else if(j==2) ordNumSufj="rd";
                  cerr<<"Error: The "<<i+1<<ordNumSufi<<" signal particle final state is same as the "<<j+1<<ordNumSufj<<" signal particle final state!"<<endl;
                  cerr<<"Infor: Please check the input card and remove one of them."<<endl;
                  exit(146);
                }
            }
          m_vSigPFSts.push_back(sigPFSts);
          m_vISigPFSts.push_back(m_vSigPFSts.size()-1);
          m_vNSigPFSts.push_back(0);
        }

      cout<<"i.e.:"<<endl<<endl;
      for(unsigned int i=0;i<m_vSigPFSts.size();i++)
        {
          sigPFSts.clear();
          sigPFSts=m_vSigPFSts[i];
          cout<<" ";
          list<int>::iterator liit=sigPFSts.begin();
          optPnmFromPid(cout,"TxtPnm",(*liit));
          cout<<" -->";
          for(liit++;liit!=sigPFSts.end();liit++) optPnmFromPid(cout,"TxtPnm",(*liit));
          cout<<endl<<endl;
        }
    }

  if(m_vVSigPid4.size()==0)
    {
      cout<<"There are not signal event trees."<<endl<<endl;
    }
  else
    {
      cout<<"Signal event trees:"<<endl<<endl;
      for(unsigned int i=0;i<m_vVSigPid4.size();i++)
	{
          for(unsigned int j=0;j<m_vVSigPid4[i].size();j++)
	    {
	      cout<<"  "<<j<<"\t";
              optPnmFromPid(cout,"TxtPnm",m_vVSigPid4[i][j]);
              if(m_pidTxtPnmMap[m_vVSigPid4[i][j]].size()<7)  cout<<"\t\t\t";
              else if(m_pidTxtPnmMap[m_vVSigPid4[i][j]].size()<15) cout<<"\t\t";
              else cout<<"\t";
              cout<<setiosflags(ios::right)<<setw(3)<<m_vVSigMidx4[i][j]<<resetiosflags(ios::adjustfield)<<endl;
	    }
          cout<<endl;
	}

      m_vSigEvtTr.clear();
      vector< list<int> > sigEvtTr;
      m_vISigEvtTr.clear();
      m_vNSigEvtTr.clear();
      m_vSigEvtIFSts.clear();
      list<int> sigEvtIFSts;
      m_vISigEvtIFSts.clear();
      m_vNSigEvtIFSts.clear();
      m_iSigEvtTrISigEvtIFStsMap.clear();
      for(unsigned int i=0;i<m_vVSigPid4.size();i++)
        {
          sortPs(m_vVSigPid4[i],m_vVSigMidx4[i]);
          sigEvtTr.clear();      
          getEvtTr(m_vVSigPid4[i],m_vVSigMidx4[i],sigEvtTr);
          sigEvtIFSts.clear();
          getEvtIFSts(m_vVSigPid4[i],m_vVSigMidx4[i],sigEvtIFSts);
          string ordNumSufi="th";
          string ordNumSufj="th";
          for(unsigned int j=0;j<m_vSigEvtTr.size();j++)
            {
              if(sigEvtTr==m_vSigEvtTr[j])
                {
                  if(i==0) ordNumSufi="st"; else if(i==1) ordNumSufi="nd"; else if(i==2) ordNumSufi="rd";
                  if(j==0) ordNumSufj="st"; else if(j==1) ordNumSufj="nd"; else if(j==2) ordNumSufj="rd";
                  cerr<<"Error: The "<<i+1<<ordNumSufi<<" signal event tree is same as the "<<j+1<<ordNumSufj<<" signal event tree!"<<endl;
                  cerr<<"Infor: Please check the input card and remove one of them."<<endl;
                  exit(145);    
                }
            }
          m_vSigEvtTr.push_back(sigEvtTr);
          m_vISigEvtTr.push_back(m_vSigEvtTr.size()-1);
          m_vNSigEvtTr.push_back(0);          

          bool newSigEvtIFSts=true;
          int whichEvtIFSts;
          for(unsigned int j=0;j<m_vSigEvtIFSts.size();j++)
            {
              if(sigEvtIFSts==m_vSigEvtIFSts[j])
                {
                  if(i==0) ordNumSufi="st"; else if(i==1) ordNumSufi="nd"; else if(i==2) ordNumSufi="rd";
                  if(j==0) ordNumSufj="st"; else if(j==1) ordNumSufj="nd"; else if(j==2) ordNumSufj="rd";
                  cerr<<"Infor: The final state of the "<<i+1<<ordNumSufi<<" signal event tree is same as that of the "<<j+1<<ordNumSufj<<" signal event tree."<<endl<<endl;
                  newSigEvtIFSts=false;
                  whichEvtIFSts=j;
                  break;
                }
            }
          if(newSigEvtIFSts)
            {
              m_vSigEvtIFSts.push_back(sigEvtIFSts);
              m_vISigEvtIFSts.push_back(m_vSigEvtIFSts.size()-1);
              m_vNSigEvtIFSts.push_back(0);
              m_iSigEvtTrISigEvtIFStsMap[m_vSigEvtTr.size()-1]=m_vSigEvtIFSts.size()-1;
            }
          else
            {
              m_iSigEvtTrISigEvtIFStsMap[m_vSigEvtTr.size()-1]=whichEvtIFSts;
            }
        }

      cout<<"With the initial e+ e-:"<<endl<<endl;
      list<int> sigEvtBr;
      for(unsigned int i=0;i<m_vSigEvtTr.size();i++)
        { 
          sigEvtTr.clear();
          sigEvtTr=m_vSigEvtTr[i];
          for(unsigned int j=0;j<sigEvtTr.size();j++)
            {
              sigEvtBr.clear();
              sigEvtBr=sigEvtTr[j];
              cout<<" ";
              list<int>::iterator liit=sigEvtBr.begin();
              optPnmFromPid(cout,"TxtPnm",(*liit));
              // The condition "j==0" is set for the initial state particle pair e+e-;the condition "(*liit)==1, 2, 3, 4, 5 or 6" is set for the intermediate state quark pair ddbar, uubar, ssbar, ccbar, bbbar or ttbar;
              if(j==0||(*liit)==1||(*liit)==2||(*liit)==3||(*liit)==4||(*liit)==5||(*liit)==6)
                {
                  liit++;
                  optPnmFromPid(cout,"TxtPnm",(*liit));
                }
              cout<<" -->";
              for(liit++;liit!=sigEvtBr.end();liit++) optPnmFromPid(cout,"TxtPnm",(*liit));
              cout<<endl;
            }
          cout<<endl;
        }
    }

  if(m_vVSigPid5.size()==0)
    {
      cout<<"There are not signal event final states."<<endl<<endl;
    }
  else
    {
      cout<<"Signal event final states:"<<endl<<endl;
      for(unsigned int i=0;i<m_vVSigPid5.size();i++)
	{
          for(unsigned int j=0;j<m_vVSigPid5[i].size();j++)
	    {
	      cout<<"  "<<j<<"\t";
              optPnmFromPid(cout,"TxtPnm",m_vVSigPid5[i][j]);
              cout<<endl;
	    }
          cout<<endl;
	}

      m_vSigEvtIFSts2.clear();
      list<int> sigEvtIFSts2;
      m_vISigEvtIFSts2.clear();
      m_vNSigEvtIFSts2.clear();
      for(unsigned int i=0;i<m_vVSigPid5.size();i++)
        {
          sigEvtIFSts2.clear();
          for(unsigned int j=0;j<m_vVSigPid5[i].size();j++) sigEvtIFSts2.push_back(m_vVSigPid5[i][j]);
          sortByPidAndPchrg(sigEvtIFSts2);
          sigEvtIFSts2.push_front(11);
          sigEvtIFSts2.push_front(-11);

          string ordNumSufi="th";
          string ordNumSufj="th";
          for(unsigned int j=0;j<m_vSigEvtIFSts2.size();j++)
            {
              if(sigEvtIFSts2==m_vSigEvtIFSts2[j])
                {
                  if(i==0) ordNumSufi="st"; else if(i==1) ordNumSufi="nd"; else if(i==2) ordNumSufi="rd";
                  if(j==0) ordNumSufj="st"; else if(j==1) ordNumSufj="nd"; else if(j==2) ordNumSufj="rd";
                  cerr<<"Error: The "<<i+1<<ordNumSufi<<" signal event final state is same as the "<<j+1<<ordNumSufj<<" signal event final state!"<<endl;
                  cerr<<"Infor: Please check the input card and remove one of them."<<endl;
                  exit(146);
                }
            }
          m_vSigEvtIFSts2.push_back(sigEvtIFSts2);
          m_vISigEvtIFSts2.push_back(m_vSigEvtIFSts2.size()-1);
          m_vNSigEvtIFSts2.push_back(0);
        }

      cout<<"With the initial e+ e-:"<<endl<<endl;
      for(unsigned int i=0;i<m_vSigEvtIFSts2.size();i++)
        {
          sigEvtIFSts2.clear();
          sigEvtIFSts2=m_vSigEvtIFSts2[i];
          cout<<" ";
          list<int>::iterator liit=sigEvtIFSts2.begin();
          optPnmFromPid(cout,"TxtPnm",(*liit));
          liit++;
          optPnmFromPid(cout,"TxtPnm",(*liit));
          cout<<" -->";
          for(liit++;liit!=sigEvtIFSts2.end();liit++) optPnmFromPid(cout,"TxtPnm",(*liit));
          cout<<endl<<endl;
        }
    }

  if(m_nEvtsMax!=LONG_MAX)
    {
      cout<<"Maximum number of events to be processed: "<<m_nEvtsMax<<endl<<endl;
    }
  else
    {
      cout<<"Maximum number of events to be processed: "<<LONG_MAX<<" (default)"<<endl<<endl;
    }

  if(m_cut.empty())
    {
      cout<<"No cut is used to select events."<<endl<<endl;
    }
  else
    {
      cout<<"Cut used to select events: "<<m_cut<<endl<<endl;
    }
}

unsigned int topoana::countLiaInVlib(list<int> & lia, vector< list<int> > & Vlib)
{
  unsigned int nCount=0;
  if(lia.size()<2)
    {
      cerr<<"Infor: The size of the list less than two!"<<endl<<endl;
      return nCount;
    }
  if(Vlib.size()==0)
    {
      cerr<<"Infor: The size of the vector is zero!"<<endl<<endl;
      return nCount;
    }
  for(unsigned int i=0;i<Vlib.size();i++)
    {
      list<int> lib=Vlib[i];
      list<int>::iterator liita=lia.begin(),liitb=lib.begin();
      if((*liitb)==(*liita))
        {
          // The logic in the block should be considered seriously again!
          for(liita++;(liita!=lia.end())&&(liitb!=lib.end());liita++)
            {
              for(liitb++;liitb!=lib.end();liitb++)
                {
                  if((*liitb)==(*liita)) break; 
                }
            }
          if(liitb!=lib.end()) nCount++;
        }
    }
  return nCount;
}

unsigned int topoana::countSeqEvtBrsInEvtTr(vector< list<int> > & seqEvtBrs, vector<int> vIdxOfHead1, vector<int> vMidxOfHead1, vector< list<int> > & evtTr, vector<int> vIdxOfHead2, vector<int> vMidxOfHead2)
{
  unsigned int nCount=0;
  if(seqEvtBrs.size()==0)
    {
      cerr<<"Infor: The size of the vector for the sequential event branches is zero!"<<endl<<endl;
      return nCount;
    }
  if(evtTr.size()==0)
    {
      cerr<<"Infor: The size of the vector for the event tree is zero!"<<endl<<endl;
      return nCount;
    }
  if(seqEvtBrs.size()<=evtTr.size())
    {
      /*for(unsigned int i=0;i<seqEvtBrs.size();i++)
        {
          list<int>::iterator liit,liitTmp=seqEvtBrs[i].end();liitTmp--;
          for(liit=seqEvtBrs[i].begin();liit!=seqEvtBrs[i].end();liit++)
            {
              if(liit!=liitTmp) cout<<(*liit)<<"\t";
              else cout<<(*liit)<<endl;
            }
        }
      cout<<endl;
      for(unsigned int i=0;i<evtTr.size();i++)
        {
          list<int>::iterator liit,liitTmp=evtTr[i].end();liitTmp--;
          for(liit=evtTr[i].begin();liit!=evtTr[i].end();liit++)
            {
              if(liit!=liitTmp) cout<<(*liit)<<"\t";
              else cout<<(*liit)<<endl;
            }
        }
      cout<<endl;*/
      vector< vector<int> > vVIdx2ToIdx1;
      vVIdx2ToIdx1.clear();
      vector<int> vIdx2ToIdx1;
      for(unsigned int i=1;i<evtTr.size();i++)
        {
          if(evtTr[i]==seqEvtBrs[0])
            {
              vIdx2ToIdx1.clear();
              vIdx2ToIdx1.push_back(i);
              vVIdx2ToIdx1.push_back(vIdx2ToIdx1);
            }
        }

      vector<int> vMidx1;
      vMidx1.push_back(0);
      for(unsigned int i=1;i<seqEvtBrs.size();i++)
        {
          for(unsigned int j=0;j<i;j++)
            {
              if(vIdxOfHead1[j]==vMidxOfHead1[i])
                {
                  vMidx1.push_back(j);
                  break;
                }
            }
        }

      for(unsigned int i=0;i<vVIdx2ToIdx1.size();i++)
        {
          for(unsigned int j=1;j<seqEvtBrs.size();j++)
            {
              for(unsigned int k=vVIdx2ToIdx1[i][j-1]+1;k<evtTr.size();k++)
                {
                  if(evtTr[k]==seqEvtBrs[j]&&vMidxOfHead2[k]==vIdxOfHead2[(unsigned int) vVIdx2ToIdx1[i][(unsigned int) vMidx1[j]]])
                    {
                      vVIdx2ToIdx1[i].push_back(k);
                      break;
                    }
                }
            }
          if(vVIdx2ToIdx1[i].size()==seqEvtBrs.size()) nCount++;
        }
    }

  return nCount;
}

void topoana::sortBy1stFromLrgToSml(vector<int> &via,vector< vector< list<int> > > &vVLib,vector<int> &vic)
{
  if(via.size()!=vVLib.size()||vVLib.size()!=vic.size())
    {
      cerr<<"Error: The three vectors have different sizes!"<<endl;
      cerr<<"Infor: The size of the first vector is "<<via.size()<<"."<<endl;
      cerr<<"Infor: The size of the second vector is "<<vVLib.size()<<"."<<endl;
      cerr<<"Infor: The size of the third vector is "<<vic.size()<<"."<<endl;
      cerr<<"Infor: Please check them."<<endl;
      exit(64);
    }
  if(via.size()==0)
    {
      cerr<<"Infor: The sizes of the three vectors are zero!"<<endl<<endl;
      return;
    }
  int iaTmp;vector< list<int> > vLibTmp;int icTmp;
  for(unsigned int i=0;i<(via.size()-1);i++)
    for(unsigned int j=i+1;j<via.size();j++)
      if(via[i]<via[j])
        {
          iaTmp=via[i];
          via[i]=via[j];
          via[j]=iaTmp;
          vLibTmp=vVLib[i];
          vVLib[i]=vVLib[j];
          vVLib[j]=vLibTmp;
          icTmp=vic[i];
          vic[i]=vic[j];
          vic[j]=icTmp;
        }
}

void topoana::sortBy1stFromLrgToSml(vector<int> &via,vector< list<int> > &vLib,vector<int> &vic)
{
  if(via.size()!=vLib.size()||vLib.size()!=vic.size())
    {
      cerr<<"Error: The three vectors have different sizes!"<<endl;
      cerr<<"Infor: The size of the first vector is "<<via.size()<<"."<<endl;
      cerr<<"Infor: The size of the second vector is "<<vLib.size()<<"."<<endl;
      cerr<<"Infor: The size of the third vector is "<<vic.size()<<"."<<endl;
      cerr<<"Infor: Please check them."<<endl;
      exit(65);
    }
  if(via.size()==0)
    {
      cerr<<"Infor: The sizes of the three vectors are zero!"<<endl<<endl;
      return;
    }
  int iaTmp;list<int> libTmp;int icTmp;
  for(unsigned int i=0;i<(via.size()-1);i++)
    for(unsigned int j=i+1;j<via.size();j++)
      if(via[i]<via[j])
        {
          iaTmp=via[i];
          via[i]=via[j];
          via[j]=iaTmp;
          libTmp=vLib[i];
          vLib[i]=vLib[j];
          vLib[j]=libTmp;
          icTmp=vic[i];
          vic[i]=vic[j];
          vic[j]=icTmp;
        }
}

void topoana::sortBy1stFromLrgToSml(vector<int> &via,vector<int> &vib,vector<int> &vic)
{
  if(via.size()!=vib.size()||vib.size()!=vic.size())
    {
      cerr<<"Error: The three vectors have different sizes!"<<endl;
      cerr<<"Infor: The size of the first vector is "<<via.size()<<"."<<endl;
      cerr<<"Infor: The size of the second vector is "<<vib.size()<<"."<<endl;
      cerr<<"Infor: The size of the third vector is "<<vic.size()<<"."<<endl;
      cerr<<"Infor: Please check them."<<endl;
      exit(66);
    }
  if(via.size()==0)
    {
      cerr<<"Infor: The sizes of the three vectors are zero!"<<endl<<endl;
      return;
    }
  int iaTmp,ibTmp,icTmp;
  for(unsigned int i=0;i<(via.size()-1);i++)
    for(unsigned int j=i+1;j<via.size();j++)
      if(via[i]<via[j])
        {
          iaTmp=via[i];
          via[i]=via[j];
          via[j]=iaTmp;
          ibTmp=vib[i];
          vib[i]=vib[j];
          vib[j]=ibTmp;
          icTmp=vic[i];
          vic[i]=vic[j];
          vic[j]=icTmp;
        } 
}

void topoana::getRslt()
{
  unsigned int Nstars=89;
  for(unsigned int i=0;i<Nstars;i++) cout<<"*";
  cout<<endl<<endl;

  TChain * chn=new TChain(m_trNm.c_str());
  for(unsigned int i=0;i<m_nmsOfIptRootFls.size();i++)
    {
      chn->Add(m_nmsOfIptRootFls[i].c_str());
    }

  const unsigned int NpsMax=chn->GetMaximum(m_brNmOfNps.c_str());
  int Nps,Pid[NpsMax],Midx[NpsMax];
  chn->SetBranchAddress(m_brNmOfNps.c_str(),&Nps);
  chn->SetBranchAddress(m_brNmOfPid.c_str(),&Pid);
  chn->SetBranchAddress(m_brNmOfMidx.c_str(),&Midx);

  string NmOfOptRootFl=m_mainNmOfOptFls+".root";
  TFile * fl=new TFile(NmOfOptRootFl.c_str(),"recreate"); 
  if(!fl)
    {      
      cerr<<"Error: Can't create the output root file \""<<NmOfOptRootFl<<"\"!"<<endl;
      cerr<<"Infor: Please check it."<<endl;
      exit(14);
    }
  TTree * tr=chn->CloneTree(0);
  int iEvtTr,iEvtIFSts,nSigP[(const unsigned int)(m_vSigPid.size()>0?m_vSigPid.size():1)],nSigIncEvtBr[(const unsigned int)(m_vSigIncEvtBr.size()>0?m_vSigIncEvtBr.size():1)],nSigSeqEvtBrs[(const unsigned int)(m_vSigSeqEvtBrs.size()>0?m_vSigSeqEvtBrs.size():1)],nSigPFSts[(const unsigned int)(m_vSigPFSts.size()>0?m_vSigPFSts.size():1)],iSigEvtTr,iSigEvtIFSts,iSigEvtIFSts2;
  tr->Branch("IEvtTr",&iEvtTr,"iEvtTr/I");
  tr->Branch("IEvtIFSts",&iEvtIFSts,"iEvtIFSts/I");
  if(m_vSigPid.size()>0)
    {
      char specifier[20];
      sprintf(specifier,"nSigP[%d]/I", int(m_vSigPid.size())); 
      tr->Branch("NSigPid",&nSigP,specifier);
    }
  if(m_vSigIncEvtBr.size()>0)
    {
      char specifier[20];
      sprintf(specifier,"nSigIncEvtBr[%d]/I", int(m_vSigIncEvtBr.size()));
      tr->Branch("NSigIncEvtBr",&nSigIncEvtBr,specifier);
    }
  if(m_vSigSeqEvtBrs.size()>0)
    {
      char specifier[20];
      sprintf(specifier,"nSigSeqEvtBrs[%d]/I", int(m_vSigSeqEvtBrs.size()));
      tr->Branch("NSigSeqEvtBrs",&nSigSeqEvtBrs,specifier);
    }
  if(m_vSigPFSts.size()>0)
    {
      char specifier[20];
      sprintf(specifier,"nSigPFSts[%d]/I", int(m_vSigPFSts.size()));
      tr->Branch("NSigPFSts",&nSigPFSts,specifier);
    }
  if(m_vSigEvtTr.size()>0)
    {
      tr->Branch("ISigEvtTr",&iSigEvtTr,"iSigEvtTr/I");
      tr->Branch("ISigEvtIFSts",&iSigEvtIFSts,"iSigEvtIFSts/I");
    }
  if(m_vSigEvtIFSts2.size()>0)
    {
      tr->Branch("ISigEvtIFSts2",&iSigEvtIFSts2,"iSigEvtIFSts2/I");
    }
 
  vector<int> vPid;
  vector<int> vMidx;

  m_vEvtTr.clear();
  vector< list<int> > evtTr;
  vector<int> vIdxOfHead;
  vector<int> vMidxOfHead;
  m_vIEvtTr.clear();
  m_vNEvtTr.clear();
  m_vEvtIFSts.clear();
  list<int> evtIFSts;
  m_vIEvtIFSts.clear();
  m_vNEvtIFSts.clear();
  m_iEvtTrIEvtIFStsMap.clear();
  if(m_vSigEvtTr.size()>0)
    {
      m_iSigEvtTrIEvtTrMap.clear();
      m_iSigEvtIFStsIEvtIFStsMap.clear();
    }
  if(m_vSigEvtIFSts2.size()>0)
    {
      m_iSigEvtIFSts2IEvtIFStsMap.clear();
    }

  long nEvts=chn->GetEntries();
  cout<<"There are "<<nEvts<<" events in total in the input root files."<<endl<<endl;
  long nEvtsToBePrcsd=nEvts<m_nEvtsMax?nEvts:m_nEvtsMax;
  long nEvtsThroughTheCut=0;
  clock_t starttime;
  TTreeFormula * trfml;
  unsigned int nInsts=1;
  if(!m_cut.empty())
    { 
      trfml=new TTreeFormula("trfml",m_cut.c_str(),chn);
      chn->SetNotify(trfml); // This statement is indispensible if more than one root file is added to the object of the TChain class.
    }
  for(unsigned int i=0;i<nEvtsToBePrcsd;i++)
    {
      if(i==0) starttime=clock();
      chn->GetEntry(i);
      if(!m_cut.empty())
        { 
          // The following four statements are used to handle the cases where array variables are used in the cut.
          nInsts=trfml->GetNdata(); // This statement is indispensable if multiple instances have to be evaluated by the object of the TTreeFormula class.
          bool passTheCut=true; 
          for(unsigned int j=0;j<nInsts;j++) if(!(trfml->EvalInstance(j))) {passTheCut=false; break;}
          if(!passTheCut)
            {
              if((i+1>=5000)&&(((i+1)%5000==0)||((i+1)==nEvtsToBePrcsd)))
                {
                  if((i+1)==5000) cout<<"Number of events processed\tNumber of seconds elapsed"<<endl<<endl;
                  cout<<setiosflags(ios::right)<<setw(14)<<i+1<<"\t\t\t"<<setiosflags(ios::fixed)<<setprecision(2)<<setw(14)<<(clock()-starttime)/((double) CLOCKS_PER_SEC)<<resetiosflags(ios::adjustfield)<<endl;
                  if((i+1)==nEvtsToBePrcsd) 
                    {
                      cout<<endl<<"Note that only "<<nEvtsThroughTheCut<<" events passed the cut."<<endl<<endl;
                    }
                }
              if((i+1)==nEvtsToBePrcsd)
                {
                  for(unsigned int j=0;j<Nstars;j++) cout<<"*";
                  cout<<endl<<endl;
                }
              continue;
            }   
          else
            {
              nEvtsThroughTheCut++;
            }
        }
      for(unsigned int j=0;j<m_vSigPid.size();j++) nSigP[j]=0;
      for(unsigned int j=0;j<m_vSigSeqEvtBrs.size();j++) nSigSeqEvtBrs[j]=0;
      vPid.clear();
      vMidx.clear();
      for(int j=0;j<Nps;j++)
        {
          vPid.push_back(Pid[j]);
          vMidx.push_back(Midx[j]);
          //cout<<j<<"\t"<<Pid[j]<<"\t"<<Midx[j]<<endl; 
        }
      //cout<<endl;

      /*for(unsigned int j=0;j<vPid.size();j++)
        {
          cout<<j<<"\t"<<vPid[j]<<"\t"<<vMidx[j]<<endl;
        }
      cout<<endl;*/

      sortPs(vPid,vMidx);
      evtTr.clear();
      vIdxOfHead.clear();
      vMidxOfHead.clear();
      getEvtTr(vPid,vMidx,evtTr,vIdxOfHead,vMidxOfHead);
      evtIFSts.clear();
      getEvtIFSts(vPid,vMidx,evtIFSts);
      bool newEvtTr=true;
      int whichEvtTr;
      iEvtTr=-1;
      for(unsigned int j=0;j<m_vEvtTr.size();j++)
        {
          if(evtTr==m_vEvtTr[j])
            {
              newEvtTr=false;
              whichEvtTr=j;
              break;
            }
        }
      if(newEvtTr==true)
        {
          m_vEvtTr.push_back(evtTr);
          m_vIEvtTr.push_back(m_vEvtTr.size()-1);
          m_vNEvtTr.push_back(1);
          iEvtTr=m_vEvtTr.size()-1;

          bool newEvtIFSts=true;
          int whichEvtIFSts;
          iEvtIFSts=-1;
          for(unsigned int j=0;j<m_vEvtIFSts.size();j++)
            {
              if(evtIFSts==m_vEvtIFSts[j])
                {
                  newEvtIFSts=false;
                  whichEvtIFSts=j;
                  break;
                }
            }
          if(newEvtIFSts==true)
            {
              m_vEvtIFSts.push_back(evtIFSts);
              m_vIEvtIFSts.push_back(m_vEvtIFSts.size()-1);
              m_vNEvtIFSts.push_back(1);
              iEvtIFSts=m_vEvtIFSts.size()-1;
            }
          else
            {
              m_vNEvtIFSts[whichEvtIFSts]++;
              iEvtIFSts=whichEvtIFSts;
            }
          m_iEvtTrIEvtIFStsMap[iEvtTr]=iEvtIFSts;
        }
      else
        {
          m_vNEvtTr[whichEvtTr]++;
          iEvtTr=whichEvtTr;

          m_vNEvtIFSts[m_iEvtTrIEvtIFStsMap[whichEvtTr]]++;
          iEvtIFSts=m_iEvtTrIEvtIFStsMap[whichEvtTr];
        }
      if(m_vSigPid.size()>0)
        {
          for(unsigned int j=0;j<vPid.size();j++)
            {
              for(unsigned int k=0;k<m_vSigPid.size();k++)
                {
                  if(vPid[j]==m_vSigPid[k])
                    {
                      m_vNSigP[k]++;
                      nSigP[k]++;
                      break;
                    }
                }
            }
        }
      if(m_vSigIncEvtBr.size()>0)
        {
          unsigned int nCount;
          for(unsigned int j=0;j<m_vSigIncEvtBr.size();j++)
            {
              nCount=countLiaInVlib(m_vSigIncEvtBr[j],evtTr);
              //cout<<"nCount="<<nCount<<endl;
              m_vNSigIncEvtBr[j]=m_vNSigIncEvtBr[j]+nCount;
              nSigIncEvtBr[j]=nCount;
            }
        }
      if(m_vSigSeqEvtBrs.size()>0)
        {
          unsigned int nCount;
          for(unsigned int j=0;j<m_vSigSeqEvtBrs.size();j++)
            {
              nCount=countSeqEvtBrsInEvtTr(m_vSigSeqEvtBrs[j],m_vVSigIdxOfHead[j],m_vVSigMidxOfHead[j],evtTr,vIdxOfHead,vMidxOfHead);
              //cout<<"nCount="<<nCount<<endl;
              m_vNSigSeqEvtBrs[j]=m_vNSigSeqEvtBrs[j]+nCount;
              nSigSeqEvtBrs[j]=nCount;
            }
        }
      if(m_vSigPFSts.size()>0)
        {
          unsigned int nCount;
          for(unsigned int j=0;j<m_vSigPFSts.size();j++)
            {
              nCount=countPFSts(vPid,vMidx,m_vSigPFSts[j]);
              //cout<<"nCount="<<nCount<<endl;
              m_vNSigPFSts[j]=m_vNSigPFSts[j]+nCount;
              nSigPFSts[j]=nCount;
            }
        }
      if(m_vSigEvtTr.size()>0)
        {
          iSigEvtTr=-1;
          iSigEvtIFSts=-1;
          for(unsigned int j=0;j<m_vSigEvtTr.size();j++)
            {
              if(evtTr==m_vSigEvtTr[j])
                {
                  m_vNSigEvtTr[j]++;
                  iSigEvtTr=j;
                  m_vNSigEvtIFSts[m_iSigEvtTrISigEvtIFStsMap[j]]++;
                  iSigEvtIFSts=m_iSigEvtTrISigEvtIFStsMap[j];
                  if(m_vNSigEvtTr[j]==1) m_iSigEvtTrIEvtTrMap[j]=iEvtTr;
                  if(m_vNSigEvtIFSts[m_iSigEvtTrISigEvtIFStsMap[j]]==1) m_iSigEvtIFStsIEvtIFStsMap[m_iSigEvtTrISigEvtIFStsMap[j]]=iEvtIFSts;
                  break;
                }
            }
        }
      if(m_vSigEvtIFSts2.size()>0)
        {
          iSigEvtIFSts2=-1;
          for(unsigned int j=0;j<m_vSigEvtIFSts2.size();j++)
            {
              if(evtIFSts==m_vSigEvtIFSts2[j])
                {
                  m_vNSigEvtIFSts2[j]++;
                  iSigEvtIFSts2=j;
                  if(m_vNSigEvtIFSts2[j]==1) m_iSigEvtIFSts2IEvtIFStsMap[j]=iEvtIFSts;
                  break;
                }
            }
        }
      tr->Fill();
      if((i+1>=5000)&&(((i+1)%5000==0)||((i+1)==nEvtsToBePrcsd)))
        {
          if((i+1)==5000) cout<<"Number of events processed\tNumber of seconds elapsed"<<endl<<endl;
          cout<<setiosflags(ios::right)<<setw(14)<<i+1<<"\t\t\t"<<setiosflags(ios::fixed)<<setprecision(2)<<setw(14)<<(clock()-starttime)/((double) CLOCKS_PER_SEC)<<resetiosflags(ios::adjustfield)<<endl;
          if((i+1)==nEvtsToBePrcsd) cout<<endl;
        }
      if(!m_cut.empty()&&(i+1)==nEvtsToBePrcsd) cout<<"Note that only "<<nEvtsThroughTheCut<<" events passed the cut."<<endl<<endl; 
      if((i+1)==nEvtsToBePrcsd)
        {
          for(unsigned int j=0;j<Nstars;j++) cout<<"*";
          cout<<endl<<endl;
        }
    }
  fl->Write();
  delete chn; // This statement is indispensable, or a tough problem will arise before the "return 0;" statement in the main function.
  delete tr;
  delete fl;
  sortBy1stFromLrgToSml(m_vNEvtTr,m_vEvtTr,m_vIEvtTr);
  sortBy1stFromLrgToSml(m_vNEvtIFSts,m_vEvtIFSts,m_vIEvtIFSts);
  if(m_vSigPid.size()>0)
    {  
      sortBy1stFromLrgToSml(m_vNSigP,m_vSigPid,m_vISigP);
    }
  if(m_vSigIncEvtBr.size()>0)
    { 
      sortBy1stFromLrgToSml(m_vNSigIncEvtBr,m_vSigIncEvtBr,m_vISigIncEvtBr);
    }
  if(m_vSigSeqEvtBrs.size()>0)
    {
      sortBy1stFromLrgToSml(m_vNSigSeqEvtBrs,m_vSigSeqEvtBrs,m_vISigSeqEvtBrs);
    }
  if(m_vSigPFSts.size()>0)
    {
      sortBy1stFromLrgToSml(m_vNSigPFSts,m_vSigPFSts,m_vISigPFSts);
    }
  if(m_vSigEvtTr.size()>0)
    {
      sortBy1stFromLrgToSml(m_vNSigEvtTr,m_vSigEvtTr,m_vISigEvtTr);
      sortBy1stFromLrgToSml(m_vNSigEvtIFSts,m_vSigEvtIFSts,m_vISigEvtIFSts);
    }
  if(m_vSigEvtIFSts2.size()>0)
    {
      sortBy1stFromLrgToSml(m_vNSigEvtIFSts2,m_vSigEvtIFSts2,m_vISigEvtIFSts2);
    }
}

void topoana::optRsltIntoTxtFl()
{
  string NmOfOptTxtFl=m_mainNmOfOptFls+".txt";
  ofstream fout(NmOfOptTxtFl.c_str(),ios::out);
  if(!fout)
    {
      cerr<<"Error: Can't create the output txt file \""<<NmOfOptTxtFl<<"\"!"<<endl;
      cerr<<"Infor: Please check it."<<endl;
      exit(15);
    }

  fout<<"Event trees and their respective initial-final states:"<<endl<<endl;
  vector< list<int> > evtTr;
  list<int> evtBr;
  list<int> evtIFSts;
  unsigned int nCmltEvts=0;
  for(unsigned int i=0;i<m_vEvtTr.size();i++)
    { 
      evtTr.clear();
      evtTr=m_vEvtTr[i];
      nCmltEvts=nCmltEvts+m_vNEvtTr[i];
      fout<<"index:  "<<i+1<<"\tiEvtTr:  "<<m_vIEvtTr[i]<<"\tiEvtIFSts:  "<<m_iEvtTrIEvtIFStsMap[m_vIEvtTr[i]]<<"\tnEvts:  "<<m_vNEvtTr[i]<<"\tnCmltEvts:  "<<nCmltEvts<<endl;
      for(unsigned int j=0;j<evtTr.size();j++)
        {
          evtBr.clear();
          evtBr=evtTr[j];
          fout<<" ";
          list<int>::iterator liit=evtBr.begin();
          optPnmFromPid(fout,"TxtPnm",(*liit));
          // The condition "j==0" is set for the initial state particle pair e+e-;the condition "(*liit)==1, 2, 3, 4, 5 or 6" is set for the intermediate state quark pair ddbar, uubar, ssbar, ccbar, bbbar or ttbar;
          if(j==0||(*liit)==1||(*liit)==2||(*liit)==3||(*liit)==4||(*liit)==5||(*liit)==6)
            {
              liit++;
              optPnmFromPid(fout,"TxtPnm",(*liit));
            }
          fout<<" -->";
          for(liit++;liit!=evtBr.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<endl;
        }

      for(unsigned int j=0;j<m_vEvtIFSts.size();j++)
        {
          if(m_vIEvtIFSts[j]==m_iEvtTrIEvtIFStsMap[m_vIEvtTr[i]])
            {
              evtIFSts.clear();
              evtIFSts=m_vEvtIFSts[j];
              break;
            }
        }
      fout<<"(";
      list<int>::iterator liit=evtIFSts.begin();
      optPnmFromPid(fout,"TxtPnm",(*liit));
      liit++;
      optPnmFromPid(fout,"TxtPnm",(*liit));
      fout<<" -->";
      for(liit++;liit!=evtIFSts.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
      fout<<" )"<<endl; 

      fout<<endl;
    }

  fout<<endl;

  fout<<"Event initial-final states:"<<endl<<endl;
  //list<int> evtIFSts; The list<int> variable evtIFSts has been previously declared.
  nCmltEvts=0;
  for(unsigned int i=0;i<m_vEvtIFSts.size();i++)
    {
      evtIFSts.clear();
      evtIFSts=m_vEvtIFSts[i];
      nCmltEvts=nCmltEvts+m_vNEvtIFSts[i];
      fout<<"index:  "<<i+1<<"\tiEvtIFSts:  "<<m_vIEvtIFSts[i]<<"\tnEvts:  "<<m_vNEvtIFSts[i]<<"\tnCmltEvts:  "<<nCmltEvts<<endl;
      fout<<" ";
      list<int>::iterator liit=evtIFSts.begin();
      optPnmFromPid(fout,"TxtPnm",(*liit));
      liit++;
      optPnmFromPid(fout,"TxtPnm",(*liit));
      fout<<" -->";
      for(liit++;liit!=evtIFSts.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
      fout<<endl<<endl;
    }

  if(m_vSigPid.size()>0)
    {
      fout<<endl;

      fout<<"Signal particles:"<<endl<<endl;
      unsigned int nCmltPs=0;
      for(unsigned int i=0;i<m_vNSigP.size();i++)
        {
          fout<<"index:  "<<i+1<<"\tiSigP:  "<<m_vISigP[i]<<"\tSigNm: ";
          optPnmFromPid(fout,"TxtPnm",m_vSigPid[i]);
          fout<<"\tnPs:   "<<m_vNSigP[i]<<"\tnCmltPs:  ";
          nCmltPs=nCmltPs+m_vNSigP[i];
          fout<<nCmltPs<<endl<<endl;
        }
    }

  if(m_vSigIncEvtBr.size()>0)
    {
      fout<<endl;

      fout<<"Signal inclusive event branches:"<<endl<<endl;

      list<int> sigIncEvtBr;
      unsigned int nCmltCases=0;
      for(unsigned int i=0;i<m_vSigIncEvtBr.size();i++)
        {
          sigIncEvtBr.clear();
          sigIncEvtBr=m_vSigIncEvtBr[i];
          fout<<"index:  "<<i+1<<"\tiSigIncEvtBr:  "<<m_vISigIncEvtBr[i]<<"\tnCases:  "<<m_vNSigIncEvtBr[i]<<"\tnCmltCases:  ";
          nCmltCases=nCmltCases+m_vNSigIncEvtBr[i];
          fout<<nCmltCases<<endl;
          fout<<" ";
          list<int>::iterator liit=sigIncEvtBr.begin();
          optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<" -->";
          for(liit++;liit!=sigIncEvtBr.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<" + anything";
          fout<<endl<<endl;
        }
    }

  if(m_vSigSeqEvtBrs.size()>0)
    {
      fout<<endl;

      fout<<"Signal sequential event branches:"<<endl<<endl;
      vector< list<int> > sigSeqEvtBrs;
      list<int> sigEvtBr;
      unsigned int nCmltCases=0;
      for(unsigned int i=0;i<m_vSigSeqEvtBrs.size();i++)
        { 
          sigSeqEvtBrs.clear();
          sigSeqEvtBrs=m_vSigSeqEvtBrs[i];
          nCmltCases=nCmltCases+m_vNSigSeqEvtBrs[i];
          fout<<"index:  "<<i+1<<"\tiSigSeqEvtBrs:  "<<m_vISigSeqEvtBrs[i]<<"\tnCases:  "<<m_vNSigSeqEvtBrs[i]<<"\tnCmltCases:  "<<nCmltCases<<endl;
          for(unsigned int j=0;j<sigSeqEvtBrs.size();j++)
            {
              sigEvtBr.clear();
              sigEvtBr=sigSeqEvtBrs[j];
              fout<<" ";
              list<int>::iterator liit=sigEvtBr.begin();
              optPnmFromPid(fout,"TxtPnm",(*liit));
              fout<<" -->";
              for(liit++;liit!=sigEvtBr.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
              fout<<endl;
            }
          fout<<endl;
        }
    }

  if(m_vSigPFSts.size()>0)
    {
      fout<<endl;

      fout<<"Signal particle final states:"<<endl<<endl;

      list<int> sigPFSts;
      unsigned int nCmltCases=0;
      for(unsigned int i=0;i<m_vSigPFSts.size();i++)
        {
          sigPFSts.clear();
          sigPFSts=m_vSigPFSts[i];
          fout<<"index:  "<<i+1<<"\tiSigPFSts:  "<<m_vISigPFSts[i]<<"\tnCases:  "<<m_vNSigPFSts[i]<<"\tnCmltCases:  ";
          nCmltCases=nCmltCases+m_vNSigPFSts[i];
          fout<<nCmltCases<<endl;
          fout<<" ";
          list<int>::iterator liit=sigPFSts.begin();
          optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<" -->";
          for(liit++;liit!=sigPFSts.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<endl<<endl;
        }
    }

  if(m_vSigEvtTr.size()>0)
    {
      fout<<endl;

      fout<<"Signal event trees and their respective initial-final states:"<<endl<<endl;
      vector< list<int> > sigEvtTr;
      list<int> sigEvtBr;
      list<int> sigEvtIFSts;
      nCmltEvts=0;
      for(unsigned int i=0;i<m_vSigEvtTr.size();i++)
        { 
          sigEvtTr.clear();
          sigEvtTr=m_vSigEvtTr[i];
          fout<<"index:  "<<i+1<<"\tiSigEvtTr:  "<<m_vISigEvtTr[i]<<"\tiSigEvtIFSts:  "<<m_iSigEvtTrISigEvtIFStsMap[m_vISigEvtTr[i]]<<"\tiEvtTr:  ";
          if(m_iSigEvtTrIEvtTrMap.find(m_vISigEvtTr[i])!=m_iSigEvtTrIEvtTrMap.end()) fout<<m_iSigEvtTrIEvtTrMap[m_vISigEvtTr[i]];
          else fout<<"---";
          fout<<"\tiEvtIFSts:  ";
          if(m_iSigEvtIFStsIEvtIFStsMap.find(m_iSigEvtTrISigEvtIFStsMap[m_vISigEvtTr[i]])!=m_iSigEvtIFStsIEvtIFStsMap.end()) fout<<m_iSigEvtIFStsIEvtIFStsMap[m_iSigEvtTrISigEvtIFStsMap[m_vISigEvtTr[i]]]<<endl;
          else fout<<"---"<<endl;
          fout<<"\t\t\t\tnEvts:  "<<m_vNSigEvtTr[i]<<"\tnCmltEvts:  ";
          nCmltEvts=nCmltEvts+m_vNSigEvtTr[i];
          fout<<nCmltEvts<<endl;
          for(unsigned int j=0;j<sigEvtTr.size();j++)
            {
              sigEvtBr.clear();
              sigEvtBr=sigEvtTr[j];
              fout<<" ";
              list<int>::iterator liit=sigEvtBr.begin();
              optPnmFromPid(fout,"TxtPnm",(*liit));
              // The condition "j==0" is set for the initial state particle pair e+e-;the condition "(*liit)==1, 2, 3, 4, 5 or 6" is set for the intermediate state quark pair ddbar, uubar, ssbar, ccbar, bbbar or ttbar;
              if(j==0||(*liit)==1||(*liit)==2||(*liit)==3||(*liit)==4||(*liit)==5||(*liit)==6)
                {
                  liit++;
                  optPnmFromPid(fout,"TxtPnm",(*liit));
                }
              fout<<" -->";
              for(liit++;liit!=sigEvtBr.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
              fout<<endl;
            }

          for(unsigned int j=0;j<m_vSigEvtIFSts.size();j++)
            {
              if(m_vISigEvtIFSts[j]==m_iSigEvtTrISigEvtIFStsMap[m_vISigEvtTr[i]])
                {
                  sigEvtIFSts.clear();
                  sigEvtIFSts=m_vSigEvtIFSts[j];
                  break;
                }
            }
          fout<<"(";
          list<int>::iterator liit=sigEvtIFSts.begin();
          optPnmFromPid(fout,"TxtPnm",(*liit)); 
          liit++;
          optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<" -->";
          for(liit++;liit!=sigEvtIFSts.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<" )"<<endl;

          fout<<endl;
        }

      fout<<endl;

      fout<<"Signal event initial-final states corresponding to signal event trees:"<<endl<<endl;
      //list<int> sigEvtIFSts; The list<int> variable sigEvtIFSts has been previously declared.
      nCmltEvts=0;
      for(unsigned int i=0;i<m_vSigEvtIFSts.size();i++)
        {
          sigEvtIFSts.clear();
          sigEvtIFSts=m_vSigEvtIFSts[i];
          fout<<"index:  "<<i+1<<"\tiSigEvtIFSts:  "<<m_vISigEvtIFSts[i]<<"\tiEvtIFSts:  ";
          if(m_iSigEvtIFStsIEvtIFStsMap.find(m_vISigEvtIFSts[i])!=m_iSigEvtIFStsIEvtIFStsMap.end()) fout<<m_iSigEvtIFStsIEvtIFStsMap[m_vISigEvtIFSts[i]];
          else fout<<"---";
          fout<<"\tnEvts:  "<<m_vNSigEvtIFSts[i]<<"\tnCmltEvts:  ";
          nCmltEvts=nCmltEvts+m_vNSigEvtIFSts[i];
          fout<<nCmltEvts<<endl;
          fout<<" ";
          list<int>::iterator liit=sigEvtIFSts.begin();
          optPnmFromPid(fout,"TxtPnm",(*liit));
          liit++;
          optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<" -->";
          for(liit++;liit!=sigEvtIFSts.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<endl<<endl;
        }
    }

  if(m_vSigEvtIFSts2.size()>0)
    {
      fout<<endl;

      fout<<"Signal event initial-final states:"<<endl<<endl;

      list<int> sigEvtIFSts2;
      nCmltEvts=0;
      for(unsigned int i=0;i<m_vSigEvtIFSts2.size();i++)
        {
          sigEvtIFSts2.clear();
          sigEvtIFSts2=m_vSigEvtIFSts2[i];
          fout<<"index:  "<<i+1<<"\tiSigEvtIFSts2:  "<<m_vISigEvtIFSts2[i]<<"\tiEvtIFSts2:  ";
          if(m_iSigEvtIFSts2IEvtIFStsMap.find(m_vISigEvtIFSts2[i])!=m_iSigEvtIFSts2IEvtIFStsMap.end()) fout<<m_iSigEvtIFSts2IEvtIFStsMap[m_vISigEvtIFSts2[i]];
          else fout<<"---";
          fout<<"\tnEvts:  "<<m_vNSigEvtIFSts2[i]<<"\tnCmltEvts:  ";
          nCmltEvts=nCmltEvts+m_vNSigEvtIFSts2[i];
          fout<<nCmltEvts<<endl;
          fout<<" ";
          list<int>::iterator liit=sigEvtIFSts2.begin();
          optPnmFromPid(fout,"TxtPnm",(*liit));
          liit++;
          optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<" -->";
          for(liit++;liit!=sigEvtIFSts2.end();liit++) optPnmFromPid(fout,"TxtPnm",(*liit));
          fout<<endl<<endl;
        }
    }
}

void topoana::mkPidTexPnmMap()
{
  m_pidTexPnmMap.clear();
  int pid;string texpnm;
  string pidTexPnmDatFlNm=m_pkgPath+"core/pid_texpnm.dat";
  ifstream fin(pidTexPnmDatFlNm.c_str(),ios::in);
  if(!fin)
    {
      cerr<<"Error: Can't open the data file \""<<pidTexPnmDatFlNm<<"\"!"<<endl;
      cerr<<"Infor: Please check it."<<endl;
      exit(16);
    }
  while(fin>>pid>>texpnm)
    {
      m_pidTexPnmMap[pid]=texpnm;
      //cout<<pid<<"\t"<<m_pidTexPnmMap[pid]<<endl;
    }
}

void topoana::optRsltIntoTexFl()
{
  string NmOfOptTexFl=m_mainNmOfOptFls+".tex";
  ofstream fout(NmOfOptTexFl.c_str(),ios::out);
  if(!fout)
    {
      cerr<<"Error: Can't create the output tex file \""<<NmOfOptTexFl<<"\"!"<<endl;
      cerr<<"Infor: Please check it."<<endl;
      exit(17);
    }

  fout<<"\\documentclass[landscape]{article}"<<endl;
  fout<<"\\usepackage{geometry}"<<endl;
  fout<<"\\geometry{left=0.0cm,right=0.0cm,top=2.5cm,bottom=2.5cm}"<<endl;
  fout<<"\\usepackage{array}"<<endl;
  string pathOfMakeCellStyFl=m_pkgPath+"core/";
  fout<<"\\usepackage{"<<pathOfMakeCellStyFl<<"makecell}"<<endl;
  fout<<"\\usepackage{color}"<<endl;
  fout<<"\\begin{document}"<<endl;
  fout<<"\\title{Topology Analysis \\\\ \\vspace{0.1cm} \\Large{(v1.3)}}"<<endl;
  fout<<"\\author{Xing-Yu Zhou \\\\ \\vspace{0.1cm} Beihang University}"<<endl;
  fout<<"\\maketitle"<<endl;

  const unsigned int nLinesMin=37;
  const unsigned int nLinesMax=40;
  unsigned int nBrsInALine=6; // The value of this variable is changed to 5 for the case of the table titled signal event trees and their respective initial-final states.
  unsigned int nLines;
  unsigned int nCmltEvts;

  nLines=0;
  vector< list<int> > evtTr;
  list<int> evtBr;
  list<int> evtIFSts;
  nCmltEvts=0;
  for(unsigned int i=0;i<m_vEvtTr.size();i++)
    {
      if(nLines==0)
        {
          fout<<endl<<"\\clearpage"<<endl<<endl;
          fout<<"\\begin{table}[htbp!]"<<endl;
          if(i==0)
            {
              fout<<"\\caption{Event trees and their respective initial-final states.}"<<endl;
              nLines++;
            }
          fout<<"\\small"<<endl;
          fout<<"\\centering"<<endl;
          fout<<"\\begin{tabular}{|c|>{\\centering}p{18cm}|c|c|c|c|}"<<endl;
          fout<<"\\hline"<<endl;
          fout<<"index & \\thead{event tree \\\\ (event initial-final states)} & iEvtTr & iEvtIFSts & nEvts & nCmltEvts \\\\"<<endl;
          nLines++;
          nLines++;
          fout<<"\\hline"<<endl;
        }
      evtTr.clear();
      evtTr=m_vEvtTr[i];
      unsigned int nVldEvtBrs=0;
      fout<<i+1<<" & \\makecell{ $ "<<endl;
      for(unsigned int j=0;j<evtTr.size();j++)
        {
          evtBr.clear();
          evtBr=evtTr[j];
          // Since a lot of pi0s are produced and almost all of them decay to gammma pairs, to save paper and for convenience of readers, all branches of pi0 to gamma pairs are not outputted into the tex file, and hence not printed in the pdf file.
          list<int>::iterator liit=evtBr.begin();
          list<int>::iterator liit1=evtBr.begin();
          liit1++;
          list<int>::iterator liit2=evtBr.begin();
          liit2++;
          liit2++;
          if(((*liit)==111)&&(evtBr.size()==3)&&((*liit1)==22)&&((*liit2)==22)) continue;
          nVldEvtBrs++;
          optPnmFromPid(fout,"TexPnm",(*liit));
          // The condition "j==0" is set for the initial state particle pair e+e-;the condition "(*liit)==1, 2, 3, 4, 5 or 6" is set for the intermediate state quark pair ddbar, uubar, ssbar, ccbar, bbbar or ttbar;
          if(j==0||(*liit)==1||(*liit)==2||(*liit)==3||(*liit)==4||(*liit)==5||(*liit)==6)
            {
              liit++;
              optPnmFromPid(fout,"TexPnm",(*liit));
            }
          fout<<"\\rightarrow ";
          for(liit++;liit!=evtBr.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
          // The following bool variable is used to judge whether the current branch is the last one outputed or not.
          bool lastOneOrAllPiZeroToGammaPairsBehind=true;
          list<int> evtBrTmp;
          for(unsigned int k=j+1;k<evtTr.size();k++)
            {
              evtBrTmp.clear();
              evtBrTmp=evtTr[k];
              list<int>::iterator liitTmp=evtBrTmp.begin();
              list<int>::iterator liitTmp1=evtBrTmp.begin();
              liitTmp1++;
              list<int>::iterator liitTmp2=evtBrTmp.begin();
              liitTmp2++;
              liitTmp2++;
              if(((*liitTmp)!=111)||(evtBrTmp.size()!=3)||((*liitTmp1)!=22)||((*liitTmp2)!=22))
                {
                  lastOneOrAllPiZeroToGammaPairsBehind=false;
                  break;
                }
            }
          if(!lastOneOrAllPiZeroToGammaPairsBehind)
            {
              fout<<","<<endl;
              if(nVldEvtBrs%nBrsInALine==0) fout<<"$ \\\\ $"<<endl;
            }
          else
            {
              fout<<endl<<"$ \\\\ ($"<<endl;
              break;
            }
        }

      for(unsigned int j=0;j<m_vEvtIFSts.size();j++)
        {
          if(m_vIEvtIFSts[j]==m_iEvtTrIEvtIFStsMap[m_vIEvtTr[i]])
            {
              evtIFSts.clear();
              evtIFSts=m_vEvtIFSts[j];
              break;
            }
        }
      list<int>::iterator liit=evtIFSts.begin();
      optPnmFromPid(fout,"TexPnm",(*liit));
      liit++;
      optPnmFromPid(fout,"TexPnm",(*liit));
      fout<<"\\rightarrow ";
      for(liit++;liit!=evtIFSts.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
      fout<<endl<<"$) } & "<<m_vIEvtTr[i]<<" & "<<m_iEvtTrIEvtIFStsMap[m_vIEvtTr[i]]<<" & "<<m_vNEvtTr[i]<<" & ";
      nCmltEvts=nCmltEvts+m_vNEvtTr[i];
      fout<<nCmltEvts<<" \\\\"<<endl;
      fout<<"\\hline"<<endl;
      nLines=nLines+ceil(nVldEvtBrs/((double ) nBrsInALine))+1;
      if(nLines>=nLinesMin||i==(m_vEvtTr.size()-1))
        {
          fout<<"\\end{tabular}"<<endl;
          fout<<"\\end{table}"<<endl;
          nLines=0;
        }
    }

  //list<int> evtIFSts; The list<int> variable evtIFSts has been previously declared.
  nCmltEvts=0;
  for(unsigned int i=0;i<m_vEvtIFSts.size();i++)
    {
      if(i%nLinesMax==0)
        {
          fout<<endl<<"\\clearpage"<<endl<<endl;
          fout<<"\\begin{table}[htbp!]"<<endl;
          if(i==0) fout<<"\\caption{Event initial-final states.}"<<endl;
          fout<<"\\small"<<endl;
          fout<<"\\centering"<<endl;
          fout<<"\\begin{tabular}{|c|>{\\centering}p{18cm}|c|c|c|}"<<endl;
          fout<<"\\hline"<<endl;
          fout<<"index & event initial-final states & iEvtIFSts & nEvts & nCmltEvts \\\\"<<endl;
          fout<<"\\hline"<<endl;
        }
      fout<<i+1<<" & $ "; 
      evtIFSts.clear();
      evtIFSts=m_vEvtIFSts[i];
      list<int>::iterator liit=evtIFSts.begin();
      optPnmFromPid(fout,"TexPnm",(*liit));
      liit++;
      optPnmFromPid(fout,"TexPnm",(*liit));
      fout<<"\\rightarrow ";
      for(liit++;liit!=evtIFSts.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
      fout<<"$ & "<<m_vIEvtIFSts[i]<<" & "<<m_vNEvtIFSts[i]<<" & ";
      nCmltEvts=nCmltEvts+m_vNEvtIFSts[i];
      fout<<nCmltEvts<<" \\\\"<<endl;
      fout<<"\\hline"<<endl;
      if(i%nLinesMax==nLinesMax-1||i==(m_vEvtIFSts.size()-1))
        {
          fout<<"\\end{tabular}"<<endl;
          fout<<"\\end{table}"<<endl;
        }
    }

  if(m_vSigPid.size()>0)
    {
      unsigned int nCmltPs=0;
      for(unsigned int i=0;i<m_vNSigP.size();i++)
        {
          if(i%nLinesMax==0)
            {
              fout<<endl<<"\\clearpage"<<endl<<endl;
              fout<<"\\begin{table}[htbp!]"<<endl;
              if(i==0) fout<<"\\caption{Signal particles.}"<<endl;
              fout<<"\\small"<<endl;
              fout<<"\\centering"<<endl;
              fout<<"\\begin{tabular}{|c|c|c|c|c|}"<<endl;
              fout<<"\\hline"<<endl;
              fout<<"index & signal particle & iSigP & nPs & nCmltPs \\\\"<<endl;
              fout<<"\\hline"<<endl;
            }
          fout<<i+1<<" & $ ";
          optPnmFromPid(fout,"TexPnm",m_vSigPid[i]);
          fout<<"$ & "<<m_vISigP[i]<<" & "<<m_vNSigP[i]<<" & ";
          nCmltPs=nCmltPs+m_vNSigP[i];
          fout<<nCmltPs<<" \\\\"<<endl;
          fout<<"\\hline"<<endl;
          if(i%nLinesMax==nLinesMax-1||i==(m_vNSigP.size()-1))
            {
              fout<<"\\end{tabular}"<<endl;
              fout<<"\\end{table}"<<endl;
            }
        }
    }

  if(m_vSigIncEvtBr.size()>0)
    {
      list<int> sigIncEvtBr;
      unsigned int nCmltCases=0;
      for(unsigned int i=0;i<m_vSigIncEvtBr.size();i++)
        {
          if(i%nLinesMax==0)
            {
              fout<<endl<<"\\clearpage"<<endl<<endl;
              fout<<"\\begin{table}[htbp!]"<<endl;
              if(i==0) fout<<"\\caption{Signal inclusive event branches.}"<<endl;
              fout<<"\\small"<<endl;
              fout<<"\\centering"<<endl;
              fout<<"\\begin{tabular}{|c|c|c|c|c|}"<<endl;
              fout<<"\\hline"<<endl;
              fout<<"index & signal inclusive event branch & iSigIncEvtBr & nCases & nCmltCases \\\\"<<endl;
              fout<<"\\hline"<<endl;
            }
          fout<<i+1<<" & $ "; 
          sigIncEvtBr.clear();
          sigIncEvtBr=m_vSigIncEvtBr[i];
          list<int>::iterator liit=sigIncEvtBr.begin();
          optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<"\\rightarrow ";
          for(liit++;liit!=sigIncEvtBr.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<" + \\rm{anything}";
          fout<<"$ & "<<m_vISigIncEvtBr[i]<<" & "<<m_vNSigIncEvtBr[i]<<" & ";
          nCmltCases=nCmltCases+m_vNSigIncEvtBr[i];
          fout<<nCmltCases<<" \\\\"<<endl;
          fout<<"\\hline"<<endl;
          if(i%nLinesMax==nLinesMax-1||i==(m_vSigIncEvtBr.size()-1))
            {
              fout<<"\\end{tabular}"<<endl;
              fout<<"\\end{table}"<<endl;
            }
        }
    }

  if(m_vSigSeqEvtBrs.size()>0)
    {
      nBrsInALine=5; 
      nLines=0;
      vector< list<int> > sigSeqEvtBrs;
      list<int> sigEvtBr;
      unsigned int nCmltCases=0;
      for(unsigned int i=0;i<m_vSigSeqEvtBrs.size();i++)
        {
          if(nLines==0)
            {
              fout<<endl<<"\\clearpage"<<endl<<endl;
              fout<<"\\begin{table}[htbp!]"<<endl;
              if(i==0)
                {
                  fout<<"\\caption{Signal sequential event branches.}"<<endl;
                  nLines++;
                }
              fout<<"\\small"<<endl;
              fout<<"\\centering"<<endl;
              fout<<"\\begin{tabular}{|c|>{\\centering}p{18cm}|c|c|c|}"<<endl;
              fout<<"\\hline"<<endl;
              fout<<"index & \\thead{signal sequential event branches} & iSigSeqEvtBrs & nCases & nCmltCases \\\\"<<endl;
              nLines++;
              fout<<"\\hline"<<endl;
            }
          sigSeqEvtBrs.clear();
          sigSeqEvtBrs=m_vSigSeqEvtBrs[i];
          unsigned int nVldSigSeqEvtBrs=0;
          fout<<i+1<<" & \\makecell{ $ "<<endl;
          for(unsigned int j=0;j<sigSeqEvtBrs.size();j++)
            {
              sigEvtBr.clear();
              sigEvtBr=sigSeqEvtBrs[j];              
              // Since a lot of pi0s are produced and almost all of them decay to gammma pairs, to save paper and for convenience of readers, all branches of pi0 to gamma pairs are not outputted into the tex file, and hence not printed in the pdf file.
              list<int>::iterator liit=sigEvtBr.begin();
              list<int>::iterator liit1=sigEvtBr.begin();
              liit1++;
              list<int>::iterator liit2=sigEvtBr.begin();
              liit2++;
              liit2++;
              if(((*liit)==111)&&(sigEvtBr.size()==3)&&((*liit1)==22)&&((*liit2)==22)) continue;
              nVldSigSeqEvtBrs++;
              optPnmFromPid(fout,"TexPnm",(*liit));
              fout<<"\\rightarrow ";
              for(liit++;liit!=sigEvtBr.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
              // The following bool variable is used to judge whether the current branch is the last one outputed or not.
              bool lastOneOrAllPiZeroToGammaPairsBehind=true;
              list<int> sigEvtBrTmp;
              for(unsigned int k=j+1;k<sigSeqEvtBrs.size();k++)
                {
                  sigEvtBrTmp.clear();
                  sigEvtBrTmp=sigSeqEvtBrs[k];
                  list<int>::iterator liitTmp=sigEvtBrTmp.begin();
                  list<int>::iterator liitTmp1=sigEvtBrTmp.begin();
                  liitTmp1++;
                  list<int>::iterator liitTmp2=sigEvtBrTmp.begin();
                  liitTmp2++;
                  liitTmp2++;
                  if(((*liitTmp)!=111)||(sigEvtBrTmp.size()!=3)||((*liitTmp1)!=22)||((*liitTmp2)!=22))
                    {
                      lastOneOrAllPiZeroToGammaPairsBehind=false;
                      break;
                    }
                }
              if(!lastOneOrAllPiZeroToGammaPairsBehind)
                {
                  fout<<","<<endl;
                  if(nVldSigSeqEvtBrs%nBrsInALine==0) fout<<"$ \\\\ $"<<endl;
                }
              else
                {
                  fout<<endl<<"$ }";
                  break;
                }
            }

          fout<<" & "<<m_vISigSeqEvtBrs[i]<<" & "<<m_vNSigSeqEvtBrs[i]<<" & ";
          nCmltCases=nCmltCases+m_vNSigSeqEvtBrs[i];
          fout<<nCmltCases<<" \\\\"<<endl;
          fout<<"\\hline"<<endl;
          nLines=nLines+ceil(nVldSigSeqEvtBrs/((double ) nBrsInALine));
          if(nLines>=nLinesMin||i==(m_vSigSeqEvtBrs.size()-1))
            {
              fout<<"\\end{tabular}"<<endl;
              fout<<"\\end{table}"<<endl;
              nLines=0;
            }
        }
    }

  if(m_vSigPFSts.size()>0)
    {
      list<int> sigPFSts;
      unsigned int nCmltCases=0;
      for(unsigned int i=0;i<m_vSigPFSts.size();i++)
        {
          if(i%nLinesMax==0)
            {
              fout<<endl<<"\\clearpage"<<endl<<endl;
              fout<<"\\begin{table}[htbp!]"<<endl;
              if(i==0) fout<<"\\caption{Signal particle final states.}"<<endl;
              fout<<"\\small"<<endl;
              fout<<"\\centering"<<endl;
              fout<<"\\begin{tabular}{|c|>{\\centering}p{16cm}|c|c|c|}"<<endl;
              fout<<"\\hline"<<endl;
              fout<<"index & signal particle final states & iSigPFSts & nCases & nCmltCases \\\\"<<endl;
              fout<<"\\hline"<<endl;
            }
          fout<<i+1<<" & $ "; 
          sigPFSts.clear();
          sigPFSts=m_vSigPFSts[i];
          list<int>::iterator liit=sigPFSts.begin();
          optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<"\\rightarrow ";
          for(liit++;liit!=sigPFSts.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<"$ & "<<m_vISigPFSts[i]<<" & "<<m_vNSigPFSts[i]<<" & ";
          nCmltCases=nCmltCases+m_vNSigPFSts[i];
          fout<<nCmltCases<<" \\\\"<<endl;
          fout<<"\\hline"<<endl;
          if(i%nLinesMax==nLinesMax-1||i==(m_vSigPFSts.size()-1))
            {
              fout<<"\\end{tabular}"<<endl;
              fout<<"\\end{table}"<<endl;
            }
        }
    }

  if(m_vSigEvtTr.size()>0)
    {
      nLines=0;
      vector< list<int> > sigEvtTr;
      list<int> sigEvtBr;
      list<int> sigEvtIFSts;
      nCmltEvts=0;
      for(unsigned int i=0;i<m_vSigEvtTr.size();i++)
        {
          if(nLines==0)
            {
              fout<<endl<<"\\clearpage"<<endl<<endl;
              fout<<"\\begin{table}[htbp!]"<<endl;
              if(i==0)
                {
                  fout<<"\\caption{Signal event trees and their respective initial-final states.}"<<endl;
                  nLines++;
                }
              fout<<"\\small"<<endl;
              fout<<"\\centering"<<endl;
              fout<<"\\begin{tabular}{|c|>{\\centering}p{15cm}|c|c|c|c|c|c|}"<<endl;
              fout<<"\\hline"<<endl;
              fout<<"index & \\thead{signal event tree \\\\ (signal event initial-final states)} & iSigEvtTr & iSigEvtIFSts & iEvtTr & iEvtIFSts & nEvts & nCmltEvts \\\\"<<endl;
              nLines++;
              nLines++;
              fout<<"\\hline"<<endl;
            }
          sigEvtTr.clear();
          sigEvtTr=m_vSigEvtTr[i];
          unsigned int nVldSigSeqEvtBrs=0;
          fout<<i+1<<" & \\makecell{ $ "<<endl;
          for(unsigned int j=0;j<sigEvtTr.size();j++)
            {
              sigEvtBr.clear();
              sigEvtBr=sigEvtTr[j];              
              // Since a lot of pi0s are produced and almost all of them decay to gammma pairs, to save paper and for convenience of readers, all branches of pi0 to gamma pairs are not outputted into the tex file, and hence not printed in the pdf file.
              list<int>::iterator liit=sigEvtBr.begin();
              list<int>::iterator liit1=sigEvtBr.begin();
              liit1++;
              list<int>::iterator liit2=sigEvtBr.begin();
              liit2++;
              liit2++;
              if(((*liit)==111)&&(sigEvtBr.size()==3)&&((*liit1)==22)&&((*liit2)==22)) continue;
              nVldSigSeqEvtBrs++;
              optPnmFromPid(fout,"TexPnm",(*liit));
              // The condition "j==0" is set for the initial state particle pair e+e-;the condition "(*liit)==1, 2, 3, 4, 5 or 6" is set for the intermediate state quark pair ddbar, uubar, ssbar, ccbar, bbbar or ttbar;
              if(j==0||(*liit)==1||(*liit)==2||(*liit)==3||(*liit)==4||(*liit)==5||(*liit)==6)
                {
                  liit++;
                  optPnmFromPid(fout,"TexPnm",(*liit));
                }
              fout<<"\\rightarrow ";
              for(liit++;liit!=sigEvtBr.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
              // The following bool variable is used to judge whether the current branch is the last one outputed or not.
              bool lastOneOrAllPiZeroToGammaPairsBehind=true;
              list<int> sigEvtBrTmp;
              for(unsigned int k=j+1;k<sigEvtTr.size();k++)
                {
                  sigEvtBrTmp.clear();
                  sigEvtBrTmp=sigEvtTr[k];
                  list<int>::iterator liitTmp=sigEvtBrTmp.begin();
                  list<int>::iterator liitTmp1=sigEvtBrTmp.begin();
                  liitTmp1++;
                  list<int>::iterator liitTmp2=sigEvtBrTmp.begin();
                  liitTmp2++;
                  liitTmp2++;
                  if(((*liitTmp)!=111)||(sigEvtBrTmp.size()!=3)||((*liitTmp1)!=22)||((*liitTmp2)!=22))
                    {
                      lastOneOrAllPiZeroToGammaPairsBehind=false;
                      break;
                    }
                }
              if(!lastOneOrAllPiZeroToGammaPairsBehind)
                {
                  fout<<","<<endl;
                  if(nVldSigSeqEvtBrs%nBrsInALine==0) fout<<"$ \\\\ $"<<endl;
                }
              else
                {
                  fout<<endl<<"$ \\\\ ($"<<endl;
                  break;
                }
            }

          for(unsigned int j=0;j<m_vSigEvtIFSts.size();j++)
            {
              if(m_vISigEvtIFSts[j]==m_iSigEvtTrISigEvtIFStsMap[m_vISigEvtTr[i]])
                {
                  sigEvtIFSts.clear();
                  sigEvtIFSts=m_vSigEvtIFSts[j];
                  break;
                }
            }
          list<int>::iterator liit=sigEvtIFSts.begin();
          optPnmFromPid(fout,"TexPnm",(*liit));
          liit++;
          optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<"\\rightarrow ";
          for(liit++;liit!=sigEvtIFSts.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<endl<<"$) } & "<<m_vISigEvtTr[i]<<" & "<<m_iSigEvtTrISigEvtIFStsMap[m_vISigEvtTr[i]]<<" & ";
          if(m_iSigEvtTrIEvtTrMap.find(m_vISigEvtTr[i])!=m_iSigEvtTrIEvtTrMap.end()) fout<<m_iSigEvtTrIEvtTrMap[m_vISigEvtTr[i]];
          else fout<<"---";
          fout<<" & ";
          if(m_iSigEvtIFStsIEvtIFStsMap.find(m_iSigEvtTrISigEvtIFStsMap[m_vISigEvtTr[i]])!=m_iSigEvtIFStsIEvtIFStsMap.end()) fout<<m_iSigEvtIFStsIEvtIFStsMap[m_iSigEvtTrISigEvtIFStsMap[m_vISigEvtTr[i]]];
          else fout<<"---";
          fout<<" & "<<m_vNSigEvtTr[i]<<" & ";
          nCmltEvts=nCmltEvts+m_vNSigEvtTr[i];
          fout<<nCmltEvts<<" \\\\"<<endl;
          fout<<"\\hline"<<endl;
          nLines=nLines+ceil(nVldSigSeqEvtBrs/((double ) nBrsInALine))+1;
          if(nLines>=nLinesMin||i==(m_vSigEvtTr.size()-1))
            {
              fout<<"\\end{tabular}"<<endl;
              fout<<"\\end{table}"<<endl;
              nLines=0;
            }
        }

      //list<int> sigEvtIFSts; The list<int> variable sigEvtIFSts has been previously declared.
      nCmltEvts=0;
      for(unsigned int i=0;i<m_vSigEvtIFSts.size();i++)
        {
          if(i%nLinesMax==0)
            {
              fout<<endl<<"\\clearpage"<<endl<<endl;
              fout<<"\\begin{table}[htbp!]"<<endl;
              if(i==0) fout<<"\\caption{Signal event initial-final states corresponding to signal event trees.}"<<endl;
              fout<<"\\small"<<endl;
              fout<<"\\centering"<<endl;
              fout<<"\\begin{tabular}{|c|>{\\centering}p{16cm}|c|c|c|c|}"<<endl;
              fout<<"\\hline"<<endl;
              fout<<"index & signal event initial-final states & iSigEvtIFSts & iEvtIFSts & nEvts & nCmltEvts \\\\"<<endl;
              fout<<"\\hline"<<endl;
            }
          fout<<i+1<<" & $ "; 
          sigEvtIFSts.clear();
          sigEvtIFSts=m_vSigEvtIFSts[i];
          list<int>::iterator liit=sigEvtIFSts.begin();
          optPnmFromPid(fout,"TexPnm",(*liit));
          liit++;
          optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<"\\rightarrow ";
          for(liit++;liit!=sigEvtIFSts.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<"$ & "<<m_vISigEvtIFSts[i]<<" & ";
          if(m_iSigEvtIFStsIEvtIFStsMap.find(m_vISigEvtIFSts[i])!=m_iSigEvtIFStsIEvtIFStsMap.end()) fout<<m_iSigEvtIFStsIEvtIFStsMap[m_vISigEvtIFSts[i]];
          else fout<<"---";
          fout<<" & "<<m_vNSigEvtIFSts[i]<<" & ";
          nCmltEvts=nCmltEvts+m_vNSigEvtIFSts[i];
          fout<<nCmltEvts<<" \\\\"<<endl;
          fout<<"\\hline"<<endl;
          if(i%nLinesMax==nLinesMax-1||i==(m_vSigEvtIFSts.size()-1))
            {
              fout<<"\\end{tabular}"<<endl;
              fout<<"\\end{table}"<<endl;
            }
        }
    }

  if(m_vSigEvtIFSts2.size()>0)
    {
      list<int> sigEvtIFSts2;
      nCmltEvts=0;
      for(unsigned int i=0;i<m_vSigEvtIFSts2.size();i++)
        {
          if(i%nLinesMax==0)
            {
              fout<<endl<<"\\clearpage"<<endl<<endl;
              fout<<"\\begin{table}[htbp!]"<<endl;
              if(i==0) fout<<"\\caption{Signal event initial-final states.}"<<endl;
              fout<<"\\small"<<endl;
              fout<<"\\centering"<<endl;
              fout<<"\\begin{tabular}{|c|>{\\centering}p{16cm}|c|c|c|c|}"<<endl;
              fout<<"\\hline"<<endl;
              fout<<"index & signal event initial-final states & iSigEvtIFSts2 & iEvtIFSts & nEvts & nCmltEvts \\\\"<<endl;
              fout<<"\\hline"<<endl;
            }
          fout<<i+1<<" & $ "; 
          sigEvtIFSts2.clear();
          sigEvtIFSts2=m_vSigEvtIFSts2[i];
          list<int>::iterator liit=sigEvtIFSts2.begin();
          optPnmFromPid(fout,"TexPnm",(*liit));
          liit++;
          optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<"\\rightarrow ";
          for(liit++;liit!=sigEvtIFSts2.end();liit++) optPnmFromPid(fout,"TexPnm",(*liit));
          fout<<"$ & "<<m_vISigEvtIFSts2[i]<<" & ";
          if(m_iSigEvtIFSts2IEvtIFStsMap.find(m_vISigEvtIFSts2[i])!=m_iSigEvtIFSts2IEvtIFStsMap.end()) fout<<m_iSigEvtIFSts2IEvtIFStsMap[m_vISigEvtIFSts2[i]];
          else fout<<"---";
          fout<<" & "<<m_vNSigEvtIFSts2[i]<<" & ";
          nCmltEvts=nCmltEvts+m_vNSigEvtIFSts2[i];
          fout<<nCmltEvts<<" \\\\"<<endl;
          fout<<"\\hline"<<endl;
          if(i%nLinesMax==nLinesMax-1||i==(m_vSigEvtIFSts2.size()-1))
            {
              fout<<"\\end{tabular}"<<endl;
              fout<<"\\end{table}"<<endl;
            }
        }
    }

  fout<<"\\end{document}"<<endl;
}

void topoana::getPdfFlFromTexFl()
{
  string NmOfOptTexFl=m_mainNmOfOptFls+".tex";
  string pdflatexcmd="pdflatex "+NmOfOptTexFl;
  system(pdflatexcmd.c_str());
  system(pdflatexcmd.c_str());
  system(pdflatexcmd.c_str());

  string NmOfOptAuxFl=m_mainNmOfOptFls+".aux";
  string NmOfOptLogFl=m_mainNmOfOptFls+".log";
  string rmcmd="rm "+NmOfOptAuxFl+" "+NmOfOptLogFl;
  system(rmcmd.c_str());
}

void topoana::optInfOnRslt()
{

}

int main(int argc,char *argv[])
{
  topoana ta;
  ta.mkPidTxtPnmMap();
  ta.mkPid3PchrgMap();
  if(argc>1)
    {
      ta.readCard(argv[1]);
    }
  else
    {
      string dftTopoAnaCardFlNm="topoana.card";
      ta.readCard(dftTopoAnaCardFlNm);
    }
  ta.getRslt();
  ta.optRsltIntoTxtFl();
  ta.mkPidTexPnmMap();
  ta.optRsltIntoTexFl();
  ta.getPdfFlFromTexFl();
  ta.optInfOnRslt();
  return 0;
}
