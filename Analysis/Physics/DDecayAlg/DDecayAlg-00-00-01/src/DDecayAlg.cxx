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
        declareProperty("Debug", m_debug = true);
}

StatusCode DDecayAlg::initialize() {
    MsgStream log(msgSvc(), name());
    log << MSG::INFO << ">>>>>>> in initialize()" << endmsg;

    StatusCode status;

    NTuplePtr nt(ntupleSvc(), "FILE1/STD");
    if (nt) m_tuple = nt;
    else {
        m_tuple = ntupleSvc()->book("FILE1/STD", CLID_ColumnWiseTuple, "Single tag D decay");
        if (m_tuple) {
            status = m_tuple->addItem("run", m_runNo);
            status = m_tuple->addItem("evt", m_evtNo);
            status = m_tuple->addItem("flag1", m_flag1);
            status = m_tuple->addItem("beamE", m_beamE);
            status = m_tuple->addItem("ntrkD", m_n_trkD, 0, 5); // number of members should locates in 0~5
            status = m_tuple->addIndexedItem("DtrkP4_raw", m_n_trkD, 4, m_rawp4_Dtrk); // four members array
            status = m_tuple->addIndexedItem("DtrkP4", m_n_trkD, 4, m_p4_Dtrk);
            status = m_tuple->addItem("nshwD", m_n_shwD, 0, 2); 
            status = m_tuple->addIndexedItem("DshwP4_raw", m_n_shwD, 4, m_rawp4_Dshw);
            status = m_tuple->addIndexedItem("DshwP4", m_n_shwD, 4, m_p4_Dshw);
            status = m_tuple->addItem("decay mode", m_mode);
            status = m_tuple->addItem("type of charm quark", m_charm);
            status = m_tuple->addItem("chi2 of vertex fit", m_chi2_vf);
            status = m_tuple->addItem("chi2 of kinematic fit", m_chi2_kf);
            status = m_tuple->addItem("number of other tracks", m_n_othertrks, 0, 20);
            status = m_tuple->addIndexedItem("otherMdcTrkP4_raw", m_n_othertrks, 6, m_rawp4_otherMdctrk);
            status = m_tuple->addIndexedItem("otherMdcKalTrkP4_raw", m_n_othertrks, 6, m_rawp4_otherMdcKaltrk);
            status = m_tuple->addItem("number of other showers", m_n_othershws, 0, 50);
            status = m_tuple->addIndexedItem("otherShwP4_raw", m_n_othershws, 4, m_rawp4_othershw);
            status = m_tuple->addItem("Multi-counting D in one event", m_n_count);

            if (m_isMonteCarlo) {
                status = m_tuple->addItem("indexmc", m_idxmc, 0, 100);
                status = m_tuple->addIndexedItem("pdgid", m_idxmc, m_pdgid);
                status = m_tuple->addIndexedItem("motheridx", m_idxmc, m_motheridx);
                status = m_tuple->addIndexedItem("alltrkP4", m_idxmc, 4, m_p4_alltrk);
            }
        }
        else {
            log << MSG::ERROR << "Cannot book N-tuple:" << long(m_tuple) << endmsg;
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

    // get beam energy
    getBeamEnergy();

    // record all McTruth info
    if (runNo < 0 && m_isMonteCarlo) stat_McTruth = saveMcTruthInfo();
    if (runNo < 0 && stat_McTruth == false) std::cout << "There are some errors when recording McTruth Info in event: " << evtNo << std::endl;

    // use DTagTool
    stat_DTagTool = useDTagTool();
    if (stat_DTagTool == false) std::cout << "Please check chi2_vf/kf, other trks/shws or no wanted D in run, event: " << runNo << ", " << evtNo << std::endl;

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
    beam_energy = -999;

    // McTruth info
    for (int i = 0; i < 100; i++) {
        pdgid[i] = 0;
        motheridx[i] = 0;
        for (int j = 0; j < 4; j++) {
            p4_alltrk[i][j] = -999;
        }
    }
    idxmc = 0;
    for (int i = 0; i < 100; i++) {
        m_pdgid[i] = 0;
        m_motheridx[i] = 0;
        for (int j = 0; j < 4; j++) {
            m_p4_alltrk[i][j] = -999;
        }
    }
    m_idxmc = 0;
    pAll.clear();
    pdg.clear();
    mother.clear();

    // single D tag
    m_n_trkD = 0;
    n_trkD = 0;
    m_n_shwD = 0;
    n_shwD = 0;
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 4; j++) {
            m_rawp4_Dtrk[i][j] = -999;
            m_p4_Dtrk[i][j] = -999;
            rawp4_Dtrk[i][j] = -999;
            p4_Dtrk[i][j] = -999;
        }
    }
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 4; j++) {
            m_rawp4_Dshw[i][j] = -999;
            rawp4_Dshw[i][j] = -999;
            m_p4_Dshw[i][j] = -999;
            p4_Dshw[i][j] = -999;
        }
    }
    MODE = -999;
    mode = -999;
    m_mode = -999;
    charm = -999;
    m_charm = -999;
    chi2_vf = -999;
    m_chi2_vf = -999;
    chi2_kf = -999;
    m_chi2_kf = -999;
    n_othertrks = 0;
    m_n_othertrks = 0;
    mDcand = 0;
    for (int i = 0; i < 20; i++) {
        for (int j = 0; j < 6; j++) {
            rawp4_otherMdctrk[i][j] = -999;
            rawp4_otherMdcKaltrk[i][j] = -999;
            m_rawp4_otherMdctrk[i][j] = -999;
            m_rawp4_otherMdcKaltrk[i][j] = -999;
        }
    }
    n_othershws = 0;
    m_n_othershws = 0;
    for (int i = 0; i < 50; i++) {
        for (int j = 0; j < 4; j++) {
            rawp4_othershw[i][j] = -999;
            m_rawp4_othershw[i][j] = -999;
        }
    }
    n_count = 0;
    m_n_count = 0;

    // judgement variables
    stat_McTruth = false;
    stat_DTagTool = false;
    stat_tagSD = false;
    stat_saveCandD = false;
    stat_saveOthertrks = false;
    stat_saveOthershws = false;
}

