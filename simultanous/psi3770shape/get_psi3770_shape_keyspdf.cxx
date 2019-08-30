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

void get_psi3770_shape_keyspdf() {

	double xmin = 2.0;
	double xmax = 2.8;
	RooRealVar rmD("rm_D", "rm_D", xmin, xmax);
	TChain *psi3770_4360 = new TChain("save");
	TChain *psi3770_4420 = new TChain("save");
	TChain *psi3770_4600 = new TChain("save");
	psi3770_4360->Add("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4360/sigMC_psi_3770_4360_selected_signal.root");
	psi3770_4420->Add("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4420/sigMC_psi_3770_4420_selected_signal.root");
	psi3770_4600->Add("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4600/sigMC_psi_3770_4600_selected_signal.root");
	TFile *f = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/psi3770shape/psi3770_shape_keyspdf.root","recreate");
	
	RooDataSet* set_psi3770_4360 = new RooDataSet("set_psi3770_4360", "set_psi3770_4360", psi3770_4360, rmD);
	RooDataSet* set_psi3770_4420 = new RooDataSet("set_psi3770_4420", "set_psi3770_4420", psi3770_4420, rmD);
	RooDataSet* set_psi3770_4600 = new RooDataSet("set_psi3770_4600", "set_psi3770_4600", psi3770_4600, rmD);

	RooDataSet  *set_psi3770_compact_4360 = (RooDataSet*)set_psi3770_4360->reduce(RooArgSet(rmD), "rm_D>2.1 && rm_D<2.5");
	RooDataSet  *set_psi3770_compact_4420 = (RooDataSet*)set_psi3770_4420->reduce(RooArgSet(rmD), "rm_D>2.1 && rm_D<2.55");
	RooDataSet  *set_psi3770_compact_4600 = (RooDataSet*)set_psi3770_4600->reduce(RooArgSet(rmD), "rm_D>2.1 && rm_D<2.75");

	RooKeysPdf pdf_psi3770_4360("pdf_psi3770_4360", "", rmD, *set_psi3770_compact_4360, RooKeysPdf::NoMirror, 2);
	RooKeysPdf pdf_psi3770_4420("pdf_psi3770_4420", "", rmD, *set_psi3770_compact_4420, RooKeysPdf::NoMirror, 2);
	RooKeysPdf pdf_psi3770_4600("pdf_psi3770_4600", "", rmD, *set_psi3770_compact_4600, RooKeysPdf::NoMirror, 2);

	pdf_psi3770_4360.Write();
	pdf_psi3770_4420.Write();
	pdf_psi3770_4600.Write();

}
