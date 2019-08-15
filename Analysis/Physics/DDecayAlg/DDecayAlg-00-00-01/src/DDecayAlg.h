#ifndef Physics_Analysis_DDecayAlg_H
#define Physics_Analysis_DDecayAlg_H 

#include "GaudiKernel/Algorithm.h"
#include "GaudiKernel/DeclareFactoryEntries.h"
#include "GaudiKernel/LoadFactoryEntries.h"
#include "GaudiKernel/INTupleSvc.h"
#include "GaudiKernel/NTuple.h"
#include "GaudiKernel/ISvcLocator.h"
#include "GaudiKernel/PropertyMgr.h"
#include "GaudiKernel/SmartDataPtr.h"
#include "GaudiKernel/Service.h"
#include "GaudiKernel/MsgStream.h"
#include "GaudiKernel/PropertyMgr.h"
#include "DatabaseSvc/IDatabaseSvc.h"

// don't know their functions
#include "GaudiKernel/Bootstrap.h"
#include "GaudiKernel/IDataProviderSvc.h"
#include "GaudiKernel/IHistogramSvc.h"
#include "EventModel/Event.h"
/////////////////////////////

#include "EventModel/EventModel.h"
#include "EventModel/EventHeader.h"

#include "EvtRecEvent/EvtRecEvent.h"
#include "EvtRecEvent/EvtRecTrack.h"
#include "EvtRecEvent/EvtRecDTag.h"
#include "EvtRecEvent/EvtRecPi0.h"
#include "EvtRecEvent/EvtRecVeeVertex.h"
#include "MdcRecEvent/RecMdcKalTrack.h"
#include "DTagTool/DTagTool.h"

#include "VertexFit/KinematicFit.h"
#include "VertexFit/VertexFit.h"
#include "VertexFit/IVertexDbSvc.h"
#include "VertexFit/Helix.h"
#include "VertexFit/WTrackParameter.h"
#include "ParticleID/ParticleID.h"

#include "McTruth/McParticle.h"

#include "TMath.h"
#include <vector>
#include <TTree.h>

#include "CLHEP/Vector/LorentzVector.h"
#include "CLHEP/Vector/ThreeVector.h"
using CLHEP::Hep3Vector;
using CLHEP::HepLorentzVector;
typedef std::vector<HepLorentzVector> Vp4;
typedef std::vector<int> Vint;
typedef std::vector<WTrackParameter> VWTrkPara;

class DDecayAlg : public Algorithm {

    public:
        DDecayAlg(const std::string& name, ISvcLocator* pSvcLocator);
        StatusCode initialize();
        StatusCode execute();
        StatusCode finalize();  

    private:
        std::vector<int> m_DModes;
        bool m_isMonteCarlo;
        bool m_pid;
        bool m_debug;

        // judgement variables
        bool stat_DTagTool;
        bool stat_tagSD;
        bool stat_saveCandD;
        bool stat_saveOthertrks;
        bool stat_saveOthershws;
        
        // common info
        int runNo;
        int evtNo;
        long flag1;

        // All McTruth info
        int pdgid[100];
        int motheridx[100];
        int idxmc;
        double p4_alltrk[100][4];
        Vp4 pAll;
        Vint pdg;
        Vint mother;

        // Dstst McTruth info
        double p4_pip[4];
        double p4_pim[4];
        double p4_D1[4];
        double p4_D2[4];
        double p4_Dstst[4];

        // psi(3770) McTruth info
        double p4_pip_psi[4];
        double p4_pim_psi[4];
        double p4_psi[4];
        double p4_Dp_psi[4];
        double p4_Dm_psi[4];

        // DpDm McTruth info
        int DpId;
        int DmId;

        // DTagTool
        EvtRecDTagCol::iterator dtag_iter_end;
        EvtRecDTagCol::iterator dtag_iter_begin;
        EvtRecDTagCol::iterator dtag_iter;
        int n_trkD;
        int n_shwD;
        double rawp4_Dtrk[5][4];
        double p4_Dtrk[5][4];
        double rawp4_Dshw[2][4];
        double p4_Dshw[2][4];
        int mode;
        int MODE;
        int charm;
        double chi2_vf;
        VertexParameter birth;
        double chi2_kf;
        int n_othertrks;
        double rawp4_otherMdctrk[20][6];
        double rawp4_otherMdcKaltrk[20][6];
        int charge_otherMdctrk;
        int n_othershws;
        double rawp4_othershw[50][4];
        double mDcand;
        int n_count;

