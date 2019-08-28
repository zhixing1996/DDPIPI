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

void fit_rmDpipi_4420() {

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

    TFile *f = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected.root", "READ");
    TTree *t = (TTree*)f->Get("save");

    RooRealVar rmDpipi("rm_Dpipi", "rm_Dpipi", 1.79, 1.96);
    RooDataSet* data = new RooDataSet("data", "dataset", t, rmDpipi);

    // signal
    RooRealVar mean("mean", "mean of crystal ball", 1.86, 1.83, 1.89);
    RooRealVar sigma("sigma", "width of crystal ball", 4.6e-03, 0, 0.2);
    RooRealVar asym("asym", "asym", -1.1, -10, 10);
    RooRealVar amp("amp", "amp", 1.76, 0, 200);
    RooAbsPdf* CB = new RooCBShape("CB", "CB", rmDpipi, mean, sigma, asym, amp);

    // background
    RooRealVar a("a" ,"a", 4.7, -5, 7);
    RooRealVar b("b" ,"b", -3.4, -10, 10);
    RooRealVar c("c" ,"c", 0.4, -5, 5);
    RooRealVar d("d" ,"d", 0.3, -5, 5);
    RooPolynomial bkgpdf("bkgpdf", "bkgpdf", rmDpipi, RooArgSet(a, b, c, d));

    RooRealVar nsig("nsig", "nsig", 2000, 0, 100000) ;
    RooRealVar nbkg("nbkg", "nbkg", 28000, 0, 100000) ;

    // build P.D.F model
    RooAddPdf model("model", "CB+bkg", RooArgList(*CB, bkgpdf), RooArgList(nsig, nbkg));

    model.fitTo(*data);

    rmDpipi.setRange("srange", 1.855, 1.882);
    rmDpipi.setRange("sbrangel", 1.786, 1.84);
    rmDpipi.setRange("sbrangeh", 1.897, 1.951);

    RooAbsReal* nsrange = bkgpdf.createIntegral(rmDpipi, NormSet(rmDpipi), Range("srange"));   
    RooAbsReal* nsbrangel = bkgpdf.createIntegral(rmDpipi, NormSet(rmDpipi), Range("sbrangel"));
    RooAbsReal* nsbrangeh = bkgpdf.createIntegral(rmDpipi, NormSet(rmDpipi), Range("sbrangeh"));

    double S_srv = nsrange->getVal()*(nbkg.getVal()) + nsig.getVal();
    double srv = nsrange->getVal()*nbkg.getVal();
    double srv_err = nsrange->getVal()*nbkg.getError();
    double sbrlv = nsbrangel->getVal()*nbkg.getVal();
    double sbrhv = nsbrangeh->getVal()*nbkg.getVal();

    RooPlot* xframe = rmDpipi.frame(Bins(50), Range(1.79, 1.96));
    data->plotOn(xframe);
    model.plotOn(xframe);
    model.plotOn(xframe, Components(*CB), LineColor(kYellow), LineWidth(2), LineStyle(1));
    model.plotOn(xframe, Components(bkgpdf), LineColor(kRed), LineWidth(2), LineStyle(1));
    xframe->GetXaxis()->SetTitle("RM(D^{+}#pi^{+}#pi^{-})(GeV/c^{2})");
    xframe->GetXaxis()->SetNdivisions(508);
    xframe->GetYaxis()->SetNdivisions(504);
    xframe->GetYaxis()->SetTitleOffset(1.12);
    xframe->Draw();

    cout << "S_srv: " << S_srv << " srv: " << srv << " srv_err: " << srv_err << " sbrlv: " << sbrlv << " sbrhv: " << sbrhv << endl;
    cout << "nsrange: " << nsrange->getVal() << " nsbrangl: " << nsbrangel->getVal() << " nsbrangeh: " << nsbrangeh->getVal() << endl;

    ofstream fout;
    fout.open("/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/PHSP/4420/rmDpipi_fitresult_4420.txt");
    if (!fout) {
        cout << "ERROR: Unable to open output file" << endl;
    }
    fout << "S_srv: " << S_srv << " srv: " << srv << "  srv_err: " << srv_err << " sbrlv: " << sbrlv << " sbrhv: " << sbrhv << endl;
    fout << "nsrange: " << nsrange->getVal() << " nsbrangl: " << nsbrangel->getVal() << " nsbrangeh: " << nsbrangeh->getVal() << endl;

}
