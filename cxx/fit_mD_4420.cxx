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

void fit_mD_4420() {

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

    TFile *f = new TFile("/besfs/users/jingmq/bes/DDPIPI/v0.2/incMC/hadrons/4420/incMC_hadrons_4420_before.root", "READ");
    TTree *t = (TTree*)f->Get("save");

    RooRealVar mD0("m_D0", "m_D0", 1.79, 1.95);
    RooDataSet* data = new RooDataSet("data", "dataset", t, mD0);

    // signal
    RooRealVar mean1("mean1", "mean of gaussian", 1.86, 1.83, 1.89);
    RooRealVar sigma1("sigma1", "width of gaussian", 0.01, 0, 0.2);
    RooGaussian gauss1("gauss1", "gauss", mD0, mean1, sigma1);
    RooRealVar mean2("mean2", "mean of gaussian", 1.86, 1.83, 1.89);
    RooRealVar sigma2("sigma2", "width of gaussian", 0.1, 0, 0.2);
    RooGaussian gauss2("gauss2", "gauss", mD0, mean2, sigma2);
    RooRealVar sigfrac("sigfrac", "fraction of components in signal", 0.8, 0., 1.);
    RooAddPdf sigpdf("sigpdf", "gauss1+gauss2", RooArgList(gauss1, gauss2), sigfrac);

    // background
    RooRealVar a("a" ,"a", 0, -99, 99);
    RooRealVar b("b" ,"b", 0, -99, 99);
    RooRealVar c("c" ,"c", 0, -99, 99);
    RooRealVar d("d" ,"d", 0, -99, 99);
    // RooPolynomial bkgpdf("bkgpdf", "bkgpdf", mD0, RooArgSet(a, b, c, d));
    RooPolynomial bkgpdf("bkgpdf", "bkgpdf", mD0, RooArgSet(a, b));

    RooRealVar nsig("nsig", "nsig", 2000, 0, 100000) ;
    RooRealVar nbkg("nbkg", "nbkg", 5000, 0, 100000) ;

    // build P.D.F model
    RooAddPdf model("model", "gauss+bkg", RooArgList(sigpdf, bkgpdf), RooArgList(nsig, nbkg));

    model.fitTo(*data);
    RooPlot* xframe = mD0.frame(Bins(40), Range(1.79, 1.95));
    data->plotOn(xframe);
    model.plotOn(xframe);
    model.plotOn(xframe, Components(RooArgSet(gauss1)), LineColor(kGreen), LineWidth(2), LineStyle(1));
    model.plotOn(xframe, Components(RooArgSet(gauss2)), LineColor(kGreen), LineWidth(2), LineStyle(1));
    model.plotOn(xframe, Components(bkgpdf), LineColor(kRed), LineWidth(2), LineStyle(1));
    xframe->GetXaxis()->SetTitle("M(D or D^{*})(GeV)");
    xframe->GetXaxis()->SetNdivisions(508);
    xframe->GetXaxis()->CenterTitle();
    xframe->GetXaxis()->SetTitleSize(0.06);
    xframe->GetXaxis()->SetLabelSize(0.06);
    xframe->GetXaxis()->SetTitleOffset(1.3);
    xframe->GetXaxis()->SetLabelOffset(0.008);
    xframe->GetYaxis()->SetNdivisions(504);
    xframe->GetYaxis()->SetTitleSize(0.06);
    xframe->GetYaxis()->SetLabelSize(0.06);
    xframe->GetYaxis()->SetTitleOffset(1.0);
    xframe->GetYaxis()->SetLabelOffset(0.008);
    xframe->GetYaxis()->SetTitle("Events");
    xframe->GetYaxis()->CenterTitle();
    xframe->Draw();

}
