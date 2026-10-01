     **free
       ctl-opt DFTACTGRP(*NO) ACTGRP('AZANDRES') PGMINFO(*PCML:*MODULE);
       //  Testing metodo GET simple en RPG usando IWS como Framework
       //
       //  Servicio:
       //  http://x.x.x.x:10555/web/services/GETCUST/123
       //
       //  Para compilar:
       //  *>  CRTBNDRPG PGM(GETCUST) SRCFILE(*LIBL/QRPGLESRC) DBGVIEW(*LIST)
       //
       //  Para ver el PCML, sacar PGMINFO de arriba y compilar asi:
       //  CRTBNDRPG  GETCUST SRCFILE(*LIBL/QRPGLESRC) DBGVIEW(*LIST) -
       //             PGMINFO(*PCML) INFOSTMF('getcust.pcml')
       //

       dcl-f CUSTFILE disk keyed usage(*INPUT) prefix('CUST.') UsrOpn;

       dcl-ds CUST ext qualified extname('CUSTFILE') end-ds;

       // *ENTRY PLIST
       dcl-pi *N;
         CustNo  like(Cust.Custno);
         Name    like(Cust.Name  );
         Street  like(Cust.Street);
         City    like(Cust.City  );
         State   like(Cust.State );
         Postal  like(Cust.Postal);
         Contact like(Cust.Contact);
         Title  like(Cust.Title);
         Balance like(Cust.Balance);
       end-pi;

       dcl-pr QMHSNDPM ExtPgm;
         MessageID   char(7)     Const;
         QualMsgF    char(20)    Const;
         MsgData     char(32767) Const options(*varsize);
         MsgDtaLen   int(10)     Const;
         MsgType     char(10)    Const;
         CallStkEnt  char(10)    Const;
         CallStkCnt  int(10)     Const;
         MessageKey  char(4);
         ErrorCode   char(32767) options(*varsize);
       end-pr;

       dcl-pr system int(10) ExtProc(*dclcase);
         command pointer value options(*string);
       end-pr;

       dcl-ds err qualified;
         bytesProv   int(10) inz(0);
         bytesAvail  int(10) inz(0);
       end-ds;

       dcl-s MsgDta  varchar(1000);
       dcl-s MsgKey  char(4);

       if not %open(CUSTFILE);
         monitor;
           open CUSTFILE;
         on-error;
           system('DSPJOBLOG OUTPUT(*PRINT)');
         endmon;
       endif;

       chain CustNo CUSTFILE;
       if not %found;
         msgdta = 'Cliente no encontrado.';
         QMHSNDPM( 'CPF9897'
                 : 'QCPFMSG   *LIBL'
                 : msgdta
                 : %len(msgdta)
                 : '*ESCAPE'
                 : '*PGMBDY'
                 : 1
                 : MsgKey
                 : err );
       else;
           Custno = Cust.Custno;
           Name   = Cust.name;
           Street = Cust.Street;
           City   = Cust.City;
           State  = Cust.State;
           Postal = Cust.Postal;
           Contact = Cust.Contact;
           Title   = Cust.Title;
           Balance = Cust.Balance;
       endif;

       *inlr = *on;
     **end-free
