//+------------------------------------------------------------------+
//|                                                  SimpleMA.mq4    |
//|                        Copyright 2024, MetaQuotes Software Corp. |
//|                                       https://www.metaquotes.net |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Software Corp."
#property link      "https://www.metaquotes.net"
#property version   "1.00"
#property strict

// Input parameters
input int MA_Period = 14;          // Moving Average period
input int MA_Shift = 0;             // Moving Average shift
input ENUM_MA_METHOD MA_Method = MODE_SMA;  // Moving Average method

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   Print("Simple MA Expert Advisor initialized");
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   Print("Simple MA Expert Advisor deinitialized");
  }

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   double ma = iMA(NULL, 0, MA_Period, MA_Shift, MA_Method, PRICE_CLOSE, 0);
   double currentPrice = Close[0];

   if(currentPrice > ma)
     {
      Comment("Price is above MA(", MA_Period, "): ", DoubleToStr(ma, Digits));
     }
   else
     {
      Comment("Price is below MA(", MA_Period, "): ", DoubleToStr(ma, Digits));
     }
  }
//+------------------------------------------------------------------+