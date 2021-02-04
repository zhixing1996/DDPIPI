#ifndef Physics_Analysis_DDecay_H
#define Physics_Analysis_DDecay_H 

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

class DDecay : public Algorithm {

    public:
        DDecay(const std::string& name, ISvcLocator* pSvcLocator);
        StatusCode initialize();
        StatusCode execute();
        StatusCode finalize();  

    private:
        std::vector<int> m_DModes;
        bool m_isMonteCarlo;
        bool m_pid;
        bool m_debug;
        double m_Ecms;
        double m_W_m_Kpipi;
        double m_W_rm_Dpipi;
        double mD_low;
        double mD_up;
        double mDtag_signal_low;
        double mDtag_signal_up;
        double mDtag_sidebandlow_low;
        double mDtag_sidebandlow_up;
        double mDtag_sidebandup_low;
        double mDtag_sidebandup_up;
        double rawm_D;
        double mDmiss_signal_low;
        double mDmiss_signal_up;
        double mDmiss_sidebandlow_low;
        double mDmiss_sidebandlow_up;
        double mDmiss_sidebandup_low;
        double mDmiss_sidebandup_up;

        // judgement variables
        bool stat_DTagTool;
        bool stat_tagSD;
        bool stat_saveCandD;
        bool stat_saveOthertrks;
        bool stat_saveOthershws;
        bool stat_fitpi0;
        bool stat_fitpi0_STDDmiss;
        bool stat_fitSecondVertex_STDDmiss;
        bool stat_fitSecondVertex_Dtrk;
        bool has_lep;
        bool has_lep_STDDmiss;
        
        // common info
        int runNo;
        int evtNo;
        long flag1;

        // All McTruth info
        double p4_mc_all[100][4];
        int pdgid[100];
        int motheridx[100];
        int idxmc;

        // background check
        int n_p;
        int n_pbar;
        int n_Kp;
        int n_Km;

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
        double chi2_kf_low;
        double chi2_kf_up;
        double chi2_kf_STDDmiss;
        double chi2_kf_STDDmiss_side1_low;
        double chi2_kf_STDDmiss_side1_up;
        double chi2_kf_STDDmiss_side2_low;
        double chi2_kf_STDDmiss_side2_up;
        double chi2_kf_STDDmiss_side3_low;
        double chi2_kf_STDDmiss_side3_up;
        double chi2_kf_STDDmiss_side4_low;
        double chi2_kf_STDDmiss_side4_up;
        int charge_otherMdctrk;
        double rawp4_othershw[50][4];
        double mDcand;
        int n_count;
        int charge_left_STDDmiss;
        VWTrkPara vwtrkpara_othershws;
        int is_OK_STD;
        int is_OK_STD_low;
        int is_OK_STD_up;
        int is_OK_STDDmiss;
        int is_OK_STDDmiss_side1_low;
        int is_OK_STDDmiss_side1_up;
        int is_OK_STDDmiss_side2_low;
        int is_OK_STDDmiss_side2_up;
        int is_OK_STDDmiss_side3_low;
        int is_OK_STDDmiss_side3_up;
        int is_OK_STDDmiss_side4_low;
        int is_OK_STDDmiss_side4_up;

