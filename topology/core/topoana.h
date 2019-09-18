#ifndef TOPOANA_H
#define TOPOANA_H

#include <vector>
#include <string>
#include <list>
#include <map>
#include <climits>
using namespace std;

class topoana
{
  private:
    string m_pkgPath;

    map<int,int> m_pid3PchrgMap;
    map<int,string> m_pidTxtPnmMap;
    map<int,string> m_pidTexPnmMap;

    vector<string> m_nmsOfIptRootFls;
    string m_trNm;
    string m_brNmOfNps;
    string m_brNmOfPid;
    string m_brNmOfMidx;
    string m_mainNmOfOptFls;
    vector<int> m_vSigPid;
    vector< vector<int> > m_vVSigPid1;
    vector< vector<int> > m_vVSigPid2;
    vector< vector<int> > m_vVSigMidx2;
    vector< vector<int> > m_vVSigPid3;
    vector< vector<int> > m_vVSigPid4;
    vector< vector<int> > m_vVSigMidx4;
    vector< vector<int> > m_vVSigPid5;
    long m_nEvtsMax;
    string m_cut;      

    vector<int> m_vISigP;              
    vector<int> m_vNSigP;
    vector< list<int> > m_vSigIncEvtBr;
    vector<int> m_vISigIncEvtBr;
    vector<int> m_vNSigIncEvtBr;
    vector< vector< list<int> > > m_vSigSeqEvtBrs;
    vector<int> m_vISigSeqEvtBrs;
    vector<int> m_vNSigSeqEvtBrs;
    vector< list<int> > m_vSigPFSts;
    vector< vector<int> > m_vVSigIdxOfHead;
    vector< vector<int> > m_vVSigMidxOfHead;
    vector<int> m_vISigPFSts;
    vector<int> m_vNSigPFSts;
    vector< vector< list<int> > > m_vSigEvtTr;
    vector<int> m_vISigEvtTr;
    vector<int> m_vNSigEvtTr;
    vector< list<int> > m_vSigEvtIFSts;
    vector<int> m_vISigEvtIFSts;
    vector<int> m_vNSigEvtIFSts;
    map<int,int> m_iSigEvtTrISigEvtIFStsMap;
    vector< list<int> > m_vSigEvtIFSts2;
    vector<int> m_vISigEvtIFSts2;
    vector<int> m_vNSigEvtIFSts2;
    vector< vector< list<int> > > m_vEvtTr;
    vector<int> m_vIEvtTr;
    vector<int> m_vNEvtTr;
    vector< list<int> > m_vEvtIFSts;
    vector<int> m_vIEvtIFSts;
    vector<int> m_vNEvtIFSts;
    map<int,int> m_iEvtTrIEvtIFStsMap;
    map<int,int> m_iSigEvtTrIEvtTrMap;
    map<int,int> m_iSigEvtIFStsIEvtIFStsMap;
    map<int,int> m_iSigEvtIFSts2IEvtIFStsMap;
  public:
    topoana()
    {
      m_pkgPath="/afs/ihep.ac.cn/users/j/jingmq/bes/DDPIPI/v0.2/topology/";
      m_nEvtsMax=LONG_MAX; // LONG_MAX=9223372036854775807 is the maximum long int number.
    }
    ~topoana(){}
    string &       trim(string & line);
    void           mkPidTxtPnmMap();
    void           mkPid3PchrgMap();
    int 	   getPidFromTxtPnm(string pnm);
    void           optErrInfOnPid3PchrgMap(int pid);
    void           optPnmFromPid(ostream & out,string pnmType,int pid);
    void           sortByPidAndPchrg(vector<int> &via,vector<int> &vib,vector<int> &vic,vector<int> &vid);
    void           sortBySzPidAndPchrg(vector< vector<int> > &vVia,vector< vector<int> > &vVib,vector< vector<int> >&vVic,vector< vector<int> > &vVid);
    void           sortPs(vector<int> & vPid,vector<int> & vMidx);
    void           getEvtTr(vector<int> vPid,vector<int> vMidx,vector< list<int> > & evtTr);
    void           getEvtTr(vector<int> vPid,vector<int> vMidx,vector< list<int> > & evtTr, vector<int> & vIdxOfHead, vector<int> & vMidxOfHead);
    void           sortByPidAndPchrg(list<int> &lia);
    void           getEvtIFSts(vector<int> & vPid,vector<int> & vMidx,list<int> & evtIFSts);
    unsigned int   countPFSts(vector<int> & vPid, vector<int> & vMidx, list<int> pFSts);
    void           readOpenCurly(ifstream & fin, string & line, string prompt);
    void           read1stLineOrCloseCurly(ifstream & fin, string & line, bool essential, string errinforprompt);
    void           readExtraLinesOrCloseCurly(ifstream & fin, string & line, string prompt);
    void           readCloseCurly(ifstream & fin, string & line, string prompt);
    void           readCard(string topoAnaCardFlNm);
    unsigned int   countLiaInVlib(list<int> & lia, vector< list<int> > & Vlib);
    unsigned int   countSeqEvtBrsInEvtTr(vector< list<int> > & seqEvtBrs, vector<int> vIdxOfHead1, vector<int> vMidxOfHead1, vector< list<int> > & evtTr, vector<int> vIdxOfHead2, vector<int> vMidxOfHead2);
    void           sortBy1stFromLrgToSml(vector<int> &via,vector< vector< list<int> > > &vVLib,vector<int> &vic);
    void           sortBy1stFromLrgToSml(vector<int> &via,vector< list<int> > &vLib,vector<int> &vic);
    void           sortBy1stFromLrgToSml(vector<int> &via,vector<int> &vib,vector<int> &vic);
    void           getRslt();

    void           optRsltIntoTxtFl();
    void           mkPidTexPnmMap();
    void           optRsltIntoTexFl();
    void           getPdfFlFromTexFl();
    void           optInfOnRslt();
};

#endif
