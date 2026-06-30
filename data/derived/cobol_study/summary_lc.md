# COBOL-in-SWH exploratory study — summary

_Generated 2026-06-30T10:39:55Z · 350 samples (340 text, 10 non-text), 291 LLM-judged._

## Lines of code (code lines, excl. blank/comment)

- min **1** · median **107.0** · mean **404.5** · max **15350** · total **137525**

## Source format (mechanical heuristic)

- fixed: 293
- free: 40
- unknown: 7

## Feature prevalence (mechanical, over text files)

- EXEC SQL: 27 (7.9%)
- EXEC CICS: 22 (6.5%)
- COMP-3: 24 (7.1%)
- COPY: 122 (35.9%)
- CALL: 103 (30.3%)

## Is COBOL? (judge)

  - true: 291 (100.0%)

## Dialect family (judge)

  - gnucobol: 143 (49.1%)
  - ibm-mainframe: 55 (18.9%)
  - unknown: 51 (17.5%)
  - micro-focus: 28 (9.6%)
  - acucobol: 9 (3.1%)
  - other-vendor: 4 (1.4%)
  - rm-cobol: 1 (0.3%)

## COBOL standard (judge)

  - COBOL-85: 271 (93.1%)
  - COBOL-2002: 11 (3.8%)
  - COBOL-2014: 8 (2.7%)
  - unknown: 1 (0.3%)

## Source format (judge)

  - fixed: 238 (81.8%)
  - free: 51 (17.5%)
  - unknown: 1 (0.3%)
  - mixed: 1 (0.3%)

## Domain (judge)

  - education-tutorial: 105 (36.1%)
  - demo-example: 31 (10.7%)
  - retail-commerce: 29 (10.0%)
  - banking-finance: 23 (7.9%)
  - accounting-erp: 23 (7.9%)
  - test-suite: 20 (6.9%)
  - utility-tooling: 16 (5.5%)
  - other: 11 (3.8%)
  - manufacturing-logistics: 11 (3.8%)
  - healthcare-medical: 8 (2.7%)
  - insurance: 6 (2.1%)
  - government-public: 5 (1.7%)
  - payroll-hr: 2 (0.7%)
  - telecom: 1 (0.3%)

## Program type (judge)

  - batch: 96 (33.0%)
  - demo: 74 (25.4%)
  - online-cics: 55 (18.9%)
  - subprogram: 39 (13.4%)
  - test: 27 (9.3%)

## Maturity (judge)

  - production-like: 131 (45.0%)
  - student-exercise: 114 (39.2%)
  - snippet: 28 (9.6%)
  - toy-or-hello-world: 18 (6.2%)

_Judge tokens: 1316869 prompt + 143839 completion._

## Samples

