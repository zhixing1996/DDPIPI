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

void get_background_shape_histpdf() {

    gSystem->Load("libRooFit");

	double xmin = 2.0;
	double xmax = 2.8;
    int xbin = 80;
    TCut cut;
	RooRealVar rmD("rm_D", "rm_D", xmin, xmax);
    TFile *file_sideband_4360 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected_sideband.root");
    TFile *file_sideband_4420 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected_sideband.root");
    TFile *file_sideband_4600 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected_sideband.root");
    TTree *t_sideband_4360 = (TTree*)file_sideband_4360->Get("save");
    TTree *t_sideband_4420 = (TTree*)file_sideband_4420->Get("save");
    TTree *t_sideband_4600 = (TTree*)file_sideband_4600->Get("save");
	TFile *f = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/sideband/bakground_shape_histpdf.root","recreate");

    TH1F *h_sideband_4360 = new TH1F("h_sideband_4360", "", xbin, xmin, xmax);
    TH1F *h_sideband_4420 = new TH1F("h_sideband_4420", "", xbin, xmin, xmax);
    TH1F *h_sideband_4600 = new TH1F("h_sideband_4600", "", xbin, xmin, xmax);

    t_sideband_4360->Project("h_sideband_4360", "rm_D", cut);
    t_sideband_4420->Project("h_sideband_4420", "rm_D", cut);
    t_sideband_4600->Project("h_sideband_4600", "rm_D", cut);

    RooDataHist* set_sideband_4360 = new RooDataHist("set_sideband_4360", "set_sideband_4360", rmD, h_sideband_4360);
    RooDataHist* set_sideband_4420 = new RooDataHist("set_sideband_4420", "set_sideband_4420", rmD, h_sideband_4420);
    RooDataHist* set_sideband_4600 = new RooDataHist("set_sideband_4600", "set_sideband_4600", rmD, h_sideband_4600);
		
    RooHistPdf pdf_sideband_4360("pdf_sideband_4360", "pdf_sideband_4360", rmD, *set_sideband_4360, 0);
    RooHistPdf pdf_sideband_4420("pdf_sideband_4420", "pdf_sideband_4420", rmD, *set_sideband_4420, 0);
    RooHistPdf pdf_sideband_4600("pdf_sideband_4600", "pdf_sideband_4600", rmD, *set_sideband_4600, 0);

	pdf_sideband_4360.Write();
	pdf_sideband_4420.Write();
	pdf_sideband_4600.Write();

}
