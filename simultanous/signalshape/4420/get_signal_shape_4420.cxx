#include <iostream>
#include <fstream>
#include "TFile.h"
#include "TH1F.h"
#include "TF1.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include <cmath>
#include "TString.h"
using namespace std;

void get_signal_shape_4420() {

    TFile *fsignal = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/signal_hist_4420.root");
    TFile *fsideband = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sideband_hist_4420.root");
    TFile file_out("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/signal_shape_4420.root","RECREATE");

    TH1F  *hsignal[500][500];
    TH1F  *hsideband[500][500];
    TH1F  *h_shape_[500][500];
    char hname[50];

    for (int i = 0; i < 80; i++) {
        for (int j = 0; j < 20; j++) {
            sprintf(hname, "h_%d_%d", i, j);
            hsignal[i][j] = (TH1F*)fsignal->Get(hname);
            hsideband[i][j] = (TH1F*)fsideband->Get(hname);
            h_shape_[i][j] = new TH1F(hname, "", 200, 2.1, 2.75);
            h_shape_[i][j]->Add(hsignal[i][j], hsideband[i][j], 1, -0.25);
            h_shape_[i][j]->Write();
        }
    }

}
