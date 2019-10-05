#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit;

void fit_mDpi0_4420() {

    gStyle->SetFrameBorderMode(0);
    gStyle->SetCanvasBorderMode(0);
    gStyle->SetPadBorderMode(0);
    gStyle->SetPadColor(0);
    gStyle->SetCanvasColor(0);
    gStyle->SetTitleColor(1);
    gStyle->SetStatColor(0);
    gStyle->SetTitleFillColor(0);
    gStyle->SetHistFillColor(0);
    gStyle->SetLineWidth(2);
    // set the paper & margin sizes
    gStyle->SetPaperSize(20,26);
    gStyle->SetPadTopMargin(0.03);
    gStyle->SetPadRightMargin(0.05);
    gStyle->SetPadBottomMargin(0.22);
    gStyle->SetPadLeftMargin(0.21);
    gStyle->SetTitleFont(42,"xyz");  // set the all 3 axes title font                        
    gStyle->SetTitleFont(42," ");    // set the pad title font
    gStyle->SetTitleSize(0.09,"xyz"); // set the 3 axes title size
    gStyle->SetTitleSize(0.1," ");   // set the pad title size
    gStyle->SetLabelFont(42,"xyz");
    gStyle->SetLabelSize(0.07,"xyz");
    gStyle->SetTextFont(42);
    gStyle->SetTextSize(0.08);
    gStyle->SetStatFont(42);
    // do not display any of the standard histogram decorations
    gStyle->SetOptTitle(0);
    gStyle->SetOptStat(0);
    gStyle->SetOptFit(0);
    // put tick marks on top and RHS of plots
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    // put tick marks on top and RHS of plots
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);

    TFile *f = new TFile("/besfs/users/jingmq/bes/DDPIPI/v0.2/data/4420/data_4420_signal_sel.root", "READ");
    TTree *t = (TTree*)f->Get("save");

    RooRealVar mDpi0("m_Dpi0", "m_Dpi0", 2.004, 2.015);
    RooDataSet* data = new RooDataSet("data", "dataset", t, mDpi0);

    // signal
    RooRealVar mean("mean", "mean of gaussian", 2.01026, 2.008, 2.013);
    RooRealVar sigma("sigma", "width of gaussian", 0.001, 0, 0.008);
    RooGaussian gauss("gauss", "gauss", mDpi0, mean, sigma);

    // background
    RooRealVar a("a" ,"a", 0, -99, 99);
    RooRealVar b("b" ,"b", 0, -99, 99);
    RooRealVar c("c" ,"c", 0, -99, 99);
    RooRealVar d("d" ,"d", 0, -99, 99);
    RooPolynomial bkgpdf("bkgpdf", "bkgpdf", mDpi0, RooArgSet(a, b, c, d));

    RooRealVar nsig("nsig", "nsig", 2000, 0, 100000) ;
    RooRealVar nbkg("nbkg", "nbkg", 5000, 0, 100000) ;

    // build P.D.F model
    RooAddPdf model("model", "gauss+bkg", RooArgList(gauss, bkgpdf), RooArgList(nsig, nbkg));

    model.fitTo(*data);
    RooPlot* xframe = mDpi0.frame(Bins(40), Range(2.004, 2.015));
    data->plotOn(xframe);
    model.plotOn(xframe);
    model.plotOn(xframe, Components(gauss), LineColor(kYellow), LineWidth(2), LineStyle(1));
    model.plotOn(xframe, Components(bkgpdf), LineColor(kRed), LineWidth(2), LineStyle(1));
    xframe->GetXaxis()->SetTitle("M(D^{+}#pi^{0})(GeV/c^{2})");
    xframe->GetXaxis()->SetNdivisions(508);
    xframe->GetXaxis()->CenterTitle();
    xframe->GetYaxis()->SetNdivisions(504);
    xframe->GetYaxis()->SetTitleOffset(1.02);
    xframe->GetYaxis()->SetTitle("Events");
    xframe->GetYaxis()->CenterTitle();
    xframe->Draw();

    std::cout << "Decided signal region: [" << mean.getVal() - 9*sigma.getVal() << ", " << mean.getVal() + 9*sigma.getVal() << "]" << std::endl;

}