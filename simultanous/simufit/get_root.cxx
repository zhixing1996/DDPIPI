void get_root() {

    ifstream in_1; 
    ifstream in_2; 
    ifstream in_3; 
    in_1.open("/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/simufit_results_1.txt");
    in_2.open("/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/simufit_results_2.txt");
    in_3.open("/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/simufit_results_3.txt");
    TFile *f = new TFile("/besfs/users/jingmq/DDPIPI/v0.1/ana/simu/simufit_results.root", "RECREATE");
    
    double likelihood=0;
    double mass2420=0;
    double width2420=0;
    double n4360=0;
    double n4420=0;
    double n4600=0;
    double npsipp4360=0;
    double npsipp4420=0;
    double npsipp4600=0;
    int nlines= 0;
    
    TTree *save = new TTree("save", "save");
    save->Branch("likelihood", &likelihood, "likelihood/D");
    save->Branch("mass2420", &mass2420, "mass2420/D");
    save->Branch("width2420", &width2420, "width2420/D");
    save->Branch("n4360", &n4360, "n4360/D");
    save->Branch("n4420", &n4420, "n4420/D");
    save->Branch("n4600", &n4600, "n4600/D");
    save->Branch("npsipp4360", &npsipp4360, "npsipp4360/D");
    save->Branch("npsipp4420", &npsipp4420, "npsipp4420/D");
    save->Branch("npsipp4600", &npsipp4600, "npsipp4600/D");
    
    while(1) {
        in_1 >> likelihood >> mass2420 >> width2420 >> n4360 >> n4420 >> n4600 >> npsipp4360 >> npsipp4420 >> npsipp4600; 
        if (!in_1.good()) break;
        save->Fill();
    }
    in_1.close();

    while(1) {
        in_2 >> likelihood >> mass2420 >> width2420 >> n4360 >> n4420 >> n4600 >> npsipp4360 >> npsipp4420 >> npsipp4600; 
        if (!in_2.good()) break;
        save->Fill();
    }
    in_2.close();

    while(1) {
        in_3 >> likelihood >> mass2420 >> width2420 >> n4360 >> n4420 >> n4600 >> npsipp4360 >> npsipp4420 >> npsipp4600; 
        if (!in_3.good()) break;
        save->Fill();
    }
    in_3.close();

    f->Write();

}
