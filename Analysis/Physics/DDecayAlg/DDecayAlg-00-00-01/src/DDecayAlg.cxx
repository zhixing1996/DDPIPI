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
const double M_Dplus = 1.86960;
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
            status = m_tuple1->addIndexedItem("rawp4_Dtrk", m_n_trkD, 4, m_rawp4_Dtrk); // four members array
            status = m_tuple1->addIndexedItem("p4_Dtrk", m_n_trkD, 4, m_p4_Dtrk);
            status = m_tuple1->addItem("n_shwD", m_n_shwD, 0, 2); 
            status = m_tuple1->addIndexedItem("rawp4_Dshw", m_n_shwD, 4, m_rawp4_Dshw);
            status = m_tuple1->addIndexedItem("p4_Dshw", m_n_shwD, 4, m_p4_Dshw);
            status = m_tuple1->addItem("mode", m_mode);
            status = m_tuple1->addItem("charm", m_charm);
            status = m_tuple1->addItem("chi2_vf", m_chi2_vf);
            status = m_tuple1->addItem("chi2_kf", m_chi2_kf);
            status = m_tuple1->addItem("n_count", m_n_count); // multi-counting D in one event

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
            status = m_tuple2->addIndexedItem("rawp4_otherMdcKaltrk", m_n_othertrks, 6, m_rawp4_otherMdcKaltrk);
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
            status = m_tuple4->addIndexedItem("p4_alltrk", m_idxmc, 4, m_p4_alltrk);
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

    // all McTruth info
    m_idxmc = 0;
    pAll.clear();
    pdg.clear();
    mother.clear();

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
    n_trkD = 0;
    m_n_shwD = 0;
    n_shwD = 0;
    MODE = -999;
    mode = -999;
    m_mode = -999;
    charm = -999;
    m_charm = -999;
    chi2_vf = -999;
    m_chi2_vf = -999;
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
}

