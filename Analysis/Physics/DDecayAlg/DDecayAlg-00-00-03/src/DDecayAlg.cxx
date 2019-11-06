// -*- C++ -*- //
//
// Description: ee -> DD(2420) -> DDPIPI
//
// Original Author:  Maoqiang JING <jingmq@ihep.ac.cn>
//         Created:  [2019-08-08 Thu 15:09] 
//         Inspired by Suyu XIAO's code 
// 
//

#include "DDecayAlg.h"

const double PI = 3.1415927;
const double M_Pi0 = 0.1349766;
const double M_D0 = 1.86483;
const double M_Dplus = 1.86965;
const double M_Dst = 2.01026;
const double mass[5] = {
    0.000511, 0.105658, 0.139570, 0.493677, 0.938272 // e, mu, pi, K, p
};

// 
// module declare
//

VertexFit * vtxfit = VertexFit::instance();
KinematicFit * kmfit = KinematicFit::instance();

DECLARE_ALGORITHM_FACTORY( DDecayAlg )
DECLARE_FACTORY_ENTRIES( DDecayAlg ) {
    DECLARE_ALGORITHM( DDecayAlg );
}

LOAD_FACTORY_ENTRIES( DDecayAlg )

DDecayAlg::DDecayAlg(const std::string& name, ISvcLocator* pSvcLocator) :
	Algorithm(name, pSvcLocator) {
        m_DModes.push_back(200);
        m_DModes.push_back(205);
        m_DModes.push_back(208);
        m_DModes.push_back(213);
        m_DModes.push_back(216);
        declareProperty("DMode", m_DModes);
        declareProperty("IsMonteCarlo", m_isMonteCarlo = true);
        declareProperty("UsePID", m_pid = true);
        declareProperty("Debug", m_debug = false);
}

