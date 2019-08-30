#include "iostream"
#include "fstream"
#include "RooAddition.h"
#include <iomanip>
#include "RooFit.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TString.h"
#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooDataHist.h"
#include "RooHist.h"
#include "RooHistPdf.h"
#include "RooFFTConvPdf.h"
#include "RooGaussModel.h"
#include <TBenchmark.h>
#include <TSystem.h>
#include "RooGaussian.h"
#include "TStyle.h"
using namespace std;

void get_psi3770_shape_histpdf() {

	double xmin = 2.0;
	double xmax = 2.8;
    int xbin = 80;
    TCut cut;
	RooRealVar rmD("rm_D", "rm_D", xmin, xmax);
    TFile *file_psi3770_4360 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4360/sigMC_psi_3770_4360_selected_signal.root", "READ");
    TFile *file_psi3770_4420 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4420/sigMC_psi_3770_4420_selected_signal.root", "READ");
    TFile *file_psi3770_4600 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4600/sigMC_psi_3770_4600_selected_signal.root", "READ");
    TTree *t_psi3770_4360 = (TTree*)file_psi3770_4360->Get("save");
    TTree *t_psi3770_4420 = (TTree*)file_psi3770_4420->Get("save");
    TTree *t_psi3770_4600 = (TTree*)file_psi3770_4600->Get("save");
	TFile *f = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/psi3770shape/psi3770_shape_histpdf.root","recreate");

    TH1F *h_psi3770_4360 = new TH1F("h_psi3770_4360", "", xbin, xmin, xmax);
    TH1F *h_psi3770_4420 = new TH1F("h_psi3770_4420", "", xbin, xmin, xmax);
    TH1F *h_psi3770_4600 = new TH1F("h_psi3770_4600", "", xbin, xmin, xmax);

    t_psi3770_4360->Project("h_psi3770_4360", "rm_D", cut);
    t_psi3770_4420->Project("h_psi3770_4420", "rm_D", cut);
    t_psi3770_4600->Project("h_psi3770_4600", "rm_D", cut);

    RooDataHist* set_psi3770_4360 = new RooDataHist("set_psi3770_4360", "set_psi3770_4360", rmD, h_psi3770_4360);
    RooDataHist* set_psi3770_4420 = new RooDataHist("set_psi3770_4420", "set_psi3770_4420", rmD, h_psi3770_4420);
    RooDataHist* set_psi3770_4600 = new RooDataHist("set_psi3770_4600", "set_psi3770_4600", rmD, h_psi3770_4600);

    RooHistPdf pdf_psi3770_4360("pdf_psi3770_4360", "pdf_psi3770_4360", rmD, *set_psi3770_4360, 0);
    RooHistPdf pdf_psi3770_4420("pdf_psi3770_4420", "pdf_psi3770_4420", rmD, *set_psi3770_4420, 0);
    RooHistPdf pdf_psi3770_4600("pdf_psi3770_4600", "pdf_psi3770_4600", rmD, *set_psi3770_4600, 0);

	pdf_psi3770_4360.Write();
	pdf_psi3770_4420.Write();
	pdf_psi3770_4600.Write();

}
