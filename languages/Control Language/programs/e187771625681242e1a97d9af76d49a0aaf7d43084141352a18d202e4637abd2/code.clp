/*-------------------------------------------------------------------*/
/*                                                                   */
/*  Program . . : CUS001CL                                           */
/*  Description : Customer File Maintenance - CLP                    */
/*  Author  . . : Barry S. Somervill                                 */
/*  Date  . . . : January 23, 2012                                   */
/*                                                                   */
/*  History . . :                                                    */
/*    01/23/12  BSS  Created                                         */
/*                                                                   */
/*-------------------------------------------------------------------*/
     PGM        PARM(&RTNCODE)

     DCL        VAR(&RTNCODE) TYPE(*CHAR) LEN(7)
     DCL        VAR(&CUSNBR) TYPE(*DEC) LEN(7 0)
     DCL        VAR(&CUSNAME) TYPE(*CHAR) LEN(30)
     DCL        VAR(&CUSADDR) TYPE(*CHAR) LEN(30)
     DCL        VAR(&CUSCITY) TYPE(*CHAR) LEN(25)
     DCL        VAR(&CUSSTATE) TYPE(*CHAR) LEN(2)
     DCL        VAR(&CUSZIP) TYPE(*DEC) LEN(5 0)

     CALL       PGM(CUS001RG) PARM(&RTNCODE &CUSNBR &CUSNAME +
                  &CUSADDR &CUSCITY &CUSSTATE &CUSZIP)

     ENDPGM