        // Ntuple1 info
        NTuple::Tuple* m_tuple1;
        NTuple::Item<int> m_runNo;
        NTuple::Item<int> m_evtNo;
        NTuple::Item<int> m_flag1;
        NTuple::Item<int> m_n_trkD;
        NTuple::Matrix<double> m_rawp4_Dtrk;
        NTuple::Matrix<double> m_p4_Dtrk;
        NTuple::Matrix<double> m_p4_Dlowtrk;
        NTuple::Matrix<double> m_p4_Duptrk;
        NTuple::Item<int> m_n_shwD;
        NTuple::Matrix<double> m_rawp4_Dshw;
        NTuple::Matrix<double> m_p4_Dshw;
        NTuple::Matrix<double> m_p4_Dlowshw;
        NTuple::Matrix<double> m_p4_Dupshw;
        NTuple::Item<int> m_mode;
        NTuple::Item<int> m_charm;
        NTuple::Item<double> m_chi2_vf;
        NTuple::Item<double> m_chi2_kf;
        NTuple::Item<double> m_chi2_kf_low;
        NTuple::Item<double> m_chi2_kf_up;
        NTuple::Item<int> m_is_OK_STD;
        NTuple::Item<int> m_is_OK_STD_low;
        NTuple::Item<int> m_is_OK_STD_up;
        NTuple::Item<int> m_n_count;
        NTuple::Item<int> m_n_othertrks;
        NTuple::Item<int> m_n_otherleps;
        NTuple::Item<int> m_n_p;
        NTuple::Item<int> m_n_pbar;
        NTuple::Item<int> m_n_Kp;
        NTuple::Item<int> m_n_Km;
        NTuple::Matrix<double> m_rawp4_otherMdctrk;
        NTuple::Matrix<double> m_rawp4_otherMdcKaltrk;
        NTuple::Matrix<double> m_rawp4_otherlep;
        NTuple::Matrix<double> m_vtx_otherMdcKaltrk;
        NTuple::Item<int> m_charge_otherMdctrk;
        NTuple::Item<int> m_n_othershws;
        NTuple::Matrix<double> m_rawp4_othershw;
        NTuple::Matrix<double> m_vtx_othershw;
        NTuple::Item<int> m_n_pi0;
        NTuple::Array<double> m_chi2_pi0;
        NTuple::Matrix<double> m_p4_pi0;
        NTuple::Item<double> m_chi2_pi0_save;
        NTuple::Array<double> m_p4_pi0_save;
        NTuple::Item<int> m_idxmc;
        NTuple::Array<int> m_pdgid;
        NTuple::Array<int> m_motheridx;
        NTuple::Matrix<double> m_p4_mc_all;
        // for sys error
        NTuple::Item<double> m_chi2_svf_Dtrk;
        NTuple::Item<double> m_ctau_svf_Dtrk;
        NTuple::Item<double> m_L_svf_Dtrk;
        NTuple::Item<double> m_Lerr_svf_Dtrk;