void DDecayAlg::getBeamEnergy() {
    if (runNo > 0) {
        char stmt[400];
        snprintf(stmt, 1024,
                "select BER_PRB, BPR_PRB"
                "from RunParams where run_number = %d", runNo);
        DatabaseRecordVector res;
        IDatabaseSvc* dbsvc;
        // read database use service
        Gaudi::svcLocator()->service("DatabaseSvc", dbsvc, true); // ?????????????????
        int row_no = dbsvc->query("run", stmt, res); // ????????????????
        if (row_no != 0) {
            DatabaseRecord* records = res[0];
            double E_E = 0, E_P = 0;
            E_E = records->GetDouble("BER_PRB");
            E_P = records->GetDouble("BPR_PRB");
            beam_energy = E_E + E_P;
        }
    }
    else {
        beam_energy = -1;
    }
    if (m_debug) std::cout << " beam energy " << beam_energy << std::endl;
}

bool DDecayAlg::saveMcTruthInfo() {
    SmartDataPtr<Event::McParticleCol> mcParticleCol(eventSvc(), "/Event/MC/McParticleCol");
    if (!mcParticleCol) {
        std::cout << "Could not retreive McParticleCol" << std::endl;
        return false;
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
            p4_alltrk[i][0] = pAll[i].px();
            p4_alltrk[i][1] = pAll[i].py();
            p4_alltrk[i][2] = pAll[i].pz();
            p4_alltrk[i][3] = pAll[i].e();
            if (m_debug) {
                if (fabs(pdg[i]) == 411 && fabs(mother[i]) == 10413) std::cout << " m_alltrkP4:  " << p4_alltrk[i][3] << std::endl;
            }
        }
        idxmc = pdg.size();
        if (m_debug) std::cout << " PDG.SIZE():  " << idxmc << std::endl;
    }
    return true;
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
                for (int k = 0; k < 4; k++) rawp4_Dtrk[j][k] = KalTrk->p4(mass[3])[k]; // MDC gives three momentum, combined with mass, we can get energy which means four momentum
            }
            // to fill Pion candidates
            else {
                KalTrk->setPidType(RecMdcKalTrack::pion);
                if (m_debug) std::cout << " filling pion track " << std::endl;
                vwtrkpara_charge.push_back(WTrackParameter(mass[2], KalTrk->getZHelix(), KalTrk->getZError()));
                for (int k = 0; k < 4; k++) rawp4_Dtrk[j][k] = KalTrk->p4(mass[2])[k];
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
            for (int k = 0; k < 4; k++) rawp4_Dshw[j][k] = Gm_p4[k];
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
            recordVariables();
            n_count++;
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
            for (int j = 0; j < 4; j++) p4_Dtrk[i][j] = kmfit->pfit(i)[j];
        }
        if (m_debug) std::cout << " fill D1trkP4 successfully for mode !!! " << mode << std::endl;
        for (int i = 0; i < n_shwD; i++) {
            for (int j = 0; j < 4; j++) p4_Dshw[i][j] = kmfit->pfit(i + n_trkD)[j];
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
    // to find the good pions
    for (int i = 0; i < othertracks.size(); i++) {
        if (!(dtagTool.isGoodTrack(othertracks[i]))) continue;
        if (dtagTool.isPion(othertracks[i])) {
            RecMdcTrack *mdcTrk = othertracks[i]->mdcTrack();
            RecMdcKalTrack *mdcKalTrk = othertracks[i]->mdcKalTrack();
            mdcKalTrk->setPidType(RecMdcKalTrack::pion);
            for (int j = 0; j < 4; j++) {
                rawp4_otherMdctrk[i][j] = mdcTrk->p4(mass[2])[j];
                rawp4_otherMdcKaltrk[i][j] = mdcKalTrk->p4(mass[2])[j];
            }
            rawp4_otherMdctrk[i][4] = mdcTrk->chi2();
            rawp4_otherMdctrk[i][5] = mdcTrk->stat(); // stat: status
            rawp4_otherMdcKaltrk[i][4] = mdcKalTrk->charge();
            rawp4_otherMdcKaltrk[i][5] = 2;
        }
        if (dtagTool.isKaon(othertracks[i])) {
            RecMdcKalTrack *mdcKalTrk = othertracks[i]->mdcKalTrack();
            mdcKalTrk->setPidType(RecMdcKalTrack::kaon);
            for (int j = 0; j < 4; j++) rawp4_otherMdcKaltrk[i][j] = mdcKalTrk->p4(mass[3])[j];
            rawp4_otherMdcKaltrk[i][4] = mdcKalTrk->charge();
            rawp4_otherMdcKaltrk[i][5] = 3;
        }
        n_othertrks++;
        if (n_othertrks >= 20) return false;
    }
    if (m_debug) std::cout << " recorded " << n_othertrks << " other charged good tracks " << std::endl;
    if (n_othertrks >= 20) return false;
    else return true;
}

