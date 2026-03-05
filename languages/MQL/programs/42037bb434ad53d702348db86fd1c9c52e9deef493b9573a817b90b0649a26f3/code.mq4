//+------------------------------------------------------------------+
//|                                           SimpleScript.mq4        |
//|                        Copyright 2010, MetaQuotes Software Corp.   |
//|                                       https://www.metaquotes.net/  |
//+------------------------------------------------------------------+
#property copyright "MetaQuotes Software Corp."
#property link      "https://www.metaquotes.net/"

//+------------------------------------------------------------------+
//| Script program start function                                      |
//+------------------------------------------------------------------+
void OnStart()
  {
   double balance = AccountBalance();
   double equity  = AccountEquity();
   double margin  = AccountMargin();

   PrintFormat("Account: %s", AccountName());
   PrintFormat("Balance: %.2f %s", balance, AccountCurrency());
   PrintFormat("Equity:  %.2f %s", equity,  AccountCurrency());
   PrintFormat("Margin:  %.2f %s", margin,  AccountCurrency());
   PrintFormat("Free Margin: %.2f %s", AccountFreeMargin(), AccountCurrency());
  }
