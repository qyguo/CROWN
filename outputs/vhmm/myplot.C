#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <string>
#include <algorithm>

#include "TLatex.h"
#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TBranch.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TObject.h"
#include "TGraph2D.h"

#include "TPaveText.h"
#include "TF1.h"
#include "TGraph.h"
#include "TGraphQQ.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TMath.h"
#include "TFitResult.h"
#include "TLine.h"
#include "TColor.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TLegend.h"
#include "THStack.h"

#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooMCStudy.h"
#include "RooPlot.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TH2.h"
#include "RooFitResult.h"
#include "TStyle.h"
#include "TDirectory.h"

void fill(TH1F *h, Double_t xs, Double_t SumW, Double_t lumi, TString inputfile1, TString inputfile2){

    cout << "inputfile: " << inputfile1 << endl;
    cout << "inputfile: " << inputfile2 << endl;
    Float_t mass1,mass2;
    Float_t w1,w2;
    Float_t weight1,weight2;

    Bool_t trg1,trg2,is1,is2;
    Int_t flag1,flag2;

    TFile *file1 = TFile::Open(inputfile1);
    TFile *file2 = TFile::Open(inputfile2);
    
    TTree *tree1 = (TTree*)file1->Get("ntuple");
    TTree *tree2 = (TTree*)file2->Get("ntuple");
        
    TTree *tree3 = (TTree*)file1->Get("conditions");
    TTree *tree4 = (TTree*)file2->Get("conditions");
    
    Long64_t nentries1 = tree1->GetEntries();
    Long64_t nentries2 = tree2->GetEntries();
    

    tree1->SetBranchAddress("H_mass",&mass1);
    tree2->SetBranchAddress("H_mass",&mass2);
    

    tree1->SetBranchAddress("genWeight",&weight1);
    tree2->SetBranchAddress("genWeight",&weight2);
    
    tree1->SetBranchAddress("trg_single_mu24",&trg1);
    tree2->SetBranchAddress("trg_single_mu24",&trg2);

    tree1->SetBranchAddress("Flag_dimuon_Zmass_veto",&flag1);
    tree2->SetBranchAddress("Flag_dimuon_Zmass_veto",&flag2);

    tree1->SetBranchAddress("is_vhmm",&is1);
    tree2->SetBranchAddress("is_vhmm",&is2);
    
    for (Long64_t i=0;i<nentries1;i++){
            tree1->GetEntry(i);
        if (trg1==1&&flag1==1&&is1==1){
        w1 = lumi*xs*weight1/SumW;
        h->Fill(mass1,w1);
    }
    }
    for (Long64_t j=0;j<nentries2;j++){
            tree2->GetEntry(j);
        if (trg2==1&&flag2==1&&is2==1){
        w2 = lumi*xs*weight2/SumW;
        h->Fill(mass2,w2);
        }
    }
}

void myplot(){

    TString output_WpH_e2m = "output_WpH_m2m.root";
    TString output_WpH_m2m = "output_WpH_e2m.root";
    TString output_WmH_e2m = "output_WmH_m2m.root";
    TString output_WmH_m2m = "output_WmH_e2m.root";

    TCanvas * canv = new TCanvas("C","",1200,800);//another option: pass the canvas as argument and only create it once. Usually better not to.
    canv->cd();//usually do not need that
        
    TH1F *h_WpH = new TH1F("h_WpH","WplusH_mass",8,110,150);
    TH1F *h_WmH = new TH1F("h_WmH","WminusH_mass",8,110,150);
    TH1F *h_WH = new TH1F("h_WH","WH_mass",8,110,150);

    double xs_WpH = 0.189;
    double xs_WmH = 0.11799;

    double SumW_WpH = 519770.3327;
    double SumW_WmH = 324655.7988960001;

    float lumi = 137; 

    fill(h_WpH, xs_WpH, SumW_WpH, lumi, output_WpH_e2m, output_WpH_m2m);
    fill(h_WmH, xs_WmH, SumW_WmH, lumi, output_WmH_e2m, output_WmH_m2m);
    h_WpH->Scale(50);
    h_WmH->Scale(50);
    h_WH->Add(h_WpH, h_WmH);

    //h_WH->SetMarkerStyle(kFullCircle);
    //h_WH->SetMarkerSize(1);
    //h_WH->SetMarkerColor(kBlue);
    h_WpH->SetLineColor(kRed);
    h_WmH->SetLineColor(kGreen);
    h_WH->SetLineColor(kBlue);

    h_WH->Draw("hist");h_WpH->Draw("hist same");h_WmH->Draw("hist same");
    //h_WH->SetTitle("M_{\mu\mu} GeV");
    h_WH->GetYaxis()->SetTitle("Events/Bins");
    //h_WH->GetXaxis()->SetTitle("M_{\mu\mu} GeV");

    auto leg = new TLegend(0.7,0.6,0.82,0.85);
    //leg->AddEntry(h_W1,"W^{-}H","L");
    leg->AddEntry(h_WH,"WH X50","L");
    leg->AddEntry(h_WpH,"WpH X50","L");
    leg->AddEntry(h_WmH,"WmH X50","L");
    leg->SetFillStyle(0);
    leg->SetBorderSize(0);
    leg->SetTextFont(132);
    leg->SetTextSize(0.04);
    leg->Draw();
    gStyle->SetOptStat(0);

    canv->Update();//usually do not need that
    canv->SaveAs("mass.pdf");

}