StatusCode DDecayAlg::initialize() {
    MsgStream log(msgSvc(), name());
    log << MSG::INFO << ">>>>>>> in initialize()" << endmsg;

    StatusCode status;

    NTuplePtr nt1(ntupleSvc(), "FILE1/STD");
    if (nt1) m_tuple1 = nt1;
    else {
        m_tuple1 = ntupleSvc()->book("FILE1/STD", CLID_ColumnWiseTuple, "Single tag D decay");
        if (m_tuple1) {
            status = m_tuple1->addItem("runNo", m_runNo);
            status = m_tuple1->addItem("evtNo", m_evtNo);
            status = m_tuple1->addItem("flag1", m_flag1);
            status = m_tuple1->addItem("n_trkD", m_n_trkD, 0, 5); // number of members should locates in 0~5
            status = m_tuple1->addIndexedItem("rawp4_Dtrk", m_n_trkD, 6, m_rawp4_Dtrk); // four members array
            status = m_tuple1->addIndexedItem("p4_Dtrk", m_n_trkD, 4, m_p4_Dtrk);
            status = m_tuple1->addItem("n_shwD", m_n_shwD, 0, 2); 
            status = m_tuple1->addIndexedItem("rawp4_Dshw", m_n_shwD, 4, m_rawp4_Dshw);
            status = m_tuple1->addIndexedItem("p4_Dshw", m_n_shwD, 4, m_p4_Dshw);
            status = m_tuple1->addItem("mode", m_mode);
            status = m_tuple1->addItem("charm", m_charm);
            status = m_tuple1->addItem("chi2_vf", m_chi2_vf);
            status = m_tuple1->addItem("chi2_kf", m_chi2_kf);
            status = m_tuple1->addItem("n_count", m_n_count); // multi-counting D in one event
            status = m_tuple1->addItem("matched_D", m_matched_D);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple1) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt2(ntupleSvc(), "FILE1/otherTrk");
    if (nt2) m_tuple2 = nt2;
    else {
        m_tuple2 = ntupleSvc()->book("FILE1/otherTrk", CLID_ColumnWiseTuple, "tracks info does not come from tagged D");
        if (m_tuple2) {
            status = m_tuple2->addItem("runNo", m_runNo_otherTrk);
            status = m_tuple2->addItem("evtNo", m_evtNo_otherTrk);
            status = m_tuple2->addItem("flag1", m_flag1_otherTrk);
            status = m_tuple2->addItem("n_othertrks", m_n_othertrks, 0, 20);
            status = m_tuple2->addIndexedItem("rawp4_otherMdctrk", m_n_othertrks, 6, m_rawp4_otherMdctrk);
            status = m_tuple2->addIndexedItem("rawp4_otherMdcKaltrk", m_n_othertrks, 7, m_rawp4_otherMdcKaltrk);
            status = m_tuple2->addItem("charge_otherMdctrk", m_charge_otherMdctrk, 0, 10);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple2) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt3(ntupleSvc(), "FILE1/otherShw");
    if (nt3) m_tuple3 = nt3;
    else {
        m_tuple3 = ntupleSvc()->book("FILE1/otherShw", CLID_ColumnWiseTuple, "showers info does not come from tagged D");
        if (m_tuple3) {
            status = m_tuple3->addItem("runNo", m_runNo_otherShw);
            status = m_tuple3->addItem("evtNo", m_evtNo_otherShw);
            status = m_tuple3->addItem("flag1", m_flag1_otherShw);
            status = m_tuple3->addItem("n_othershws", m_n_othershws, 0, 50);
            status = m_tuple3->addIndexedItem("rawp4_othershw", m_n_othershws, 4, m_rawp4_othershw);
            status = m_tuple3->addItem("n_pi0", m_n_pi0, 0, 200);
            status = m_tuple3->addIndexedItem("chi2_pi0", m_n_pi0, m_chi2_pi0);
            status = m_tuple3->addIndexedItem("p4_pi0", m_n_pi0, 4, m_p4_pi0);
            status = m_tuple3->addItem("chi2_pi0_save", m_chi2_pi0_save);
            status = m_tuple3->addItem("p4_pi0_save", 4, m_p4_pi0_save);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple3) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt4(ntupleSvc(), "FILE1/allTruth");
    if (nt4) m_tuple4 = nt4;
    else {
        m_tuple4 = ntupleSvc()->book("FILE1/allTruth", CLID_ColumnWiseTuple, "all McTruth info");
        if (m_tuple4) {
            status = m_tuple4->addItem("runNo", m_runNo_allTruth);
            status = m_tuple4->addItem("evtNo", m_evtNo_allTruth);
            status = m_tuple4->addItem("flag1", m_flag1_allTruth);
            status = m_tuple4->addItem("indexmc", m_idxmc, 0, 100);
            status = m_tuple4->addIndexedItem("pdgid", m_idxmc, m_pdgid);
            status = m_tuple4->addIndexedItem("motheridx", m_idxmc, m_motheridx);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple4) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt5(ntupleSvc(), "FILE1/DststTruth");
    if (nt5) m_tuple5 = nt5;
    else {
        m_tuple5 = ntupleSvc()->book("FILE1/DststTruth", CLID_ColumnWiseTuple, "D1_2420 McTruth info");
        if (m_tuple5) {
            status = m_tuple5->addItem("runNo", m_runNo_DststTruth);
            status = m_tuple5->addItem("evtNo", m_evtNo_DststTruth);
            status = m_tuple5->addItem("flag1", m_flag1_DststTruth);
            status = m_tuple5->addItem("p4_pip", 4, m_p4_pip);
            status = m_tuple5->addItem("p4_pim", 4, m_p4_pim);
            status = m_tuple5->addItem("p4_Dstst", 4, m_p4_Dstst);
            status = m_tuple5->addItem("p4_D1", 4, m_p4_D1);
            status = m_tuple5->addItem("p4_D2", 4, m_p4_D2);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple5) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt6(ntupleSvc(), "FILE1/PsiTruth");
    if (nt6) m_tuple6 = nt6;
    else {
        m_tuple6 = ntupleSvc()->book("FILE1/PsiTruth", CLID_ColumnWiseTuple, "Psi_3770 McTruth info");
        if (m_tuple6) {
            status = m_tuple6->addItem("runNo", m_runNo_PsiTruth);
            status = m_tuple6->addItem("evtNo", m_evtNo_PsiTruth);
            status = m_tuple6->addItem("flag1", m_flag1_PsiTruth);
            status = m_tuple6->addItem("p4_pip", 4, m_p4_pip_psi);
            status = m_tuple6->addItem("p4_pim", 4, m_p4_pim_psi);
            status = m_tuple6->addItem("p4_psi", 4, m_p4_psi);
            status = m_tuple6->addItem("p4_Dp", 4, m_p4_Dp_psi);
            status = m_tuple6->addItem("p4_Dm", 4, m_p4_Dm_psi);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple6) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt7(ntupleSvc(), "FILE1/DpDmTruth");
    if (nt7) m_tuple7 = nt7;
    else {
        m_tuple7 = ntupleSvc()->book("FILE1/DpDmTruth", CLID_ColumnWiseTuple, "Dplus and Dminus McTruth info");
        if (m_tuple7) {
            status = m_tuple7->addItem("runNo", m_runNo_DpDmTruth);
            status = m_tuple7->addItem("evtNo", m_evtNo_DpDmTruth);
            status = m_tuple7->addItem("flag1", m_flag1_DpDmTruth);
            status = m_tuple7->addItem("DpId", m_Id_Dp);
            status = m_tuple7->addItem("DmId", m_Id_Dm);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple7) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt8(ntupleSvc(), "FILE1/STD_signal");
    if (nt8) m_tuple8 = nt8;
    else {
        m_tuple8 = ntupleSvc()->book("FILE1/STD_signal", CLID_ColumnWiseTuple, "Single tag D decay with kinematic fit missing a D in signal region");
        if (m_tuple8) {
            status = m_tuple8->addItem("runNo", m_runNo_signal);
            status = m_tuple8->addItem("evtNo", m_evtNo_signal);
            status = m_tuple8->addItem("flag1", m_flag1_signal);
            status = m_tuple8->addItem("n_trkD", m_n_trkD_signal, 0, 5); // number of members should locates in 0~5
            status = m_tuple8->addIndexedItem("rawp4_Dtrk", m_n_trkD_signal, 6, m_rawp4_Dtrk_signal); // four members array
            status = m_tuple8->addIndexedItem("p4_Dtrk", m_n_trkD_signal, 4, m_p4_Dtrk_signal);
            status = m_tuple8->addIndexedItem("p4_Dtrkold", m_n_trkD_signal, 4, m_p4_Dtrkold_signal);
            status = m_tuple8->addItem("n_shwD", m_n_shwD_signal, 0, 2); 
            status = m_tuple8->addIndexedItem("rawp4_Dshw", m_n_shwD_signal, 4, m_rawp4_Dshw_signal);
            status = m_tuple8->addIndexedItem("p4_Dshw", m_n_shwD_signal, 4, m_p4_Dshw_signal);
            status = m_tuple8->addItem("p4_piplus", 4, m_p4_piplus_signal);
            status = m_tuple8->addItem("p4_piminus", 4, m_p4_piminus_signal);
            status = m_tuple8->addItem("mode", m_mode_signal);
            status = m_tuple8->addItem("charm", m_charm_signal);
            status = m_tuple8->addItem("chi2_vf", m_chi2_vf_signal);
            status = m_tuple8->addItem("chi2_kf", m_chi2_kf_signal);
            status = m_tuple8->addItem("indexmc", m_idxmc_signal, 0, 100);
            status = m_tuple8->addIndexedItem("pdgid", m_idxmc_signal, m_pdgid_signal);
            status = m_tuple8->addIndexedItem("motheridx", m_idxmc_signal, m_motheridx_signal);
            status = m_tuple8->addItem("charge_left", m_charge_left_signal);
            status = m_tuple8->addItem("n_othertrks", m_n_othertrks_signal, 0, 20);
            status = m_tuple8->addIndexedItem("rawp4_otherMdctrk", m_n_othertrks_signal, 6, m_rawp4_otherMdctrk_signal);
            status = m_tuple8->addIndexedItem("rawp4_otherMdcKaltrk", m_n_othertrks_signal, 6, m_rawp4_otherMdcKaltrk_signal);
            status = m_tuple8->addItem("rawp4_tagPiplus", 4, m_rawp4_tagPiplus_signal);
            status = m_tuple8->addItem("rawp4_tagPiminus", 4, m_rawp4_tagPiminus_signal);
            status = m_tuple8->addItem("n_othershws", m_n_othershws_signal, 0, 50);
            status = m_tuple8->addIndexedItem("rawp4_othershw", m_n_othershws_signal, 4, m_rawp4_othershw_signal);
            status = m_tuple8->addItem("n_pi0", m_n_pi0_signal, 0, 200);
            status = m_tuple8->addIndexedItem("chi2_pi0", m_n_pi0_signal, m_chi2_pi0_signal);
            status = m_tuple8->addIndexedItem("p4_pi0", m_n_pi0_signal, 4, m_p4_pi0_signal);
            status = m_tuple8->addItem("chi2_pi0_save", m_chi2_pi0_save_signal);
            status = m_tuple8->addItem("p4_pi0_save", 4, m_p4_pi0_save_signal);
            status = m_tuple8->addItem("matched_D", m_matched_D_signal);
            status = m_tuple8->addItem("matched_pi", m_matched_pi);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple8) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt9(ntupleSvc(), "FILE1/STD_sidebandlow");
    if (nt9) m_tuple9 = nt9;
    else {
        m_tuple9 = ntupleSvc()->book("FILE1/STD_sidebandlow", CLID_ColumnWiseTuple, "Single tag D decay with kinematic fit missing a D in lower sideband region");
        if (m_tuple9) {
            status = m_tuple9->addItem("runNo", m_runNo_sidebandlow);
            status = m_tuple9->addItem("evtNo", m_evtNo_sidebandlow);
            status = m_tuple9->addItem("flag1", m_flag1_sidebandlow);
            status = m_tuple9->addItem("n_trkD", m_n_trkD_sidebandlow, 0, 5); // number of members should locates in 0~5
            status = m_tuple9->addIndexedItem("rawp4_Dtrk", m_n_trkD_sidebandlow, 6, m_rawp4_Dtrk_sidebandlow); // four members array
            status = m_tuple9->addIndexedItem("p4_Dtrk", m_n_trkD_sidebandlow, 4, m_p4_Dtrk_sidebandlow);
            status = m_tuple9->addIndexedItem("p4_Dtrkold", m_n_trkD_sidebandlow, 4, m_p4_Dtrkold_sidebandlow);
            status = m_tuple9->addItem("n_shwD", m_n_shwD_sidebandlow, 0, 2); 
            status = m_tuple9->addIndexedItem("rawp4_Dshw", m_n_shwD_sidebandlow, 4, m_rawp4_Dshw_sidebandlow);
            status = m_tuple9->addIndexedItem("p4_Dshw", m_n_shwD_sidebandlow, 4, m_p4_Dshw_sidebandlow);
            status = m_tuple9->addItem("p4_piplus", 4, m_p4_piplus_sidebandlow);
            status = m_tuple9->addItem("p4_piminus", 4, m_p4_piminus_sidebandlow);
            status = m_tuple9->addItem("mode", m_mode_sidebandlow);
            status = m_tuple9->addItem("charm", m_charm_sidebandlow);
            status = m_tuple9->addItem("chi2_vf", m_chi2_vf_sidebandlow);
            status = m_tuple9->addItem("chi2_kf", m_chi2_kf_sidebandlow);
            status = m_tuple9->addItem("indexmc", m_idxmc_sidebandlow, 0, 100);
            status = m_tuple9->addIndexedItem("pdgid", m_idxmc_sidebandlow, m_pdgid_sidebandlow);
            status = m_tuple9->addIndexedItem("motheridx", m_idxmc_sidebandlow, m_motheridx_sidebandlow);
            status = m_tuple9->addItem("charge_left", m_charge_left_sidebandlow);
            status = m_tuple9->addItem("n_othertrks", m_n_othertrks_sidebandlow, 0, 20);
            status = m_tuple9->addIndexedItem("rawp4_otherMdctrk", m_n_othertrks_sidebandlow, 6, m_rawp4_otherMdctrk_sidebandlow);
            status = m_tuple9->addIndexedItem("rawp4_otherMdcKaltrk", m_n_othertrks_sidebandlow, 6, m_rawp4_otherMdcKaltrk_sidebandlow);
            status = m_tuple9->addItem("rawp4_tagPiplus", 4, m_rawp4_tagPiplus_sidebandlow);
            status = m_tuple9->addItem("rawp4_tagPiminus", 4, m_rawp4_tagPiminus_sidebandlow);
            status = m_tuple9->addItem("n_othershws", m_n_othershws_sidebandlow, 0, 50);
            status = m_tuple9->addIndexedItem("rawp4_othershw", m_n_othershws_sidebandlow, 4, m_rawp4_othershw_sidebandlow);
            status = m_tuple9->addItem("n_pi0", m_n_pi0_sidebandlow, 0, 200);
            status = m_tuple9->addIndexedItem("chi2_pi0", m_n_pi0_sidebandlow, m_chi2_pi0_sidebandlow);
            status = m_tuple9->addIndexedItem("p4_pi0", m_n_pi0_sidebandlow, 4, m_p4_pi0_sidebandlow);
            status = m_tuple9->addItem("chi2_pi0_save", m_chi2_pi0_save_sidebandlow);
            status = m_tuple9->addItem("p4_pi0_save", 4, m_p4_pi0_save_sidebandlow);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple9) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    NTuplePtr nt10(ntupleSvc(), "FILE1/STD_sidebandup");
    if (nt10) m_tuple10 = nt10;
    else {
        m_tuple10 = ntupleSvc()->book("FILE1/STD_sidebandup", CLID_ColumnWiseTuple, "Single tag D decay with kinematic fit missing a D in higher sideband region");
        if (m_tuple10) {
            status = m_tuple10->addItem("runNo", m_runNo_sidebandup);
            status = m_tuple10->addItem("evtNo", m_evtNo_sidebandup);
            status = m_tuple10->addItem("flag1", m_flag1_sidebandup);
            status = m_tuple10->addItem("n_trkD", m_n_trkD_sidebandup, 0, 5); // number of members should locates in 0~5
            status = m_tuple10->addIndexedItem("rawp4_Dtrk", m_n_trkD_sidebandup, 6, m_rawp4_Dtrk_sidebandup); // four members array
            status = m_tuple10->addIndexedItem("p4_Dtrk", m_n_trkD_sidebandup, 4, m_p4_Dtrk_sidebandup);
            status = m_tuple10->addIndexedItem("p4_Dtrkold", m_n_trkD_sidebandup, 4, m_p4_Dtrkold_sidebandup);
            status = m_tuple10->addItem("n_shwD", m_n_shwD_sidebandup, 0, 2); 
            status = m_tuple10->addIndexedItem("rawp4_Dshw", m_n_shwD_sidebandup, 4, m_rawp4_Dshw_sidebandup);
            status = m_tuple10->addIndexedItem("p4_Dshw", m_n_shwD_sidebandup, 4, m_p4_Dshw_sidebandup);
            status = m_tuple10->addItem("p4_piplus", 4, m_p4_piplus_sidebandup);
            status = m_tuple10->addItem("p4_piminus", 4, m_p4_piminus_sidebandup);
            status = m_tuple10->addItem("mode", m_mode_sidebandup);
            status = m_tuple10->addItem("charm", m_charm_sidebandup);
            status = m_tuple10->addItem("chi2_vf", m_chi2_vf_sidebandup);
            status = m_tuple10->addItem("chi2_kf", m_chi2_kf_sidebandup);
            status = m_tuple10->addItem("indexmc", m_idxmc_sidebandup, 0, 100);
            status = m_tuple10->addIndexedItem("pdgid", m_idxmc_sidebandup, m_pdgid_sidebandup);
            status = m_tuple10->addIndexedItem("motheridx", m_idxmc_sidebandup, m_motheridx_sidebandup);
            status = m_tuple10->addItem("charge_left", m_charge_left_sidebandup);
            status = m_tuple10->addItem("n_othertrks", m_n_othertrks_sidebandup, 0, 20);
            status = m_tuple10->addIndexedItem("rawp4_otherMdctrk", m_n_othertrks_sidebandup, 6, m_rawp4_otherMdctrk_sidebandup);
            status = m_tuple10->addIndexedItem("rawp4_otherMdcKaltrk", m_n_othertrks_sidebandup, 6, m_rawp4_otherMdcKaltrk_sidebandup);
            status = m_tuple10->addItem("rawp4_tagPiplus", 4, m_rawp4_tagPiplus_sidebandup);
            status = m_tuple10->addItem("rawp4_tagPiminus", 4, m_rawp4_tagPiminus_sidebandup);
            status = m_tuple10->addItem("n_othershws", m_n_othershws_sidebandup, 0, 50);
            status = m_tuple10->addIndexedItem("rawp4_othershw", m_n_othershws_sidebandup, 4, m_rawp4_othershw_sidebandup);
            status = m_tuple10->addItem("n_pi0", m_n_pi0_sidebandup, 0, 200);
            status = m_tuple10->addIndexedItem("chi2_pi0", m_n_pi0_sidebandup, m_chi2_pi0_sidebandup);
            status = m_tuple10->addIndexedItem("p4_pi0", m_n_pi0_sidebandup, 4, m_p4_pi0_sidebandup);
            status = m_tuple10->addItem("chi2_pi0_save", m_chi2_pi0_save_sidebandup);
            status = m_tuple10->addItem("p4_pi0_save", 4, m_p4_pi0_save_sidebandup);
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple10) << endmsg;
            return StatusCode::FAILURE;
        }
    }

    log << MSG::INFO << "successfully return from initialize()" << endmsg;
    return StatusCode::SUCCESS;
}

StatusCode DDecayAlg::execute() {
    MsgStream log(msgSvc(), name());
    log << MSG::INFO << "in execute()" << endreq;

    // clear variables
    clearVariables();

    // grt common info
    SmartDataPtr<Event::EventHeader> eventHeader(eventSvc(),"/Event/EventHeader");
    if (!eventHeader) return StatusCode::FAILURE;
    runNo = eventHeader->runNumber();
    evtNo = eventHeader->eventNumber();

    if (m_debug) {
        std::cout << "**************************************" << std::endl;
        std::cout << "run = "  <<  runNo  <<  ", event = " << evtNo << std::endl;
        std::cout << "**************************************" << std::endl;
    }

    flag1 = eventHeader->flag1();
    int decay_1 = ((eventHeader->flag1()/1000000))%1000;
    int decay_2 = (eventHeader->flag1()/1000)%1000;
    int decay_3 = eventHeader->flag1()%1000;
    if (m_debug) std::cout << " flg " << decay_1 << "     " << decay_2 << "     " << decay_3 << std::endl;

    // save McTruth info
    if (runNo < 0 && m_isMonteCarlo) saveAllMcTruthInfo();
    if (runNo < 0 && m_isMonteCarlo) saveDststMcTruthInfo();
    if (runNo < 0 && m_isMonteCarlo) savePsi_3770McTruthInfo();
    if (runNo < 0 && m_isMonteCarlo) saveDpDmMcTruthInfo();

    // use DTagTool
    stat_DTagTool = useDTagTool();

    return StatusCode::SUCCESS;
}

StatusCode DDecayAlg::finalize() {
    MsgStream log(msgSvc(), name());
    log << MSG::INFO << ">>>>>>> in finalize()" << endmsg;

    return StatusCode::SUCCESS;
}

void DDecayAlg::clearVariables() {
    // common info
    runNo = 0;
    evtNo = 0;
    flag1 = 0;
    m_runNo = 0;
    m_evtNo = 0;
    m_flag1 = 0;
    m_runNo_otherTrk = 0;
    m_evtNo_otherTrk = 0;
    m_flag1_otherTrk = 0;
    m_runNo_otherShw = 0;
    m_evtNo_otherShw = 0;
    m_flag1_otherShw = 0;
    m_runNo_allTruth = 0;
    m_evtNo_allTruth = 0;
    m_flag1_allTruth = 0;
    m_runNo_DststTruth = 0;
    m_evtNo_DststTruth = 0;
    m_flag1_DststTruth = 0;
    m_runNo_PsiTruth = 0;
    m_evtNo_PsiTruth = 0;
    m_flag1_PsiTruth = 0;
    m_runNo_DpDmTruth = 0;
    m_evtNo_DpDmTruth = 0;
    m_flag1_DpDmTruth = 0;
    m_runNo_signal = 0;
    m_evtNo_signal = 0;
    m_flag1_signal = 0;
    m_runNo_sidebandlow = 0;
    m_evtNo_sidebandlow = 0;
    m_flag1_sidebandlow = 0;
    m_runNo_sidebandup = 0;
    m_evtNo_sidebandup = 0;
    m_flag1_sidebandup = 0;
    m_matched_D = 0;
    m_matched_D_signal = 0;
    m_matched_pi = 0;

    // all McTruth info
    m_idxmc = 0;

    // Dstst McTruth info
    for (int i = 0; i < 4; i++) {
        p4_pip[i] = -999;
        p4_pim[i] = -999;
        p4_D1[i] = -999;
        p4_D2[i] = -999;
        p4_Dstst[i] = -999;
        m_p4_pip[i] = -999;
        m_p4_pim[i] = -999;
        m_p4_D1[i] = -999;
        m_p4_D2[i] = -999;
        m_p4_Dstst[i] = -999;
    }

    // psi(3770) McTruth info
    for (int i = 0; i < 4; i++) {
        p4_pip_psi[i] = -999;
        p4_pim_psi[i] = -999;
        p4_Dp_psi[i] = -999;
        p4_Dm_psi[i] = -999;
        p4_psi[i] = -999;
        m_p4_pip_psi[i] = -999;
        m_p4_pim_psi[i] = -999;
        m_p4_Dp_psi[i] = -999;
        m_p4_Dm_psi[i] = -999;
        m_p4_psi[i] = -999;
    }

    // DpDm McTruth info
    DpId = -999;
    DmId = -999;

    // single D tag
    m_n_trkD = 0;
    m_n_trkD_signal = 0;
    m_n_trkD_sidebandlow = 0;
    m_n_trkD_sidebandup = 0;
    n_trkD = 0;
    m_n_shwD = 0;
    m_n_shwD_signal = 0;
    m_n_shwD_sidebandlow = 0;
    m_n_shwD_sidebandup = 0;
    n_shwD = 0;
    MODE = -999;
    mode = -999;
    m_mode = -999;
    m_mode_signal = -999;
    m_mode_sidebandlow = -999;
    m_mode_sidebandup = -999;
    charm = -999;
    m_charm = -999;
    m_charm_signal = -999;
    m_charm_sidebandlow = -999;
    m_charm_sidebandup = -999;
    chi2_vf = -999;
    m_chi2_vf = -999;
    m_chi2_vf_signal = -999;
    m_chi2_vf_sidebandlow = -999;
    m_chi2_vf_sidebandup = -999;
    chi2_kf = -999;
    m_chi2_kf = -999;
    mDcand = 0;
    charge_otherMdctrk = 0;
    n_count = 0;
    m_n_count = 0;

    // judgement variables
    stat_DTagTool = false;
    stat_tagSD = false;
    stat_saveCandD = false;
    stat_saveOthertrks = false;
    stat_saveOthershws = false;
    stat_fitpi0 = false;
    stat_fitpi0_signal = false;
    stat_fitpi0_sidebandlow = false;
    stat_fitpi0_sidebandup = false;
}

void DDecayAlg::saveAllMcTruthInfo() {
    SmartDataPtr<Event::McParticleCol> mcParticleCol(eventSvc(), "/Event/MC/McParticleCol");
    if (!mcParticleCol) {
        std::cout << "Could not retreive McParticleCol" << std::endl;
    }
    else {
        Event::McParticleCol::iterator iter_mc = mcParticleCol->begin(); // loop all the particles in the decay chain(MCTruth)
        int pid = (*iter_mc)->particleProperty();
        unsigned int idx;
        unsigned int midx;
        idxmc = 0;
        if (pid == 90022 || pid == 80022) {
             for (iter_mc++; iter_mc != mcParticleCol->end(); iter_mc++) {
                 if (!(*iter_mc)->decayFromGenerator()) continue;
                 pid = (*iter_mc)->particleProperty();
                 idx = (*iter_mc)->trackIndex();
                 midx = ((*iter_mc)->mother()).trackIndex();
                 pdgid[idxmc] = pid;
                 if (idx == midx || midx == 0) motheridx[idxmc] = idx - 1;
                 else motheridx[idxmc] = midx - 1;
                 idxmc++;
             }
        }
        else {
            for (; iter_mc != mcParticleCol->end(); iter_mc++) {
                if (!(*iter_mc)->decayFromGenerator()) continue;
                pdgid[idxmc] = (*iter_mc)->particleProperty();
                motheridx[idxmc]= ((*iter_mc)->mother()).trackIndex();
                idxmc++;
            }
        }
        if (m_debug) std::cout << " PDG.SIZE():  " << idxmc << std::endl;
    }
}

void DDecayAlg::saveDststMcTruthInfo() {
    SmartDataPtr<Event::McParticleCol> mcParticleCol(eventSvc(), "/Event/MC/McParticleCol");
    Event::McParticleCol::iterator iter_Dststmc = mcParticleCol->begin();
    int num_D=0, num_pion=0, num_Dstst=0, num_others=0;
    for (; iter_Dststmc != mcParticleCol->end(); iter_Dststmc++) {
        if (fabs((*iter_Dststmc)->particleProperty()) == 411 && fabs((*iter_Dststmc)->mother().particleProperty()) != 10413) {
            for (int j = 0; j < 4; j++) p4_D1[j] = (*iter_Dststmc)->initialFourMomentum()[j];
            num_D++;
        }
        if(fabs((*iter_Dststmc)->particleProperty()) == 10413) {
            for (int j = 0; j < 4; j++) p4_Dstst[j] = (*iter_Dststmc)->initialFourMomentum()[j];
            num_Dstst++;
            const SmartRefVector<Event::McParticle>& gcd = (*iter_Dststmc)->daughterList();
            if (gcd.size() < 0) continue;
            for (unsigned int j = 0; j < gcd.size(); j++) {
                if (fabs(gcd[j]->particleProperty()) == 411) {
                    for(int k = 0; k < 4; k++) p4_D2[k] = gcd[j]->initialFourMomentum()[k];
                    num_D++;
                }
                if (fabs(gcd[j]->particleProperty()) == 211) {
                    if (gcd[j]->particleProperty()>0) {
                        for (int k = 0; k < 4; k++) {
                            p4_pip[k] = gcd[j]->initialFourMomentum()[k];
                            num_pion++;
                        }
                    }
                    if (gcd[j]->particleProperty()<0) {
                        for (int k = 0; k < 4; k++) {
                            p4_pim[k] = gcd[j]->initialFourMomentum()[k];
                            num_pion++;
                        }
                    }
                }
            }
        }
        if (fabs((*iter_Dststmc)->particleProperty()) != 411 && fabs((*iter_Dststmc)->particleProperty()) != 10413) {
            num_others++;
        }
    }
    if (m_debug) std::cout << " DststD truth information 1:  " << num_pion << "  " << num_D << "  " << num_Dstst << "  " << num_others << std::endl;
    if (m_debug) std::cout << " DststD truth information 2:  " << p4_pip[3] << "  " << p4_D1[3] << "  " << p4_D2[3] << "  " <<p4_Dstst[3] << std::endl;
}

void DDecayAlg::savePsi_3770McTruthInfo() {
    SmartDataPtr<Event::McParticleCol> mcParticleCol(eventSvc(), "/Event/MC/McParticleCol");
    Event::McParticleCol::iterator iter_Psimc = mcParticleCol->begin();
    int num_Dp=0,num_Dm=0, num_pip=0, num_pim=0, num_psip=0, num_others;
    for (; iter_Psimc != mcParticleCol->end(); iter_Psimc++) {
        if (m_debug) std::cout << "  Psippp truth:  " << (*iter_Psimc)->particleProperty() << "   mother:  " << (*iter_Psimc)->mother().particleProperty() << std::endl;
        if ((*iter_Psimc)->particleProperty() == 211 && fabs((*iter_Psimc)->mother().particleProperty()) != 411) {
            for (int j = 0; j < 4; j++) p4_pip_psi[j] = (*iter_Psimc)->initialFourMomentum()[j];
            num_pip++;
        }
        if ((*iter_Psimc)->particleProperty() == -211 && fabs((*iter_Psimc)->mother().particleProperty()) != 411) {
            for (int j = 0; j < 4; j++) p4_pim_psi[j] = (*iter_Psimc)->initialFourMomentum()[j];
            num_pim++;
        }
        if ((*iter_Psimc)->particleProperty() == 30443) {
            for (int j = 0; j < 4; j++) p4_psi[j] = (*iter_Psimc)->initialFourMomentum()[j];
            num_psip++;
            const SmartRefVector<Event::McParticle>& gcd = (*iter_Psimc)->daughterList();
            if (m_debug) std::cout << " GCD.SIZE():   " << gcd.size() << std::endl;
            if (gcd.size() < 0) continue;
            for(unsigned int j = 0; j < gcd.size(); j++) {
                if (gcd[j]->particleProperty() == 411) {
                    for (int k = 0; k < 4; k++) p4_Dp_psi[k] = gcd[j]->initialFourMomentum()[k];
                    num_Dp++;
                }
                if (gcd[j]->particleProperty() == -411) {
                    for (int k = 0; k < 4; k++) p4_Dm_psi[k] = gcd[j]->initialFourMomentum()[k];
                    num_Dm++;
                }
            }
        }
        if (fabs((*iter_Psimc)->particleProperty()) != 211 || (*iter_Psimc)->particleProperty() == 30443 || fabs((*iter_Psimc)->particleProperty()) != 411) num_others++;
    }
    if (m_debug) std::cout << " recording Psippp truth information 1:  " << num_pip << "  " << num_pim << "  " << num_psip << "  " << num_Dp << "  " << num_Dm << std::endl;
    if (m_debug) std::cout << " recording Psippp truth information 2:  " << p4_pip_psi[3] << "  " << p4_pim_psi[3] << "  " << p4_psi[3] << "  " << p4_Dp_psi[3] << "  " << p4_Dm_psi[3] << std::endl;
}

void DDecayAlg::saveDpDmMcTruthInfo() {
    SmartDataPtr<Event::McParticleCol> mcParticleCol(eventSvc(), "/Event/MC/McParticleCol");
    Event::McParticleCol::iterator iter_DpDmmc = mcParticleCol->begin();
    for (; iter_DpDmmc != mcParticleCol->end(); iter_DpDmmc++) {
        if ((*iter_DpDmmc)->particleProperty() == 421) { // D0
            const SmartRefVector<Event::McParticle>& gc = (*iter_DpDmmc)->daughterList();
            int num_k=0, num_pip=0, num_pi0=0, num_others=0;
            if (gc.size() > 0) {
                if (m_debug) std::cout << " D0  daughter particles" << gc[0]->particleProperty() << "   " << gc[1]->particleProperty() << std::endl;
                for (unsigned int j = 0; j < gc.size(); j++) {
                    if (gc[j]->particleProperty() == -22) continue;
                    else if (fabs(gc[j]->particleProperty()) == 321) num_k++;
                    else if (fabs(gc[j]->particleProperty()) == 211) num_pip++;
                    else if (gc[j]->particleProperty() == 111) num_pi0++;
                    else num_others++;
                }
            }
            if (num_k == 1 && num_pip == 1 && num_pi0 == 1 && num_others==0) { // D->K-pi+pi0
                DpId = 1;
            }
            else if (num_k == 1 && num_pip == 1 && num_pi0 == 0 && num_others == 0) { // D->Kpi
                DpId = 0;
            }
            else DpId = 3;
        }
        if ((*iter_DpDmmc)->particleProperty() == 411) { //D+
            const SmartRefVector<Event::McParticle>& gc = (*iter_DpDmmc)->daughterList();
            int num_k = 0, num_pip = 0, num_others = 0;
            if (gc.size() > 0) {
                if (m_debug) std::cout << " Dp  daughter particles" << gc[0]->particleProperty() << "   " << gc[1]->particleProperty() << std::endl;
                for(unsigned int j = 0; j < gc.size(); j++) {
                    if (gc[j]->particleProperty() == -22) continue; // D+->Kpipi
                    else if (gc[j]->particleProperty() == -321) num_k++;
                    else if (gc[j]->particleProperty() == 211) num_pip++;
                    else num_others++;
                }
            }
            if (num_k == 1 && num_pip == 2 && num_others == 0) {
                DpId = 200;
            }
        }
        if (m_debug) std::cout << runNo << " : " << evtNo << " : decay mode " << DpId << "   " << DmId << std::endl;
    }
}

bool DDecayAlg::useDTagTool() {
    DTagTool dtagTool; // before running this program, DTagTool have running, and the suited D candidates have been tagged
    if (m_pid) dtagTool.setPID(true); // all the combinations of tracks have been tested, the suited D candidantes among them have been tagged "true", others have been tagged "false"
    if (dtagTool.isDTagListEmpty()) {
        if (m_debug) std::cout << "no D candidates found" << std::endl;
        return false;
    }
    else {
        // to retrieve RecEvent
        SmartDataPtr<EvtRecEvent> evtRecEvent(eventSvc(), "/Event/EvtRec/EvtRecEvent");
        if (!evtRecEvent) {
            std::cout << MSG::FATAL << "Could not find EvtRecEvent" << std::endl;
            return false;
        }
        // to retrieve RecTrackCol
        SmartDataPtr<EvtRecTrackCol> evtRecTrackCol(eventSvc(), "/Event/EvtRec/EvtRecTrackCol");
        if (!evtRecTrackCol) {
            std::cout << MSG::FATAL << "Could not find EvtRecTrackCol" << std::endl;
            return false;
        }
    }
    
    stat_tagSD = tagSingleD();
    if (stat_tagSD) return true;
    else return false;
}

bool DDecayAlg::tagSingleD() {
    VWTrkPara vwtrkpara_charge, vwtrkpara_photon;
    for (int i = 0; i < m_DModes.size(); i++) {
        mode = m_DModes[i];
        if (mode != 200 && mode != 205 && mode != 208 && mode != 213 && mode != 216) continue; 
        // mode = 200 includes: D+->K-pi+pi+ or D-->K+pi-pi-
        // mode = 201 includes: D+->K-pi+pi+pi0
        // mode = 202 includes: D+->Kspi+
        // mode = 203 includes: D+->Kspi+pi0
        // mode = 204 includes: D+->Kspi+pi-pi+
        // mode = 205 includes: D+->K-K+pi+
        // mode = 208 includes: D+->KsK+
        // mode = 213 includes: D+->KsKsK+
        // mode = 216 includes: D+->KsK+pi+pi-

        // define D candidate mass
        if ((int)mode < 200) mDcand = M_D0;
        else if ((int)mode < 400) mDcand = M_Dplus;
        else {
            std::cout << "single tag mode is not found! " << std::endl;
            return false;
        }
        stat_saveCandD = saveCandD(vwtrkpara_charge, vwtrkpara_photon);
    }
    if (stat_saveCandD) return true;
    else return false;
}

bool DDecayAlg::saveCandD(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon) {
    // Accessing DTagList
    SmartDataPtr<EvtRecDTagCol> evtRecDTagCol(eventSvc(), EventModel::EvtRec::EvtRecDTagCol);
    if (!evtRecDTagCol) {
        std::cout << MSG::FATAL <<"Could not find EvtRecDTagCol" << std::endl;
        return false;
    }

    // keep all the candidate of D
    dtag_iter_begin = evtRecDTagCol->begin();
    dtag_iter_end = evtRecDTagCol->end();
    dtag_iter = dtag_iter_begin;

    // loop over the dtag list
    for (; dtag_iter != dtag_iter_end; dtag_iter++) {
        // whether to use pid
        if (m_pid) {
            if ((*dtag_iter)->type() !=1 || (*dtag_iter)->decayMode() != mode) {
                continue; // type = 1: PID has been performed, type = 0, PID hasn't been performed
            }
        }
        else {
            if ((*dtag_iter)->decayMode() != mode) {
                continue;
            }
        }

        if (m_debug) std::cout << " --> dtag found : " << mode << std::endl;
        if (m_debug) std::cout<< " D charm number: " << (*dtag_iter)->charm() << std::endl; // (*dtag_iter)->charm() = 1: c, -1: cbar

        // very broad mass window requirement
        double DELTAM = 0;
        if (fabs(runNo) >= 30616 && fabs(runNo) <= 31279) {
            DELTAM = 0.0179;
        }
        if ((fabs(runNo) >= 31327 && fabs(runNo) <= 31390) || (fabs(runNo) >= 36773 && fabs(runNo) <= 38140)) {
            DELTAM = 0.02063;
        }
        if (fabs(runNo) >= 35227 && fabs(runNo) <= 36213) {
            DELTAM = 0.02063;
        }
        if (fabs((*dtag_iter)->mass() - mDcand) > DELTAM) {
            continue;
        }

        SmartRefVector<EvtRecTrack> Dtrks = (*dtag_iter)->tracks();
        SmartRefVector<EvtRecTrack> Dshws = (*dtag_iter)->showers();
        n_trkD = Dtrks.size();
        n_shwD = Dshws.size();
        MODE = (*dtag_iter)->decayMode();
        charm = (*dtag_iter)->charm(); // (*dtag_iter)->charm() = 1: c, -1: cbar

        if (m_debug) std::cout<<" D: ntrk  nshw " << n_trkD << "  " << n_shwD << std::endl;

        vwtrkpara_charge.clear();
        HepLorentzVector pK;
        HepLorentzVector ppi;
        m_matched_D = 0;
        m_matched_D_signal = 0;
        int tag_K_Match = 1;
        DTagTool dtagTool;
        for (int j = 0; j < n_trkD; j++) {
            RecMdcKalTrack* KalTrk = Dtrks[j]->mdcKalTrack();
            // to fill Kaon candidates
            // if (j == 0) { // default arrangement: (K,pi), number of K depend on the mode you choose
            if (dtagTool.isKaon(Dtrks[j])) {
                KalTrk->setPidType(RecMdcKalTrack::kaon);
                if (m_debug) std::cout << " filling kaon track " << std::endl;
                vwtrkpara_charge.push_back(WTrackParameter(mass[3], KalTrk->getZHelixK(), KalTrk->getZErrorK()));
                for (int k = 0; k < 4; k++) m_rawp4_Dtrk[j][k] = KalTrk->p4(mass[3])[k]; // MDC gives three momentum, combined with mass, we can get energy which means four momentum
                m_rawp4_Dtrk[j][4] = KalTrk->charge();
                m_rawp4_Dtrk[j][5] = 3;
                pK.setPx(KalTrk->p4(mass[3])[0]);
                pK.setPy(KalTrk->p4(mass[3])[1]);
                pK.setPz(KalTrk->p4(mass[3])[2]);
                pK.setE(KalTrk->p4(mass[3])[3]);
                m_matched_D = MatchMC(pK, "D_tag");
                m_matched_D_signal = MatchMC(pK, "D_tag");
                tag_K_Match = 0;
            }
            // to fill Pion candidates
            else {
                KalTrk->setPidType(RecMdcKalTrack::pion);
                if (m_debug) std::cout << " filling pion track " << std::endl;
                vwtrkpara_charge.push_back(WTrackParameter(mass[2], KalTrk->getZHelix(), KalTrk->getZError()));
                for (int k = 0; k < 4; k++) m_rawp4_Dtrk[j][k] = KalTrk->p4(mass[2])[k];
                m_rawp4_Dtrk[j][4] = KalTrk->charge();
                m_rawp4_Dtrk[j][5] = 2;
                ppi.setPx(KalTrk->p4(mass[2])[0]);
                ppi.setPy(KalTrk->p4(mass[2])[1]);
                ppi.setPz(KalTrk->p4(mass[2])[2]);
                ppi.setE(KalTrk->p4(mass[2])[3]);
                if (m_matched_D || tag_K_Match == 1) m_matched_D = MatchMC(ppi, "D_tag");
                if (m_matched_D_signal || tag_K_Match == 1) m_matched_D_signal = MatchMC(ppi, "D_tag");
            }
        }

        // to check the vector in each dtag item
        if (m_debug) {
            double index_vector = 0;
            std::cout << "total cahrged: " << vwtrkpara_charge.size() << std::endl;
            while(index_vector < vwtrkpara_charge.size()) {
                std::cout << " Add charged tracks: " << index_vector 
                << " with charge: " << vwtrkpara_charge[index_vector].charge()
                << " with momentum: " << vwtrkpara_charge[index_vector].p() 
                << " mass: " << vwtrkpara_charge[index_vector].mass() << std::endl;
                index_vector++;
            }
        }

        if (vwtrkpara_charge.size() != n_trkD) {
            continue;
        }

        // do vertex fit
        chi2_vf = fitVertex(vwtrkpara_charge, birth);
        if (chi2_vf > 100) {
            continue;
        }

        if (m_debug) std::cout << " vertex fitting chisq: " << chi2_vf << std::endl;
        if (m_debug) std::cout << " vertex fitting vertex: " << birth.vx() << std::endl;

        HepLorentzVector pgam;
        vwtrkpara_photon.clear(); // for mode ee->DDpipi, there is no pi0, so the vector will be empty
        for(int j = 0; j < Dshws.size(); j++) {
            RecEmcShower *gTrk = Dshws[j]->emcShower();
            Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
            Hep3Vector Gm_Mom = Gm_Vec - birth.vx(); // vx: Vertex, we regard that the track of the gamma before it enters EMC is a line, so to get the info of this line, we can just subtract the vertex info from the EMC hit point
            Gm_Mom.setMag(gTrk->energy());
            HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
            vwtrkpara_photon.push_back(WTrackParameter(gTrk->position(), Gm_p4, gTrk->dphi(), gTrk->dtheta(), gTrk->dE())); // dE, error of the gamma energy
            for (int k = 0; k < 4; k++) m_rawp4_Dshw[j][k] = Gm_p4[k];
            pgam.setPx(Gm_p4[0]);
            pgam.setPy(Gm_p4[1]);
            pgam.setPz(Gm_p4[2]);
            pgam.setE(Gm_p4[3]);
            if (m_matched_D_signal) m_matched_D_signal = MatchMC(pgam, "D_tag");
        }
        
        if (m_debug) {
            double index_vector=0;
            std::cout << "total neutral: " << vwtrkpara_photon.size() << std::endl;
            while(index_vector < vwtrkpara_photon.size()) {
                std::cout << " Add neutral tracks: " << index_vector 
                << " with momentum: " << vwtrkpara_photon[index_vector].p() << std::endl;
                index_vector++;
            }
        }

        // KM fit on D candidate
        chi2_kf = fitKM(vwtrkpara_charge, vwtrkpara_photon, birth);

        // to store the other showers information
        stat_saveOthershws = saveOthershws();

        // to store the other track information
        stat_saveOthertrks = saveOthertrks(vwtrkpara_charge, vwtrkpara_photon, birth);

        // record variables
        if (fabs(chi2_vf) < 100 && fabs(chi2_kf) < 999 && stat_saveOthertrks && stat_saveOthershws) {
            n_count++;
            recordVariables();
        }
    }
    if (fabs(chi2_vf) < 100 && fabs(chi2_kf) < 999 && stat_saveOthertrks && stat_saveOthershws) return true;
    else return false;
}

double DDecayAlg::fitVertex(VWTrkPara &vwtrkpara, VertexParameter &birth) {
    VertexParameter vxpar;
    Hep3Vector xorigin(0,0,0);
    HepSymMatrix Exorigin(3,0); // error matrix
    double bx = 1E+6, by = 1E+6, bz = 1E+6;
    Exorigin[0][0] = bx*bx; Exorigin[1][1] = by*by; Exorigin[2][2] = bz*bz;
    vxpar.setVx(xorigin); vxpar.setEvx(Exorigin); // vx: vertex
    vtxfit->init();
    for (int i = 0; i < vwtrkpara.size(); i++) vtxfit->AddTrack(i, vwtrkpara[i]);
    Vint trkId(vwtrkpara.size(), 0); // ????????????????
    for (int i = 0; i < vwtrkpara.size(); i++) trkId[i] = i;
    vtxfit->AddVertex(0, vxpar, trkId);
    if (!vtxfit->Fit(0)) return 9999; // 0: which vertex to fit
    double vf_chi2 = vtxfit->chisq(0);
    vtxfit->Swim(0); // adjust momentum according to errorr matrix
    for (int i = 0; i < vwtrkpara.size(); i++) vwtrkpara[i] = vtxfit->wtrk(i);
    if (vf_chi2 == 1) std::cout << "==========  VF chi2: " << vf_chi2 << std::endl;
    birth = vtxfit->vpar(0);
    return vf_chi2;
}

double DDecayAlg::fitKM(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth) {
    kmfit->init();
    // kmfit->setEspread(0.0011);
    kmfit->setBeamPosition(birth.vx());
    kmfit->setVBeamPosition(birth.Evx()); // error matrix of vertex

    if (m_debug) std::cout << " to start add tracks to KF fit " << std::endl;

    int count = 0;
    Vint D1list;
    Vint Pi0list;
    D1list.clear();
    Pi0list.clear();
    while (count < vwtrkpara_charge.size()) {
        kmfit->AddTrack(count, vwtrkpara_charge[count]);
        D1list.push_back(count);
        count++;
    }
    while (count < vwtrkpara_charge.size() + vwtrkpara_photon.size()) {
        kmfit->AddTrack(count, vwtrkpara_photon[count - vwtrkpara_charge.size()]);
        Pi0list.push_back(count);
        D1list.push_back(count);
        count++;
    }
    int n_res = 0;
    for (int i = 0; i < (Pi0list.size()/2); i++) kmfit->AddResonance(n_res++, M_Pi0, n_trkD + i*2, n_trkD + i*2 + 1); // the last two variales: two gamma tracks
    kmfit->AddResonance(n_res, mDcand, D1list);

    if (m_debug) std::cout << " finished KF add Tracks ... " << std::endl;

    double kf_chi2 = 999;
    if (!kmfit->Fit(0)) return 999;
    if (!kmfit->Fit()) return 999;
    else {
        // kf_chi2 = kmfit->chisq()/(1 + Pi0list.size()/2); // chi2/ndf, 1: constration of mD, Pi0list.size()/2: constration of Pi0
        kf_chi2 = kmfit->chisq();
        if (m_debug) std::cout << "  " << mode << "  fit chisq:   " << kf_chi2 << std::endl;
        for (int i = 0; i < n_trkD; i++) {
            for (int j = 0; j < 4; j++) m_p4_Dtrk[i][j] = kmfit->pfit(i)[j];
        }
        if (m_debug) std::cout << " fill D1trkP4 successfully for mode !!! " << mode << std::endl;
        for (int i = 0; i < n_shwD; i++) {
            for (int j = 0; j < 4; j++) m_p4_Dshw[i][j] = kmfit->pfit(i + n_trkD)[j];
        }
        if (m_debug) std::cout << " recorded the four momentum of showers and tracks in tagged D " << std::endl;
    }
    return kf_chi2;
}

double DDecayAlg::fitKM_signal(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth) {
    kmfit->init();
    // kmfit->setEspread(0.0011);
    kmfit->setBeamPosition(birth.vx());
    kmfit->setVBeamPosition(birth.Evx()); // error matrix of vertex

    if (m_debug) std::cout << " to start add tracks to KF fit " << std::endl;

    int count = 0;
    Vint D1list;
    Vint Pi0list;
    D1list.clear();
    Pi0list.clear();
    while (count < vwtrkpara_charge.size()) {
        kmfit->AddTrack(count, vwtrkpara_charge[count]);
        D1list.push_back(count);
        count++;
    }
    while (count < vwtrkpara_charge.size() + vwtrkpara_photon.size()) {
        kmfit->AddTrack(count, vwtrkpara_photon[count - vwtrkpara_charge.size()]);
        Pi0list.push_back(count);
        D1list.push_back(count);
        count++;
    }
    int n_res = 0;
    for (int i = 0; i < (Pi0list.size()/2); i++) kmfit->AddResonance(n_res++, M_Pi0, n_trkD + i*2, n_trkD + i*2 + 1); // the last two variales: two gamma tracks
    kmfit->AddResonance(n_res++, mDcand, D1list);
    double cms = 0;
    if (fabs(runNo) >= 30616 && fabs(runNo) <= 31279) {
        cms = 4.358;
    }
    if ((fabs(runNo) >= 31327 && fabs(runNo) <= 31390) || (fabs(runNo) >= 36773 && fabs(runNo) <= 38140)) {
        cms = 4.416;
    }
    if (fabs(runNo) >= 35227 && fabs(runNo) <= 36213) {
        cms = 4.600;
    }
    kmfit->AddTrack(count++, vwtrkpara_piplus[n_piplus]);
    kmfit->AddTrack(count++, vwtrkpara_piminus[n_piminus]);
    kmfit->AddMissTrack(count++, M_Dplus);
    HepLorentzVector ecms(0.011*cms, 0, 0, cms);
    kmfit->AddFourMomentum(n_res, ecms);

    if (m_debug) std::cout << " finished KF add Tracks ... " << std::endl;

    double kf_chi2 = 999;
    if (!kmfit->Fit(0)) return 999;
    if (!kmfit->Fit()) return 999;
    else {
        // kf_chi2 = kmfit->chisq()/(1 + Pi0list.size()/2); // chi2/ndf, 1: constration of mD, Pi0list.size()/2: constration of Pi0
        kf_chi2 = kmfit->chisq();
        if (m_debug) std::cout << "  " << mode << "  fit chisq:   " << kf_chi2 << std::endl;
        for (int i = 0; i < n_trkD; i++) {
            for (int j = 0; j < 4; j++) m_p4_Dtrk_signal[i][j] = kmfit->pfit(i)[j];
        }
        if (m_debug) std::cout << " fill D1trkP4 successfully for mode !!! " << mode << std::endl;
        for (int i = 0; i < n_shwD; i++) {
            for (int j = 0; j < 4; j++) m_p4_Dshw_signal[i][j] = kmfit->pfit(i + n_trkD)[j];
        }
        for (int i = 0; i < 4; i++) m_p4_piplus_signal[i] = kmfit->pfit(n_trkD + n_shwD)[i];
        for (int i = 0; i < 4; i++) m_p4_piminus_signal[i] = kmfit->pfit(n_trkD + n_shwD + 1)[i];
        if (m_debug) std::cout << " recorded the four momentum of showers and tracks in tagged D " << std::endl;
    }
    return kf_chi2;
}

double DDecayAlg::fitKM_sidebandlow(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double sidebandlow_mean) {
    kmfit->init();
    // kmfit->setEspread(0.0011);
    kmfit->setBeamPosition(birth.vx());
    kmfit->setVBeamPosition(birth.Evx()); // error matrix of vertex

    if (m_debug) std::cout << " to start add tracks to KF fit " << std::endl;

    int count = 0;
    Vint D1list;
    Vint Pi0list;
    D1list.clear();
    Pi0list.clear();
    while (count < vwtrkpara_charge.size()) {
        kmfit->AddTrack(count, vwtrkpara_charge[count]);
        D1list.push_back(count);
        count++;
    }
    while (count < vwtrkpara_charge.size() + vwtrkpara_photon.size()) {
        kmfit->AddTrack(count, vwtrkpara_photon[count - vwtrkpara_charge.size()]);
        Pi0list.push_back(count);
        D1list.push_back(count);
        count++;
    }
    int n_res = 0;
    for (int i = 0; i < (Pi0list.size()/2); i++) kmfit->AddResonance(n_res++, M_Pi0, n_trkD + i*2, n_trkD + i*2 + 1); // the last two variales: two gamma tracks
    kmfit->AddResonance(n_res++, mDcand, D1list);
    double cms = 0;
    if (fabs(runNo) >= 30616 && fabs(runNo) <= 31279) {
        cms = 4.358;
    }
    if ((fabs(runNo) >= 31327 && fabs(runNo) <= 31390) || (fabs(runNo) >= 36773 && fabs(runNo) <= 38140)) {
        cms = 4.416;
    }
    if (fabs(runNo) >= 35227 && fabs(runNo) <= 36213) {
        cms = 4.600;
    }
    kmfit->AddTrack(count++, vwtrkpara_piplus[n_piplus]);
    kmfit->AddTrack(count++, vwtrkpara_piminus[n_piminus]);
    kmfit->AddMissTrack(count++, sidebandlow_mean);
    HepLorentzVector ecms(0.011*cms, 0 , 0, cms);
    kmfit->AddFourMomentum(n_res, ecms);

    if (m_debug) std::cout << " finished KF add Tracks ... " << std::endl;

    double kf_chi2 = 999;
    if (!kmfit->Fit(0)) return 999;
    if (!kmfit->Fit()) return 999;
    else {
        // kf_chi2 = kmfit->chisq()/(1 + Pi0list.size()/2); // chi2/ndf, 1: constration of mD, Pi0list.size()/2: constration of Pi0
        kf_chi2 = kmfit->chisq();
        if (m_debug) std::cout << "  " << mode << "  fit chisq:   " << kf_chi2 << std::endl;
        for (int i = 0; i < n_trkD; i++) {
            for (int j = 0; j < 4; j++) m_p4_Dtrk_sidebandlow[i][j] = kmfit->pfit(i)[j];
        }
        if (m_debug) std::cout << " fill D1trkP4 successfully for mode !!! " << mode << std::endl;
        for (int i = 0; i < n_shwD; i++) {
            for (int j = 0; j < 4; j++) m_p4_Dshw_sidebandlow[i][j] = kmfit->pfit(i + n_trkD)[j];
        }
        for (int i = 0; i < 4; i++) m_p4_piplus_sidebandlow[i] = kmfit->pfit(n_trkD + n_shwD)[i];
        for (int i = 0; i < 4; i++) m_p4_piminus_sidebandlow[i] = kmfit->pfit(n_trkD + n_shwD + 1)[i];
        if (m_debug) std::cout << " recorded the four momentum of showers and tracks in tagged D " << std::endl;
    }
    return kf_chi2;
}

double DDecayAlg::fitKM_sidebandup(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VWTrkPara &vwtrkpara_piplus, VWTrkPara &vwtrkpara_piminus, int n_piplus, int n_piminus, VertexParameter &birth, double sidebandup_mean) {
    kmfit->init();
    // kmfit->setEspread(0.0011);
    kmfit->setBeamPosition(birth.vx());
    kmfit->setVBeamPosition(birth.Evx()); // error matrix of vertex

    if (m_debug) std::cout << " to start add tracks to KF fit " << std::endl;

    int count = 0;
    Vint D1list;
    Vint Pi0list;
    D1list.clear();
    Pi0list.clear();
    while (count < vwtrkpara_charge.size()) {
        kmfit->AddTrack(count, vwtrkpara_charge[count]);
        D1list.push_back(count);
        count++;
    }
    while (count < vwtrkpara_charge.size() + vwtrkpara_photon.size()) {
        kmfit->AddTrack(count, vwtrkpara_photon[count - vwtrkpara_charge.size()]);
        Pi0list.push_back(count);
        D1list.push_back(count);
        count++;
    }
    int n_res = 0;
    for (int i = 0; i < (Pi0list.size()/2); i++) kmfit->AddResonance(n_res++, M_Pi0, n_trkD + i*2, n_trkD + i*2 + 1); // the last two variales: two gamma tracks
    kmfit->AddResonance(n_res++, mDcand, D1list);
    double cms = 0;
    if (fabs(runNo) >= 30616 && fabs(runNo) <= 31279) {
        cms = 4.358;
    }
    if ((fabs(runNo) >= 31327 && fabs(runNo) <= 31390) || (fabs(runNo) >= 36773 && fabs(runNo) <= 38140)) {
        cms = 4.416;
    }
    if (fabs(runNo) >= 35227 && fabs(runNo) <= 36213) {
        cms = 4.600;
    }
    kmfit->AddTrack(count++, vwtrkpara_piplus[n_piplus]);
    kmfit->AddTrack(count++, vwtrkpara_piminus[n_piminus]);
    kmfit->AddMissTrack(count++, sidebandup_mean);
    HepLorentzVector ecms(0.011*cms, 0 , 0, cms);
    kmfit->AddFourMomentum(n_res, ecms);

    if (m_debug) std::cout << " finished KF add Tracks ... " << std::endl;

    double kf_chi2 = 999;
    if (!kmfit->Fit(0)) return 999;
    if (!kmfit->Fit()) return 999;
    else {
        // kf_chi2 = kmfit->chisq()/(1 + Pi0list.size()/2); // chi2/ndf, 1: constration of mD, Pi0list.size()/2: constration of Pi0
        kf_chi2 = kmfit->chisq();
        if (m_debug) std::cout << "  " << mode << "  fit chisq:   " << kf_chi2 << std::endl;
        for (int i = 0; i < n_trkD; i++) {
            for (int j = 0; j < 4; j++) m_p4_Dtrk_sidebandup[i][j] = kmfit->pfit(i)[j];
        }
        if (m_debug) std::cout << " fill D1trkP4 successfully for mode !!! " << mode << std::endl;
        for (int i = 0; i < n_shwD; i++) {
            for (int j = 0; j < 4; j++) m_p4_Dshw_sidebandup[i][j] = kmfit->pfit(i + n_trkD)[j];
        }
        for (int i = 0; i < 4; i++) m_p4_piplus_sidebandup[i] = kmfit->pfit(n_trkD + n_shwD)[i];
        for (int i = 0; i < 4; i++) m_p4_piminus_sidebandup[i] = kmfit->pfit(n_trkD + n_shwD + 1)[i];
        if (m_debug) std::cout << " recorded the four momentum of showers and tracks in tagged D " << std::endl;
    }
    return kf_chi2;
}

bool DDecayAlg::saveOthertrks(VWTrkPara &vwtrkpara_charge, VWTrkPara &vwtrkpara_photon, VertexParameter &birth) {
    SmartRefVector<EvtRecTrack> othertracks = (*dtag_iter)->otherTracks();
    SmartDataPtr<EvtRecEvent> evtRecEvent(eventSvc(), "/Event/EvtRec/EvtRecEvent");
    if (m_debug) std::cout << " total charged tracks : " << evtRecEvent->totalCharged() << std::endl;
    if (m_debug) std::cout << " other track number : " << othertracks.size() << " for mode " << mode << std::endl;
    DTagTool dtagTool;
    m_n_othertrks = 0;
    HepLorentzVector ppi_cand;
    int matched_pi_cand = -999;
    // to find the good pions and kaons
    for (int i = 0; i < othertracks.size(); i++) {
        if (!(dtagTool.isGoodTrack(othertracks[i]))) continue;
        if (dtagTool.isPion(othertracks[i])) {
            RecMdcTrack *mdcTrk = othertracks[i]->mdcTrack();
            RecMdcKalTrack *mdcKalTrk = othertracks[i]->mdcKalTrack();
            mdcKalTrk->setPidType(RecMdcKalTrack::pion);
            ppi_cand.setPx(mdcKalTrk->p4(mass[2])[0]);
            ppi_cand.setPy(mdcKalTrk->p4(mass[2])[1]);
            ppi_cand.setPz(mdcKalTrk->p4(mass[2])[2]);
            ppi_cand.setE(mdcKalTrk->p4(mass[2])[3]);
            for (int j = 0; j < 4; j++) {
                m_rawp4_otherMdctrk[m_n_othertrks][j] = mdcTrk->p4(mass[2])[j];
                m_rawp4_otherMdcKaltrk[m_n_othertrks][j] = mdcKalTrk->p4(mass[2])[j];
            }
            m_rawp4_otherMdctrk[m_n_othertrks][4] = mdcTrk->chi2();
            m_rawp4_otherMdctrk[m_n_othertrks][5] = mdcTrk->stat(); // stat: status
            charge_otherMdctrk = mdcTrk->charge();
            m_rawp4_otherMdcKaltrk[m_n_othertrks][4] = mdcKalTrk->charge();
            m_rawp4_otherMdcKaltrk[m_n_othertrks][5] = 2;
            matched_pi_cand = -999;
            matched_pi_cand = MatchMC(ppi_cand, "pi_solo");
            m_rawp4_otherMdcKaltrk[m_n_othertrks][6] = matched_pi_cand;
        }
        if (dtagTool.isKaon(othertracks[i])) {
            RecMdcTrack *mdcTrk = othertracks[i]->mdcTrack();
            RecMdcKalTrack *mdcKalTrk = othertracks[i]->mdcKalTrack();
            mdcKalTrk->setPidType(RecMdcKalTrack::kaon);
            for (int j = 0; j < 4; j++) {
                m_rawp4_otherMdctrk[m_n_othertrks][j] = mdcTrk->p4(mass[2])[j];
                m_rawp4_otherMdcKaltrk[m_n_othertrks][j] = mdcKalTrk->p4(mass[3])[j];
            }
            m_rawp4_otherMdctrk[m_n_othertrks][4] = mdcTrk->chi2();
            m_rawp4_otherMdctrk[m_n_othertrks][5] = mdcTrk->stat(); // stat: status
            m_rawp4_otherMdcKaltrk[m_n_othertrks][4] = mdcKalTrk->charge();
            m_rawp4_otherMdcKaltrk[m_n_othertrks][5] = 3;
            m_rawp4_otherMdcKaltrk[m_n_othertrks][6] = -999;
        }
        m_n_othertrks++;
        if (m_n_othertrks >= 20) return false;
    }

    VWTrkPara vwtrkpara_piplus, vwtrkpara_piminus;
    vwtrkpara_piplus.clear();
    vwtrkpara_piminus.clear();
    int n_piplus = 0;
    int n_piminus = 0;
    HepLorentzVector ppi;
    for (int i = 0; i < othertracks.size(); i++) {
        if (!(dtagTool.isGoodTrack(othertracks[i]))) continue;
        if (m_rawp4_otherMdcKaltrk[i][4] != 1) continue;
        if (m_rawp4_otherMdcKaltrk[i][5] != 2) continue;
        RecMdcKalTrack *mdcKalTrk_plus = othertracks[i]->mdcKalTrack();
        ppi.setPx(mdcKalTrk_plus->p4(mass[2])[0]);
        ppi.setPy(mdcKalTrk_plus->p4(mass[2])[1]);
        ppi.setPz(mdcKalTrk_plus->p4(mass[2])[2]);
        ppi.setE(mdcKalTrk_plus->p4(mass[2])[3]);
        m_matched_pi = 0;
        m_matched_pi = MatchMC(ppi, "pi_solo");
        vwtrkpara_piplus.push_back(WTrackParameter(mass[2], mdcKalTrk_plus->getZHelix(), mdcKalTrk_plus->getZError()));
        n_piplus++;
        for (int j = 0; j < othertracks.size(); j++) {
            if (!(dtagTool.isGoodTrack(othertracks[j]))) continue;
            if (m_rawp4_otherMdcKaltrk[j][4] != -1) continue;
            if (m_rawp4_otherMdcKaltrk[j][5] != 2) continue;
            RecMdcKalTrack *mdcKalTrk_minus = othertracks[j]->mdcKalTrack();
            ppi.setPx(mdcKalTrk_minus->p4(mass[2])[0]);
            ppi.setPy(mdcKalTrk_minus->p4(mass[2])[1]);
            ppi.setPz(mdcKalTrk_minus->p4(mass[2])[2]);
            ppi.setE(mdcKalTrk_minus->p4(mass[2])[3]);
            if (m_matched_pi) m_matched_pi = MatchMC(ppi, "pi_solo");
            vwtrkpara_piminus.push_back(WTrackParameter(mass[2], mdcKalTrk_minus->getZHelix(), mdcKalTrk_minus->getZError()));
            n_piminus++;
            HepLorentzVector pD;
            pD.setPx(0.);
            pD.setPy(0.);
            pD.setPz(0.);
            pD.setE(0.);
            for (int k = 0; k < n_trkD; k++) {
                HepLorentzVector ptrack;
                ptrack.setPx(m_p4_Dtrk[k][0]);
                ptrack.setPy(m_p4_Dtrk[k][1]);
                ptrack.setPz(m_p4_Dtrk[k][2]);
                ptrack.setE(m_p4_Dtrk[k][3]);
                pD += ptrack;
            }
            for(int k = 0; k < n_shwD; k++) {
                HepLorentzVector pshower;
                pshower.setPx(m_p4_Dshw[k][0]);
                pshower.setPy(m_p4_Dshw[k][1]);
                pshower.setPz(m_p4_Dshw[k][2]);
                pshower.setE(m_p4_Dshw[k][3]);
                pD += pshower;
            }
            HepLorentzVector pPip;
            pPip.setPx(mdcKalTrk_plus->p4(mass[2])[0]);
            pPip.setPy(mdcKalTrk_plus->p4(mass[2])[1]);
            pPip.setPz(mdcKalTrk_plus->p4(mass[2])[2]);
            pPip.setE(mdcKalTrk_plus->p4(mass[2])[3]);
            HepLorentzVector pPim;
            pPim.setPx(mdcKalTrk_minus->p4(mass[2])[0]);
            pPim.setPy(mdcKalTrk_minus->p4(mass[2])[1]);
            pPim.setPz(mdcKalTrk_minus->p4(mass[2])[2]);
            pPim.setE(mdcKalTrk_minus->p4(mass[2])[3]);
            double cms = 0;
            double signal_low = 0;
            double signal_up = 0;
            double sidebandlow_low = 0;
            double sidebandlow_up = 0;
            double sidebandup_low = 0;
            double sidebandup_up = 0;
            if (fabs(runNo) >= 30616 && fabs(runNo) <= 31279) {
                cms = 4.358;
                signal_low = 1.8590;
                signal_up = 1.8803;
                sidebandup_low = signal_up + (signal_up - signal_low);
                sidebandup_up = sidebandup_low + (signal_up - signal_low);
                sidebandlow_up = signal_low - (signal_up - signal_low);
                sidebandlow_low = sidebandlow_up - (signal_up - signal_low);
            }
            if ((fabs(runNo) >= 31327 && fabs(runNo) <= 31390) || (fabs(runNo) >= 36773 && fabs(runNo) <= 38140)) {
                cms = 4.416;
                signal_low = 1.8593;
                signal_up = 1.8800;
                sidebandup_low = signal_up + (signal_up - signal_low);
                sidebandup_up = sidebandup_low + (signal_up - signal_low);
                sidebandlow_up = signal_low - (signal_up - signal_low);
                sidebandlow_low = sidebandlow_up - (signal_up - signal_low);
            }
            if (fabs(runNo) >= 35227 && fabs(runNo) <= 36213) {
                cms = 4.600;
                signal_low = 1.8548;
                signal_up = 1.8845;
                sidebandup_low = signal_up + (signal_up - signal_low);
                sidebandup_up = sidebandup_low + (signal_up - signal_low);
                sidebandlow_up = signal_low - (signal_up - signal_low);
                sidebandlow_low = sidebandlow_up - (signal_up - signal_low);
            }
            if (m_debug) {
                std::cout << "Signal region, Sidebandup region, Sidebandlow_region..." << std::endl;
                std::cout << "[" << signal_low << "," << signal_up << "], " << "[" << sidebandup_low << ", " << sidebandup_up << "], " << "[" << sidebandlow_low << ", " << sidebandlow_up << "]" << std::endl;
            }
            HepLorentzVector ecms(0.011*cms, 0, 0, cms);
            double rm_Dpipi = (ecms - pD - pPip - pPim).m();
            chi2_kf_signal = -999;
            m_chi2_kf_signal = -999;
            if (rm_Dpipi > signal_low && rm_Dpipi < signal_up) {
                chi2_kf_signal = fitKM_signal(vwtrkpara_charge, vwtrkpara_photon, vwtrkpara_piplus, vwtrkpara_piminus, n_piplus-1, n_piminus-1, birth);
            }
            chi2_kf_sidebandlow = -999;
            m_chi2_kf_sidebandlow = -999;
            if (rm_Dpipi > sidebandlow_low && rm_Dpipi < sidebandlow_up) {
                double sidebandlow_mean = (sidebandlow_low + sidebandlow_up)/2;
                chi2_kf_sidebandlow = fitKM_sidebandlow(vwtrkpara_charge, vwtrkpara_photon, vwtrkpara_piplus, vwtrkpara_piminus, n_piplus-1, n_piminus-1, birth , sidebandlow_mean);
            }
            chi2_kf_sidebandup = -999;
            m_chi2_kf_sidebandup = -999;
            if (rm_Dpipi > sidebandup_low && rm_Dpipi < sidebandup_up) {
                double sidebandup_mean = (sidebandup_low + sidebandup_up)/2;
                chi2_kf_sidebandup = fitKM_sidebandup(vwtrkpara_charge, vwtrkpara_photon, vwtrkpara_piplus, vwtrkpara_piminus, n_piplus-1, n_piminus-1, birth, sidebandup_mean);
            }
            if (m_debug) std::cout << "Start recording region info if passed the requirement" << std::endl;
            if (fabs(chi2_kf_signal) < 999.) {
                SmartRefVector<EvtRecTrack> Dtrks = (*dtag_iter)->tracks();
                for (int k = 0; k < n_trkD; k++) {
                    RecMdcKalTrack* KalTrk = Dtrks[k]->mdcKalTrack();
                    // if (k == 0) {
                    if (dtagTool.isKaon(Dtrks[k])) {
                        KalTrk->setPidType(RecMdcKalTrack::kaon);
                        for (int l = 0; l < 4; l++) m_rawp4_Dtrk_signal[k][l] = KalTrk->p4(mass[3])[l];
                        m_rawp4_Dtrk_signal[k][4] = KalTrk->charge();
                        m_rawp4_Dtrk_signal[k][5] = 3;
                    }
                    else {
                        KalTrk->setPidType(RecMdcKalTrack::pion);
                        for (int l = 0; l < 4; l++) m_rawp4_Dtrk_signal[k][l] = KalTrk->p4(mass[2])[l];
                        m_rawp4_Dtrk_signal[k][4] = KalTrk->charge();
                        m_rawp4_Dtrk_signal[k][5] = 2;
                    }
                    for (int l = 0; l < 4; l++) m_p4_Dtrkold_signal[k][l] = m_p4_Dtrk[k][l];
                }
                SmartRefVector<EvtRecTrack> Dshws = (*dtag_iter)->showers();
                for(int k = 0; k < Dshws.size(); k++) {
                    RecEmcShower *gTrk = Dshws[k]->emcShower();
                    Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
                    Hep3Vector Gm_Mom = Gm_Vec - birth.vx();
                    Gm_Mom.setMag(gTrk->energy());
                    HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
                    for (int l = 0; l < 4; l++) m_rawp4_Dshw_signal[k][l] = Gm_p4[l];
                }
                charge_left_signal = 0;
                m_charge_left_signal = 0;
                for (int k = 0; k < othertracks.size(); k++) {
                    if (k != i && k != j) charge_left_signal += m_rawp4_otherMdcKaltrk[k][4];
                }
                // to find the good pions and kaons
                m_n_othertrks_signal = 0;
                for (int k = 0; k < othertracks.size(); k++) {
                    if (k != i && k != j) {
                        if (!(dtagTool.isGoodTrack(othertracks[k]))) continue;
                        if (dtagTool.isPion(othertracks[k])) {
                            RecMdcTrack *mdcTrk = othertracks[k]->mdcTrack();
                            RecMdcKalTrack *mdcKalTrk = othertracks[k]->mdcKalTrack();
                            mdcKalTrk->setPidType(RecMdcKalTrack::pion);
                            for (int m = 0; m < 4; m++) {
                                m_rawp4_otherMdctrk_signal[m_n_othertrks_signal][m] = mdcTrk->p4(mass[2])[m];
                                m_rawp4_otherMdcKaltrk_signal[m_n_othertrks_signal][m] = mdcKalTrk->p4(mass[2])[m];
                            }
                            m_rawp4_otherMdctrk_signal[m_n_othertrks_signal][4] = mdcTrk->chi2();
                            m_rawp4_otherMdctrk_signal[m_n_othertrks_signal][5] = mdcTrk->stat(); // stat: status
                            m_rawp4_otherMdcKaltrk_signal[m_n_othertrks_signal][4] = mdcKalTrk->charge();
                            m_rawp4_otherMdcKaltrk_signal[m_n_othertrks_signal][5] = 2;
                        }
                        if (dtagTool.isKaon(othertracks[k])) {
                            RecMdcTrack *mdcTrk = othertracks[k]->mdcTrack();
                            RecMdcKalTrack *mdcKalTrk = othertracks[k]->mdcKalTrack();
                            mdcKalTrk->setPidType(RecMdcKalTrack::kaon);
                            for (int m = 0; m < 4; m++) {
                                m_rawp4_otherMdctrk_signal[m_n_othertrks_signal][m] = mdcTrk->p4(mass[2])[m];
                                m_rawp4_otherMdcKaltrk_signal[m_n_othertrks_signal][m] = mdcKalTrk->p4(mass[3])[m];
                            }
                            m_rawp4_otherMdctrk_signal[m_n_othertrks_signal][4] = mdcTrk->chi2();
                            m_rawp4_otherMdctrk_signal[m_n_othertrks_signal][5] = mdcTrk->stat(); // stat: status
                            m_rawp4_otherMdcKaltrk_signal[m_n_othertrks_signal][4] = mdcKalTrk->charge();
                            m_rawp4_otherMdcKaltrk_signal[m_n_othertrks_signal][5] = 3;
                        }
                        m_n_othertrks_signal++;
                        if (m_n_othertrks_signal >= 20) continue;
                    }
                }
                RecMdcKalTrack *Piplus = othertracks[i]->mdcKalTrack();
                for (int k = 0; k < 4; k++) m_rawp4_tagPiplus_signal[k] = Piplus->p4(mass[2])[k];
                RecMdcKalTrack *Piminus = othertracks[j]->mdcKalTrack();
                for (int k = 0; k < 4; k++) m_rawp4_tagPiminus_signal[k] = Piminus->p4(mass[2])[k];
                SmartRefVector<EvtRecTrack> othershowers = (*dtag_iter)->otherShowers();
                // to find the good photons in the othershowers list
                VWTrkPara vwtrkpara_photons_signal;
                vwtrkpara_photons_signal.clear();
                m_n_othershws_signal = 0;
                for (int k = 0; k < othershowers.size(); k++) {
                    if (!(dtagTool.isGoodShower(othershowers[k]))) continue;
                    RecEmcShower *gTrk = othershowers[k]->emcShower();
                    Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
                    Hep3Vector Gm_Mom = Gm_Vec - birth.vx();
                    Gm_Mom.setMag(gTrk->energy());
                    HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
                    for (int m = 0; m < 4; m++) m_rawp4_othershw_signal[m_n_othershws_signal][m] = Gm_p4[m];
                    m_n_othershws_signal++;
                    if (m_n_othershws_signal >= 50) continue;
                    vwtrkpara_photons_signal.push_back(WTrackParameter(gTrk->position(), Gm_p4, gTrk->dphi(), gTrk->dtheta(), gTrk->dE()));
                }
                stat_fitpi0_signal = fitpi0_signal(vwtrkpara_photons_signal, birth, pD);
                if (!stat_fitpi0_signal && m_debug) std::cout << "Cannot find enough gamma to reconstruct pi0 for signal!" << std::endl;
                recordVariables_signal();
            }
            if (fabs(chi2_kf_sidebandlow) < 999.) {
                SmartRefVector<EvtRecTrack> Dtrks = (*dtag_iter)->tracks();
                for (int k = 0; k < n_trkD; k++) {
                    RecMdcKalTrack* KalTrk = Dtrks[k]->mdcKalTrack();
                    // if (k == 0) {
                    if (dtagTool.isKaon(Dtrks[k])) {
                        KalTrk->setPidType(RecMdcKalTrack::kaon);
                        for (int l = 0; l < 4; l++) m_rawp4_Dtrk_sidebandlow[k][l] = KalTrk->p4(mass[3])[l];
                        m_rawp4_Dtrk_sidebandlow[k][4] = KalTrk->charge();
                        m_rawp4_Dtrk_sidebandlow[k][5] = 3;
                    }
                    else {
                        KalTrk->setPidType(RecMdcKalTrack::pion);
                        for (int l = 0; l < 4; l++) m_rawp4_Dtrk_sidebandlow[k][l] = KalTrk->p4(mass[2])[l];
                        m_rawp4_Dtrk_sidebandlow[k][4] = KalTrk->charge();
                        m_rawp4_Dtrk_sidebandlow[k][5] = 2;
                    }
                    for (int l = 0; l < 4; l++) m_p4_Dtrkold_sidebandlow[k][l] = m_p4_Dtrk[k][l];
                }
                SmartRefVector<EvtRecTrack> Dshws = (*dtag_iter)->showers();
                for(int k = 0; k < Dshws.size(); k++) {
                    RecEmcShower *gTrk = Dshws[k]->emcShower();
                    Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
                    Hep3Vector Gm_Mom = Gm_Vec - birth.vx();
                    Gm_Mom.setMag(gTrk->energy());
                    HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
                    for (int l = 0; l < 4; l++) m_rawp4_Dshw_sidebandlow[k][l] = Gm_p4[l];
                }
                charge_left_sidebandlow = 0;
                m_charge_left_sidebandlow = 0;
                for (int k = 0; k < othertracks.size(); k++) {
                    if (k != i && k != j) charge_left_sidebandlow += m_rawp4_otherMdcKaltrk[k][4];
                }
                // to find the good pions and kaons
                m_n_othertrks_sidebandlow = 0;
                for (int k = 0; k < othertracks.size(); k++) {
                    if (k != i && k != j) {
                        if (!(dtagTool.isGoodTrack(othertracks[k]))) continue;
                        if (dtagTool.isPion(othertracks[k])) {
                            RecMdcTrack *mdcTrk = othertracks[k]->mdcTrack();
                            RecMdcKalTrack *mdcKalTrk = othertracks[k]->mdcKalTrack();
                            mdcKalTrk->setPidType(RecMdcKalTrack::pion);
                            for (int m = 0; m < 4; m++) {
                                m_rawp4_otherMdctrk_sidebandlow[m_n_othertrks_sidebandlow][m] = mdcTrk->p4(mass[2])[m];
                                m_rawp4_otherMdcKaltrk_sidebandlow[m_n_othertrks_sidebandlow][m] = mdcKalTrk->p4(mass[2])[m];
                            }
                            m_rawp4_otherMdctrk_sidebandlow[m_n_othertrks_sidebandlow][4] = mdcTrk->chi2();
                            m_rawp4_otherMdctrk_sidebandlow[m_n_othertrks_sidebandlow][5] = mdcTrk->stat(); // stat: status
                            m_rawp4_otherMdcKaltrk_sidebandlow[m_n_othertrks_sidebandlow][4] = mdcKalTrk->charge();
                            m_rawp4_otherMdcKaltrk_sidebandlow[m_n_othertrks_sidebandlow][5] = 2;
                        }
                        if (dtagTool.isKaon(othertracks[k])) {
                            RecMdcTrack *mdcTrk = othertracks[k]->mdcTrack();
                            RecMdcKalTrack *mdcKalTrk = othertracks[k]->mdcKalTrack();
                            mdcKalTrk->setPidType(RecMdcKalTrack::kaon);
                            for (int m = 0; m < 4; m++) {
                                m_rawp4_otherMdctrk_sidebandlow[m_n_othertrks_sidebandlow][m] = mdcTrk->p4(mass[2])[m];
                                m_rawp4_otherMdcKaltrk_sidebandlow[m_n_othertrks_sidebandlow][m] = mdcKalTrk->p4(mass[3])[m];
                            }
                            m_rawp4_otherMdctrk_sidebandlow[m_n_othertrks_sidebandlow][4] = mdcTrk->chi2();
                            m_rawp4_otherMdctrk_sidebandlow[m_n_othertrks_sidebandlow][5] = mdcTrk->stat(); // stat: status
                            m_rawp4_otherMdcKaltrk_sidebandlow[m_n_othertrks_sidebandlow][4] = mdcKalTrk->charge();
                            m_rawp4_otherMdcKaltrk_sidebandlow[m_n_othertrks_sidebandlow][5] = 3;
                        }
                        m_n_othertrks_sidebandlow++;
                        if (m_n_othertrks_sidebandlow >= 20) continue;
                    }
                }
                RecMdcKalTrack *Piplus = othertracks[i]->mdcKalTrack();
                for (int k = 0; k < 4; k++) m_rawp4_tagPiplus_sidebandlow[k] = Piplus->p4(mass[2])[k];
                RecMdcKalTrack *Piminus = othertracks[j]->mdcKalTrack();
                for (int k = 0; k < 4; k++) m_rawp4_tagPiminus_sidebandlow[k] = Piminus->p4(mass[2])[k];
                SmartRefVector<EvtRecTrack> othershowers = (*dtag_iter)->otherShowers();
                // to find the good photons in the othershowers list
                VWTrkPara vwtrkpara_photons_sidebandlow;
                vwtrkpara_photons_sidebandlow.clear();
                m_n_othershws_sidebandlow = 0;
                for (int k = 0; k < othershowers.size(); k++) {
                    if (!(dtagTool.isGoodShower(othershowers[k]))) continue;
                    RecEmcShower *gTrk = othershowers[k]->emcShower();
                    Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
                    Hep3Vector Gm_Mom = Gm_Vec - birth.vx();
                    Gm_Mom.setMag(gTrk->energy());
                    HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
                    for (int m = 0; m < 4; m++) m_rawp4_othershw_sidebandlow[m_n_othershws_sidebandlow][m] = Gm_p4[m];
                    m_n_othershws_sidebandlow++;
                    if (m_n_othershws_sidebandlow >= 50) continue;
                    vwtrkpara_photons_sidebandlow.push_back(WTrackParameter(gTrk->position(), Gm_p4, gTrk->dphi(), gTrk->dtheta(), gTrk->dE()));
                }
                stat_fitpi0_sidebandlow = fitpi0_sidebandlow(vwtrkpara_photons_sidebandlow, birth, pD);
                if (!stat_fitpi0_sidebandlow && m_debug) std::cout << "Cannot find enough gamma to reconstruct pi0 for sidebandlow!" << std::endl;
                recordVariables_sidebandlow();
            }
            if (fabs(chi2_kf_sidebandup) < 999.) {
                SmartRefVector<EvtRecTrack> Dtrks = (*dtag_iter)->tracks();
                for (int k = 0; k < n_trkD; k++) {
                    RecMdcKalTrack* KalTrk = Dtrks[k]->mdcKalTrack();
                    // if (k == 0) {
                    if (dtagTool.isKaon(Dtrks[k])) {
                        KalTrk->setPidType(RecMdcKalTrack::kaon);
                        for (int l = 0; l < 4; l++) m_rawp4_Dtrk_sidebandup[k][l] = KalTrk->p4(mass[3])[l];
                        m_rawp4_Dtrk_sidebandup[k][4] = KalTrk->charge();
                        m_rawp4_Dtrk_sidebandup[k][5] = 3;
                    }
                    else {
                        KalTrk->setPidType(RecMdcKalTrack::pion);
                        for (int l = 0; l < 4; l++) m_rawp4_Dtrk_sidebandup[k][l] = KalTrk->p4(mass[2])[l];
                        m_rawp4_Dtrk_sidebandup[k][4] = KalTrk->charge();
                        m_rawp4_Dtrk_sidebandup[k][5] = 2;
                    }
                    for (int l = 0; l < 4; l++) m_p4_Dtrkold_sidebandup[k][l] = m_p4_Dtrk[k][l];
                }
                SmartRefVector<EvtRecTrack> Dshws = (*dtag_iter)->showers();
                for(int k = 0; k < Dshws.size(); k++) {
                    RecEmcShower *gTrk = Dshws[k]->emcShower();
                    Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
                    Hep3Vector Gm_Mom = Gm_Vec - birth.vx();
                    Gm_Mom.setMag(gTrk->energy());
                    HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
                    for (int l = 0; l < 4; l++) m_rawp4_Dshw_sidebandup[k][l] = Gm_p4[l];
                }
                charge_left_sidebandup = 0;
                m_charge_left_sidebandup = 0;
                for (int k = 0; k < othertracks.size(); k++) {
                    if (k != i && k != j) charge_left_sidebandup += m_rawp4_otherMdcKaltrk[k][4];
                }
                // to find the good pions and kaons
                m_n_othertrks_sidebandup = 0;
                for (int k = 0; k < othertracks.size(); k++) {
                    if (k != i && k != j) {
                        if (!(dtagTool.isGoodTrack(othertracks[k]))) continue;
                        if (dtagTool.isPion(othertracks[k])) {
                            RecMdcTrack *mdcTrk = othertracks[k]->mdcTrack();
                            RecMdcKalTrack *mdcKalTrk = othertracks[k]->mdcKalTrack();
                            mdcKalTrk->setPidType(RecMdcKalTrack::pion);
                            for (int m = 0; m < 4; m++) {
                                m_rawp4_otherMdctrk_sidebandup[m_n_othertrks_sidebandup][m] = mdcTrk->p4(mass[2])[m];
                                m_rawp4_otherMdcKaltrk_sidebandup[m_n_othertrks_sidebandup][m] = mdcKalTrk->p4(mass[2])[m];
                            }
                            m_rawp4_otherMdctrk_sidebandup[m_n_othertrks_sidebandup][4] = mdcTrk->chi2();
                            m_rawp4_otherMdctrk_sidebandup[m_n_othertrks_sidebandup][5] = mdcTrk->stat(); // stat: status
                            m_rawp4_otherMdcKaltrk_sidebandup[m_n_othertrks_sidebandup][4] = mdcKalTrk->charge();
                            m_rawp4_otherMdcKaltrk_sidebandup[m_n_othertrks_sidebandup][5] = 2;
                        }
                        if (dtagTool.isKaon(othertracks[k])) {
                            RecMdcTrack *mdcTrk = othertracks[k]->mdcTrack();
                            RecMdcKalTrack *mdcKalTrk = othertracks[k]->mdcKalTrack();
                            mdcKalTrk->setPidType(RecMdcKalTrack::kaon);
                            for (int m = 0; m < 4; m++) {
                                m_rawp4_otherMdctrk_sidebandup[m_n_othertrks_sidebandup][m] = mdcTrk->p4(mass[2])[m];
                                m_rawp4_otherMdcKaltrk_sidebandup[m_n_othertrks_sidebandup][m] = mdcKalTrk->p4(mass[3])[m];
                            }
                            m_rawp4_otherMdctrk_sidebandup[m_n_othertrks_sidebandup][4] = mdcTrk->chi2();
                            m_rawp4_otherMdctrk_sidebandup[m_n_othertrks_sidebandup][5] = mdcTrk->stat(); // stat: status
                            m_rawp4_otherMdcKaltrk_sidebandup[m_n_othertrks_sidebandup][4] = mdcKalTrk->charge();
                            m_rawp4_otherMdcKaltrk_sidebandup[m_n_othertrks_sidebandup][5] = 3;
                        }
                        m_n_othertrks_sidebandup++;
                        if (m_n_othertrks_sidebandup >= 20) continue;
                    }
                }
                RecMdcKalTrack *Piplus = othertracks[i]->mdcKalTrack();
                for (int k = 0; k < 4; k++) m_rawp4_tagPiplus_sidebandup[k] = Piplus->p4(mass[2])[k];
                RecMdcKalTrack *Piminus = othertracks[j]->mdcKalTrack();
                for (int k = 0; k < 4; k++) m_rawp4_tagPiminus_sidebandup[k] = Piminus->p4(mass[2])[k];
                SmartRefVector<EvtRecTrack> othershowers = (*dtag_iter)->otherShowers();
                // to find the good photons in the othershowers list
                VWTrkPara vwtrkpara_photons_sidebandup;
                vwtrkpara_photons_sidebandup.clear();
                m_n_othershws_sidebandup = 0;
                for (int k = 0; k < othershowers.size(); k++) {
                    if (!(dtagTool.isGoodShower(othershowers[k]))) continue;
                    RecEmcShower *gTrk = othershowers[k]->emcShower();
                    Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
                    Hep3Vector Gm_Mom = Gm_Vec - birth.vx();
                    Gm_Mom.setMag(gTrk->energy());
                    HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
                    for (int m = 0; m < 4; m++) m_rawp4_othershw_sidebandup[m_n_othershws_sidebandup][m] = Gm_p4[m];
                    m_n_othershws_sidebandup++;
                    if (m_n_othershws_sidebandup >= 50) continue;
                    vwtrkpara_photons_sidebandup.push_back(WTrackParameter(gTrk->position(), Gm_p4, gTrk->dphi(), gTrk->dtheta(), gTrk->dE()));
                }
                stat_fitpi0_sidebandup = fitpi0_sidebandup(vwtrkpara_photons_sidebandup, birth, pD);
                if (!stat_fitpi0_sidebandup && m_debug) std::cout << "Cannot find enough gamma to reconstruct pi0 for sidebandup!" << std::endl;
                recordVariables_sidebandup();
            }
        }
    }

    if (m_debug) std::cout << " recorded " << m_n_othertrks << " other charged good tracks " << std::endl;
    if (m_n_othertrks >= 20) return false;
    else return true;
}

int DDecayAlg::MatchMC(HepLorentzVector &p4, std::string MODE) {
    SmartDataPtr<Event::McParticleCol> mcParticleCol(eventSvc(), "/Event/MC/McParticleCol");
    if (!mcParticleCol) {
        return -999;
    } else {
        Event::McParticleCol::iterator iter_mc = mcParticleCol->begin();
        double clst_ang = 999.;
        Event::McParticle* clst_particle;
        for (; iter_mc != mcParticleCol->end(); iter_mc++) {
            if (!(*iter_mc)->decayFromGenerator())  continue;
            double pid_cand = (*iter_mc)->particleProperty();
            if (!(pid_cand == 211 || pid_cand == -211 || pid_cand == 321 || pid_cand == -321)) continue;
            double ang = p4.angle((*iter_mc)->initialFourMomentum());
            if (clst_ang > ang) {
                clst_ang = ang;
                clst_particle = (*iter_mc);
            }
        }
        if (clst_ang < 999) {
            Event::McParticle mom = clst_particle->mother();
            int pid_mom = mom.particleProperty();
            Event::McParticle grandmom = mom.mother();
            int pid_grandmom = grandmom.particleProperty();
            if (MODE == "D_tag" && (fabs(pid_mom) == 411 || (pid_mom == 310 && fabs(pid_grandmom) == 411)) || (pid_mom == 111 && fabs(pid_grandmom) == 411)) {
                return 1;
            } 
            if (MODE == "D_tag" && (fabs(pid_mom) != 411 && (pid_mom != 310 && fabs(pid_grandmom) != 411)) && (pid_mom != 111 && fabs(pid_grandmom) != 411)) {
                return 0;
            }
            if (MODE == "pi_solo" && (pid_mom == 9020443 || pid_mom == 9030443 || pid_mom == 90022 || pid_mom == 80022)) {
                return 1;
            } 
            if (MODE == "pi_solo" && (pid_mom != 9020443 || pid_mom != 9030443 || pid_mom != 90022 || pid_mom != 80022)) {
                return 0;
            }
        }
    }
    return 0;
}

bool DDecayAlg::saveOthershws() {
    HepLorentzVector pD;
    pD.setPx(0.);
    pD.setPy(0.);
    pD.setPz(0.);
    pD.setE(0.);
    for (int k = 0; k < n_trkD; k++) {
        HepLorentzVector ptrack;
        ptrack.setPx(m_p4_Dtrk[k][0]);
        ptrack.setPy(m_p4_Dtrk[k][1]);
        ptrack.setPz(m_p4_Dtrk[k][2]);
        ptrack.setE(m_p4_Dtrk[k][3]);
        pD += ptrack;
    }
    for(int k = 0; k < n_shwD; k++) {
        HepLorentzVector pshower;
        pshower.setPx(m_p4_Dshw[k][0]);
        pshower.setPy(m_p4_Dshw[k][1]);
        pshower.setPz(m_p4_Dshw[k][2]);
        pshower.setE(m_p4_Dshw[k][3]);
        pD += pshower;
    }
    SmartRefVector<EvtRecTrack> othershowers = (*dtag_iter)->otherShowers();
    SmartDataPtr<EvtRecEvent> evtRecEvent(eventSvc(), "/Event/EvtRec/EvtRecEvent");
    if (m_debug) std::cout << " total showers : " << evtRecEvent->totalNeutral() <<endl;
    if (m_debug) std::cout << " other shower numbers : " << othershowers.size() << " for mode " << mode << std::endl;
    DTagTool dtagTool;
    m_n_othershws = 0;
    // to find the good photons in the othershowers list
    vwtrkpara_othershws.clear();
    for (int i = 0; i < othershowers.size(); i++) {
        if (!(dtagTool.isGoodShower(othershowers[i]))) continue;
        RecEmcShower *gTrk = othershowers[i]->emcShower();
        Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
        Hep3Vector Gm_Mom = Gm_Vec - birth.vx();
        Gm_Mom.setMag(gTrk->energy());
        HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
        for (int j = 0; j < 4; j++) m_rawp4_othershw[m_n_othershws][j] = Gm_p4[j];
        m_n_othershws++;
        if (m_n_othershws >= 50) return false;
        vwtrkpara_othershws.push_back(WTrackParameter(gTrk->position(), Gm_p4, gTrk->dphi(), gTrk->dtheta(), gTrk->dE()));
    }
    stat_fitpi0 = fitpi0(vwtrkpara_othershws, birth, pD);
    if (!stat_fitpi0 && m_debug) std::cout << "Cannot find enough gamma to reconstruct pi0!" << std::endl;
    if (m_debug) std::cout << " recorded " << m_n_othershws << " other good showers " << std::endl;
    if (m_n_othershws >= 50) return false;
    else return true;
}

bool DDecayAlg::fitpi0(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD) {
    m_n_pi0 = 0;
    for (int i = 0; i < 4; i++) {
        m_p4_pi0_save[i] = -999.;
    }
    m_chi2_pi0_save = -999.;
    if (vwtrkpara_photons.size() <= 1) return false;
    double delta_M = 999.;
    for (int i = 0; i < vwtrkpara_photons.size() - 1; i++) {
        for (int j = i + 1; j < vwtrkpara_photons.size(); j++) {
            kmfit->init();
            kmfit->AddTrack(0, vwtrkpara_photons[i]);
            kmfit->AddTrack(1, vwtrkpara_photons[j]);
            kmfit->AddResonance(0, M_Pi0, 0, 1);
            bool oksq = kmfit->Fit();
            if (oksq) {
                double chi2 = kmfit->chisq();
                if (chi2 < 200) {
                    m_chi2_pi0[m_n_pi0] = chi2;
                    HepLorentzVector ppi0 = kmfit->pfit(0) + kmfit->pfit(1);
                    for (int k = 0; k < 4; k++) m_p4_pi0[m_n_pi0][k] = ppi0[k];
                    m_n_pi0++;
                    if (fabs((ppi0 + pD).m() - M_Dst) < delta_M) {
                        delta_M = fabs((ppi0 + pD).m() - M_Dst);
                        m_chi2_pi0_save = chi2;
                        for (int k = 0; k < 4; k++) m_p4_pi0_save[k] = ppi0[k];
                    }
                }
            }
            else {
                continue;
            }
        }
    }
    return true;
}

bool DDecayAlg::fitpi0_signal(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD) {
    m_n_pi0_signal = 0;
    for (int i = 0; i < 4; i++) {
        m_p4_pi0_save_signal[i] = -999.;
    }
    m_chi2_pi0_save_signal = -999.;
    if (vwtrkpara_photons.size() <= 1) return false;
    double delta_M = 999.;
    for (int i = 0; i < vwtrkpara_photons.size() - 1; i++) {
        for (int j = i + 1; j < vwtrkpara_photons.size(); j++) {
            kmfit->init();
            kmfit->AddTrack(0, vwtrkpara_photons[i]);
            kmfit->AddTrack(1, vwtrkpara_photons[j]);
            kmfit->AddResonance(0, M_Pi0, 0, 1);
            bool oksq = kmfit->Fit();
            if (oksq) {
                double chi2 = kmfit->chisq();
                if (chi2 < 200) {
                    m_chi2_pi0_signal[m_n_pi0_signal] = chi2;
                    HepLorentzVector ppi0 = kmfit->pfit(0) + kmfit->pfit(1);
                    for (int k = 0; k < 4; k++) m_p4_pi0_signal[m_n_pi0_signal][k] = ppi0[k];
                    m_n_pi0_signal++;
                    if (fabs((ppi0 + pD).m() - M_Dst) < delta_M) {
                        delta_M = fabs((ppi0 + pD).m() - M_Dst);
                        m_chi2_pi0_save_signal = chi2;
                        for (int k = 0; k < 4; k++) m_p4_pi0_save_signal[k] = ppi0[k];
                    }
                }
            }
            else {
                continue;
            }
        }
    }
    return true;
}

bool DDecayAlg::fitpi0_sidebandlow(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD) {
    m_n_pi0_sidebandlow = 0;
    for (int i = 0; i < 4; i++) {
        m_p4_pi0_save_sidebandlow[i] = -999.;
    }
    m_chi2_pi0_save_sidebandlow = -999.;
    if (vwtrkpara_photons.size() <= 1) return false;
    double delta_M = 999.;
    for (int i = 0; i < vwtrkpara_photons.size() - 1; i++) {
        for (int j = i + 1; j < vwtrkpara_photons.size(); j++) {
            kmfit->init();
            kmfit->AddTrack(0, vwtrkpara_photons[i]);
            kmfit->AddTrack(1, vwtrkpara_photons[j]);
            kmfit->AddResonance(0, M_Pi0, 0, 1);
            bool oksq = kmfit->Fit();
            if (oksq) {
                double chi2 = kmfit->chisq();
                if (chi2 < 200) {
                    m_chi2_pi0_sidebandlow[m_n_pi0_sidebandlow] = chi2;
                    HepLorentzVector ppi0 = kmfit->pfit(0) + kmfit->pfit(1);
                    for (int k = 0; k < 4; k++) m_p4_pi0_sidebandlow[m_n_pi0_sidebandlow][k] = ppi0[k];
                    m_n_pi0_sidebandlow++;
                    if (fabs((ppi0 + pD).m() - M_Dst) < delta_M) {
                        delta_M = fabs((ppi0 + pD).m() - M_Dst);
                        m_chi2_pi0_save_sidebandlow = chi2;
                        for (int k = 0; k < 4; k++) m_p4_pi0_save_sidebandlow[k] = ppi0[k];
                    }
                }
            }
        }
    }
    return true;
}

bool DDecayAlg::fitpi0_sidebandup(VWTrkPara &vwtrkpara_photons, VertexParameter &birth, HepLorentzVector &pD) {
    m_n_pi0_sidebandup = 0;
    for (int i = 0; i < 4; i++) {
        m_p4_pi0_save_sidebandup[i] = -999.;
    }
    m_chi2_pi0_save_sidebandup = -999.;
    if (vwtrkpara_photons.size() <= 1) return false;
    double delta_M = 999.;
    for (int i = 0; i < vwtrkpara_photons.size() - 1; i++) {
        for (int j = i + 1; j < vwtrkpara_photons.size(); j++) {
            kmfit->init();
            kmfit->AddTrack(0, vwtrkpara_photons[i]);
            kmfit->AddTrack(1, vwtrkpara_photons[j]);
            kmfit->AddResonance(0, M_Pi0, 0, 1);
            bool oksq = kmfit->Fit();
            if (oksq) {
                double chi2 = kmfit->chisq();
                if (chi2 < 200) {
                    m_chi2_pi0_sidebandup[m_n_pi0_sidebandup] = chi2;
                    HepLorentzVector ppi0 = kmfit->pfit(0) + kmfit->pfit(1);
                    for (int k = 0; k < 4; k++) m_p4_pi0_sidebandup[m_n_pi0_sidebandup][k] = ppi0[k];
                    m_n_pi0_sidebandup++;
                    if (fabs((ppi0 + pD).m() - M_Dst) < delta_M) {
                        delta_M = fabs((ppi0 + pD).m() - M_Dst);
                        m_chi2_pi0_save_sidebandup = chi2;
                        for (int k = 0; k < 4; k++) m_p4_pi0_save_sidebandup[k] = ppi0[k];
                    }
                }
            }
        }
    }
    return true;
}

void DDecayAlg::recordVariables() {
    m_runNo = runNo;
    m_evtNo = evtNo;
    m_flag1 = flag1;
    m_runNo_otherTrk = runNo;
    m_evtNo_otherTrk = evtNo;
    m_flag1_otherTrk = flag1;
    m_runNo_otherShw = runNo;
    m_evtNo_otherShw = evtNo;
    m_flag1_otherShw = flag1;
    m_runNo_allTruth = runNo;
    m_evtNo_allTruth = evtNo;
    m_flag1_allTruth = flag1;
    m_runNo_DststTruth = runNo;
    m_evtNo_DststTruth = evtNo;
    m_flag1_DststTruth = flag1;
    m_runNo_PsiTruth = runNo;
    m_evtNo_PsiTruth = evtNo;
    m_flag1_PsiTruth = flag1;
    m_runNo_DpDmTruth = runNo;
    m_evtNo_DpDmTruth = evtNo;
    m_flag1_DpDmTruth = flag1;

    // save all McTruth info
    if (m_runNo < 0 && m_isMonteCarlo) {
        m_idxmc = idxmc;
        for (int i = 0; i< m_idxmc; i++) {
            m_motheridx[i] = motheridx[i];
            m_pdgid[i] = pdgid[i];
        }
    }

    // save Dstst McTruth info
    if (m_runNo < 0 && m_isMonteCarlo) {
        for (int i = 0; i < 4; i++) {
            m_p4_pip[i] = p4_pip[i];
            m_p4_pim[i] = p4_pim[i];
            m_p4_Dstst[i] = p4_Dstst[i];
            m_p4_D1[i] = p4_D1[i];
            m_p4_D2[i] = p4_D2[i];
        }
    }

    // save psi(3770) McTruth info
    if (m_runNo < 0 && m_isMonteCarlo) {
        for (int i = 0; i < 4; i++) {
            m_p4_pip_psi[i] = p4_pip_psi[i];
            m_p4_pim_psi[i] = p4_pim_psi[i];
            m_p4_psi[i] = p4_psi[i];
            m_p4_Dp_psi[i] = p4_Dp_psi[i];
            m_p4_Dm_psi[i] = p4_Dm_psi[i];
        }
    }

    // save DpDm McTruth info
    m_Id_Dp = DpId;
    m_Id_Dm = DmId;

    // save DTag inDststfo
    m_n_trkD = n_trkD;
    m_n_shwD = n_shwD;
    m_mode = MODE;
    m_charm = charm;
    m_chi2_vf = chi2_vf;
    m_chi2_kf = chi2_kf;
    m_n_count = n_count;

    m_tuple1->write();
    m_tuple2->write();
    m_tuple3->write();
    m_tuple4->write();
    m_tuple5->write();
    m_tuple6->write();
    m_tuple7->write();

    if (m_debug) std::cout << " entry in ntuple is filled for " << mode << std::endl;
}

void DDecayAlg::recordVariables_signal() {
    m_runNo_signal = runNo;
    m_evtNo_signal = evtNo;
    m_flag1_signal = flag1;

    // save DTag info
    m_n_trkD_signal = n_trkD;
    m_n_shwD_signal = n_shwD;
    m_mode_signal = MODE;
    m_charm_signal = charm;
    m_chi2_vf_signal = chi2_vf;
    m_chi2_kf_signal = chi2_kf_signal;
    m_charge_left_signal = charge_left_signal;

    // save all McTruth info for fitKM_signal
    if (m_runNo_signal < 0 && m_isMonteCarlo) {
        m_idxmc_signal = idxmc;
        for (int i = 0; i< m_idxmc_signal; i++) {
            m_motheridx_signal[i] = motheridx[i];
            m_pdgid_signal[i] = pdgid[i];
        }
    }
    m_tuple8->write();

    if (m_debug) std::cout << " Signal region: entry in ntuple is filled for " << mode << std::endl;
}

void DDecayAlg::recordVariables_sidebandlow() {
    m_runNo_sidebandlow = runNo;
    m_evtNo_sidebandlow = evtNo;
    m_flag1_sidebandlow = flag1;

    // save DTag info
    m_n_trkD_sidebandlow = n_trkD;
    m_n_shwD_sidebandlow = n_shwD;
    m_mode_sidebandlow = MODE;
    m_charm_sidebandlow = charm;
    m_chi2_vf_sidebandlow = chi2_vf;
    m_chi2_kf_sidebandlow = chi2_kf_sidebandlow;
    m_charge_left_sidebandlow = charge_left_sidebandlow;

    // save all McTruth info for fitKM_sidebandlow
    if (m_runNo_sidebandlow < 0 && m_isMonteCarlo) {
        m_idxmc_sidebandlow = idxmc;
        for (int i = 0; i< m_idxmc_sidebandlow; i++) {
            m_motheridx_sidebandlow[i] = motheridx[i];
            m_pdgid_sidebandlow[i] = pdgid[i];
        }
    }
    m_tuple9->write();

    if (m_debug) std::cout << " Lower sideband region: entry in ntuple is filled for " << mode << std::endl;
}

void DDecayAlg::recordVariables_sidebandup() {
    m_runNo_sidebandup = runNo;
    m_evtNo_sidebandup = evtNo;
    m_flag1_sidebandup = flag1;

    // save DTag info
    m_n_trkD_sidebandup = n_trkD;
    m_n_shwD_sidebandup = n_shwD;
    m_mode_sidebandup = MODE;
    m_charm_sidebandup = charm;
    m_chi2_vf_sidebandup = chi2_vf;
    m_chi2_kf_sidebandup = chi2_kf_sidebandup;
    m_charge_left_sidebandup = charge_left_sidebandup;

    // save all McTruth info for fitKM_sidebandup
    if (m_runNo_sidebandup < 0 && m_isMonteCarlo) {
        m_idxmc_sidebandup = idxmc;
        for (int i = 0; i< m_idxmc_sidebandup; i++) {
            m_motheridx_sidebandup[i] = motheridx[i];
            m_pdgid_sidebandup[i] = pdgid[i];
        }
    }
    m_tuple10->write();

    if (m_debug) std::cout << "Higher sideband region: entry in ntuple is filled for " << mode << std::endl;
}
