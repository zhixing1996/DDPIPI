#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
#include "TStyle.h"
#include "TString.h"
#include "TROOT.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TFile.h"
#include "TVector3.h"
#include "TH2F.h"
#include "TCut.h"
#include "TSystem.h"
#include "RooFit.h"
#include "TLegend.h"
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
#include "RooMinuit.h"
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

void simu_fit() {

    double xmin=2.0;
    double xmax=2.8;
    int xbin2=100;

    RooRealVar rmD("rm_D", "rm_D", xmin, xmax);
    RooRealVar nsig_4360("nsig_4360", "nsig_4360", 1100, 0, 10000);
    RooRealVar nsig_4420("nsig_4420", "nsig_4420", 1500, 0, 10000);
    RooRealVar nsig_4600("nsig_4600", "nsig_4600", 580, 0, 10000);
    RooRealVar nbkg_4360("nbkg_4360", "nbkg_4360", 2746.5);  // defined by fitting to rmDpipi distribution  
    RooRealVar nbkg_4420("nbkg_4420", "nbkg_4420", 8923.53); // defined by fitting to rmDpipi distribution   
    RooRealVar nbkg_4600("nbkg_4600", "nbkg_4600", 5368.13); // defined by fitting to rmDpipi distribution    
    RooRealVar npsi3770_4360("npsi3770_4360", "npsi3770_4360", 0, 100000);
    RooRealVar npsi3770_4420("npsi3770_4420", "npsi3770_4420", 0, 100000);
    RooRealVar npsi3770_4600("npsi3770_4600", "npsi3770_4600", 0, 100000);

    TFile *file_data_4360 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected_signal.root", "READ");
    TFile *file_data_4420 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected_signal.root", "READ");
    TFile *file_data_4600 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected_signal.root", "READ");

    TTree *t_data_4360 = (TTree*)file_data_4360->Get("save");
    TTree *t_data_4420 = (TTree*)file_data_4420->Get("save");
    TTree *t_data_4600 = (TTree*)file_data_4600->Get("save");
    RooDataSet* set_data_4360 = new RooDataSet("set_data_4360", "set_data_4360", t_data_4360, rmD);
    RooDataSet* set_data_4420 = new RooDataSet("set_data_4420", "set_data_4420", t_data_4420, rmD);
    RooDataSet* set_data_4600 = new RooDataSet("set_data_4600", "set_data_4600", t_data_4600, rmD);

    TFile *file_psi3770 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/psi3770shape/psi3770_shape.root", "READ");
    RooKeysPdf *pdf_psi3770_4360 = (RooKeysPdf*)file_psi3770->Get("pdf_psi3770_4360");
    RooKeysPdf *pdf_psi3770_4420 = (RooKeysPdf*)file_psi3770->Get("pdf_psi3770_4420");
    RooKeysPdf *pdf_psi3770_4600 = (RooKeysPdf*)file_psi3770->Get("pdf_psi3770_4600");

    TFile *file_bkg = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/bkgMC/sideband/bakground_shape.root", "READ");
    RooKeysPdf *pdf_bkg_4360 = (RooKeysPdf*)file_bkg->Get("pdf_sideband_4360");
    RooKeysPdf *pdf_bkg_4420 = (RooKeysPdf*)file_bkg->Get("pdf_sideband_4420");
    RooKeysPdf *pdf_bkg_4600 = (RooKeysPdf*)file_bkg->Get("pdf_sideband_4600");

    TFile *file_sig =new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/conv/signal_conv_gauss.root", "READ");

    ofstream fout;
    fout.open("/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/simufit_results.txt");
    if (!fout) {
        cout << "ERROR: Unable to open output file" << endl;
    }

    char pdfname_4360[50], pdfname_4420[50], pdfname_4600[50];
    char canvas_4360[500], canvas_4420[500], canvas_4600[500];

    cout << "Test1" << endl;
    for (int i = 0; i < 80; i++) {
        for (int j = 0; j < 20; j++) {
            sprintf(pdfname_4360, "Covpdf_2420_4360_%d_%d", i, j);
            sprintf(pdfname_4420, "Covpdf_2420_4420_%d_%d", i, j);
            sprintf(pdfname_4600, "Covpdf_2420_4600_%d_%d", i, j);
            cout << "Test2_1" << endl;
            sprintf(canvas_4360, "/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/canvas_4360/simufit_4360_%d_%d.pdf", i, j);
            sprintf(canvas_4420, "/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/canvas_4420/simufit_4420_%d_%d.pdf", i, j);
            sprintf(canvas_4600, "/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/canvas_4600/simufit_4600_%d_%d.pdf", i, j);
            cout << "Test2_2" << endl;

            RooFFTConvPdf *pdf_sig_4360 = (RooFFTConvPdf*)file_sig->Get(pdfname_4360);
            RooFFTConvPdf *pdf_sig_4420 = (RooFFTConvPdf*)file_sig->Get(pdfname_4420);
            RooFFTConvPdf *pdf_sig_4600 = (RooFFTConvPdf*)file_sig->Get(pdfname_4600);

            RooAddPdf model_4360("model_4360", "model_4360", RooArgList(*pdf_sig_4360, *pdf_bkg_4360, *pdf_psi3770_4360), RooArgList(nsig_4360, nbkg_4360, npsi3770_4360));
            RooAddPdf model_4420("model_4420", "model_4420", RooArgList(*pdf_sig_4420, *pdf_bkg_4420, *pdf_psi3770_4420), RooArgList(nsig_4420, nbkg_4420, npsi3770_4420));
            RooAddPdf model_4600("model_4600", "model_4600", RooArgList(*pdf_sig_4600, *pdf_bkg_4600, *pdf_psi3770_4600), RooArgList(nsig_4600, nbkg_4600, npsi3770_4600));
            cout << "Test3" << endl;

            RooAbsReal* nl_4360 = model_4360.createNLL(*set_data_4360, Range(2.1, 2.5));
            RooAbsReal* nl_4420 = model_4420.createNLL(*set_data_4420, Range(2.1, 2.55));
            RooAbsReal* nl_4600 = model_4600.createNLL(*set_data_4600, Range(2.1, 2.75));
            cout << "Test4" << endl;

            RooArgSet list;
            list.add(*nl_4360);
            list.add(*nl_4420);
            list.add(*nl_4600);
            cout << "Test5" << endl;

            RooAddition nll("nll", "nll", list);
            RooMinuit mm(nll);
            mm.migrad();
            RooFitResult *r = mm.save();
            cout << "Test6" << endl;

            double mass2420 = 2.4240;
            double width2420 = 0.018;
            double n4360 = nsig_4360.getVal();
            double n4420 = nsig_4420.getVal();
            double n4600 = nsig_4600.getVal();
            double npsipp4360 = npsi3770_4360.getVal();
            double npsipp4420 = npsi3770_4420.getVal();
            double npsipp4600 = npsi3770_4600.getVal();

            fout << setiosflags(ios::fixed) << setprecision(3) << r->minNll() << setprecision(5) << " " << mass2420 + 0.0001*i << " " << width2420 + 0.001*j;
            fout << " " << n4360 << " " << n4420 << " " << n4600 << " " << npsipp4360 << " " << npsipp4420 << " " << npsipp4600 << endl;

            TString xfname[5];
            xfname[0] = "Data";
            xfname[1] = "Backgrounds";
            xfname[2] = "Signal MC";
            xfname[3] = "psi(3770)";
            xfname[4] = "Fit Result";

            TCanvas *c1 = new TCanvas("c1", "", 800, 600);
            c1->cd();
            RooPlot* xframe_1 = rmD.frame(Bins(40), Range(2.1, 2.5), Title("A RooPlot of RM(D) in 4360MeV"));
            c1->SetLeftMargin(0.15);
            c1->SetRightMargin(0.05);
            c1->SetTopMargin(0.05);
            c1->SetBottomMargin(0.15);
            xframe_1->GetXaxis()->SetTitle("RM(D^{+})(GeV/c^{2})");
            xframe_1->GetXaxis()->SetTitleFont(42);
            xframe_1->GetXaxis()->SetLabelOffset(0.01);
            xframe_1->GetXaxis()->SetLabelSize(0.06);
            xframe_1->GetXaxis()->SetTitleSize(0.06);
            xframe_1->GetXaxis()->SetTitleOffset(1.1);
            xframe_1->GetYaxis()->SetTitle("Events/(0.01GeV/c^{2})");
            xframe_1->GetYaxis()->SetTitleFont(42);
            xframe_1->GetYaxis()->SetLabelOffset(0.01);
            xframe_1->GetYaxis()->SetLabelSize(0.06);
            xframe_1->GetYaxis()->SetTitleSize(0.06);
            xframe_1->GetYaxis()->SetTitleOffset(1.2);
            set_data_4360->plotOn(xframe_1, MarkerSize(1), LineWidth(1));
            model_4360.plotOn(xframe_1, Components(*pdf_bkg_4360), LineColor(kGreen), FillStyle(1001), FillColor(3), LineColor(3), VLines(), DrawOption("F"));
            model_4360.plotOn(xframe_1, Components(*pdf_sig_4360), LineColor(kRed), LineWidth(2), LineStyle(8));
            model_4360.plotOn(xframe_1, Components(*pdf_psi3770_4360), LineColor(kBlue), LineWidth(2), LineStyle(kDotted));
            model_4360.plotOn(xframe_1, LineColor(kBlack), LineWidth(3));
            TLegend *lg1 = new TLegend(.2, .45, .45, .85);
            for(unsigned int k = 0; k < 5; k++) {
                TString objName = xframe_1->nameOf(k);
                TObject *obj = xframe_1->findObject(objName.Data());
                if (k!=1) lg1->AddEntry(obj, xfname[k], "PL");
                if (k==1) lg1->AddEntry(obj, xfname[k], "F");
                lg1->SetTextFont(42);
                lg1->SetTextSize(0.07);
            }
            lg1->SetBorderSize(1);
            lg1->SetLineColor(0);
            lg1->SetFillColor(0);
            xframe_1->Draw();
            lg1->Draw();
            c1->SaveAs(canvas_4360);

            TCanvas *c2 = new TCanvas("c2", "", 800, 600);                                                                                                               
            c2->cd();
            RooPlot* xframe_2 = rmD.frame(Bins(45), Range(2.1, 2.55), Title("A RooPlot of RM(D) in 4420MeV"));
            c2->SetLeftMargin(0.15);
            c2->SetRightMargin(0.05);
            c2->SetTopMargin(0.05);
            c2->SetBottomMargin(0.15);
            xframe_2->GetXaxis()->SetTitle("RM(D^{+})(GeV/c^{2})");
            xframe_2->GetXaxis()->SetTitleFont(42);
            xframe_2->GetXaxis()->SetLabelOffset(0.01);
            xframe_2->GetXaxis()->SetLabelSize(0.06);
            xframe_2->GetXaxis()->SetTitleSize(0.06);
            xframe_2->GetXaxis()->SetTitleOffset(1.1);
            xframe_2->GetYaxis()->SetTitle("Events/(0.01GeV/c^{2})");
            xframe_2->GetYaxis()->SetTitleFont(42);
            xframe_2->GetYaxis()->SetLabelOffset(0.01);
            xframe_2->GetYaxis()->SetLabelSize(0.06);
            xframe_2->GetYaxis()->SetTitleSize(0.06);
            xframe_2->GetYaxis()->SetTitleOffset(1.2);
            set_data_4420->plotOn(xframe_2, MarkerSize(1), LineWidth(1));
            model_4420.plotOn(xframe_2, Components(*pdf_bkg_4420), LineColor(kGreen), FillStyle(1001), FillColor(3), LineColor(3), VLines(), DrawOption("F"));
            model_4420.plotOn(xframe_2, Components(*pdf_sig_4420), LineColor(kRed), LineWidth(2), LineStyle(8));
            model_4420.plotOn(xframe_2, Components(*pdf_psi3770_4420), LineColor(kBlue), LineWidth(2), LineStyle(kDotted));
            model_4420.plotOn(xframe_2, LineColor(kBlack), LineWidth(3));
            TLegend *lg2 = new TLegend(.2, .45, .45, .85);
            for(unsigned int k = 0; k < 5; k++) {
                TString objName = xframe_2->nameOf(k);
                TObject *obj = xframe_2->findObject(objName.Data());
                if (k!=1) lg2->AddEntry(obj, xfname[k], "PL");
                if (k==1) lg2->AddEntry(obj, xfname[k], "F");
                lg2->SetTextFont(42);
                lg2->SetTextSize(0.07);
            }
            lg2->SetBorderSize(1);
            lg2->SetLineColor(0);
            lg2->SetFillColor(0);
            xframe_2->Draw();
            lg2->Draw();
            c2->SaveAs(canvas_4420);

            TCanvas *c3 = new TCanvas("c3", "", 800, 600);                                                                                                               
            c3->cd();
            RooPlot* xframe_3 = rmD.frame(Bins(65), Range(2.1, 2.75), Title("A RooPlot of RM(D) in 4600MeV"));
            c3->SetLeftMargin(0.15);
            c3->SetRightMargin(0.05);
            c3->SetTopMargin(0.05);
            c3->SetBottomMargin(0.15);
            xframe_3->GetXaxis()->SetTitle("RM(D^{+})(GeV/c^{2})");
            xframe_3->GetXaxis()->SetTitleFont(42);
            xframe_3->GetXaxis()->SetLabelOffset(0.01);
            xframe_3->GetXaxis()->SetLabelSize(0.06);
            xframe_3->GetXaxis()->SetTitleSize(0.06);
            xframe_3->GetXaxis()->SetTitleOffset(1.1);
            xframe_3->GetYaxis()->SetTitle("Events/(0.01GeV/c^{2})");
            xframe_3->GetYaxis()->SetTitleFont(42);
            xframe_3->GetYaxis()->SetLabelOffset(0.01);
            xframe_3->GetYaxis()->SetLabelSize(0.06);
            xframe_3->GetYaxis()->SetTitleSize(0.06);
            xframe_3->GetYaxis()->SetTitleOffset(1.2);
            set_data_4600->plotOn(xframe_3, MarkerSize(1), LineWidth(1));
            model_4600.plotOn(xframe_3, Components(*pdf_bkg_4600), LineColor(kGreen), FillStyle(1001), FillColor(3), LineColor(3), VLines(), DrawOption("F"));
            model_4600.plotOn(xframe_3, Components(*pdf_sig_4600), LineColor(kRed), LineWidth(2), LineStyle(8));
            model_4600.plotOn(xframe_3, Components(*pdf_psi3770_4600), LineColor(kBlue), LineWidth(2), LineStyle(kDotted));
            model_4600.plotOn(xframe_3, LineColor(kBlack), LineWidth(3));
            TLegend *lg3 = new TLegend(.2, .45, .45, .85);
            for(unsigned int k = 0; k < 5; k++) {
                TString objName = xframe_3->nameOf(k);
                TObject *obj = xframe_3->findObject(objName.Data());
                if (k!=1) lg3->AddEntry(obj, xfname[k], "PL");
                if (k==1) lg3->AddEntry(obj, xfname[k], "F");
                lg3->SetTextFont(42);
                lg3->SetTextSize(0.07);
            }
            lg3->SetBorderSize(1);
            lg3->SetLineColor(0);
            lg3->SetFillColor(0);
            xframe_3->Draw();
            lg3->Draw();
            c3->SaveAs(canvas_4600);

            delete pdf_sig_4360;
            delete pdf_sig_4420;
            delete pdf_sig_4600;
        }
    }

    delete pdf_psi3770_4360;
    delete pdf_psi3770_4420;
    delete pdf_psi3770_4600;

    delete pdf_bkg_4360;
    delete pdf_bkg_4420;
    delete pdf_bkg_4600;
    
    fout.close();

}