void DDecayAlg::saveAllMcTruthInfo() {
    SmartDataPtr<Event::McParticleCol> mcParticleCol(eventSvc(), "/Event/MC/McParticleCol");
    if (!mcParticleCol) {
        std::cout << "Could not retreive McParticleCol" << std::endl;
    }
    else {
        Event::McParticleCol::iterator iter_mc = mcParticleCol->begin(); // loop all the particles in the decay chain(MCTruth)
        for (; iter_mc != mcParticleCol->end(); iter_mc++) {
            pAll.push_back((*iter_mc)->initialFourMomentum()); // initialFourMomentum: Four Momentum in the iteraction point
            pdg.push_back((*iter_mc)->particleProperty());
            mother.push_back((*iter_mc)->mother().particleProperty());
        }
        for (int i = 0; i < pdg.size(); i++) {
            pdgid[i] = pdg[i];
            motheridx[i] = mother[i];
            m_p4_alltrk[i][0] = pAll[i].px();
            m_p4_alltrk[i][1] = pAll[i].py();
            m_p4_alltrk[i][2] = pAll[i].pz();
            m_p4_alltrk[i][3] = pAll[i].e();
            if (m_debug) {
                if (fabs(pdg[i]) == 411 && fabs(mother[i]) == 10413) std::cout << " m_alltrkP4:  " << m_p4_alltrk[i][3] << std::endl;
            }
        }
        idxmc = pdg.size();
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
        if (mode!=200) continue; // mode = 200 includes: D+->K-pi+pi+ or D-->K+pi-pi-

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
        if (fabs((*dtag_iter)->mass() - mDcand) > 0.07) {
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
        for (int j = 0; j < n_trkD; j++) {
            RecMdcKalTrack* KalTrk = Dtrks[j]->mdcKalTrack();
            // to fill Kaon candidates
            if (j == 0) { // default arrangement: (K,pi), number of K depend on the mode you choose
                KalTrk->setPidType(RecMdcKalTrack::kaon);
                if (m_debug) std::cout << " filling kaon track " << std::endl;
                vwtrkpara_charge.push_back(WTrackParameter(mass[3], KalTrk->getZHelixK(), KalTrk->getZErrorK()));
                for (int k = 0; k < 4; k++) m_rawp4_Dtrk[j][k] = KalTrk->p4(mass[3])[k]; // MDC gives three momentum, combined with mass, we can get energy which means four momentum
            }
            // to fill Pion candidates
            else {
                KalTrk->setPidType(RecMdcKalTrack::pion);
                if (m_debug) std::cout << " filling pion track " << std::endl;
                vwtrkpara_charge.push_back(WTrackParameter(mass[2], KalTrk->getZHelix(), KalTrk->getZError()));
                for (int k = 0; k < 4; k++) m_rawp4_Dtrk[j][k] = KalTrk->p4(mass[2])[k];
            }
        }

        // to check the vector in each dtag item
        if (m_debug) {
            double index_vector=0;
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

        vwtrkpara_photon.clear(); // for mode ee->DDpipi, there is no pi0, so the vector will be empty
        for(int j = 0; j < Dshws.size(); j++) {
            RecEmcShower *gTrk = Dshws[j]->emcShower();
            Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
            Hep3Vector Gm_Mom = Gm_Vec - birth.vx(); // vx: Vertex, we regard that the track of the gamma before it enters EMC is a line, so to get the info of this line, we can just subtract the vertex info from the EMC hit point
            Gm_Mom.setMag(gTrk->energy());
            HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
            vwtrkpara_photon.push_back( WTrackParameter(gTrk->position(), Gm_p4, gTrk->dphi(), gTrk->dtheta(), gTrk->dE())); // dE, error of the gamma energy
            for (int k = 0; k < 4; k++) m_rawp4_Dshw[j][k] = Gm_p4[k];
        }

        // to check the vector in each dtag item
        if (m_debug) {
            double index_vector=0;
            std::cout << "total neutral: " << vwtrkpara_photon.size() << std::endl;
            while(index_vector < vwtrkpara_photon.size()) {
                std::cout << " Add neutral tracks: " << index_vector 
                << " with momentum: " << vwtrkpara_photon[index_vector].p() << std::endl;
                index_vector++;
            }
        }

        // KM fit on the D candidate
        chi2_kf = fitKM(vwtrkpara_charge, vwtrkpara_photon, birth);

        // to store the other track information
        stat_saveOthertrks = saveOthertrks();

        // to store the other showers information
        stat_saveOthershws = saveOthershws();

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

    if (m_debug) std::cout << " finished KF add Tracks ... " << std::endl;

    double kf_chi2 = 999;
    kmfit->AddResonance(0, mDcand, D1list);
    for (int i = 0; i < (Pi0list.size()/2); i++) kmfit->AddResonance(i + 1, M_Pi0, n_trkD + i*2, n_trkD + i*2 + 1); // the last two variales: two gamma tracks

    if (!kmfit->Fit(0)) return 999;
    if (!kmfit->Fit()) return 999;
    else {
        kf_chi2 = kmfit->chisq()/(1 + Pi0list.size()/2); // chi2/ndf, 1: constration of mD, Pi0list.size()/2: constration of Pi0
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

bool DDecayAlg::saveOthertrks() {
    SmartRefVector<EvtRecTrack> othertracks = (*dtag_iter)->otherTracks();
    SmartDataPtr<EvtRecEvent> evtRecEvent(eventSvc(), "/Event/EvtRec/EvtRecEvent");
    if (m_debug) std::cout << " total charged tracks : " << evtRecEvent->totalCharged() << std::endl;
    if (m_debug) std::cout << " other track number : " << othertracks.size() << " for mode " << mode << std::endl;
    DTagTool dtagTool;
    m_n_othertrks = 0;
    // to find the good pions
    for (int i = 0; i < othertracks.size(); i++) {
        if (!(dtagTool.isGoodTrack(othertracks[i]))) continue;
        if (dtagTool.isPion(othertracks[i])) {
            RecMdcTrack *mdcTrk = othertracks[i]->mdcTrack();
            RecMdcKalTrack *mdcKalTrk = othertracks[i]->mdcKalTrack();
            mdcKalTrk->setPidType(RecMdcKalTrack::pion);
            for (int j = 0; j < 4; j++) {
                m_rawp4_otherMdctrk[m_n_othertrks][j] = mdcTrk->p4(mass[2])[j];
                m_rawp4_otherMdcKaltrk[m_n_othertrks][j] = mdcKalTrk->p4(mass[2])[j];
            }
            m_rawp4_otherMdctrk[m_n_othertrks][4] = mdcTrk->chi2();
            m_rawp4_otherMdctrk[m_n_othertrks][5] = mdcTrk->stat(); // stat: status
            charge_otherMdctrk = mdcTrk->charge();
            m_rawp4_otherMdcKaltrk[m_n_othertrks][4] = mdcKalTrk->charge();
            m_rawp4_otherMdcKaltrk[m_n_othertrks][5] = 2;
        }
        if (dtagTool.isKaon(othertracks[i])) {
            RecMdcKalTrack *mdcKalTrk = othertracks[i]->mdcKalTrack();
            mdcKalTrk->setPidType(RecMdcKalTrack::kaon);
            for (int j = 0; j < 4; j++) m_rawp4_otherMdcKaltrk[m_n_othertrks][j] = mdcKalTrk->p4(mass[3])[j];
            m_rawp4_otherMdcKaltrk[m_n_othertrks][4] = mdcKalTrk->charge();
            m_rawp4_otherMdcKaltrk[m_n_othertrks][5] = 3;
        }
        m_n_othertrks++;
        if (m_n_othertrks >= 20) return false;
    }
    if (m_debug) std::cout << " recorded " << m_n_othertrks << " other charged good tracks " << std::endl;
    if (m_n_othertrks >= 20) return false;
    else return true;
}

bool DDecayAlg::saveOthershws() {
    SmartRefVector<EvtRecTrack> othershowers = (*dtag_iter)->otherShowers();
    SmartDataPtr<EvtRecEvent> evtRecEvent(eventSvc(), "/Event/EvtRec/EvtRecEvent");
    if (m_debug) std::cout << " total showers : " << evtRecEvent->totalNeutral() <<endl;
    if (m_debug) std::cout << " other shower numbers : " << othershowers.size() << " for mode " << mode << std::endl;
    DTagTool dtagTool;
    m_n_othershws = 0;
    // to find the good photons in the othershowers list
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
    }
    if (m_debug) std::cout << " recorded " << m_n_othershws << " other good showers " << std::endl;
    if (m_n_othershws >= 50) return false;
    else return true;
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
    m_charge_otherMdctrk = charge_otherMdctrk;
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