| sha1_git | file | LOC | fmt | divs | SQL | CICS | family | domain | type | std |
|---|---|---:|---|---:|:-:|:-:|---|---|---|---|
| bab43fcee6 | /DFH0XSOD.cbl | 55 | fixed | 4 |  | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| e646dd9bd2 | /COCRDUPS.cbl | 1157 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| c034210adc | /gameSummary.aspx.designer.c | 58 | fixed | 0 |  |  |  |  |  |  |
| ba85b06489 | /CWSPID.cbl | 130 | fixed | 4 |  |  | micro-focus | utility-tooling | subprogram | COBOL-85 |
| d12bac1011 | /D516KYS.cbl | 10 | free | 0 |  |  |  |  |  |  |
| f1d81029d6 | /STU-BUILDER.cbl | 94 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 4e6635112f | /Legion 006 - (New 52).cbl | 164 | fixed | 0 |  |  |  |  |  |  |
| 4c46e3c4ba | /STUDENT-SCHEDULE.cbl | 109 | fixed | 3 |  |  | micro-focus | education-tutorial | batch | COBOL-85 |
| d2d5d3298a | /[DC Comics] DC Master Readi | 2837 | free | 0 |  |  |  |  |  |  |
| c452b24bc7 | /sample.cbl | 72 | fixed | 4 |  | ✓ | ibm-mainframe | government-public | online-cics | COBOL-85 |
| fd0fcfdd6a | /pw00702s.cbl | 1455 | fixed | 4 |  |  | micro-focus | banking-finance | batch | COBOL-85 |
| 4cdbba90c5 | /DB2CBLEX.cbl | 216 | fixed | 4 | ✓ |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 26f9cadd03 | /ADDAMT.cbl | 34 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b84ee0fabd | /MyGrade.cbl | 87 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 7d31f09e60 | /OCCRS.cbl | 105 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 3a9980b553 | /SEARCH_SORT.cbl | 93 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 257284e43a | /hcipdb01.cbl | 113 | fixed | 4 | ✓ | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| ddc4ee08df | /desafioModulo2CPF.cbl | 16 | fixed | 3 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 11446809ef | /log4mas.cbl | 351 | fixed | 3 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| f572e8ac95 | /relcli.cbl | 400 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| a32402ec21 | /ph070129.cbl | 124 | fixed | 4 |  |  | gnucobol | other | online-cics | COBOL-85 |
| baec2f55f8 | /breakdown.aspx.designer.cbl | 146 | fixed | 0 |  |  |  |  |  |  |
| fdb64c219c | /cxp100-08-06-2009.cbl | 2127 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 414e4e187b | /CIB007.cbl | 947 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 0639f12478 | /desconto05.cbl | 319 | fixed | 4 |  |  | acucobol | retail-commerce | online-cics | COBOL-85 |
| d99e62f3cb | /car105.cbl | 50 | fixed | 4 |  |  | micro-focus | demo-example | batch | COBOL-85 |
| 19f6353b8b | /TypedefCyclic0.cbl | 38 | fixed | 1 |  |  | gnucobol | test-suite | test | COBOL-2014 |
| 18715e1b85 | /read_cmd_line_args.cbl | 22 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 0e9f602354 | /pl940.cbl | 405 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 4e839bd595 | /acas007.cbl | 301 | free | 4 | ✓ |  | gnucobol | accounting-erp | subprogram | COBOL-85 |
| 63b39a2c43 | /IC2134.2.cbl | 109 | free | 0 |  |  |  |  |  |  |
| f745779546 | /NC2424.2.cbl | 892 | fixed | 2 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| 0c6bdcb7b2 | /star-10-2.cbl | 23 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| bf69b8ca11 | /Wonder Woman 1 - Golden Age | 799 | fixed | 0 |  |  |  |  |  |  |
| 86c5ac403a | /Lista3E2.cbl | 39 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| b5ce23029f | /TSQL021C.cbl | 46 | fixed | 3 | ✓ |  | gnucobol | test-suite | test | COBOL-85 |
| f374403515 | /CPBD061GLS.cbl | 10 | free | 0 |  |  |  |  |  |  |
| 50971a6778 | /ph070058.cbl | 178 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| d5c6b9f779 | /SAM1.cbl | 389 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 6031fa2237 | /cgi-edit-betyg.cbl | 193 | fixed | 3 | ✓ |  | gnucobol | education-tutorial | online-cics | COBOL-85 |
| 793e317f96 | /CPRMAIN.cbl | 47 | fixed | 4 |  |  | ibm-mainframe | government-public | test | COBOL-85 |
| cdedc94ff5 | /stbefw481.cbl | 456 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 01ed7f856e | /CPBD368HKK.cbl | 17 | fixed | 0 |  |  |  |  |  |  |
| 22f6b72cb5 | /BATCH_1.cbl | 120 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| bcab17945a | /D686THN.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 72afc8ec7b | /tempCodeRunnerFile.cbl | 1 | fixed | 0 |  |  |  |  |  |  |
| a784a8091f | /exercicio_07_v2.cbl | 103 | fixed | 4 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| e2ea3bf989 | /MarksMF.cbl | 65 | fixed | 4 |  |  | micro-focus | education-tutorial | batch | COBOL-85 |
| 222f259959 | /TN0004.cbl | 420 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 689c855aa1 | /Avengers 004.cbl | 886 | fixed | 0 |  |  |  |  |  |  |
| 8243891368 | /pw04217c.cbl | 343 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 5ea4d4659b | /CPBD382SSS.cbl | 10 | free | 0 |  |  |  |  |  |  |
| d33f8409f4 | /IfThenNextSentence0.cbl | 13 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 772faf254b | /ex02.cbl | 119 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 0c49ebb21f | /MENU_INICIAL.cbl | 70 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 1ce19024c7 | /Listing-5-2-e.cbl | 67 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| e796660e82 | /workingStorageStringSubLeve | 27 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 2cda929767 | /files.cbl | 11 | free | 1 |  |  |  |  |  |  |
| a4f9c76460 | /sort2f.cbl | 94 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 2cc8ca0ea4 | /case116.cbl | 16 | fixed | 3 |  |  | gnucobol | test-suite | test | COBOL-2002 |
| 77f9854589 | /VIEW-INGREDS.cbl | 422 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 9f4f96e387 | /hcipdb01.cbl | 94 | fixed | 4 | ✓ | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| 1b865ed19f | /COBOL016.cbl | 48 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 06f6a39b02 | /server.cbl | 869 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 003a420dac | /p9BubbleSort.cbl | 38 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 580330e016 | /InfoBrg2.cbl | 41 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 5679739dc7 | /CWXTDATE.cbl | 109 | fixed | 4 |  |  | ibm-mainframe | demo-example | subprogram | COBOL-85 |
| 157243cd7d | /tictactoe.cbl | 247 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| c1e3b3bbd9 | /LGICDB01.cbl | 142 | fixed | 4 | ✓ | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 9b02fc3a73 | /evaluateExtended.cbl | 28 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| a3b55c003c | /lista de tarefas.cbl | 146 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| ad0a01ea1a | /[Marvel] 002 The Clone Wars | 92 | free | 0 |  |  |  |  |  |  |
| 1e06b76b08 | /ANK_KURINOBE.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| e8eeb1b720 | /DDS0001.LEARN.ACCT.SORT2.DA | 0 | unknown | 0 |  |  |  |  |  |  |
| 51d4566e35 | /IX1024.2.cbl | 617 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| 6f2ec7d3dc | /mygrade.cbl | 80 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 8b24899fc0 | /InputHandling.cbl | 129 | fixed | 4 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 23e313d385 | /ACTUALIZARPROV.cbl | 99 | fixed | 4 |  |  | unknown | accounting-erp | subprogram | COBOL-85 |
| 8096c9ba45 | /pwpa6046.cbl | 631 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 895e412e19 | /pw04262r.cbl | 4753 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 064a38754e | /Listing14-2.cbl | 83 | fixed | 4 |  |  | gnucobol | telecom | batch | COBOL-85 |
| a8d3b65907 | /EDGD1CLQ.cbl | 392 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 30e80d9151 | /COB2.cbl | 12 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 37a2926b94 | /playpen.cbl | 72 | fixed | 0 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 657f521567 | /S806.cbl | 14 | fixed | 3 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 29e00e6dd0 | /TestMyClass.cbl | 16 | fixed | 4 |  |  | micro-focus | education-tutorial | demo | COBOL-2002 |
| 04a0920741 | /Lista4E4.cbl | 33 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 1892be9dc5 | /peso-conv-p.cbl | 1239 | fixed | 3 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| bfe0688f7b | /IDBSL160.cbl | 769 | fixed | 4 | ✓ |  | ibm-mainframe | banking-finance | subprogram | COBOL-85 |
| c8b4e3746b | /CI0226P.cbl | 2205 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 49889982db | /BMQ034.cbl | 642 | fixed | 4 |  |  | micro-focus | other | batch | COBOL-85 |
| e614db5b4e | /testantlr212.cbl | 24 | fixed | 3 |  | ✓ | ibm-mainframe | other | test | COBOL-85 |
| 4dae03afb6 | /ACT-SEC.cbl | 79 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| b8a833b394 | /printhx3.cbl | 23 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| d1955f085c | /[Marvel] 2015-2018 Part 2.3 | 167 | free | 0 |  |  |  |  |  |  |
| 4eabc65cb4 | /mikek.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 36322dcf1c | /EXE5.cbl | 45 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| acd58de39a | /bams.cbl | 338 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| 9e396d1649 | /paris.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 304a060976 | /mov-peso.cbl | 85 | fixed | 3 |  |  | acucobol | manufacturing-logistics | batch | COBOL-85 |
| a2ab50e78c | /PGMCE.cbl | 88 | fixed | 3 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| ad6bc66117 | /TRADER9.cbl | 51 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 57c6b9f2b6 | /BDS0802.cbl | 80 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 002fd461f9 | /project3-welcome.cbl | 138 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 6f2f49a756 | /utils.cbl | 32 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| f43a9f04e7 | /calculator2.cbl | 29 | free | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 7d85209732 | /test.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 08105aa993 | /pfix.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 56e8126fa9 | /py050060.cbl | 311 | fixed | 4 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| 4d4619b919 | /pw00675s.cbl | 2952 | fixed | 4 |  |  | gnucobol | retail-commerce | subprogram | COBOL-85 |
| a26a7b1a08 | /fdsjsc.cbl | 138 | fixed | 4 |  |  | micro-focus | utility-tooling | subprogram | COBOL-2002 |
| f83699d542 | /helloworld.cbl | 11 | fixed | 2 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| ed8cd1b45e | /hcipdb01.cbl | 94 | fixed | 4 | ✓ | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| 2990fd9990 | /Chaos! Universe 1993 - 2002 | 752 | free | 0 |  |  |  |  |  |  |
| 115b00debc | /Control7.cbl | 40 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 3c6dfaa10c | /ph050027.cbl | 289 | fixed | 4 |  |  | other-vendor | manufacturing-logistics | online-cics | COBOL-85 |
| 57e81262a0 | /noncompliant.cbl | 4 | fixed | 1 |  |  |  |  |  |  |
| b626f9c095 | /samos1.cbl | 381 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 6a7025ab09 | /[Marvel] 2021-2023 Part 9.3 | 308 | fixed | 0 |  |  |  |  |  |  |
| 03fb22c866 | /fixsection.cbl | 79 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-2002 |
| fba2767747 | /DebugLinesInvalidCE.rdz.cbl | 11 | fixed | 2 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| 87e945664a | /testantlr241.cbl | 25 | fixed | 3 |  |  | gnucobol | test-suite | test | COBOL-85 |
| 7a2fd147b6 | /PROJ-PRINT-FIN-AID.cbl | 110 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 9f27236da6 | /SCHED-INQ-BY-CRSE.cbl | 124 | fixed | 4 |  |  | gnucobol | education-tutorial | online-cics | COBOL-85 |
| 1e27cbadb7 | /ofldBread.cbl | 338 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | subprogram | COBOL-85 |
| 1e909f04c7 | /shop_receipts.cbl | 50 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 25361e2dde | /application_26_insert.cbl | 27 | fixed | 4 | ✓ |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 56087f7b39 | /gordcvar.cbl | 15350 | fixed | 4 |  |  | acucobol | retail-commerce | online-cics | COBOL-85 |
| efd4b4c795 | /pfcaut7e.cbl | 3932 | fixed | 4 | ✓ |  | other-vendor | banking-finance | online-cics | COBOL-85 |
| 643412fea4 | /Vchpay01.cbl | 409 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 0669c4d684 | /PW02403P.cbl | 811 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | online-cics | COBOL-85 |
| f7ed38b47e | /CWXTCOB.cbl | 508 | fixed | 4 |  |  | ibm-mainframe | demo-example | batch | COBOL-85 |
| 982571be13 | /IEAS9800.cbl | 143 | fixed | 4 |  |  | ibm-mainframe | other | subprogram | COBOL-85 |
| 997a50e530 | /TPROG05.cbl | 119 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| bb01c5dc3c | /comutfs.cbl | 332 | fixed | 3 |  |  | gnucobol | manufacturing-logistics | batch | COBOL-85 |
| 348ca0fa76 | /BANK2.cbl | 138 | fixed | 4 |  |  | gnucobol | banking-finance | subprogram | COBOL-85 |
| f1cfa42a06 | /TransactionDataAccess.cbl | 187 | fixed | 0 |  |  |  |  |  |  |
| c7815a5dda | /pw02516c.cbl | 296 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| ec79ef32db | /crp052.cbl | 1842 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 38256cb3f9 | /server.cbl | 579 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 9f1d6eba79 | /IX1024.2.cbl | 174 | free | 0 |  |  |  |  |  |  |
| 4b85a98861 | /pw02175r.cbl | 1932 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 3fd3b4314a | /COURSE-INQ.cbl | 108 | fixed | 4 |  |  | gnucobol | education-tutorial | online-cics | COBOL-85 |
| 806d85e607 | /analRES.cbl | 101 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-2014 |
| 5e0b82d46f | /ph050037.cbl | 146 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | online-cics | COBOL-85 |
| fbb0569362 | /ASREA105.cbl | 110 | fixed | 4 |  |  | ibm-mainframe | government-public | batch | COBOL-85 |
| 66cf530e2b | /gctestrun3E.cbl | 434 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 4e57199263 | /IF1274.2.cbl | 776 | fixed | 2 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| 41b6bf4806 | /IF1394.2.cbl | 250 | free | 0 |  |  |  |  |  |  |
| e400f6a860 | /Listing16-8.cbl | 28 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 51259dd3a7 | /EDI-impord-p.cbl | 3114 | fixed | 3 |  |  | acucobol | retail-commerce | batch | COBOL-85 |
| a002a3d544 | /EXPPROG4.cbl | 139 | fixed | 3 |  |  | ibm-mainframe | government-public | batch | COBOL-85 |
| c70a544ed3 | /[Marvel] CMRO Expanded Read | 2978 | free | 0 |  |  |  |  |  |  |
| f8d6967c33 | /tscorte.cbl | 4798 | fixed | 4 |  |  | acucobol | retail-commerce | online-cics | COBOL-85 |
| 203c944d3b | /D377HIK.cbl | 81 | fixed | 0 |  |  |  |  |  |  |
| adb1fdf9f9 | /cllp7659.cbl | 653 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 1396c19dca | /TPROG06.cbl | 119 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 2b02a97c46 | /Damenbauernspiele.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 2d3d12df55 | /IFCodeElements.cbl | 149 | fixed | 0 |  |  |  |  |  |  |
| 0ffbf6ae36 | /ArrayCopybook.cbl | 12 | fixed | 0 |  |  |  |  |  |  |
| d307ef153e | /genrep.cbl | 156 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 6922b6b11f | /PW03017R.cbl | 779 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 6237e74077 | /[Marvel] 2021-2024 Part 10. | 114 | fixed | 0 |  |  |  |  |  |  |
| a1501b8e5c | /CALCULATE-AVG.cbl | 20 | fixed | 3 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 69e173661c | /first-proj.cbl | 9 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| ad6f1b1b0f | /CPBD028GZJ.cbl | 10 | free | 0 |  |  |  |  |  |  |
| f5d8a4da98 | /AromaSalesRPT.cbl | 99 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| ca586f3091 | /IF4024.2.cbl | 98 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| 78f676a4ee | /py030001.cbl | 258 | fixed | 4 |  |  | gnucobol | retail-commerce | subprogram | COBOL-2002 |
| d631293f12 | /REPORT-COURSE-BY-INST.cbl | 127 | fixed | 4 |  |  | gnucobol | education-tutorial | online-cics | COBOL-85 |
| 489a82d88e | /ssar.cbl | 80 | unknown | 0 |  |  |  |  |  |  |
| 1c47cd8ade | /StoprunGobackLastStatement. | 41 | fixed | 1 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| 343be592ed | /day4.cbl | 42 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-2014 |
| 5e0d91b832 | /Serie07Prog04.cbl | 237 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| c5c04a4e20 | /lista3e9.cbl | 63 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| e61efac7b8 | /analMT.cbl | 648 | free | 4 | ✓ |  | gnucobol | accounting-erp | subprogram | COBOL-85 |
| fdd46b6310 | /HCMADB02.cbl | 165 | fixed | 4 | ✓ | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| fd2fd3b8a6 | /pw04413c.cbl | 1479 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| 1e7cb51985 | /string_calculator_test.cbl | 37 | unknown | 3 |  |  | unknown | test-suite | test | COBOL-85 |
| 73963d659a | /LVVS0092.cbl | 129 | fixed | 4 |  |  | ibm-mainframe | insurance | subprogram | COBOL-85 |
| 5791582223 | /ph070102.cbl | 184 | fixed | 4 |  |  | gnucobol | banking-finance | online-cics | COBOL-85 |
| 5426b41dc1 | /clock.cbl | 39 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 06d4bca171 | /acceptance.cbl | 26 | unknown | 0 |  |  | acucobol | education-tutorial | test | unknown |
| 1c729edce0 | /merge_files.cbl | 38 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 6ef43e3fc9 | /squelette.cbl | 46 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| a975fbd976 | /MyGrade.cbl | 66 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| b7e3e775f0 | /MergeSort.cbl | 83 | fixed | 1 |  |  | micro-focus | education-tutorial | demo | COBOL-2014 |
| 669ff621ab | /TSQL006A.cbl | 80 | fixed | 3 | ✓ |  | gnucobol | test-suite | test | COBOL-85 |
| 18c08b83b4 | /lib-readfile.cbl | 45 | free | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-2002 |
| 1342a952bf | /Program1.cbl | 77 | fixed | 3 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 48f7d64852 | /Isogram.cbl | 42 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 745229badc | /caesarCipher.cbl | 101 | unknown | 1 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 98325bfdd9 | /PGMOD4.cbl | 353 | fixed | 4 | ✓ |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| daae57ea30 | /S09P000.cbl | 68 | fixed | 2 | ✓ |  | micro-focus | other | batch | COBOL-85 |
| eb6f4f1c46 | /gnucobol.cbl | 105 | free | 0 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 366f532354 | /HCMADB02.cbl | 165 | fixed | 4 | ✓ | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| 261e554c4e | /DoCalc.cbl | 18 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 9562f62913 | /playpen.cbl | 39 | fixed | 0 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 3940176744 | /hello.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| b9dafffd1f | /F3.cbl | 199 | fixed | 0 |  |  | gnucobol | other | batch | COBOL-85 |
| 88b0e1c1c9 | /DHELP01P.cbl | 100 | fixed | 3 |  | ✓ | micro-focus | banking-finance | online-cics | COBOL-85 |
| d6f79b8107 | /main.cbl | 443 | fixed | 4 |  |  | gnucobol | government-public | batch | COBOL-85 |
| f09c9d32d4 | /stt-day-p.cbl | 438 | fixed | 3 |  |  | acucobol | manufacturing-logistics | subprogram | COBOL-85 |
| 3a02d3c8d2 | /SHI-expfornitori.cbl | 270 | fixed | 3 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| f2efdb1e7b | /TSUBR02.cbl | 64 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | subprogram | COBOL-85 |
| 0e6aa7955d | /EJERCICIO-3.cbl | 102 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 0763532ddc | /recording.cbl | 1 | free | 0 |  |  |  |  |  |  |
| c3eadf16b9 | /SCHED-ADD.cbl | 157 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 937b2d9eb4 | /CI0448P.cbl | 1169 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 80d726d8e2 | /gctestsetup.cbl | 276 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 0dcaca63dd | /utl-sub-var-env-get.cbl | 15 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| 08b4c0c7fd | /Data1.cbl | 16 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| f6bbf4167c | /TABLES-TWO-DIMENSION-39.cbl | 28 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1ec430e416 | /callprog.cbl | 16 | fixed | 4 |  |  | unknown | utility-tooling | subprogram | COBOL-85 |
| c6eb3dbce9 | /SeqReadNo88.cbl | 38 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1bb37b54a3 | /[DC] Batman Modern Age - Pa | 200 | free | 0 |  |  |  |  |  |  |
| 8088f70695 | /TP.cbl | 489 | fixed | 4 |  |  | rm-cobol | retail-commerce | batch | COBOL-85 |
| 8396f6b555 | /IF1104.2.cbl | 160 | free | 0 |  |  |  |  |  |  |
| 3887d56948 | /crearIndexado.cbl | 70 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 1dd24bb28e | /epsmlist.cbl | 178 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 1eefb71758 | /HBSI20AO.cbl | 261 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| baf682ec57 | /control-break2.cbl | 58 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| e0daeb8445 | /arr.cbl | 401 | fixed | 3 |  |  | gnucobol | education-tutorial | test | COBOL-85 |
| 97d4df3e0b | /lgicus01.cbl | 96 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 126882fa09 | /load_program.cbl | 253 | fixed | 4 |  |  | gnucobol | other | subprogram | COBOL-2014 |
| 358f634b91 | /edit5.cbl | 30 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 8cf77ec814 | /FUNCTION.cbl | 19 | fixed | 2 |  |  | unknown | education-tutorial | test | COBOL-2002 |
| 91448c70d3 | /cosy.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 22ec78e862 | /ricalini-p.cbl | 389 | fixed | 3 |  |  | micro-focus | manufacturing-logistics | batch | COBOL-85 |
| c34ea9a9ce | /cbl2xml_Test112.cbl | 23 | fixed | 0 |  |  |  |  |  |  |
| 1fe9449266 | /sortingStudents_End.cbl | 51 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| abfa2dc761 | /AKLAB7MultilBreakC.cbl | 231 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 0c79341280 | /subsample.cbl | 17 | fixed | 4 |  |  | unknown | demo-example | subprogram | COBOL-85 |
| cdf79099eb | /template.cbl | 17 | free | 3 |  |  | gnucobol | demo-example | demo | COBOL-2002 |
| ebb0fc235c | /EL6523.cbl | 4688 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 0603fb7084 | /COACTVWD.cbl | 788 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 9da94c4b7a | /HCV1BI01.cbl | 56 | fixed | 4 |  | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| 9c756b03ec | /fdvnd02.cbl | 12 | fixed | 0 |  |  |  |  |  |  |
| efd05ee8e3 | /SUB-TUGAS-KELOMPOK.cbl | 12 | fixed | 3 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 052d35c06a | /Combo-Box.cbl | 31 | fixed | 4 |  |  | acucobol | demo-example | demo | COBOL-85 |
| fb1d2d37c0 | /LISTA.cbl | 77 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 1dbe047bef | /MARBLE18.cbl | 286 | fixed | 4 | ✓ | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| 20ecf751ca | /py990001.cbl | 174 | fixed | 2 |  |  | micro-focus | utility-tooling | subprogram | COBOL-2002 |
| 2571f4b82b | /lista11exercicio1v2.cbl | 133 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 2fe99f64db | /Ej2A.cbl | 70 | fixed | 4 |  |  | unknown | banking-finance | batch | COBOL-85 |
| 69f5765885 | /admin-server.cbl | 200 | fixed | 4 |  |  | gnucobol | banking-finance | subprogram | COBOL-85 |
| ab8b59c267 | /RL110A.cbl | 575 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| 8863e4a2a1 | /ExecSqlWithAlterSequence.rd | 59 | fixed | 4 | ✓ |  | ibm-mainframe | test-suite | test | COBOL-85 |
| a019c6552b | /FunDeclare.rdz.cbl | 128 | fixed | 2 |  |  | micro-focus | education-tutorial | test | COBOL-2014 |
| ef16a32a62 | /BANK2.cbl | 138 | fixed | 4 |  |  | gnucobol | banking-finance | subprogram | COBOL-85 |
| bcd1c79da8 | /MATHXMPL.cbl | 152 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b5cdbcb00c | /D642UTG.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| bee92b5849 | /acasirsub1.cbl | 428 | free | 4 |  |  | gnucobol | accounting-erp | subprogram | COBOL-2014 |
| dec486347b | /CallPublicProcFromPrivatePr | 106 | fixed | 3 |  |  | other-vendor | demo-example | demo | COBOL-85 |
| 227851e996 | /tictac.cbl | 248 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| d59e54cc84 | /prova02.cbl | 54 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| d3cfe5d1ab | /Search_sort.cbl | 90 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 0c4ca62b4d | /pp01165c.cbl | 1527 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 802e7482ad | /hello.cbl | 10 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 242acb27d4 | /NC108M.cbl | 619 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| c6706a2b56 | /CobolAssignment1-COMP210.cb | 127 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 091aab254a | /pwpe0401.cbl | 1766 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 5ed4b92a20 | /[DC Comics] DC Master Readi | 3203 | free | 0 |  |  |  |  |  |  |
| 2edad5c812 | /CWXTCOB.cbl | 508 | fixed | 4 |  |  | ibm-mainframe | demo-example | batch | COBOL-85 |
| cce29a2f18 | /Listing5-7.cbl | 42 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| fd4771e946 | /UPDATE_EMP.cbl | 26 | free | 4 |  |  | gnucobol | payroll-hr | subprogram | COBOL-85 |
| c88936a072 | /Aquaman 2 - Silver_Bronze.c | 610 | fixed | 0 |  |  |  |  |  |  |
| 695dfaa51f | /ProjectPart2(1).cbl | 244 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 04c3924ab4 | /GalhoCRD020.cbl | 93 | fixed | 3 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 97e6462dbc | /CPBD816BSK.cbl | 57 | fixed | 0 |  |  |  |  |  |  |
| 7c31733e72 | /CIRE010.cbl | 492 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 3b4400ad46 | /SecuenciarArchivoClientes.c | 44 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| fc31f67252 | /connecttoserver.cbl | 110 | free | 3 |  |  | gnucobol | utility-tooling | subprogram | COBOL-2002 |
| 539f2bde25 | /VPOPUPMSG.cbl | 517 | free | 4 |  |  | micro-focus | utility-tooling | subprogram | COBOL-85 |
| d57d709e87 | /Docalc.cbl | 18 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 464e1e9d73 | /pwpe0201.cbl | 258 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| 8d5739b635 | /CommunicationDescriptionInp | 16 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b64a755bfa | /soutfsqf02b2.cbl | 130 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| cd5a2ff151 | /tempCodeRunnerFile.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 6389b49efe | /ZECS001.cbl | 1435 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| 870f0c39b2 | /py050087.cbl | 3329 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | batch | COBOL-85 |
| a6c5e6c085 | /ANK_WORK010.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 673885971e | /pw02143c.cbl | 3437 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | online-cics | COBOL-85 |
| 51d66f5b13 | /pw02599c.cbl | 565 | fixed | 4 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| b1a6363754 | /pw00178p.cbl | 270 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 52a3a55ffe | /IVP01018.cbl | 18 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 584e79e3da | /types.llvm.cbl | 27 | unknown | 0 |  |  |  |  |  |  |
| 9e7bf74805 | /[X-Men Krakoa 2.5] Destiny  | 221 | free | 0 |  |  |  |  |  |  |
| 5a7716ef65 | /UPDATE_PART.cbl | 49 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | subprogram | COBOL-85 |
| f0061c9964 | /fr-date.cbl | 20 | fixed | 4 |  |  | gnucobol | demo-example | subprogram | COBOL-85 |
| 82acdb244e | /CIFPBCNV.cbl | 130 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 568f3ce519 | /Data2.cbl | 18 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 385b511c79 | /SortStatement.rdz.cbl | 45 | fixed | 3 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| 37a01ed77e | /sortandusing.cbl | 27 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| cc95ff7b5b | /CPBCO005.cbl | 10 | free | 0 |  |  |  |  |  |  |
| 90dc452f77 | /py070071.cbl | 118 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-2002 |
| 10c6ab469c | /PW01316C.cbl | 403 | fixed | 4 |  |  | gnucobol | banking-finance | online-cics | COBOL-85 |
| 1a5e5860ab | /CPBD469KUS.cbl | 23 | fixed | 0 |  |  |  |  |  |  |
| 722954c235 | /HellloCoboll.cbl | 7 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 461dc02444 | /ph070121.cbl | 298 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| 2ed721cd27 | /TRADER9.cbl | 66 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| ba01fa7c9e | /search.cbl | 112 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| c281d72aaf | /AOC04A.cbl | 92 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 7169494d83 | /CPBD026GRZ.cbl | 41 | fixed | 0 |  |  |  |  |  |  |
| 583f6ed962 | /pw02499c.cbl | 383 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| aa8d25af65 | /RelationCombinedGreaterOr.c | 4 | unknown | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 9dba1a25b9 | /CGPRG004.cbl | 93 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| d627895a56 | /BCE618.cbl | 245 | fixed | 4 | ✓ |  | gnucobol | retail-commerce | batch | COBOL-85 |
| cb7251f285 | /assign_var.cbl | 96 | fixed | 4 |  |  | gnucobol | education-tutorial | subprogram | COBOL-2014 |
| 824b444097 | /ACBACSLSTS.cbl | 477 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| babcdb7e85 | /CPBD098HKJ.cbl | 18 | fixed | 0 |  |  |  |  |  |  |
| 8435f1ede6 | /ExecSqlWithAlterSequence.rd | 32 | fixed | 3 | ✓ |  | ibm-mainframe | test-suite | test | COBOL-85 |
| 1eb9dec477 | /crp058.cbl | 649 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 0cf41bcd05 | /lbp201.cbl | 498 | fixed | 4 |  |  | micro-focus | healthcare-medical | online-cics | COBOL-85 |
| 72ac2da99a | /euler-problem-001.cbl | 17 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| fa89c610b4 | /pl900.cbl | 113 | free | 4 |  |  | gnucobol | accounting-erp | subprogram | COBOL-85 |
| 1126abf846 | /[Spider-Man] 27 - The Early | 44 | free | 0 |  |  |  |  |  |  |
| 73f3e2fff3 | /EIRemarksRemoveLevel01.rdz. | 11 | fixed | 3 |  |  | ibm-mainframe | demo-example | test | COBOL-85 |
| ead5da269a | /[Marvel] Messiah War (WEB-C | 29 | free | 0 |  |  |  |  |  |  |
| 9245af70b9 | /IF119A.cbl | 756 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| 7f9f768198 | /DCRCVE.cbl | 34 | fixed | 4 |  |  | ibm-mainframe | other | online-cics | COBOL-85 |
| e7f9266c48 | /CARTAO.cbl | 377 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| 07e0ba395a | /einfacherTaschenrechner.cbl | 16 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 383c36793a | /CICSCON0.cbl | 156 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| a6ea16f415 | /sqlenv.cbl | 854 | fixed | 0 | ✓ |  |  |  |  |  |
| bba7807c9e | /UVSON.cbl | 433 | fixed | 4 |  |  | acucobol | other | online-cics | COBOL-85 |
| 4e6690b942 | /hello.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 0a284dba8d | /Syracuse.cbl | 30 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 6dd1c35876 | /ox.cbl | 160 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 61cdb6a47a | /SELECT.cbl | 2 | free | 0 |  |  |  |  |  |  |
| 3a49873835 | /solution.cbl | 14 | fixed | 2 |  |  | gnucobol | demo-example | subprogram | COBOL-85 |
| 1364c89d5c | /EqualOr.cbl | 7 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 2fcf2e8d8c | /lista5e2.cbl | 24 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| b843798db1 | /PROG_TESTE_11.cbl | 27 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 2d3828b1db | /HELLO.cbl | 9 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| dc7e37b45d | /write-score1.cbl | 47 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 982665ce29 | /KEYS404.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 20034217a2 | /CPBD111HTR.cbl | 10 | free | 0 |  |  |  |  |  |  |
| 51b3858084 | /Listing 7-2  Reading the Em | 37 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 523897736c | /IC227A.cbl | 852 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| c40b6dd7c3 | /flightlog.cbl | 3798 | free | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| 6974257b93 | /pwpe0388.cbl | 327 | fixed | 4 |  |  | other-vendor | retail-commerce | online-cics | COBOL-85 |
| 49f150fe83 | /Program1.cbl | 881 | fixed | 3 | ✓ |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 049014181f | /EL341CI.cbl | 581 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| c2d95c20d1 | /ga0100.cbl | 2923 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| dc3e2c7789 | /Ex31.cbl | 27 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 0ed4db3d7f | /control3.cbl | 33 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 4a129da91f | /toolchaintest.cbl | 58 | fixed | 0 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 5d45562de0 | /pw01452c.cbl | 369 | fixed | 4 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| 70361799b1 | /Consult.cbl | 202 | fixed | 2 | ✓ |  | gnucobol | retail-commerce | batch | COBOL-85 |