        // Ntuple2 info
        NTuple::Tuple* m_tuple2;
        NTuple::Item<int> m_runNo_STDDmiss;
        NTuple::Item<int> m_evtNo_STDDmiss;
        NTuple::Item<int> m_flag1_STDDmiss;
        NTuple::Item<int> m_n_trkD_STDDmiss;
        NTuple::Item<int> m_n_shwD_STDDmiss;
        NTuple::Matrix<double> m_rawp4_Dtrk_STDDmiss;
        NTuple::Matrix<double> m_rawp4_Dshw_STDDmiss;
        NTuple::Matrix<double> m_p4_Dtrkold_STDDmiss;
        NTuple::Matrix<double> m_p4_Dshwold_STDDmiss;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss;
        NTuple::Array<double> m_p4_piplus_STDDmiss;
        NTuple::Array<double> m_p4_piminus_STDDmiss;
        NTuple::Item<double> m_chi2_kf_STDDmiss;
        NTuple::Item<int> m_is_OK_STDDmiss;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss_side1_low;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss_side1_low;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss_side1_low;
        NTuple::Array<double> m_p4_piplus_STDDmiss_side1_low;
        NTuple::Array<double> m_p4_piminus_STDDmiss_side1_low;
        NTuple::Item<double> m_chi2_kf_STDDmiss_side1_low;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss_side1_up;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss_side1_up;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss_side1_up;
        NTuple::Array<double> m_p4_piplus_STDDmiss_side1_up;
        NTuple::Array<double> m_p4_piminus_STDDmiss_side1_up;
        NTuple::Item<double> m_chi2_kf_STDDmiss_side1_up;
        NTuple::Item<int> m_is_OK_STDDmiss_side1_low;
        NTuple::Item<int> m_is_OK_STDDmiss_side1_up;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss_side2_low;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss_side2_low;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss_side2_low;
        NTuple::Array<double> m_p4_piplus_STDDmiss_side2_low;
        NTuple::Array<double> m_p4_piminus_STDDmiss_side2_low;
        NTuple::Item<double> m_chi2_kf_STDDmiss_side2_low;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss_side2_up;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss_side2_up;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss_side2_up;
        NTuple::Array<double> m_p4_piplus_STDDmiss_side2_up;
        NTuple::Array<double> m_p4_piminus_STDDmiss_side2_up;
        NTuple::Item<double> m_chi2_kf_STDDmiss_side2_up;
        NTuple::Item<int> m_is_OK_STDDmiss_side2_low;
        NTuple::Item<int> m_is_OK_STDDmiss_side2_up;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss_side3_low;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss_side3_low;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss_side3_low;
        NTuple::Array<double> m_p4_piplus_STDDmiss_side3_low;
        NTuple::Array<double> m_p4_piminus_STDDmiss_side3_low;
        NTuple::Item<double> m_chi2_kf_STDDmiss_side3_low;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss_side3_up;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss_side3_up;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss_side3_up;
        NTuple::Array<double> m_p4_piplus_STDDmiss_side3_up;
        NTuple::Array<double> m_p4_piminus_STDDmiss_side3_up;
        NTuple::Item<double> m_chi2_kf_STDDmiss_side3_up;
        NTuple::Item<int> m_is_OK_STDDmiss_side3_low;
        NTuple::Item<int> m_is_OK_STDDmiss_side3_up;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss_side4_low;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss_side4_low;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss_side4_low;
        NTuple::Array<double> m_p4_piplus_STDDmiss_side4_low;
        NTuple::Array<double> m_p4_piminus_STDDmiss_side4_low;
        NTuple::Item<double> m_chi2_kf_STDDmiss_side4_low;
        NTuple::Matrix<double> m_p4_Dtrk_STDDmiss_side4_up;
        NTuple::Matrix<double> m_p4_Dshw_STDDmiss_side4_up;
        NTuple::Array<double> m_p4_Dmiss_STDDmiss_side4_up;
        NTuple::Array<double> m_p4_piplus_STDDmiss_side4_up;
        NTuple::Array<double> m_p4_piminus_STDDmiss_side4_up;
        NTuple::Item<double> m_chi2_kf_STDDmiss_side4_up;
        NTuple::Item<int> m_is_OK_STDDmiss_side4_low;
        NTuple::Item<int> m_is_OK_STDDmiss_side4_up;
        NTuple::Item<int> m_mode_STDDmiss;
        NTuple::Item<int> m_charm_STDDmiss;
        NTuple::Item<double> m_chi2_vf_STDDmiss;
        NTuple::Item<double> m_chi2_svf_STDDmiss;
        NTuple::Item<double> m_ctau_svf_STDDmiss;
        NTuple::Item<double> m_L_svf_STDDmiss;
        NTuple::Item<double> m_Lerr_svf_STDDmiss;
        NTuple::Item<int> m_idxmc_STDDmiss;
        NTuple::Array<int> m_pdgid_STDDmiss;
        NTuple::Array<int> m_motheridx_STDDmiss;
        NTuple::Matrix<double> m_p4_mc_all_STDDmiss;
        NTuple::Item<int> m_charge_left_STDDmiss;
        NTuple::Item<int> m_n_othertrks_STDDmiss;
        NTuple::Item<int> m_n_otherleps_STDDmiss;
        NTuple::Item<int> m_n_p_STDDmiss;
        NTuple::Item<int> m_n_pbar_STDDmiss;
        NTuple::Item<int> m_n_Kp_STDDmiss;
        NTuple::Item<int> m_n_Km_STDDmiss;
        NTuple::Matrix<double> m_rawp4_otherMdctrk_STDDmiss;
        NTuple::Matrix<double> m_rawp4_otherMdcKaltrk_STDDmiss;
        NTuple::Matrix<double> m_vtx_otherMdcKaltrk_STDDmiss;
        NTuple::Matrix<double> m_rawp4_otherlep_STDDmiss;
        NTuple::Array<double> m_rawp4_tagPiplus_STDDmiss;
        NTuple::Array<double> m_rawp4_tagPiminus_STDDmiss;
        NTuple::Array<double> m_vtx_tagPiplus_STDDmiss;
        NTuple::Array<double> m_vtx_tagPiminus_STDDmiss;
        NTuple::Item<int> m_n_othershws_STDDmiss;
        NTuple::Matrix<double> m_rawp4_othershw_STDDmiss;
        NTuple::Matrix<double> m_vtx_othershw_STDDmiss;
        NTuple::Item<int> m_n_pi0_STDDmiss;
        NTuple::Array<double> m_chi2_pi0_STDDmiss;
        NTuple::Matrix<double> m_p4_pi0_STDDmiss;
        NTuple::Item<double> m_chi2_pi0_save_STDDmiss;
        NTuple::Array<double> m_p4_pi0_save_STDDmiss;
        NTuple::Item<int> m_matched_D;
        NTuple::Item<int> m_matched_D_STDDmiss;
        NTuple::Item<int> m_matched_pi;
        NTuple::Item<int> m_matched_piplus;
        NTuple::Item<int> m_matched_piminus;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss_side1_low;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss_side1_up;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss_side2_low;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss_side2_up;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss_side3_low;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss_side3_up;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss_side4_low;
        NTuple::Item<double> m_rm_Dpipi_STDDmiss_side4_up;
        NTuple::Array<double> m_p4_mcall_truth;
        NTuple::Array<double> m_p4_piplus_truth;
        NTuple::Array<double> m_p4_piminus_truth;
        NTuple::Array<double> m_p4_Dplus_truth;
        NTuple::Array<double> m_p4_Dminus_truth;