bool DDecayAlg::saveOthershws() {
    SmartRefVector<EvtRecTrack> othershowers = (*dtag_iter)->otherShowers();
    SmartDataPtr<EvtRecEvent> evtRecEvent(eventSvc(), "/Event/EvtRec/EvtRecEvent");
    if (m_debug) std::cout << " total showers : " << evtRecEvent->totalNeutral() <<endl;
    if (m_debug) std::cout << " other shower numbers : " << othershowers.size() << " for mode " << mode << std::endl;
    DTagTool dtagTool;
    // to find the good photons in the othershowers list
    for (int i = 0; i < othershowers.size(); i++) {
        if (!(dtagTool.isGoodShower(othershowers[i]))) continue;
        RecEmcShower *gTrk = othershowers[i]->emcShower();
        Hep3Vector Gm_Vec(gTrk->x(), gTrk->y(), gTrk->z());
        Hep3Vector Gm_Mom = Gm_Vec - birth.vx();
        Gm_Mom.setMag(gTrk->energy());
        HepLorentzVector Gm_p4(Gm_Mom, gTrk->energy());
        for (int j = 0; j < 4; j++) rawp4_othershw[i][j] = Gm_p4[j];
        n_othershws++;
        if (n_othershws >= 50) return false;
    }
    if (m_debug) std::cout << " recorded " << n_othershws << " other good showers " << std::endl;
    if (n_othershws >= 50) return false;
    else return true;
}

void DDecayAlg::recordVariables() {
    m_runNo = runNo;
    m_evtNo = evtNo;
    m_flag1 = flag1;
    m_beamE = beam_energy;

    // save McTruth info
    m_idxmc = idxmc;
    for (int i = 0; i < m_idxmc; i++) {
        m_pdgid[i] = pdgid[i];
        m_motheridx[i] = motheridx[i];
        for (int j = 0; j < 4; j++) {
            m_p4_alltrk[i][j] = p4_alltrk[i][j];
        }
    }

    // save DTag info
    m_n_trkD = n_trkD;
    for (int i = 0; i < m_n_trkD; i++) {
        for (int j = 0; j < 4; j++) m_rawp4_Dtrk[i][j] = rawp4_Dtrk[i][j];
        for (int j = 0; j < 4; j++) m_p4_Dtrk[i][j] = p4_Dtrk[i][j];
    }
    m_n_shwD = n_shwD;
    for (int i = 0; i < m_n_shwD; i++) {
        for (int j = 0; j < 4; j++) m_rawp4_Dshw[i][j] = rawp4_Dshw[i][j];
        for (int j = 0; j < 4; j++) m_p4_Dshw[i][j] = p4_Dshw[i][j];
    }
    m_mode = MODE;
    m_charm = charm;
    m_chi2_vf = chi2_vf;
    m_chi2_kf = chi2_kf;
    m_n_othertrks = n_othertrks;
    for (int i = 0; i < m_n_othertrks; i++) {
        for (int j = 0; j < 6; j++) m_rawp4_otherMdctrk[i][j] = m_rawp4_otherMdctrk[i][j];
        for (int j = 0; j < 6; j++) m_rawp4_otherMdcKaltrk[i][j] = m_rawp4_otherMdcKaltrk[i][j];
    }
    m_n_othershws = n_othershws;
    for (int i = 0; i < m_n_othershws; i++) {
        for (int j = 0; j < 4; j++) m_rawp4_othershw[i][j] = m_rawp4_othershw[i][j];
    }
    m_n_count = n_count;

    m_tuple->write();

    if (m_debug) std::cout << " entry in ntuple is filled for " << mode << std::endl;
}
