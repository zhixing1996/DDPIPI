#include <iostream>
#include <fstream>
#include "TFile.h"
#include "TH1F.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include <cmath>
#include "TString.h"
using namespace std;

Double_t BW(Double_t m, Double_t M, Double_t G) {
    double s = pow(m, 2);
    double bw = 1/(pow((s-M*M),2) + M*M*G*G);
    return bw;
}

Double_t num_sim(Double_t m, TH1F *h_in) {
    // when mass=m, find the bin number at this time
    Int_t bin = h_in->FindBin(m);
    // return this bin's event number, when find this bin
    return h_in->GetBinContent(bin);
}

void get_sideband_hist() {

    TFile *file_in = new TFile("/scratchfs/bes/jingmq/bes/DDPIPI/v0.1/sigMC/D1_2420/4420/rootfile/ana_Sig_D1_2420_D_PHSP_4420_0.root", "READ");
    TTree *t1 = (TTree*)file_in->Get("STD");
    TTree *t2 = (TTree*)file_in->Get("otherTrk");
    TTree *t3 = (TTree*)file_in->Get("DststTruth");

    Int_t mode, ntrkD;
    Double_t DtrkP4[5][4], KFchi2;
    t1->SetBranchAddress("mode", &mode);
    t1->SetBranchAddress("n_trkD", &ntrkD);
    t1->SetBranchAddress("p4_Dtrk", DtrkP4);
    t1->SetBranchAddress("chi2_kf", &KFchi2);

    Int_t nothertrks;
    Double_t otherKalTrkP4raw[20][6];
    t2->SetBranchAddress("n_othertrks", &nothertrks);
    t2->SetBranchAddress("rawp4_otherMdcKaltrk", otherKalTrkP4raw);

    Double_t p4_Dstst[4];
    t3->SetBranchAddress("p4_Dstst", p4_Dstst);

    TFile file_out("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sicdband_hist_4420.root","RECREATE");
    TH1F *h_mDstst = new TH1F("h_mDstst", "h_mDstst", 200, 2.1, 2.75);
    TH1F *h_[500][500];

    Double_t rmD,rmDpipi;
    TLorentzVector cms(0.011*4.415, 0, 0, 4.415);

    // get mass of Dstst MC Truth
    for (Int_t i = 0; i < t3->GetEntries(); i++) {
        t3->GetEntry(i);
        TLorentzVector Dstst(0, 0, 0, 0);
        Dstst.SetPxPyPzE(p4_Dstst[0], p4_Dstst[1], p4_Dstst[2], p4_Dstst[3]);
        Double_t mDstst;
        mDstst = Dstst.M();
        // get the initial Dstst histogram from MC truth
        h_mDstst->Fill(mDstst);
    }

    // MC information
    Int_t nentries = t1->GetEntries();
    for(Int_t i = 0; i < 80; i++) {
        for(Int_t j = 0; j < 20; j++) {
            char  hname[50];
            sprintf(hname, "h_%d_%d", i, j);
	        // get mass Scan and width Scan point
            h_[i][j] = new TH1F(hname, "", 200, 2.1, 2.75);
            Double_t mass, width;
            mass = 2.4240 + 0.0001*i;
            width = 0.018 + 0.001*j;
            for(Int_t k = 0; k < nentries; k++) {
                t1->GetEntry(k);
                t2->GetEntry(k);
                t3->GetEntry(k);
                if (mode!=200) continue;
                TLorentzVector Dstst(0,0,0,0);
                Double_t mDstst;
                Dstst.SetPxPyPzE(p4_Dstst[0], p4_Dstst[1], p4_Dstst[2], p4_Dstst[3]);
                mDstst = Dstst.M();
		        // when mass=Dstst_th, get the event number in h_mZ(MCtruth)
                Double_t w1 = num_sim(mDstst, h_mDstst);
		        // build the relativistic Breit-wigner distribution 
		        // when D**=mass the probability of BW-PDF is maxium
                Double_t w2 = BW(mDstst, mass, width);
		        // define the wight
                if (w1 < 0.000001) continue;
                double wight = w2/w1;
                TLorentzVector pD(0,0,0,0);
                for (Int_t m = 0; m < ntrkD; m++) {
                    TLorentzVector  ptrack(0,0,0,0);
                    ptrack.SetPxPyPzE(DtrkP4[m][0], DtrkP4[m][1], DtrkP4[m][2], DtrkP4[m][3]);
                    pD += ptrack;
                }
                rmD = (cms-pD).M();
                TLorentzVector pPip(0, 0, 0, 0);
                TLorentzVector pPim(0, 0, 0, 0);
                for (Int_t m = 0; m < nothertrks; m++) {
                    if (otherKalTrkP4raw[m][4] != 1) continue;
                    if (otherKalTrkP4raw[m][5] != 2) continue;
                    pPip.SetPxPyPzE(otherKalTrkP4raw[m][0], otherKalTrkP4raw[m][1], otherKalTrkP4raw[m][2], otherKalTrkP4raw[m][3]);
                    for (Int_t n = 0; n < nothertrks; n++) {
                        if (otherKalTrkP4raw[n][4] != -1) continue;
                        if (otherKalTrkP4raw[n][5] != 2) continue;
                        pPim.SetPxPyPzE(otherKalTrkP4raw[n][0], otherKalTrkP4raw[n][1], otherKalTrkP4raw[n][2], otherKalTrkP4raw[n][3]);
                        rmDpipi = (cms-pD-pPip-pPim).M();
                        if (KFchi2 > 20) continue;
                        if ( !( ( (rmDpipi > 1.786 && rmDpipi < 1.84) || (rmDpipi > 1.897 && rmDpipi < 1.951) ) ) ) continue;
                        h_[i][j]->Fill(rmD,wight);
                    }
                }
            }
            h_[i][j]->Write();
        }
    }

}