        // Ntuple1 info
        NTuple::Tuple* m_tuple1;
        NTuple::Item<int> m_runNo;
        NTuple::Item<int> m_evtNo;
        NTuple::Item<int> m_flag1;
        NTuple::Item<int> m_n_trkD;
        NTuple::Matrix<double> m_rawp4_Dtrk;
        NTuple::Matrix<double> m_p4_Dtrk;
        NTuple::Item<int> m_n_shwD;
        NTuple::Matrix<double> m_rawp4_Dshw;
        NTuple::Matrix<double> m_p4_Dshw;
        NTuple::Item<int> m_mode;
        NTuple::Item<int> m_charm;
        NTuple::Item<double> m_chi2_vf;
        NTuple::Item<double> m_chi2_kf;
        NTuple::Item<int> m_n_count;

        // Ntuple2 info
        NTuple::Tuple* m_tuple2;
        NTuple::Item<int> m_runNo_otherTrk;
        NTuple::Item<int> m_evtNo_otherTrk;
        NTuple::Item<int> m_flag1_otherTrk;
        NTuple::Item<int> m_n_othertrks;
        NTuple::Matrix<double> m_rawp4_otherMdctrk;
        NTuple::Matrix<double> m_rawp4_otherMdcKaltrk;
        NTuple::Item<int> m_charge_otherMdctrk;

        // Ntuple3 info
        NTuple::Tuple* m_tuple3;
        NTuple::Item<int> m_runNo_otherShw;
        NTuple::Item<int> m_evtNo_otherShw;
        NTuple::Item<int> m_flag1_otherShw;
        NTuple::Item<int> m_n_othershws;
        NTuple::Matrix<double> m_rawp4_othershw;

        // Ntuple4 info
        NTuple::Tuple* m_tuple4;
        NTuple::Item<int> m_runNo_allTruth;
        NTuple::Item<int> m_evtNo_allTruth;
        NTuple::Item<int> m_flag1_allTruth;
        NTuple::Item<int> m_idxmc;
        NTuple::Array<int> m_pdgid;
        NTuple::Array<int> m_motheridx;
        NTuple::Matrix<double> m_p4_alltrk;

        // Ntuple5 info
        NTuple::Tuple* m_tuple5;
        NTuple::Item<int> m_runNo_DststTruth;
        NTuple::Item<int> m_evtNo_DststTruth;
        NTuple::Item<int> m_flag1_DststTruth;
        NTuple::Array<double> m_p4_pip;
        NTuple::Array<double> m_p4_pim;
        NTuple::Array<double> m_p4_Dstst;
        NTuple::Array<double> m_p4_D1; // D comes from D1_2420
        NTuple::Array<double> m_p4_D2; // D comes out of D1_2420

        // Ntuple6 info
        NTuple::Tuple* m_tuple6;
        NTuple::Item<int> m_runNo_PsiTruth;
        NTuple::Item<int> m_evtNo_PsiTruth;
        NTuple::Item<int> m_flag1_PsiTruth;
        NTuple::Array<double> m_p4_pip_psi;
        NTuple::Array<double> m_p4_pim_psi;
        NTuple::Array<double> m_p4_psi;
        NTuple::Array<double> m_p4_Dp_psi;
        NTuple::Array<double> m_p4_Dm_psi;

        // Ntuple7 info
        NTuple::Tuple* m_tuple7;
        NTuple::Item<int> m_runNo_DpDmTruth;
        NTuple::Item<int> m_evtNo_DpDmTruth;
        NTuple::Item<int> m_flag1_DpDmTruth;
        NTuple::Item<int> m_Id_Dp;
        NTuple::Item<int> m_Id_Dm;

        // functions
        void clearVariables();
        void recordVariables();
        void saveAllMcTruthInfo();
        void saveDststMcTruthInfo();
        void savePsi_3770McTruthInfo();
        void saveDpDmMcTruthInfo();
        bool useDTagTool();
        bool tagSingleD();
        bool saveCandD(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon);
        double fitVertex(VWTrkPara &vwtrkpara, VertexParameter &birth_photon);
        double fitKM(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth);
        bool saveOthertrks();
        bool saveOthershws();
};
#endif
