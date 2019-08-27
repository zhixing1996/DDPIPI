#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
#include "TStyle.h"
#include "TROOT.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TFile.h"
#include "TCut.h"
#include "TSystem.h"
#include "RooFit.h"
#include "RooGenericPdf.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooHist.h"
#include "RooHistPdf.h"
#include "RooArgSet.h"
#include "RooFitResult.h"
#include "RooChebychev.h"
#include "RooPolynomial.h"
#include "RooChi2Var.h"
#include "RooPlot.h"
#include "RooGaussModel.h"
#include "RooBifurGauss.h"
#include "RooExponential.h"
#include "RooBukinPdf.h"
#include "RooFFTConvPdf.h"
#include "RooNumConvPdf.h"
#include "RooKeysPdf.h"
#include "RooAddPdf.h"
#include "RooExtendPdf.h"
#include "iostream"
#include "RooAbsPdf.h"
#include "RooPolynomial.h"
#include "iostream"
#include "fstream"
#include "RooAddition.h"
#include <iomanip>
using namespace std;
using namespace RooFit;

void fit_rmD_4360() {

    // do not display any of the standard histogram decorations
    gStyle->SetOptTitle(0);
    gStyle->SetOptStat(0);
    gStyle->SetOptFit(0);
    gStyle->SetPadColor(0);
    // put tick marks on top and RHS of plots
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    gStyle->SetCanvasColor(0);

    double xmin = 1.7;
    double xmax = 1.97;
    int xbin = 100;
    
    RooRealVar rmD("rm_D", "rm_D", xmin, xmax);
    RooRealVar nSig("nSig", "nSig", 2050, 0, 100000);
    RooRealVar nBkg("nBkg", "nBkg", 3900, 0, 100000);
    
    TFile *file_data = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_control.root", "READ");
    TFile *file_sig = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/controlMC/DD/4360/controlMC_DD_4360.root", "READ");
    
    TTree *t_data = (TTree*)file_data->Get("save");
    TTree *t_sig = (TTree*)file_sig->Get("save");
    
    TH1F *h_sig = new TH1F("h_sig", "", xbin, xmin, xmax);
    TCut cut;
    t_sig->Project("h_sig", "rm_D", cut);
    
    RooDataSet* set_data = new RooDataSet("set_data", "set_data", t_data, rmD);	
    RooDataHist* hist_sig = new RooDataHist("hist_sig", "hist_sig", rmD, h_sig);
    
    // Poly nomial function
    RooRealVar co1("co1", "co1", -3.96, -10, 100);
    RooRealVar co2("co2", "co2", 2.15, -10, 100);
    RooPolynomial pdf_bkg("pdf_bkg", "Background", rmD, RooArgList(co1,co2));
    
    // set model for FIT
    RooHistPdf pdf_sig("pdf_sig", "pdf_sig", rmD, *hist_sig, 0);
    RooRealVar mean("mean", "mean", 0.0004, -0.1, 0.5);
    RooRealVar sigma("sigma", "sigma", 0.0015, 0, 0.01);
    RooGaussian gauss("gauss", "gauss", rmD, mean, sigma);
    RooFFTConvPdf Covpdf("Covpdf", "pdf_sig (X) gauss", rmD, pdf_sig, gauss); 
    
    RooAddPdf  model("model","model",RooArgList(Covpdf,pdf_bkg),RooArgList(nSig,nBkg));

    rmD.setBins(1000, "cache");
    model.fitTo(*set_data, Extended());
    
    // create TCanvas
    TCanvas *canvas = new TCanvas("canvas", "", 800, 600);
    canvas->cd();
    RooPlot* xframe = rmD.frame(Bins(30), Range(xmin,xmax));
    set_data->plotOn(xframe, MarkerSize(1), LineWidth(2));
    model.plotOn(xframe, Components(Covpdf), LineColor(kRed), LineWidth(3), LineStyle(kDashed));
    model.plotOn(xframe, Components(pdf_bkg), LineColor(kBlue), LineWidth(3), LineStyle(kDashed));
    model.plotOn(xframe, LineColor(kBlack),LineWidth(3));
    
    xframe->GetXaxis()->SetTitleSize(0.05);
    xframe->GetXaxis()->SetTitleOffset(0.9);
    xframe->GetXaxis()->SetLabelOffset(0.01);
    xframe->GetYaxis()->SetTitleSize(0.05);
    xframe->GetYaxis()->SetTitleOffset(0.95);
    xframe->GetYaxis()->SetLabelOffset(0.01);
    xframe->GetXaxis()->SetTitle("RM(D^{+})(GeV/c^{2})");
    xframe->GetYaxis()->SetTitle("Events/(9MeV/c^{2})");
    xframe->Draw();

    cout << "Resolution: " << 2.36*sigma.getVal() << " +/- "<< 2.36*sigma.getError()<< endl;
    canvas->Print("fit_rmD_4360.pdf");

}
