{
   // Create a histogram and fill it with Gaussian random numbers
   TH1F *h1 = new TH1F("h1", "Gaussian Distribution", 100, -4, 4);
   h1->FillRandom("gaus", 10000);
   h1->SetLineColor(kBlue);
   h1->SetLineWidth(2);
   h1->GetXaxis()->SetTitle("x");
   h1->GetYaxis()->SetTitle("Entries");
   h1->Draw();
}