        // Ntuple3 info
        NTuple::Tuple* m_tuple3;
        NTuple::Item<int> m_runNo_Truth;
        NTuple::Item<int> m_evtNo_Truth;
        NTuple::Item<int> m_idxmc_Truth;
        NTuple::Array<int> m_pdgid_Truth;
        NTuple::Array<int> m_motheridx_Truth;
        NTuple::Matrix<double> m_p4_mc_all_Truth;

        // functions
        void clearVariables();
        void recordVariables();
        void recordVariables_STDDmiss();
        void recordVariables_Truth();
        void saveAllMcTruthInfo();
        bool saveTruth();
        bool useDTagTool();
        bool tagSingleD();
        bool saveCandD(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon);
        double fitVertex(VWTrkPara &vwtrkpara, VertexParameter &birth_photon);
        double fitKM(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth);
        double fitKM_low(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth, double mDtag_low);
        double fitKM_up(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth, double mDtag_up);
        double fitKM_STDDmiss(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth);
        double fitKM_STDDmiss_side1_low(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double m_Dtag, double m_Dmiss);
        double fitKM_STDDmiss_side1_up(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double m_Dtag, double m_Dmiss);
        double fitKM_STDDmiss_side2_low(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double m_Dtag, double m_Dmiss);
        double fitKM_STDDmiss_side2_up(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double m_Dtag, double m_Dmiss);
        double fitKM_STDDmiss_side3_low(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double m_Dtag, double m_Dmiss);
        double fitKM_STDDmiss_side3_up(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double m_Dtag, double m_Dmiss);
        double fitKM_STDDmiss_side4_low(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double m_Dtag, double m_Dmiss);
        double fitKM_STDDmiss_side4_up(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double m_Dtag, double m_Dmiss);
        bool fitSecondVertex_STDDmiss(VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus);
        bool fitSecondVertex_Dtrk(WTrackParameter &Dpiplus, WTrackParameter &Dpiminus);
        bool fitpi0(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD);
        bool fitpi0_STDDmiss(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD);
        bool saveOthertrks(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth);
        bool saveOthershws();
        int MatchMC(HepLorentzVector &p4, std::string MODE);
        double ECMS(int runNo);
};
#endif
