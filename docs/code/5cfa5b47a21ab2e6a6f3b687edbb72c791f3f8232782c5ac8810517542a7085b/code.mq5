//+------------------------------------------------------------------+
//|                                     CloseOnTotalProfit_Sample.mq5|
//|                        Copyright 2009, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2009, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
/*
 A simple EA that closes all positions when the total profit reaches a certain level
*/
//--- input parameters
input double ProfitLevel=10.0; // Profit level to close all positions
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   double total_profit=0;
   //--- go through all open positions
   for(int i=PositionsTotal()-1;i>=0;i--)
     {
      //--- get position properties
      ulong  position_ticket=PositionGetTicket(i);
      string position_symbol=PositionGetString(POSITION_SYMBOL);
      long   magic=PositionGetInteger(POSITION_MAGIC);
      double volume=PositionGetDouble(POSITION_VOLUME);
      double price_open=PositionGetDouble(POSITION_PRICE_OPEN);
      double price_current=PositionGetDouble(POSITION_PRICE_CURRENT);
      long   type=PositionGetInteger(POSITION_TYPE);
      double profit=PositionGetDouble(POSITION_PROFIT);
      //--- calculate total profit
      total_profit+=profit;
     }
   //--- check the total profit
   if(total_profit>=ProfitLevel)
     {
      //--- close all positions
      for(int i=PositionsTotal()-1;i>=0;i--)
        {
         //--- get position ticket
         ulong  position_ticket=PositionGetTicket(i);
         //--- create trade request
         MqlTradeRequest request;
         MqlTradeResult  result;
         //---
         request.action=TRADE_ACTION_DEAL;
         request.position=position_ticket;
         //--- send order
         OrderSend(request,result);
        }
     }
  }
//+------------------------------------------------------------------+