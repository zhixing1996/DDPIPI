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
using namespace RooFit ;

void simu_fit_2()
{
	// do not display any of the standard histogram decorations
    gStyle->SetOptTitle(0);
    gStyle->SetOptStat(0);
    gStyle->SetOptFit(0);
	gStyle->SetPadColor(0);
	// put tick marks on top and RHS of plots
	gStyle->SetPadTickX(1);
	gStyle->SetPadTickY(1);
	gStyle->SetCanvasColor(0);

	int debug=1;
	double xmin=2.;
	double xmax=2.8;
	int xbin=80;

	//set variable
	RooRealVar rmD("rm_D","rm_D",xmin,xmax) ;
	RooRealVar n2420_1("n2420_1","n2420_1",1100,0,10000);
	RooRealVar n2420_2("n2420_2","n2420_2",1500,0,10000);
	RooRealVar n2420_3("n2420_3","n2420_3",580,0,10000);
	RooRealVar nrmDpipisb_1("nrmDpipisb_1","nrmDpipisb_1",2761.4);
	RooRealVar nrmDpipisb_2("nrmDpipisb_2","nrmDpipisb_2",8811.1);
	RooRealVar nrmDpipisb_3("nrmDpipisb_3","nrmDpipisb_3",5410.2);
	RooRealVar npsipp_1("npsipp_1","npsipp_1",0,100000);
	RooRealVar npsipp_2("npsipp_2","npsipp_2",0,100000);
	RooRealVar npsipp_3("npsipp_3","npsipp_3",0,100000);
	TCut cut;

	TFile *file_data_1 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected_signal.root","READ");
	TFile *file_data_2 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected_signal.root","READ");
	TFile *file_data_3 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected_signal.root","READ");
	TFile *file_rmDpipisb_1 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4360/data_4360_selected_sideband.root","READ");
	TFile *file_rmDpipisb_2 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4420/data_4420_selected_sideband.root","READ");
	TFile *file_rmDpipisb_3 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/data/4600/data_4600_selected_sideband.root","READ");
	TFile *file_psipp_1 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4360/sigMC_psi_3770_4360_selected_signal.root","READ");
	TFile *file_psipp_2 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4420/sigMC_psi_3770_4420_selected_signal.root","READ");
	TFile *file_psipp_3 = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/psi_3770/4600/sigMC_psi_3770_4600_selected_signal.root","READ");

	TFile *f_Covpdf =new TFile("/besfs/users/jingmq/DDPIPI/v0.1/sigMC/D1_2420/conv/signal_conv_gauss.root","READ");

	TTree *t_data_1 = (TTree*)file_data_1->Get("save");
	TTree *t_data_2 = (TTree*)file_data_2->Get("save");
	TTree *t_data_3 = (TTree*)file_data_3->Get("save");
	TTree *t_rmDpipisb_1 = (TTree*)file_rmDpipisb_1->Get("save");
	TTree *t_rmDpipisb_2 = (TTree*)file_rmDpipisb_2->Get("save");
	TTree *t_rmDpipisb_3 = (TTree*)file_rmDpipisb_3->Get("save");
	TTree *t_psipp_1 = (TTree*)file_psipp_1->Get("save");
	TTree *t_psipp_2 = (TTree*)file_psipp_2->Get("save");
	TTree *t_psipp_3 = (TTree*)file_psipp_3->Get("save");

	TH1F *h_rmDpipisb_1=new TH1F("h_rmDpipisb_1","", xbin ,xmin,xmax);
	TH1F *h_rmDpipisb_2=new TH1F("h_rmDpipisb_2","", xbin ,xmin,xmax);
	TH1F *h_rmDpipisb_3=new TH1F("h_rmDpipisb_3","", xbin ,xmin,xmax);
	TH1F *h_psipp_1=new TH1F("h_psipp_1","", xbin, xmin,xmax);
	TH1F *h_psipp_2=new TH1F("h_psipp_2","", xbin, xmin,xmax);
	TH1F *h_psipp_3=new TH1F("h_psipp_3","", xbin, xmin,xmax);

	t_rmDpipisb_1->Project("h_rmDpipisb_1", "rm_D", cut);
	t_rmDpipisb_2->Project("h_rmDpipisb_2", "rm_D", cut);
	t_rmDpipisb_3->Project("h_rmDpipisb_3", "rm_D", cut);
	t_psipp_1->Project("h_psipp_1", "rm_D", cut);
	t_psipp_2->Project("h_psipp_2", "rm_D", cut);
	t_psipp_3->Project("h_psipp_3", "rm_D", cut);

	RooDataSet* set_data_1 = new RooDataSet("set_data_1","set_data_1", t_data_1,rmD);
	RooDataSet* set_data_2 = new RooDataSet("set_data_2","set_data_2", t_data_2,rmD);
	RooDataSet* set_data_3 = new RooDataSet("set_data_3","set_data_3", t_data_3,rmD);
	RooDataHist* set_rmDpipisb_1 = new RooDataHist("set_rmDpipisb_1","set_rmDpipisb_1", rmD,h_rmDpipisb_1);
	RooDataHist* set_rmDpipisb_2 = new RooDataHist("set_rmDpipisb_2","set_rmDpipisb_2", rmD,h_rmDpipisb_2);
	RooDataHist* set_rmDpipisb_3 = new RooDataHist("set_rmDpipisb_3","set_rmDpipisb_3", rmD,h_rmDpipisb_3);
	RooDataHist* set_psipp_1 = new RooDataHist("set_psipp_1","set_psipp_1", rmD,h_psipp_1);   
	RooDataHist* set_psipp_2 = new RooDataHist("set_psipp_2","set_psipp_2", rmD,h_psipp_2);
	RooDataHist* set_psipp_3 = new RooDataHist("set_psipp_3","set_psipp_3", rmD,h_psipp_3);

	RooHistPdf pdf_rmDpipisb_1("pdf_rmDpipisb_1","pdf_rmDpipisb_1", rmD, *set_rmDpipisb_1, 0);
	RooHistPdf pdf_rmDpipisb_2("pdf_rmDpipisb_2","pdf_rmDpipisb_2", rmD, *set_rmDpipisb_2, 0);
	RooHistPdf pdf_rmDpipisb_3("pdf_rmDpipisb_3","pdf_rmDpipisb_3", rmD, *set_rmDpipisb_3, 0);
	RooHistPdf pdf_psipp_1("pdf_psipp_1","pdf_psipp_1", rmD, *set_psipp_1, 0);
	RooHistPdf pdf_psipp_2("pdf_psipp_2","pdf_psipp_2", rmD, *set_psipp_2, 0);
	RooHistPdf pdf_psipp_3("pdf_psipp_3","pdf_psipp_3", rmD, *set_psipp_3, 0);

    ofstream fout;
    fout.open("/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/simufit_results_2.txt");
    if (!fout) {
        cout << "ERROR: Unable to open output file" << endl;
    }

	char pdfname1[50];
	char pdfname2[50];
	char pdfname3[50];
	char canvas1[500], canvas2[500], canvas3[500];

	for(int ii=30;ii<59;ii++) {
		for(int iii=0;iii<20;iii++) {
			sprintf(pdfname1,"Covpdf_2420_4360_%d_%d",ii,iii);
			sprintf(pdfname2,"Covpdf_2420_4420_%d_%d",ii,iii);
			sprintf(pdfname3,"Covpdf_2420_4600_%d_%d",ii,iii);
			sprintf(canvas1,"/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/canvas_4360/canvas1_rmD_%d_%d.eps",ii,iii);
			sprintf(canvas2,"/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/canvas_4420/canvas2_rmD_%d_%d.eps",ii,iii);
			sprintf(canvas3,"/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/canvas_4600/canvas3_rmD_%d_%d.eps",ii,iii);

			RooFFTConvPdf *Covpdf_2420_1 = (RooFFTConvPdf*)f_Covpdf->Get(pdfname1);
			RooFFTConvPdf *Covpdf_2420_2 = (RooFFTConvPdf*)f_Covpdf->Get(pdfname2);
			RooFFTConvPdf *Covpdf_2420_3 = (RooFFTConvPdf*)f_Covpdf->Get(pdfname3);;

			RooAddPdf  model_1("model_1","model_1",RooArgList(*Covpdf_2420_1,pdf_rmDpipisb_1,pdf_psipp_1),RooArgList(n2420_1,nrmDpipisb_1,npsipp_1));
			RooAddPdf  model_2("model_2","model_2",RooArgList(*Covpdf_2420_2,pdf_rmDpipisb_2,pdf_psipp_2),RooArgList(n2420_2,nrmDpipisb_2,npsipp_2));
			RooAddPdf  model_3("model_3","model_3",RooArgList(*Covpdf_2420_3,pdf_rmDpipisb_3,pdf_psipp_3),RooArgList(n2420_3,nrmDpipisb_3,npsipp_3));

			RooAbsReal* nl_4360   =  model_1.createNLL(*set_data_1,Range(2.1, 2.5));
			RooAbsReal* nl_4420   =  model_2.createNLL(*set_data_2,Range(2.1, 2.55));
			RooAbsReal* nl_4600   =  model_3.createNLL(*set_data_3,Range(2.1, 2.75));

			RooArgSet  list;
			list.add(*nl_4360);
			list.add(*nl_4420);
			list.add(*nl_4600);

			RooAddition nll("nll","nll",list);

			RooMinuit mm(nll);
			mm.migrad();

			RooFitResult *r = mm.save();

			double mass2420 = 2.4240;
            double width2420 = 0.018;
			double n4360 = n2420_1.getVal();
			double n4420 = n2420_2.getVal();
			double n4600 = n2420_3.getVal();
			double npsipp_4360 = npsipp_1.getVal();
			double npsipp_4420 = npsipp_2.getVal();
			double npsipp_4600 = npsipp_3.getVal();

            fout << setiosflags(ios::fixed) << setprecision(3) << r->minNll() << setprecision(5) << " " << mass2420 + 0.0001*ii << " " << width2420 + 0.001*iii;
            fout << " " << n4360 << " " << n4420 << " " << n4600 << " " << npsipp_4360 << " " << npsipp_4420 << " " << npsipp_4600 << endl;

			TCanvas *c1=new TCanvas("c1","",800,600);
			c1->cd();
			RooPlot* xframe_1 =  rmD.frame(Bins(40),Range(2.1,2.5),Title("A RooPlot of RM(D) in 4360MeV")) ;
			xframe_1->GetXaxis()->SetTitleSize(0.05);
			xframe_1->GetXaxis()->SetTitleOffset(0.9);
			xframe_1->GetXaxis()->SetLabelOffset(0.01);
			xframe_1->GetYaxis()->SetTitleSize(0.05);
			xframe_1->GetYaxis()->SetTitleOffset(0.95);
			xframe_1->GetYaxis()->SetLabelOffset(0.01);
			xframe_1->GetXaxis()->SetTitle("RM(D^{+})(GeV/c^{2})");
			xframe_1->GetYaxis()->SetTitle("Events/(10MeV/c^{2})");
			set_data_1->plotOn(xframe_1,MarkerSize(1),LineWidth(1));
			model_1.plotOn(xframe_1, Components(pdf_rmDpipisb_1), LineColor(kGreen), FillStyle(1001),FillColor(3),LineColor(3),VLines(), DrawOption("F") );
			model_1.plotOn(xframe_1, Components(*Covpdf_2420_1), LineColor(kRed), LineWidth(2), LineStyle(kDashed) );
			model_1.plotOn(xframe_1, Components(pdf_psipp_1), LineColor(kBlue), LineWidth(2), LineStyle(kDashed) );
			model_1.plotOn(xframe_1,LineColor(kBlack), LineWidth(3));

			TString xfname[4];
			xfname[0]="Data";
			xfname[1]="Backgrounds";
			xfname[2]="D_{1}(2420)^{+} D^{-}";
			xfname[3]="#psi(3770) #pi^{+} #pi^{-}";

			TLegend *lg1 =new TLegend(.2,.6,.6,.85);
			for(unsigned int i=0;i<4;i++){
				TString objName = xframe_1->nameOf(i);
				TObject *obj = xframe_1->findObject(objName.Data());
				if(i!=1)lg1->AddEntry(obj,xfname[i],"PL");
				if(i==1)lg1->AddEntry(obj,xfname[i],"F");
				lg1->SetTextFont(42);
				lg1->SetTextSize(0.05);
			}
			lg1->SetBorderSize(1);
			lg1->SetLineColor(0);
			lg1->SetFillColor(0);
			xframe_1->Draw();
			lg1->Draw();

			TCanvas *c2=new TCanvas("c2","",800,600);
			c2->cd();
			RooPlot* xframe_2 = rmD.frame(Bins(45),Range(2.1,2.55),Title("A RooPlot of RM(D) in 4420MeV")) ;
			xframe_2->GetXaxis()->SetTitleSize(0.05);
			xframe_2->GetXaxis()->SetTitleOffset(0.9);
			xframe_2->GetXaxis()->SetLabelOffset(0.01);
			xframe_2->GetYaxis()->SetTitleSize(0.05);
			xframe_2->GetYaxis()->SetTitleOffset(0.95);
			xframe_2->GetYaxis()->SetLabelOffset(0.01);
			xframe_2->GetXaxis()->SetTitle("RM(D^{+})(GeV/c^{2})");
			xframe_2->GetYaxis()->SetTitle("Events/(10MeV/c^{2})");
			set_data_2->plotOn(xframe_2);
			model_2.plotOn(xframe_2, Components(pdf_rmDpipisb_2), LineColor(kGreen), FillStyle(1001),FillColor(3),LineColor(3),VLines(), DrawOption("F") );
			model_2.plotOn(xframe_2, Components(*Covpdf_2420_2), LineColor(kRed), LineWidth(2), LineStyle(kDashed) );
			model_2.plotOn(xframe_2, Components(pdf_psipp_2), LineColor(kBlue), LineWidth(2), LineStyle(kDashed) );
			model_2.plotOn(xframe_2,LineColor(kBlack), LineWidth(3));
			TLegend *lg2 =new TLegend(.2,.6,.6,.85);
			for(unsigned int i=0;i<4;i++){
				TString objName = xframe_2->nameOf(i);
				TObject *obj = xframe_2->findObject(objName.Data());
				if(i!=1)lg2->AddEntry(obj,xfname[i],"PL");
				if(i==1)lg2->AddEntry(obj,xfname[i],"F");
				lg2->SetTextFont(42);
				lg2->SetTextSize(0.05);
			}
			lg2->SetBorderSize(1);
			lg2->SetLineColor(0);
			lg2->SetFillColor(0);
            xframe_2->Draw();
			lg2->Draw();

			TCanvas *c3=new TCanvas("c3","",800,600);
			c3->cd();
			RooPlot* xframe_3 = rmD.frame(Bins(65),Range(2.1,2.75),Title("A RooPlot of RM(D) in 4600MeV")) ;
			xframe_3->GetXaxis()->SetTitleSize(0.05);
			xframe_3->GetXaxis()->SetTitleOffset(0.9);
			xframe_3->GetXaxis()->SetLabelOffset(0.01);
			xframe_3->GetYaxis()->SetTitleSize(0.05);
			xframe_3->GetYaxis()->SetTitleOffset(0.95);
			xframe_3->GetYaxis()->SetLabelOffset(0.01);
			xframe_3->GetXaxis()->SetTitle("RM(D^{+})(GeV/c^{2})");
			xframe_3->GetYaxis()->SetTitle("Events/(10MeV/c^{2})");
			set_data_3->plotOn(xframe_3);
			model_3.plotOn(xframe_3, Components(pdf_rmDpipisb_3), LineColor(kGreen), FillStyle(1001),FillColor(3),LineColor(3),VLines(), DrawOption("F") );
			model_3.plotOn(xframe_3, Components(*Covpdf_2420_3), LineColor(kRed), LineWidth(2), LineStyle(kDashed) );
			model_3.plotOn(xframe_3, Components(pdf_psipp_3), LineColor(kBlue), LineWidth(2), LineStyle(kDashed) );
			set_data_3->plotOn(xframe_3);
			model_3.plotOn(xframe_3,LineColor(kBlack), LineWidth(3));
			TLegend *lg3 =new TLegend(.2,.6,.6,.85);
			for(unsigned int i=0;i<4;i++){
				TString objName = xframe_3->nameOf(i);
				TObject *obj = xframe_3->findObject(objName.Data());
				if(i!=1)lg3->AddEntry(obj,xfname[i],"PL");
				if(i==1)lg3->AddEntry(obj,xfname[i],"F");
				lg3->SetTextFont(42);
				lg3->SetTextSize(0.05);
			}
			lg3->SetBorderSize(1);
			lg3->SetLineColor(0);
			lg3->SetFillColor(0);
            xframe_3->Draw();
			lg3->Draw();

			c1->SaveAs(canvas1);
			c2->SaveAs(canvas2);
			c3->SaveAs(canvas3);

			delete Covpdf_2420_1;
            delete Covpdf_2420_2;
            delete Covpdf_2420_3;
		}
	}
	fout.close();

}
