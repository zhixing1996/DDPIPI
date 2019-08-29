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

void get_background_shape() {

    gSystem->Load("libRooFit");

	double xmin = 2.0;
	double xmax = 2.8;
	RooRealVar rmD("m_rm_D","m_rm_D", xmin, xmax) ;
	TChain *sideband_4360 = new TChain("save");
	TChain *sideband_4420 = new TChain("save");
	TChain *sideband_4600 = new TChain("save");
	sideband_4360->Add("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/sigMC_D1_2420_4360_selected_sideband.root");
	sideband_4420->Add("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/sigMC_D1_2420_4420_selected_sideband.root");
	sideband_4600->Add("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/sigMC_D1_2420_4600_selected_sideband.root");
	TFile *f = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/sideband/bakground_shape.root","recreate");
	
	RooDataSet* set_sideband_4360 = new RooDataSet("set_sideband_4360", "set_sideband_4360", sideband_4360, rmD);
    RooDataSet* set_sideband_4420 = new RooDataSet("set_sideband_4420", "set_sideband_4420", sideband_4420, rmD);
    RooDataSet* set_sideband_4600 = new RooDataSet("set_sideband_4600", "set_sideband_4600", sideband_4600, rmD);
		
	RooDataSet  *set_sideband_compact_4360 = (RooDataSet*)set_sideband_4360->reduce(RooArgSet(rmD), "m_rm_D>2.1 && m_rm_D<2.5");
	RooDataSet  *set_sideband_compact_4420 = (RooDataSet*)set_sideband_4420->reduce(RooArgSet(rmD), "m_rm_D>2.1 && m_rm_D<2.55");
	RooDataSet  *set_sideband_compact_4600 = (RooDataSet*)set_sideband_4600->reduce(RooArgSet(rmD), "m_rm_D>2.1 && m_rm_D<2.75");

	RooKeysPdf pdf_sideband_4360("pdf_sideband_4360", "", rmD, *set_sideband_compact_4360, RooKeysPdf::NoMirror, 2);
	RooKeysPdf pdf_sideband_4420("pdf_sideband_4420", "", rmD, *set_sideband_compact_4420, RooKeysPdf::NoMirror, 2);
	RooKeysPdf pdf_sideband_4600("pdf_sideband_4600", "", rmD, *set_sideband_compact_4600, RooKeysPdf::NoMirror, 2);

	pdf_sideband_4360.Write();
	pdf_sideband_4420.Write();
	pdf_sideband_4600.Write();

}
