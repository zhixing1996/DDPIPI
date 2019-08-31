#include <iostream>
#include <fstream>
#include "TFile.h"
#include "TStyle.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TLorentzVector.h"
#include "TClonesArray.h"
#include <cmath>
#include <iomanip>
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TGraph2DErrors.h"

void get_width() {
	// do not display any of the standard histogram decorations
	gStyle->SetOptTitle(0);
	gStyle->SetOptStat(0);
	gStyle->SetOptFit(0);
	gStyle->SetPadColor(0);
	// put tick marks on top and RHS of plots
	gStyle->SetPadTickX(1);
	gStyle->SetPadTickY(1);
	gStyle->SetCanvasColor(0);

	TFile *f = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/simufit_results.root", "READ");
	TTree *t = (TTree*)f->Get("save");

	Double_t likelihood = 0;
	Double_t mass2420 = 0;
	Double_t width2420 = 0;

	t->SetBranchAddress("likelihood", &likelihood);
	t->SetBranchAddress("mass2420", &mass2420);
	t->SetBranchAddress("width2420", &width2420);

	Int_t  nentries = t->GetEntries();

	Double_t width[20];
	for (Int_t i = 0; i < 20; i++) width[i] = 0.018 + 0.001*i;
	Double_t likemax = 1.000;

	TGraph *gr = new TGraph(20);
	for (Int_t i = 0; i < 20; i++) {
		Double_t likemini = 1.000;
		for(Int_t j = 0; j < nentries; j++) {
			t->GetEntry(j);
			if (fabs(width2420 - width[i]) > 0.000001) continue;
			if (likelihood > likemini) continue;
			likemini = likelihood;
		}
		if (likemax < likemini) continue;
		likemax = likemini;
	}

	for (Int_t i = 0; i < 20; i++) {
		Double_t likemini=1.000;
		for(Int_t j = 0; j < nentries; j++) {
			t->GetEntry(j);
			if (fabs(width2420 - width[i]) > 0.000001) continue;
			if (likelihood > likemini) continue;
			likemini = likelihood;
		}
		Double_t delta = likemini - likemax;
		gr->SetPoint(i, width[i], delta);
	}

	TF1 *fun = new TF1("fun", "([0]*(x-[1])*(x-[1]))", 0.0205, 0.029);
	fun->SetParameters(0, 100);
	fun->SetParameters(1, 0.025);

	TCanvas *myc = new TCanvas("myc", "myc", 800, 600);
	myc->cd();

	TH2F *h = new TH2F("h", "h", 400, 0.018, 0.0382, 100, -1, 12);
	h->SetStats(kFALSE);
	h->GetXaxis()->SetTitleSize(0.035);
	h->GetXaxis()->SetTitleOffset(1.12);
	h->GetXaxis()->SetLabelOffset(0.01);
	h->GetYaxis()->SetTitleSize(0.035);
	h->GetYaxis()->SetTitleOffset(1);
	h->GetYaxis()->SetLabelOffset(0.01);
	h->SetTitle("");
	h->SetMarkerSize(1);
	h->SetMarkerStyle(20);
	h->GetXaxis()->SetTitle("Width(GeV/c^{2})");
	h->GetYaxis()->SetTitle("#Delta(-lnL)");
	h->Draw(); 
	fun->SetLineColor(kRed);
	gr->Fit("fun","FR");
	gr->SetMarkerStyle(7);
	gr->SetMarkerSize(0.7);
	gr->Draw("P");
    cout << "The wanted width is : " << fun->GetParameter(1) << " +/- " << fabs(fun->GetX(0.5) - fun->GetParameter(1)) << endl;
    cout << "The selected mass is : " << ceil((fun->GetParameter(1) - 0.018)/0.001) << endl;

}
