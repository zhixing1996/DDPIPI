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
#include "VertexFit/SecondVertexFit.h"
#include "VertexFit/Helix.h"
#include "VertexFit/WTrackParameter.h"
#include "ParticleID/ParticleID.h"

#include "McTruth/McParticle.h"

#include "TMath.h"
#include "TLorentzVector.h"
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
        bool stat_fitpi0;
        bool stat_fitpi0_signal;
        bool stat_fitpi0_sidebandlow;
        bool stat_fitpi0_sidebandup;
        bool stat_fitSecondVertex;
        
        // common info
        int runNo;
        int evtNo;
        long flag1;

        // All McTruth info
        int pdgid[100];
        int motheridx[100];
        int idxmc;

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
        int mode;
        int MODE;
        int charm;
        double chi2_vf;
        VertexParameter birth;
        double chi2_kf;
        double chi2_kf_signal;
        double chi2_kf_sidebandlow;
        double chi2_kf_sidebandup;
        int charge_otherMdctrk;
        double rawp4_othershw[50][4];
        double mDcand;
        int n_count;
        int charge_left_signal;
        int charge_left_sidebandlow;
        int charge_left_sidebandup;
        VWTrkPara vwtrkpara_othershws;

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
        NTuple::Item<int> m_n_pi0;
        NTuple::Array<double> m_chi2_pi0;
        NTuple::Matrix<double> m_p4_pi0;
        NTuple::Item<double> m_chi2_pi0_save;
        NTuple::Array<double> m_p4_pi0_save;

        // Ntuple4 info
        NTuple::Tuple* m_tuple4;
        NTuple::Item<int> m_runNo_allTruth;
        NTuple::Item<int> m_evtNo_allTruth;
        NTuple::Item<int> m_flag1_allTruth;
        NTuple::Item<int> m_idxmc;
        NTuple::Array<int> m_pdgid;
        NTuple::Array<int> m_motheridx;

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

        // Ntuple8 info
        NTuple::Tuple* m_tuple8;
        NTuple::Item<int> m_runNo_signal;
        NTuple::Item<int> m_evtNo_signal;
        NTuple::Item<int> m_flag1_signal;
        NTuple::Item<int> m_n_trkD_signal;
        NTuple::Matrix<double> m_rawp4_Dtrk_signal;
        NTuple::Matrix<double> m_p4_Dtrk_signal;
        NTuple::Matrix<double> m_p4_Dtrkold_signal;
        NTuple::Item<int> m_n_shwD_signal;
        NTuple::Matrix<double> m_rawp4_Dshw_signal;
        NTuple::Matrix<double> m_p4_Dshw_signal;
        NTuple::Array<double> m_p4_piplus_signal;
        NTuple::Array<double> m_p4_piminus_signal;
        NTuple::Array<double> m_p4_Dmiss_signal;
        NTuple::Item<int> m_mode_signal;
        NTuple::Item<int> m_charm_signal;
        NTuple::Item<double> m_chi2_vf_signal;
        NTuple::Item<double> m_chi2_kf_signal;
        NTuple::Item<double> m_chi2_svf;
        NTuple::Item<double> m_ctau_svf;
        NTuple::Item<double> m_L_svf;
        NTuple::Item<double> m_Lerr_svf;
        NTuple::Item<int> m_idxmc_signal;
        NTuple::Array<int> m_pdgid_signal;
        NTuple::Array<int> m_motheridx_signal;
        NTuple::Item<int> m_charge_left_signal;
        NTuple::Item<int> m_n_othertrks_signal;
        NTuple::Matrix<double> m_rawp4_otherMdctrk_signal;
        NTuple::Matrix<double> m_rawp4_otherMdcKaltrk_signal;
        NTuple::Array<double> m_rawp4_tagPiplus_signal;
        NTuple::Array<double> m_rawp4_tagPiminus_signal;
        NTuple::Item<int> m_n_othershws_signal;
        NTuple::Matrix<double> m_rawp4_othershw_signal;
        NTuple::Item<int> m_n_pi0_signal;
        NTuple::Array<double> m_chi2_pi0_signal;
        NTuple::Matrix<double> m_p4_pi0_signal;
        NTuple::Item<double> m_chi2_pi0_save_signal;
        NTuple::Array<double> m_p4_pi0_save_signal;
        NTuple::Item<int> m_matched_D;
        NTuple::Item<int> m_matched_D_signal;
        NTuple::Item<int> m_matched_pi;
        NTuple::Item<int> m_matched_piplus;
        NTuple::Item<int> m_matched_piminus;

        // Ntuple9 info
        NTuple::Tuple* m_tuple9;
        NTuple::Item<int> m_runNo_sidebandlow;
        NTuple::Item<int> m_evtNo_sidebandlow;
        NTuple::Item<int> m_flag1_sidebandlow;
        NTuple::Item<int> m_n_trkD_sidebandlow;
        NTuple::Matrix<double> m_rawp4_Dtrk_sidebandlow;
        NTuple::Matrix<double> m_p4_Dtrk_sidebandlow;
        NTuple::Matrix<double> m_p4_Dtrkold_sidebandlow;
        NTuple::Item<int> m_n_shwD_sidebandlow;
        NTuple::Matrix<double> m_rawp4_Dshw_sidebandlow;
        NTuple::Matrix<double> m_p4_Dshw_sidebandlow;
        NTuple::Array<double> m_p4_piplus_sidebandlow;
        NTuple::Array<double> m_p4_piminus_sidebandlow;
        NTuple::Array<double> m_p4_Dmiss_sidebandlow;
        NTuple::Item<int> m_mode_sidebandlow;
        NTuple::Item<int> m_charm_sidebandlow;
        NTuple::Item<double> m_chi2_vf_sidebandlow;
        NTuple::Item<double> m_chi2_kf_sidebandlow;
        NTuple::Item<int> m_idxmc_sidebandlow;
        NTuple::Array<int> m_pdgid_sidebandlow;
        NTuple::Array<int> m_motheridx_sidebandlow;
        NTuple::Item<int> m_charge_left_sidebandlow;
        NTuple::Item<int> m_n_othertrks_sidebandlow;
        NTuple::Matrix<double> m_rawp4_otherMdctrk_sidebandlow;
        NTuple::Matrix<double> m_rawp4_otherMdcKaltrk_sidebandlow;
        NTuple::Array<double> m_rawp4_tagPiplus_sidebandlow;
        NTuple::Array<double> m_rawp4_tagPiminus_sidebandlow;
        NTuple::Item<int> m_n_othershws_sidebandlow;
        NTuple::Matrix<double> m_rawp4_othershw_sidebandlow;
        NTuple::Item<int> m_n_pi0_sidebandlow;
        NTuple::Array<double> m_chi2_pi0_sidebandlow;
        NTuple::Matrix<double> m_p4_pi0_sidebandlow;
        NTuple::Item<double> m_chi2_pi0_save_sidebandlow;
        NTuple::Array<double> m_p4_pi0_save_sidebandlow;

        // Ntuple10 info
        NTuple::Tuple* m_tuple10;
        NTuple::Item<int> m_runNo_sidebandup;
        NTuple::Item<int> m_evtNo_sidebandup;
        NTuple::Item<int> m_flag1_sidebandup;
        NTuple::Item<int> m_n_trkD_sidebandup;
        NTuple::Matrix<double> m_rawp4_Dtrk_sidebandup;
        NTuple::Matrix<double> m_p4_Dtrk_sidebandup;
        NTuple::Matrix<double> m_p4_Dtrkold_sidebandup;
        NTuple::Item<int> m_n_shwD_sidebandup;
        NTuple::Matrix<double> m_rawp4_Dshw_sidebandup;
        NTuple::Matrix<double> m_p4_Dshw_sidebandup;
        NTuple::Array<double> m_p4_piplus_sidebandup;
        NTuple::Array<double> m_p4_piminus_sidebandup;
        NTuple::Array<double> m_p4_Dmiss_sidebandup;
        NTuple::Item<int> m_mode_sidebandup;
        NTuple::Item<int> m_charm_sidebandup;
        NTuple::Item<double> m_chi2_vf_sidebandup;
        NTuple::Item<double> m_chi2_kf_sidebandup;
        NTuple::Item<int> m_idxmc_sidebandup;
        NTuple::Array<int> m_pdgid_sidebandup;
        NTuple::Array<int> m_motheridx_sidebandup;
        NTuple::Item<int> m_charge_left_sidebandup;
        NTuple::Item<int> m_n_othertrks_sidebandup;
        NTuple::Matrix<double> m_rawp4_otherMdctrk_sidebandup;
        NTuple::Matrix<double> m_rawp4_otherMdcKaltrk_sidebandup;
        NTuple::Array<double> m_rawp4_tagPiplus_sidebandup;
        NTuple::Array<double> m_rawp4_tagPiminus_sidebandup;
        NTuple::Item<int> m_n_othershws_sidebandup;
        NTuple::Matrix<double> m_rawp4_othershw_sidebandup;
        NTuple::Item<int> m_n_pi0_sidebandup;
        NTuple::Array<double> m_chi2_pi0_sidebandup;
        NTuple::Matrix<double> m_p4_pi0_sidebandup;
        NTuple::Item<double> m_chi2_pi0_save_sidebandup;
        NTuple::Array<double> m_p4_pi0_save_sidebandup;

        // functions
        void clearVariables();
        void recordVariables();
        void recordVariables_signal();
        void recordVariables_sidebandlow();
        void recordVariables_sidebandup();
        void saveAllMcTruthInfo();
        void saveDststMcTruthInfo();
        void savePsi_3770McTruthInfo();
        void saveDpDmMcTruthInfo();
        bool useDTagTool();
        bool tagSingleD();
        bool saveCandD(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon);
        double fitVertex(VWTrkPara &vwtrkpara, VertexParameter &birth_photon);
        double fitKM(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth);
        double fitKM_signal(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth);
        bool fitSecondVertex(VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus);
        double fitKM_sidebandlow(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double sidebandlow_mean);
        double fitKM_sidebandup(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double sidebandup_mean);
        bool fitpi0(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD);
        bool fitpi0_signal(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD);
        bool fitpi0_sidebandlow(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD);
        bool fitpi0_sidebandup(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD);
        bool saveOthertrks(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth);
        bool saveOthershws();
        int MatchMC(HepLorentzVector &p4, std::string MODE);
};
#endif
