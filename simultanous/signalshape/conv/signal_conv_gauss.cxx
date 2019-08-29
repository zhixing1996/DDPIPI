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

void signal_conv_gauss() {

    gSystem->Load("libRooFit"); 

    double xmin=2.0;
    double xmax=2.8;
    RooRealVar rmD("rmD", "rmD", xmin, xmax) ;
    TFile *signal_shape_4360 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4360/signal_shape_4360.root","READ");
    TFile *signal_shape_4420 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4420/signal_shape_4420.root","READ");
    TFile *signal_shape_4600 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/4600/signal_shape_4600.root","READ");
    char hname[50];
    char pdf_4360[50];
    char pdf_4420[50];
    char pdf_4600[50];
    TH1F *h_2420_4360[500][500];
    TH1F *h_2420_4420[500][500];
    TH1F *h_2420_4600[500][500];
    TFile *f = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/conv/signal_conv_gauss.root","recreate");
    
    for(int i = 0; i < 80; i++) {
        for (int j = 0; j < 20; j++) {
            sprintf(hname, "h_%d_%d", i, j);
            sprintf(pdf_4360, "Covpdf_2420_4360_%d_%d", i, j);
            sprintf(pdf_4420, "Covpdf_2420_4420_%d_%d", i, j);
            sprintf(pdf_4600, "Covpdf_2420_4600_%d_%d", i, j);

            h_2420_4360[i][j] = (TH1F*)signal_shape_4360->Get(hname);
            h_2420_4420[i][j] = (TH1F*)signal_shape_4420->Get(hname);
            h_2420_4600[i][j] = (TH1F*)signal_shape_4600->Get(hname);

            RooDataHist* hist_2420_4360 = new RooDataHist("hist_2420_4360", "hist_2420_4360", rmD, h_2420_4360[i][j]);
            RooDataHist* hist_2420_4420 = new RooDataHist("hist_2420_4420", "hist_2420_4420", rmD, h_2420_4420[i][j]);
            RooDataHist* hist_2420_4600 = new RooDataHist("hist_2420_4600", "hist_2420_4600", rmD, h_2420_4600[i][j]);

            RooHistPdf pdf_2420_4360("pdf_2420_4360", "pdf_2420_4360", rmD, *hist_2420_4360, 0);
            RooHistPdf pdf_2420_4420("pdf_2420_4420", "pdf_2420_4420", rmD, *hist_2420_4420, 0);
            RooHistPdf pdf_2420_4600("pdf_2420_4600", "pdf_2420_4600", rmD, *hist_2420_4600, 0);

            RooRealVar mean("mean", "mean", 0.0);
            RooRealVar sigma("sigma", "sigma", 0.00123);
            RooGaussian gauss("gauss", "gauss", rmD, mean, sigma);
            
            rmD.setBins(1000, "cache");
            
            RooFFTConvPdf *Covpdf_2420_4360 = new RooFFTConvPdf(pdf_4360, "pdf_2420_4360 (X) gauss", rmD, pdf_2420_4360, gauss);
            RooFFTConvPdf *Covpdf_2420_4420 = new RooFFTConvPdf(pdf_4420, "pdf_2420_4420 (X) gauss", rmD, pdf_2420_4420, gauss);
            RooFFTConvPdf *Covpdf_2420_4600 = new RooFFTConvPdf(pdf_4600, "pdf_2420_4600 (X) gauss", rmD, pdf_2420_4600, gauss);
            
            Covpdf_2420_4360->Write();
            Covpdf_2420_4420->Write();
            Covpdf_2420_4600->Write();
            
            delete Covpdf_2420_4360;
            delete Covpdf_2420_4420;
            delete Covpdf_2420_4600;
        }
    }
    f->Close();

}
