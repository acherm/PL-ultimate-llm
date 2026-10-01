     FTAXRCPT   UF A E           K DISK
     FASSETS    UF A E           K DISK
     FTAXSCR    CF   E             WORKSTN
     DSTRADD           S              1P 0
     DPHYSDON          S              1P 0
      *----------------------------------------------------------
      *This program handles the donor specific things for the CCC
      *
      *Program starts with two launch parameters, STRASTID and ENDASTID
      *When run it will attach every asset ID from STR to END to the
      *specific donor ID in the master ASSETS file
      *
      *The DONOR file will be a keyed index that just houses the donor
      *information.
      *The key will be the DONORID, a numeric ID matching the same length
      *as ASSETID in ASSETS
      *
      *The DONOR file should also have extra fields for one-time non-tang
      *ible donations; a month's free rent, $1,000 cash donation, etc
      *----------------------------------------------------------
     C                   DOU       STRADD = 1
     C                   EXFMT     TAXSTART
     C
     C                   IF        *IN01 = *ON
     C                   SETON                                        71
     C                   EVAL      STRADD = 1
     C                   EVAL      PHYSDON = 1
     C                   ELSEIF    *IN02 = *ON
     C                   SETON                                        70
     C                   EVAL      STRADD = 1
     C                   EVAL      PHYSDON = 0
     C                   ELSEIF    *IN12 = *ON
     C                   EXSR      DIE
     C                   ENDIF
     C                   ENDDO
     C
     C                   EXSR      ADDDATA
      *----------------------------------------------------
     C     ADDDATA       BEGSR
     C                   EXFMT     TAXADD
     C
     C                   IF        *IN05 = *ON
     C                   EXSR      VALIDATE
     C                   EXSR      WRITERCD
     C                   ELSEIF    *IN06 = *ON
     C                   EXSR      VALIDATE
     C                   EXSR      WRITERCD
     C*                  EXSR      PRTRCPT
     C                   ELSEIF    *IN12 = *ON
     C                   EXSR      DIE
     C                   ENDIF
     C
     C                   EXSR      VALIDATE
     C                   EXSR      WRITERCD
     C                   EXSR      DIE
     C                   ENDSR
      *----------------------------------------------------------
     C     GETLSTRCPT    BEGSR
     C                   ENDSR
      *----------------------------------------------------------
     C     VALIDATE      BEGSR
     C                   ENDSR
      *---------------------------------------------------------
     C     WRITERCD      BEGSR
     C*                  OPEN      TAXRCPT
     C
     C                   MOVE      1             TAXNBR
     C                   MOVEL     INDNAME       TAXNAME
     C                   MOVEL     INDCITY       TAXCITY
     C                   MOVEL     INDST         TAXSTREET
     C                   MOVEL     INDZIP4       TAXZIP
     C                   MOVEL     INDTEL        TAXTEL
     C
     C                   IF        PHYSDON = 1
     C*JUMP INTO A LOOP FOR THE MASTER ASS1T FILE HERE
     C                   MOVEL     'NA'          TAXNTITM
     C                   MOVEL     0             TAXNTVALU
     C                   ELSE
     C                   MOVEL     INNTDESC      TAXNTITM
     C                   MOVEL     INNTVALUE     TAXNTVALU
     C                   ENDIF
     C
     C                   WRITE     TAXREC
     C                   CLOSE     TAXRCPT

     C                   ENDSR
      *----------------------------------------------------------
     C     DIE           BEGSR
     C                   MOVEL     *ON           *INLR
     C                   RETURN
     C                   ENDSR
