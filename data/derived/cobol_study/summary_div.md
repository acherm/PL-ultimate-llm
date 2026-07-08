# COBOL-in-SWH exploratory study — summary

_Generated 2026-07-08T05:40:34Z · 1000 samples (975 text, 25 non-text), 896 LLM-judged._

## Lines of code (code lines, excl. blank/comment)

- min **0** · median **48** · mean **188.1** · max **24137** · total **183362**

## Source format (mechanical heuristic)

- fixed: 853
- free: 88
- unknown: 34

## Feature prevalence (mechanical, over text files)

- EXEC SQL: 39 (4.0%)
- EXEC CICS: 49 (5.0%)
- COMP-3: 61 (6.3%)
- COPY: 125 (12.8%)
- CALL: 130 (13.3%)

## Is COBOL? (judge)

  - true: 896 (100.0%)

## Dialect family (judge)

  - gnucobol: 370 (41.3%)
  - unknown: 331 (36.9%)
  - ibm-mainframe: 134 (15.0%)
  - micro-focus: 36 (4.0%)
  - other-vendor: 15 (1.7%)
  - rm-cobol: 4 (0.4%)
  - fujitsu-nec: 3 (0.3%)
  - acucobol: 3 (0.3%)

## COBOL standard (judge)

  - COBOL-85: 861 (96.1%)
  - COBOL-2002: 13 (1.5%)
  - unknown: 11 (1.2%)
  - COBOL-2014: 7 (0.8%)
  - COBOL-74: 4 (0.4%)

## Source format (judge)

  - fixed: 781 (87.2%)
  - free: 110 (12.3%)
  - tab: 2 (0.2%)
  - mixed: 2 (0.2%)
  - unknown: 1 (0.1%)

## Domain (judge)

  - education-tutorial: 430 (48.0%)
  - demo-example: 221 (24.7%)
  - banking-finance: 48 (5.4%)
  - retail-commerce: 48 (5.4%)
  - utility-tooling: 47 (5.2%)
  - other: 22 (2.5%)
  - test-suite: 20 (2.2%)
  - accounting-erp: 14 (1.6%)
  - payroll-hr: 13 (1.5%)
  - manufacturing-logistics: 9 (1.0%)
  - healthcare-medical: 9 (1.0%)
  - insurance: 6 (0.7%)
  - government-public: 6 (0.7%)
  - unknown: 3 (0.3%)

## Program type (judge)

  - demo: 438 (48.9%)
  - batch: 308 (34.4%)
  - subprogram: 56 (6.2%)
  - online-cics: 56 (6.2%)
  - test: 32 (3.6%)
  - unknown: 5 (0.6%)
  - copybook: 1 (0.1%)

## Maturity (judge)

  - student-exercise: 541 (60.4%)
  - toy-or-hello-world: 184 (20.5%)
  - production-like: 129 (14.4%)
  - snippet: 42 (4.7%)

_Judge tokens: 3297205 prompt + 382341 completion._

## Samples

| sha1_git | file | LOC | fmt | divs | SQL | CICS | family | domain | type | std |
|---|---|---:|---|---:|:-:|:-:|---|---|---|---|
| 341b9f1233 | /array.cbl | 41 | fixed | 4 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| e404b4d3a4 | /control-break3.cbl | 101 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| daf67fc654 | /gerirEmpregados.cbl | 446 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 0b26274b06 | /area.cbl | 28 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 292dfbd7c7 | /subprog.cbl | 25 | fixed | 3 |  | ✓ | ibm-mainframe | other | subprogram | COBOL-85 |
| ffc0c416f5 | /index.cbl | 36 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 227c51d142 | /read.cbl | 25 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 23920cf757 | /DB2CBLEV.cbl | 216 | fixed | 4 | ✓ |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 67f5768ba9 | /helloworld.cbl | 10 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 974ef28c0b | /hello.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 5a5875481f | /Z95642.CBL(CBLWRK2).cbl | 86 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| f79d4ca4a0 | /candy_sale.cbl | 48 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 3414c50970 | /CALL370.CBL | 22 | fixed | 3 |  |  | gnucobol | test-suite | test | COBOL-85 |
| bf150e60c7 | /DTAR020.cbl | 15 | fixed | 0 |  |  |  |  |  |  |
| 52c19f0308 | /DS.cbl | 25 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| f1ed2362d7 | /U10-PE-ASI01.cbl | 53 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| d0f4ff57a4 | /HELLO.cbl | 11 | fixed | 3 |  | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| d0b8ecf02d | /twosum.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| de5ace172f | /chingoon.cbl | 36 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 28e764e46c | /CBL2JAVA.cbl | 170 | fixed | 4 |  |  | ibm-mainframe | other | online-cics | COBOL-85 |
| b8ec0ecf6f | /trader.cbl | 9 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 3ab2e818fa | /blackjack.cbl | 48 | fixed | 0 |  |  | unknown | demo-example | demo | COBOL-85 |
| 037b1f1c8a | /Program1.cbl | 116 | fixed | 3 | ✓ |  | micro-focus | banking-finance | batch | COBOL-85 |
| 57b19b2f37 | /Loteria.cbl | 338 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| f1f8a5ea9f | /Form1.cbl | 9 | fixed | 1 |  |  |  |  |  |  |
| 4f8406c9d0 | /first_cobol_conditionals.cb | 42 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 636d8fde7f | /Program1.cbl | 257 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| df43ecc94f | /PRUEBA-SORT-ID.cbl | 207 | fixed | 4 |  |  | unknown | banking-finance | batch | COBOL-85 |
| 17b1600c76 | /edit5.cbl | 30 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 38a6ec20eb | /insert_job.cbl | 48 | fixed | 2 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 153c434fa7 | /hello.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | unknown |
| 43bc668068 | /ArrayDep2.cbl | 11 | fixed | 0 |  |  |  |  |  |  |
| 577257acb9 | /hidoku.cbl | 350 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 42cbeced4b | /read.cbl | 18 | free | 4 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 8ecf1515e2 | /lista16exercicio2.cbl | 299 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 85463dfb7d | /beg_pgmz_Coughlan_Ch17.cbl | 126 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 3a5a4ec5f3 | /HelloWorld.cbl | 12 | fixed | 3 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| 7d1c4d47c4 | /Solution.cbl | 20 | free | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| ee0578b617 | /testdb2.cbl | 155 | fixed | 2 | ✓ |  | ibm-mainframe | retail-commerce | test | COBOL-85 |
| 18c5000e1a | /NGUYEN-P04-MSTR-TRANS.cbl | 137 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 4d32fed3f2 | /Triangle-2.cbl | 33 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d5e03fa8b6 | /Program1.cbl | 82 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | batch | COBOL-85 |
| ab82006582 | /AddNums.cbl | 28 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 689a64a00f | /Program1.cbl | 15 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 3f498a4f03 | /Program1.cbl | 23 | fixed | 2 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| 6839d2b172 | /TEST1.CBL | 116 | fixed | 4 |  |  | fujitsu-nec | other | subprogram | COBOL-85 |
| 03a6b109ad | /location-analysis.cbl | 44 | fixed | 4 | ✓ |  | unknown | banking-finance | batch | COBOL-85 |
| 6f0f1efaf9 | /TESTCMP1.CBL | 633 | fixed | 4 |  |  | gnucobol | utility-tooling | test | COBOL-85 |
| dbc51a2ea5 | /add.cbl | 23 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 5c0e415ae1 | /TESTPRG.CBL | 229 | fixed | 4 |  |  | gnucobol | banking-finance | test | COBOL-85 |
| 4acdd8174f | /edit4.cbl | 16 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 86a5a42879 | /proof.ci.cbl | 8 | fixed | 0 |  |  | unknown | demo-example | demo | COBOL-85 |
| 41b204f8b6 | /day1.cbl | 113 | free | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 7942f1c5a0 | /SALEREPORT.CBL | 93 | fixed | 3 |  |  | ibm-mainframe | retail-commerce | batch | COBOL-85 |
| 61b01107a1 | /COBOL.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 1abca2d131 | /holaMundo.cbl | 9 | fixed | 2 |  |  | unknown | demo-example | demo | unknown |
| 8475093fa9 | /learning7.cbl | 23 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 7e6a851c1c | /dressprt.cbl | 63 | fixed | 4 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-74 |
| 38c57237c5 | /Third.cbl | 18 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 583d3176ee | /SP2TEST.cbl | 89 | fixed | 4 |  |  | micro-focus | demo-example | test | COBOL-85 |
| 98864fdb65 | /DATABASE.cbl | 56 | fixed | 4 |  |  | unknown | manufacturing-logistics | subprogram | COBOL-85 |
| 9e67eb206a | /COBOL.cbl | 30 | free | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| a52b57824d | /frmArchivoSecuencial.cbl | 69 | fixed | 1 |  |  |  |  |  |  |
| 0ac4e355cf | /ENTER-ACCOUNT.cbl | 45 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 5da3983a02 | /run_game.cbl | 174 | fixed | 4 |  |  | gnucobol | demo-example | subprogram | COBOL-85 |
| 817893cc9a | /WeAre.cbl | 10 | free | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 19588a4883 | /PROJETO CIFRA DE CESAR.cbl | 277 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 89a14aee07 | /ExpenseReport.cbl | 56 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 0cf05560fc | /read-emp.cbl | 40 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 92975448cc | /calc.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | unknown |
| 316959db6b | /ingresoEstudiante.cbl | 58 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 94ceac1b1f | /FinalProject-ValidData.cbl | 233 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 41b66d3567 | /Pro1.cbl | 191 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 22eac18266 | /pizza.cbl | 146 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 30404ce4c5 | /cobol.b7b1e314614c.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9712f68166 | /test.cbl | 4669 | fixed | 4 | ✓ |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 2c2d9ea22b | /EX01.CBL | 28 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 102a8bf289 | /TP08-CALC-SAL-LIQUIDO.cbl | 56 | fixed | 4 |  |  | gnucobol | payroll-hr | subprogram | COBOL-85 |
| e71ef44ebc | /utilBreadDelRecs.cbl | 128 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | batch | COBOL-85 |
| 51981f6e74 | /LOANAMORTSCREENS.cbl | 51 | fixed | 4 |  |  | micro-focus | banking-finance | online-cics | COBOL-85 |
| 52ae82158e | /solution-1a.cbl | 42 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 00a2cd4ab9 | /100Prisoners.cbl | 68 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 28b5d64ce6 | /StoprunGobackLastStatement. | 26 | fixed | 1 |  |  |  |  |  |  |
| a86fc23371 | /Desafio.Loteria.cbl | 249 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 704e6c20e8 | /HELLO.cbl | 14 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| bf07fddedb | /helloworld.cbl | 13 | fixed | 2 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 520a60acc2 | /go.cbl | 12 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| e85942111e | /æ®å±ççæ­»æ£å.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| 93c432ef6c | /DHWSAVE.cbl | 522 | fixed | 3 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-85 |
| 63bbf6dddd | /helloworld.cbl | 13 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 0666420c5f | /ox.cbl | 158 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 3860a962ef | /FizzBuzz.CBL | 41 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 3aa64bb1bf | /sample_34_screen.cbl | 46 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| a486655920 | /Project1.cbl | 53 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 803e24454f | /cadcli.cbl | 282 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| d7c6bf6e0d | /challenge.cbl | 39 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 171a47eee8 | /ABAP_NESTEDLOOP_EXAMPLE.cbl | 16 | unknown | 0 |  |  |  |  |  |  |
| 276284e9c4 | /MyGrade.cbl | 66 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| ecc10cb43b | /MARBLE11.cbl | 286 | fixed | 4 | ✓ | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| 2fdefde8a5 | /part1.cbl | 74 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 09e29f8825 | /progvar.cbl | 37 | fixed | 0 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1223998bf4 | /bankstatementsave.cbl | 85 | fixed | 4 |  |  | gnucobol | banking-finance | subprogram | COBOL-85 |
| 36e5d5e821 | /PersonDetection.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| a8a935873d | /CBL0004.cbl | 115 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| ff7ef55554 | /TEST01.cbl | 140 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 623dbbbe91 | /BirthDateProgram.cbl | 19 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| bf250ce994 | /HolaMundo.cbl | 8 | free | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| a5f17d84c9 | /section.cbl | 22 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| 14211c9ed3 | /A3-SalesComm.cbl | 224 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 1f21d73761 | /lista11ex3indexado.cbl | 356 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| bbb6460f12 | /HelloCobol.cbl | 7 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 9e74953d4f | /ENEB006.cbl | 19 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 2b87263b61 | /Z92415.CBL(SAMPANEL).cbl | 29 | fixed | 4 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 79f716c7c8 | /star-10-2.cbl | 23 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| daa2fabcb5 | /Train.CBL | 218 | fixed | 0 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 2c4ab653be | /calculate-average-grade.cbl | 31 | unknown | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 3312641535 | /any7dev.cbl | 124 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 06f1ab1690 | /world.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 2c29f246f3 | /MENSFEC.cbl | 44 | fixed | 0 |  |  |  |  |  |  |
| 0daa100cec | /picob_nojcl.cbl | 27 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 734d764aee | /CGZUNIT.cbl | 136 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 55b890a05c | /create_phone_number.cbl | 11 | fixed | 3 |  |  | unknown | demo-example | subprogram | COBOL-85 |
| d2dca37f03 | /VSAMTODB.cbl | 153 | fixed | 4 | ✓ |  | ibm-mainframe | other | batch | COBOL-85 |
| 6785506388 | /hello.cbl | 36 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 1a9e18ebdc | /MPCITI06.cbl | 337 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 00bc41ea77 | /compare.cbl | 17 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 079ae0272e | /HelloWorld.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 056d6e77f0 | /star-10.cbl | 28 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 0ae115db6d | /CBUP0003.cbl | 155 | fixed | 4 |  |  | gnucobol | test-suite | subprogram | COBOL-85 |
| 8d715e60af | /epscmort.cbl | 180 | fixed | 4 | ✓ | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| 55eba1acbb | /Program1.cbl | 143 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| fb45342253 | /dtehr.cbl | 46 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 8dfb7e17c1 | /hello.cbl | 6 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| ad8127a87c | /epscsmrd.cbl | 3886 | fixed | 3 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| 8534ffb04d | /cortes_01.cbl | 172 | fixed | 3 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| be8549b50a | /PROG01.cbl | 46 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 588dd82cd3 | /github.cbl | 6 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 331662989b | /SUBPROGR.CBL | 217 | fixed | 1 |  |  | ibm-mainframe | education-tutorial | subprogram | COBOL-85 |
| 6ed5b643b7 | /Thea.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| f88c9ea503 | /Program8.cbl | 34 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| a8d3b65907 | /EDGD1CLQ.cbl | 392 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| a631735e53 | /ex01.cbl | 92 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 16712b75c0 | /ATUALIZA-FORNECEDORES.cbl | 123 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| ef2f19e790 | /eqmsqlda.cbl | 74 | fixed | 0 |  |  |  |  |  |  |
| 5204a0664d | /test.cbl | 5 | fixed | 3 |  |  | unknown | unknown | unknown | unknown |
| 8726d39b5e | /View_Vendors.cbl | 44 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 0e8c9171bb | /ABX02100.cbl | 50 | fixed | 0 |  |  |  |  |  |  |
| d64e79df16 | /esPrimo.cbl | 33 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| f57908a8f6 | /main.cbl | 34 | free | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 725cf26494 | /COBOL.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 948e6da6c9 | /Program1.cbl | 141 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| ee1870362f | /UNEMP.cbl | 392 | fixed | 4 |  |  | gnucobol | government-public | batch | COBOL-85 |
| e6fbce33b3 | /Tmois.cbl | 101 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1dd49a8eb1 | /READFILE.CBL | 62 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 2f94381588 | /simple.cbl | 25 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 2a1d6668e9 | /New.cbl | 32 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 4fb93aada3 | /Cobol_HelloWorld.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 1df792502b | /string.cbl | 65 | free | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 55f24b2b77 | /checkers.cbl | 369 | fixed | 4 |  |  | other-vendor | demo-example | demo | COBOL-85 |
| 904b8f4b4f | /Rockey4Example.cbl | 239 | fixed | 3 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| e53ed1c135 | /write-emp1.cbl | 46 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| dd97cf7f6c | /Media.cbl | 57 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1317bd71b7 | /edit1.cbl | 36 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d1a100071a | /INSERTTBL.cbl | 126 | fixed | 3 | ✓ |  | gnucobol | demo-example | demo | COBOL-85 |
| 757bb5ed5a | /write-emp1.cbl | 46 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 0add7297e7 | /read-emp1.cbl | 39 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| ad8d5b7206 | /CICS2ZCX.cbl | 78 | fixed | 3 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| 9507382324 | /a.cbl | 6 | fixed | 2 |  |  | unknown | demo-example | demo | unknown |
| eec11d0883 | /bitwise.cbl | 41 | fixed | 3 |  |  | gnucobol | utility-tooling | subprogram | COBOL-2002 |
| c33b19d610 | /PROGMENU.cbl | 761 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| a458b24b80 | /Final.cbl | 81 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 0f34e4b235 | /hello.cbl | 5 | fixed | 2 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 6b25bf1a38 | /prg.cbl | 7 | free | 0 |  |  |  |  |  |  |
| 27f8e34f86 | /test.cbl | 11 | fixed | 3 |  |  | gnucobol | demo-example | test | COBOL-85 |
| b8f8c575c9 | /hello.cbl | 8 | fixed | 4 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 684bdedc98 | /day6ac.cbl | 22 | unknown | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| ca2ee3f371 | /PAYROL0X.cbl | 25 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| f0b055c0b1 | /shop_receipts.cbl | 55 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 6b9f0d730b | /COBOLCaesarCipher.cbl | 184 | free | 4 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| 2f79e45510 | /two_dim.cbl | 22 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| a8cbfb5e63 | /test.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 346969e868 | /file-exists.cbl | 32 | free | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| 96a94c328a | /Registratie_deelnemers.CBL | 216 | fixed | 4 | ✓ |  | gnucobol | education-tutorial | batch | COBOL-85 |
| cbabaaa4b3 | /main.cbl | 35 | fixed | 0 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| c83d6899a4 | /hellow65_multi_dimensional_ | 42 | fixed | 3 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| 9f9b126509 | /NGUYEN-P04-MAILING-LABELS.c | 97 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 736604f75e | /member.cbl | 84 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 32d21f79ae | /control-break1.cbl | 57 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 8340aa6d17 | /LOANPYMT.cbl | 151 | fixed | 3 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| f1924507a9 | /Loteria.cbl | 150 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 01ae25b454 | /CobolAssignment2-COMP210.cb | 145 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 24a392c4b3 | /aws_cobol.cbl | 102 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 940918a77b | /TEST.cbl | 37 | fixed | 4 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-85 |
| fff6cd8d08 | /AirportDetails.cbl | 7 | fixed | 0 |  |  |  |  |  |  |
| 3c1d1f7dd7 | /test0001.cbl | 104 | fixed | 4 |  |  | gnucobol | demo-example | test | COBOL-2014 |
| 607100bd1d | /Z95626.CBL(ODEV).cbl | 61 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 1115d93ad8 | /FINALEX.cbl | 474 | fixed | 4 |  |  | ibm-mainframe | manufacturing-logistics | batch | COBOL-85 |
| 454150b3e0 | /processCsv.cbl | 131 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 2075bd1073 | /test.cbl | 47 | fixed | 3 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 1663dd64a3 | /calculator.cbl | 29 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 7cca29a69e | /HelloWorld.cbl | 6 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 71e49f797b | /adventure.cbl | 122 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-2002 |
| e57112c964 | /TP3.cbl | 379 | fixed | 3 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 4ce4a199ac | /SAM1.cbl | 389 | fixed | 4 |  |  | ibm-mainframe | demo-example | batch | COBOL-85 |
| ed4f7cc898 | /PGMAPA99.cbl | 390 | fixed | 0 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| e8972a7556 | /naoLib.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 36844ddd18 | /MONTHINC.CBL | 244 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 773a872f2c | /HELPPGM.CBL | 3215 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| 1aceedab78 | /2393.cbl | 18 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| f8d578ed91 | /TestAIRCODE.cbl | 125 | fixed | 1 |  |  | micro-focus | demo-example | test | COBOL-85 |
| d5a58d3e8b | /excercise.cbl | 20 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1b0611c98e | /Listing12-3.cbl | 22 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 5ef6bdc501 | /ensyu1.cbl | 93 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 8ba0b23c35 | /megasena.cbl | 382 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 142562280e | /animation libraries.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 5a25c1f00a | /mygrade.cbl | 30 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| e0922439d7 | /hello-world.cbl | 4 | free | 2 |  |  | unknown | demo-example | demo | unknown |
| 08390b7732 | /CONTOH3.cbl | 14 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 6a2c1766cc | /Edit1.cbl | 37 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 975ee57b99 | /prog.cbl | 13 | fixed | 0 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 89f848c481 | /tempCodeRunnerFile.cbl | 1 | fixed | 0 |  |  |  |  |  |  |
| 4ef89ae8e6 | /HelloWorld.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| d7128cd8d0 | /pi.cbl | 76 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| deee7df11d | /control-break2.cbl | 77 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 0e776abc84 | /reportMember.cbl | 85 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 49ff283ff0 | /cat.cbl | 15 | fixed | 3 |  |  | unknown | utility-tooling | demo | COBOL-85 |
| a7adc2e42d | /Box library.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 37593c371a | /test.cbl | 11 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 39e2d4a324 | /eco9ban.cbl | 1680 | fixed | 2 |  |  | micro-focus | accounting-erp | subprogram | COBOL-85 |
| ef9b1f664b | /mygrade.cbl | 117 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 88b8967569 | /readData.cbl | 85 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| b9ec8edc8a | /cobol.cbl | 6 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 7a4f6e1459 | /one_dim_init.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 74f5377af5 | /Calculadora.cbl | 39 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| eaf973e1e2 | /ENRIQUEZ.cbl | 69 | fixed | 3 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 5835c272e3 | /Exercicio2.cbl | 97 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 726f81feb7 | /control-break1.cbl | 58 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| f316cfbd39 | /Perform3.CBL | 38 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b5168d54d7 | /sendgrid_demo.cbl | 9 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 84dc7ee980 | /01.cbl | 5 | fixed | 0 |  |  |  |  |  |  |
| 06c931b6e9 | /Data1.cbl | 15 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| da8e7d55ba | /control-break3.cbl | 98 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 87829b68f6 | /HelloWorld.cbl | 10 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 411a21b6e6 | /cobol.cbl | 51 | fixed | 4 |  | ✓ | ibm-mainframe | other | online-cics | COBOL-85 |
| 8f4a26db6e | /cobol.cbl | 38 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 3de3f30a1d | /Data5.cbl | 72 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 34cc5db4aa | /EX04-AULA04.cbl | 38 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 11845a7b76 | /06_UNSTRING1.cbl | 12 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| eb6f4f1c46 | /gnucobol.cbl | 105 | free | 0 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 51de1b4bd8 | /exercicio-16.cbl | 20 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 92e7df7694 | /NSA01.cbl | 4342 | fixed | 4 |  | ✓ | ibm-mainframe | government-public | online-cics | COBOL-85 |
| af612ade64 | /ZBNKPRT2.cbl | 119 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 113e3da0ac | /LOANAMORTSCREENS.cbl | 52 | fixed | 4 |  |  | micro-focus | banking-finance | online-cics | COBOL-85 |
| 346b7211a5 | /Wanda1.CBL | 828 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| ebe6d49ef2 | /MonoChrome.cbl | 427 | fixed | 4 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| 190c818294 | /prog01.cbl | 7 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| bf3b2a9f02 | /EX-OPCOES-CONSISTENCIA.cbl | 21 | fixed | 0 |  |  |  |  |  |  |
| 1be9ccc2d5 | /autosetup.cbl | 165 | fixed | 3 |  |  | micro-focus | utility-tooling | subprogram | COBOL-85 |
| 3029a394a7 | /Programa-MostrarLista.cbl | 58 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 879e11c4a3 | /cobchangestr.cbl | 14 | fixed | 3 |  |  | gnucobol | demo-example | subprogram | COBOL-85 |
| dd46ff7cd4 | /sampe-cobol-code.cbl | 78 | fixed | 3 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| e559789818 | /test2.cbl | 17 | free | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 30136b7fc6 | /ArqSequencial-Sort.cbl | 208 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| a5627ec6a0 | /RHBCLI01.CBL | 1155 | fixed | 4 |  |  | micro-focus | retail-commerce | batch | COBOL-85 |
| 73367c5b78 | /athlete.cbl | 15 | fixed | 0 |  |  |  |  |  |  |
| 9680a854c8 | /HELLO2.cbl | 11 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 6bca4edb2d | /UTIL0.cbl | 21 | fixed | 3 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| 3325a2c939 | /restaurante.cbl | 242 | fixed | 4 |  |  | gnucobol | retail-commerce | demo | COBOL-85 |
| d35e2b297a | /cobol.cbl | 29 | unknown | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| e44b8b9275 | /epsmlist.cbl | 178 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 729b8eba9f | /CBLKLM04.cbl | 502 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 84bc4486b5 | /TheRealDeal.cbl | 9 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 087720af22 | /main_app.cbl | 42 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 7851afc239 | /Program1.cbl | 26 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 689a0c7aae | /epscmort.cbl | 204 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 459f40652c | /ZBNKE35.CBL | 112 | fixed | 4 |  |  | micro-focus | utility-tooling | subprogram | COBOL-85 |
| 6869c0247d | /hie.yaml.cbl | 37 | fixed | 0 |  |  |  |  |  |  |
| 5658cd5999 | /two_dim.cbl | 22 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| dca70422f9 | /testingdb2.cbl | 60 | fixed | 2 | ✓ |  | ibm-mainframe | retail-commerce | batch | COBOL-85 |
| 55250b08d5 | /epsmlist.cbl | 178 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| dbdcba8a42 | /TSQL005A.cbl | 81 | fixed | 3 | ✓ |  | gnucobol | test-suite | test | COBOL-85 |
| f585f5d52a | /INTVENDR.cbl | 626 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 2fbf62a123 | /asmzx.cbl | 440 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| bcb7ee424a | /solve.cbl | 28 | fixed | 3 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| b4acf83aad | /SAM1.cbl | 389 | fixed | 4 |  |  | ibm-mainframe | demo-example | batch | COBOL-85 |
| d1376f8ea9 | /new-gilded-rose.cbl | 76 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 6e0f967364 | /Test1.cbl | 6 | fixed | 0 |  |  |  |  |  |  |
| 27605d7afa | /PROG01.cbl | 18 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 689d41e8e2 | /tempo.cbl | 237 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| abc5b5a625 | /sampprog_expand.cbl | 27 | fixed | 4 |  | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| b9eb3df0f4 | /Control2.cbl | 36 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 0ae7109e78 | /C06E02.cbl | 21 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| bbb76b3208 | /fuente.cbl | 103 | fixed | 4 |  |  | gnucobol | retail-commerce | demo | COBOL-85 |
| ae4081b079 | /Personal-info.cbl | 175 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| e3365e576a | /VALIDABOOK.cbl | 29 | fixed | 0 |  |  |  |  |  |  |
| 28003903f4 | /PROJ2023.cbl | 132 | fixed | 3 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 2db0dd4d68 | /CobolGreeting.cbl | 11 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| a9bdcb7a9c | /ac2302p2.cbl | 105 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 672e76a871 | /MAXIMINI.cbl | 24 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| dde13792d6 | /assis.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 17dccb0bce | /LAB7MultiBreak.cbl | 231 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 42d5afeed0 | /P0001.cbl | 11 | free | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 4de8a8b905 | /parouimpar.cbl | 16 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 92b92399f4 | /f-ckdate.cbl | 56 | fixed | 4 |  |  | unknown | utility-tooling | subprogram | COBOL-85 |
| ef92f6f510 | /SAM1.cbl | 447 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 78f3ccdb66 | /Calculadora.cbl | 37 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 5b8ab2d1dd | /payroll.cbl | 322 | fixed | 4 | ✓ |  | ibm-mainframe | payroll-hr | batch | COBOL-85 |
| 46f99d3c8e | /modemp.cbl | 174 | fixed | 4 |  |  | unknown | payroll-hr | batch | COBOL-85 |
| 7c117d6487 | /PlusTwoNumber.cbl | 15 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 245435fca5 | /DAMARP01.cbl | 96 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 29e3a76eb3 | /edit1.cbl | 36 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 6d7503d529 | /ryder-demo-file.cbl | 5 | fixed | 0 |  |  |  |  |  |  |
| b74a55b805 | /MDSMSDUS.CBL | 532 | fixed | 4 |  |  | unknown | demo-example | subprogram | COBOL-85 |
| 2ee70e7da1 | /BAC00110.cbl | 24137 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 1a667b4f0f | /Hello.cbl | 5 | free | 2 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| c8991c0c99 | /hello.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| bf9a5dea63 | /DB2PGM3.CBL | 140 | fixed | 4 | ✓ |  | ibm-mainframe | retail-commerce | batch | COBOL-85 |
| fa61b1a063 | /brainfuck.cbl | 134 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-2002 |
| 8decbdee2c | /calculator.cbl | 45 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 74dc4fb8f5 | /Control7.cbl | 40 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| dd8097a55e | /data-input-example.cbl | 25 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 6b46eaa886 | /puzzle.cbl | 18 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| c005f9ef14 | /CUNA_util01.cbl | 167 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 98b5f38950 | /TEST1.cbl | 7 | free | 1 |  |  |  |  |  |  |
| 8d4832710f | /PAY9.CBL | 275 | fixed | 4 |  |  | other-vendor | payroll-hr | batch | COBOL-85 |
| 8daf396688 | /CL15EJ02.v.1.1.cbl | 231 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| ad0b649514 | /TestLOANAMORT.cbl | 56 | fixed | 1 |  |  | micro-focus | banking-finance | test | COBOL-85 |
| 149d19db0b | /Lista7E4.cbl | 187 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 89e5009337 | /CobolExample.cbl | 22 | fixed | 0 |  |  |  |  |  |  |
| 0f9863fcf9 | /FACTURAS.CBL | 270 | fixed | 4 |  |  | rm-cobol | accounting-erp | batch | COBOL-85 |
| 8d30579c68 | /shop_receipts.cbl | 55 | fixed | 3 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| efa179533f | /primeiro arquivo.cbl | 2 | free | 0 |  |  |  |  |  |  |
| e2741c6e07 | /PARSESEG-PAR-EX.cbl | 58 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-2002 |
| ce87c6f20f | /EX5-1-1F.cbl | 117 | fixed | 4 |  |  | fujitsu-nec | education-tutorial | test | COBOL-85 |
| 3f5da790e0 | /read-emp1.cbl | 39 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| ba0d0eaf11 | /vary_size.cbl | 34 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| df0bc007ec | /F0.cbl | 98 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 362665b4aa | /battle.cbl | 54 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 9eb4db3228 | /shop_receipts_footer.cbl | 83 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 4cc7555233 | /LGICDB01.cbl | 144 | fixed | 4 | ✓ | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 372b46c8aa | /Custmnt2.cbl | 493 | fixed | 4 |  | ✓ | ibm-mainframe | retail-commerce | online-cics | COBOL-85 |
| 60775efb37 | /demo01.cbl | 52 | fixed | 0 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 6b89b22a02 | /Control2.cbl | 36 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 488535874d | /Multiplier.cbl | 17 | unknown | 3 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| f0f512908b | /cal.cbl | 49 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d12b2459ae | /samplel.cbl | 150 | fixed | 3 |  |  | gnucobol | test-suite | test | COBOL-85 |
| f254c26d35 | /MAIN.CBL | 124 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| d9fcc84114 | /whse_cbl.cbl | 8 | unknown | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| cc1d7959ec | /Ex1_P1.cbl | 41 | fixed | 2 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| c07d81515d | /SALE_REPORT.cbl | 76 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 05a053daa1 | /DF27TEST.CBL | 74 | fixed | 4 |  |  | ibm-mainframe | demo-example | test | COBOL-85 |
| cb1d0878a4 | /printname.cbl | 9 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| afa6299554 | /EPICTURE.cbl | 7 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 7df59b1456 | /CWXTCOB.cbl | 508 | fixed | 4 |  |  | ibm-mainframe | demo-example | batch | COBOL-85 |
| 15d397bc33 | /vary_size.cbl | 36 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| bc1c45e1be | /TrabLP.cbl | 194 | fixed | 3 |  |  | gnucobol | banking-finance | demo | COBOL-85 |
| e99d1ca715 | /member.cbl | 84 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| a0f6d0581d | /TCC.cbl | 253 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| a725cffa3b | /app.cbl | 35 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| bfec33cfde | /MUNICI.CBL | 201 | fixed | 4 |  |  | gnucobol | government-public | batch | COBOL-85 |
| 8e55b91425 | /ConditionNames.cbl | 27 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 5db13a5542 | /ox.cbl | 140 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 352abf1fa1 | /OBNC1M.CBL | 735 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| cd75813a31 | /one_dim.cbl | 29 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 2eb952614e | /playpen.cbl | 23 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 55acd921e0 | /Program2.cbl | 51 | fixed | 4 |  |  | other-vendor | education-tutorial | subprogram | COBOL-85 |
| 2e9c42da81 | /payroll.cbl | 40 | fixed | 3 |  |  | unknown | payroll-hr | demo | COBOL-85 |
| 656d4bcbc3 | /CICS_PROGRAM_SAMPLE.cbl | 450 | fixed | 3 |  | ✓ | ibm-mainframe | other | online-cics | COBOL-85 |
| bfad94e073 | /JVMQUERY.cbl | 182 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| 751bcc3cc5 | /Returns.cbl | 20 | fixed | 3 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 10ce0f6fe8 | /COBOL501.cbl | 360 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| a9aac37b86 | /datbatch.cbl | 19 | fixed | 4 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 80982ea597 | /App.xaml.cbl | 9 | fixed | 1 |  |  |  |  |  |  |
| 353c2419c7 | /ADDUSER.CBL | 114 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| ac28f5453a | /report_member.cbl | 85 | fixed | 4 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| 6ad67bf514 | /helloworld.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| e3791eebd0 | /control-break3.cbl | 100 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 83055e14b6 | /BMI.cbl | 32 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 105c997af7 | /tests.cbl | 68 | fixed | 3 |  |  | gnucobol | test-suite | test | COBOL-85 |
| d16bed5662 | /indici.cbl | 60 | unknown | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| ac2c17794a | /ExpenseReport.cbl | 56 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 5e9e5dbcf0 | /control-break3.cbl | 101 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 5bb3a329f9 | /triangle-1.cbl | 34 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 4be26af688 | /programa1.cbl | 868 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| e1a2db1b65 | /Program1(1).cbl | 6 | fixed | 2 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| f08e3f2a7b | /Exercicio2_1.cbl | 18 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 5b993249a5 | /main.cbl | 8 | fixed | 2 |  |  | gnucobol | demo-example | demo | COBOL-2014 |
| 7b6377b166 | /Control3.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| e6d14abb91 | /HWORK3.cbl | 184 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 1d8560e0ad | /HelloCobal.cbl | 7 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| ab8b0a1fd1 | /helloworld.cbl | 8 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 73ce7a9dd8 | /MissingDigits_Original.cbl | 48 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| e5a1559116 | /TRTMNTR.cbl | 800 | fixed | 4 | ✓ |  | ibm-mainframe | healthcare-medical | batch | COBOL-85 |
| 80cb577e21 | /Edit2.cbl | 15 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 61083c3093 | /Program1.cbl | 45 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| cd90905f3d | /solution.cbl | 78 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 9aaa5513d0 | /Default.cbl | 14 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 744134432d | /fourth.cbl | 27 | free | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 8e358f5137 | /MOVERDISCO.cbl | 23 | fixed | 3 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 276589e65e | /final.cbl | 49 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 866fb4e21d | /TEST.cbl | 80 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| cdfb29c800 | /DataSplitAndCount.cbl | 291 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| f3b12ea242 | /mycontacts.cbl | 65 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| a40a1cd93e | /hello-world.cbl | 6 | fixed | 2 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 93319fea5d | /colendar.cbl | 205 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 0d3ccc4c9c | /CombinationsPermutations.cb | 54 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1bda19c7e5 | /DUNGCRWL.cbl | 428 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| d5b47652ee | /parsetst1.cbl | 133 | fixed | 4 |  |  | acucobol | utility-tooling | test | COBOL-85 |
| 7cd7d0d598 | /day05p2.cbl | 114 | fixed | 0 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 0a1991a663 | /LAB5ARRAYS.cbl | 157 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 57e81262a0 | /noncompliant.cbl | 4 | fixed | 1 |  |  |  |  |  |  |
| c83a20573a | /EX01.CBL | 49 | fixed | 3 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 483dc3da54 | /program.cbl | 18 | free | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 15dfb937d5 | /Movimientos_HomeBanking.cbl | 102 | fixed | 3 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| a6cbeb19a8 | /BmiCalculator.cbl | 18 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| dc2795e89a | /stan.cbl | 420 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| c82a698ffe | /CobaltWorld.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 13ed4d1a4e | /DBBTEST.cbl | 20 | fixed | 4 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| dd268a76c2 | /ms000.cbl | 30 | free | 3 |  |  | gnucobol | utility-tooling | batch | COBOL-2014 |
| 2580b3745d | /EAD62502.CBL | 52 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 484d4127eb | /PruebaCobolVS.cbl | 26 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| bea1b9135d | /ClaveAlterVector.cbl | 207 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| cb94bc3630 | /cobol.cbl | 39 | free | 3 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| 6d116d6449 | /sqrt.cbl | 19 | fixed | 3 |  |  | unknown | education-tutorial | subprogram | COBOL-85 |
| 8a902e970b | /Z95737.CBL(WORK3).cbl | 105 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| ee4d87784c | /lista7e4vsIndexado.cbl | 340 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 6c90c26db9 | /file.cbl | 139 | fixed | 4 | ✓ |  | ibm-mainframe | demo-example | subprogram | COBOL-85 |
| 62b9a44013 | /helloworld.cbl | 10 | fixed | 0 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 3491865128 | /Starac.cbl | 6 | free | 0 |  |  |  |  |  |  |
| 9dc6132c56 | /lista16exercicio2.cbl | 302 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 9322beaa41 | /hello.cbl | 4 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 1223704b37 | /CNTRLBRK.cbl | 350 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| acab36eec2 | /MONTHINC.CBL | 51 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 781ebf5a4d | /assignment3.cbl | 81 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| adefcc9358 | /WRITERES.cbl | 854 | fixed | 4 | ✓ |  | other-vendor | retail-commerce | subprogram | COBOL-85 |
| 3d19927772 | /greetings-from-past.cbl | 11 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 80c04aef6c | /FINALSUB.cbl | 153 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | subprogram | COBOL-85 |
| 7c5bc1f8b8 | /Pi_Calculation.cbl | 19 | free | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-2002 |
| 1561bcaaca | /Edit1.cbl | 36 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 0aca69a384 | /ZFAMPLT.cbl | 95 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| 2eac4f416a | /bjyxgj5.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| 4656ce9d03 | /usage-comp.cbl | 23 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| caf389d7f5 | /CBLRA03.cbl | 269 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 205fbb3e67 | /PRO201.CBL | 313 | fixed | 0 |  |  | ibm-mainframe | other | online-cics | COBOL-85 |
| 7da3d0446a | /hello_col.cbl | 23 | unknown | 4 |  |  | gnucobol | demo-example | demo | COBOL-2014 |
| aed596ec5d | /part1.cbl | 60 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| f0b3cf4377 | /ZECSPLT.cbl | 96 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| e6364cac42 | /data5.cbl | 79 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 38430c33f5 | /part1.cbl | 71 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 88077ce319 | /GETLOAN.cbl | 46 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 1670d3de61 | /main.cbl | 8 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 7d498ec16a | /HelloWorld.cbl | 9 | fixed | 1 |  |  |  |  |  |  |
| 83668e5b82 | /helloWorld.cbl | 6 | free | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 43f8743f55 | /Gestionpaie.cbl | 51 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| 398637bd8b | /LAB4-IF.cbl | 173 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 8535bd9731 | /Data5.cbl | 77 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 544762c82a | /aric492.cbl | 475 | fixed | 4 |  | ✓ | ibm-mainframe | education-tutorial | online-cics | COBOL-85 |
| 5fbd9819d5 | /cbl.cbl | 20000 | unknown | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 5f16aaa23e | /income.cbl | 35 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 082c817c12 | /chall.cbl | 201 | fixed | 4 |  |  | micro-focus | other | demo | COBOL-85 |
| 1d4a24239b | /CLADRILD.cbl | 889 | fixed | 4 | ✓ |  | ibm-mainframe | manufacturing-logistics | batch | COBOL-85 |
| 09af8791c3 | /arr.cbl | 427 | fixed | 3 |  |  | gnucobol | education-tutorial | test | COBOL-85 |
| 0a2aaa5b03 | /suma.cbl | 18 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 099ff19bbb | /GHTML.cbl | 98 | fixed | 4 |  |  | unknown | demo-example | batch | COBOL-85 |
| fa63e9cc7d | /emprestimos.cbl | 248 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 0f9fccb462 | /Principal.cbl | 177 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 8368f0fb1a | /COBOL-1.cbl | 61 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| f638609ba1 | /M2AULA35.cbl | 49 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 56e8d41a4a | /subtraction.cbl | 14 | fixed | 3 |  |  | unknown | education-tutorial | subprogram | COBOL-85 |
| fd0c558cbd | /dN5.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| b5d1df5ace | /helloWorld.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| b9d8a75a41 | /COBCMS02.cbl | 84 | fixed | 3 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| 544dcb3388 | /FINPARTS.cbl | 71 | fixed | 3 |  |  | unknown | manufacturing-logistics | subprogram | COBOL-85 |
| 205f878fbb | /Cifras.cbl | 254 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 0ad28da905 | /PROJECT2PAYROLL.cbl | 221 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| 368ec6fe5c | /CL18EJ01.v.ESTADO.cbl | 226 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 37f79c9ef9 | /podany270895.cbl | 19 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 98dc927190 | /custmgmt.cbl | 365 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| f335a15dcf | /Edit5.cbl | 30 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 75213e8a32 | /Program1.cbl | 9 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 0c856aaded | /DAY2PZL2.cbl | 64 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| ff92cc4780 | /ParsingTestData.cbl | 12 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| fa465ee1b7 | /edit1.cbl | 36 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| c175a37f84 | /usage-comp.cbl | 22 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d6020e2da7 | /Listing12-2.cbl | 38 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 53ab35c645 | /CBLJCB02.cbl | 451 | fixed | 3 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| f4706db8b2 | /AVG-GRADE.cbl | 63 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 175a4b688c | /variables.cbl | 21 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 30873b47c5 | /primeiro.cbl | 38 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 2ee6c5ab2a | /teste.cbl | 486 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 6270d16a60 | /RentalPropertyPractice.cbl | 27 | fixed | 1 |  |  |  |  |  |  |
| 5db2ef0261 | /AWSome.cbl | 6 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 337769b3d1 | /TM.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| a36d08bd09 | /data4.cbl | 71 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 5b2c6117c8 | /DSB-P03-LOAN.cbl | 378 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 8c5904541f | /day1.cbl | 95 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| f7fc49e7d2 | /two_dim.cbl | 22 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 9d45de34b4 | /MOGO1.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| c7862e8cec | /lista16exe2_sequencial.cbl | 281 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| e7c0e95776 | /control-break1.cbl | 59 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 8f9c8b8a0d | /Z95636.CBL(DAYCALC).cbl | 66 | fixed | 4 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-85 |
| 0897b966f6 | /MIMKK21V.cbl | 172 | fixed | 4 |  | ✓ | ibm-mainframe | other | online-cics | COBOL-85 |
| 329fe8eb08 | /Final.cbl | 64 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 48526674a6 | /imsclaim.cbl | 219 | fixed | 4 |  |  | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| 158c0aec2f | /shop_receipts_footer.cbl | 54 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 3b1babf7d3 | /CALCULO DE VALOR TOTAL.cbl | 39 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| e2bd790d54 | /SESSDATA.CBL | 8 | fixed | 0 |  |  |  |  |  |  |
| 8a30bc13b5 | /hie.yaml.cbl | 4 | unknown | 0 |  |  |  |  |  |  |
| 122bc7c5c4 | /MENU.cbl | 82 | fixed | 3 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 89fbae5903 | /scrcall.cbl | 97 | fixed | 4 |  |  | acucobol | accounting-erp | subprogram | COBOL-85 |
| 1c7ba26b90 | /example.cbl | 10 | fixed | 0 |  |  |  |  |  |  |
| fcaf456135 | /mygrade.cbl | 66 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 354c98c921 | /SalesDataValidation.cbl | 198 | fixed | 3 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 6474f1e77c | /ACT3.cbl | 151 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 2f98495a40 | /triangle-2.cbl | 31 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d61d4daba0 | /bil02900.cbl | 2047 | fixed | 4 | ✓ |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 337ae393f2 | /DoCalc.cbl | 18 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 561f21cea2 | /CobolFinal.cbl | 20 | fixed | 3 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| b87d6cfb94 | /READ-VSAM.cbl | 33 | unknown | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 2a37c8b9c3 | /java collections.cbl | 35 | fixed | 0 |  |  |  |  |  |  |
| a4b1dbc856 | /sys.d.cbl | 19 | fixed | 0 |  |  | unknown | utility-tooling | copybook | unknown |
| ecee6c7fc9 | /PROG004.cbl | 21 | fixed | 4 |  |  | acucobol | demo-example | demo | COBOL-85 |
| bdd710c1fa | /lista6e7.cbl | 43 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| a336598284 | /CWXTDATE.cbl | 99 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | subprogram | COBOL-85 |
| cdcd5557e7 | /Solution.cbl | 20 | free | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| e9147e946e | /TSTMFC5.cbl | 2072 | fixed | 4 |  |  | gnucobol | utility-tooling | test | COBOL-85 |
| c4fe9501f9 | /CONBRE1.CBL | 166 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 89a76790ec | /bS_rioboo.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 95dfa39020 | /Grade.cbl | 98 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 8809eec938 | /COBOL.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| f82d8be6eb | /NOTEMODULE.cbl | 57 | fixed | 4 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 17dee61ca7 | /Control3.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| cc998c9785 | /CustomBox.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| f0da6ccfa0 | /sybhesql.cbl | 314 | fixed | 0 |  |  |  |  |  |  |
| 35a7137352 | /include.cbl | 13 | fixed | 2 | ✓ |  | ibm-mainframe | demo-example | test | COBOL-85 |
| 4734d8c435 | /birtdate.cbl | 19 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 3b4dfc3832 | /PROG.cbl | 30 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| f006c47607 | /SVERSONP.cbl | 17 | fixed | 4 |  |  | micro-focus | demo-example | subprogram | COBOL-85 |
| b809a4a116 | /Lista11Exercicio1V2.cbl | 227 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| e334c49be5 | /[DC Comics] Bloodlines (WEB | 83 | free | 0 |  |  |  |  |  |  |
| e34daafed1 | /helloCobol.cbl | 5 | fixed | 2 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| cc3f784d3d | /member.cbl | 84 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| cff9c70b1b | /DeR#.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| c8ed05b6fe | /usage-comp.cbl | 3 | fixed | 0 |  |  |  |  |  |  |
| 6d050c93d9 | /program.cbl | 11 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 38d8976824 | /TESTVSC2.CBL | 377 | fixed | 0 |  | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| ba32943efd | /And.cbl | 30 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| c4388dc98d | /Assertions2.cbl | 39 | fixed | 3 |  |  | gnucobol | test-suite | subprogram | COBOL-85 |
| 734e54412e | /Control5.cbl | 46 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 46d10a15e6 | /SinTest.cbl | 33 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-2002 |
| fdb2c388e6 | /PRO1.cbl | 109 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 50d7c3a00d | /DCI8DPGU.cbl | 293 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 290826c912 | /PGFJF005P.cbl | 369 | fixed | 4 |  |  | gnucobol | retail-commerce | subprogram | COBOL-85 |
| 5df73e927a | /main.cbl | 96 | free | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-2002 |
| b1bc5a6344 | /triangle-3.cbl | 37 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b09029a4ce | /BMI.cbl | 37 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| dc1e0e75bf | /usage-comp.cbl | 23 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 1e5cbe3bc1 | /HelloCobol.cbl | 10 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 9a371249d6 | /trade.cbl | 48 | fixed | 4 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| b27366816c | /desafiopizzacobol.cbl | 134 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| d8e854ef2c | /grade.cbl | 82 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| be18fbf72b | /Th3 Tr@p.cbl | 4 | free | 0 |  |  |  |  |  |  |
| 2cdc81bc88 | /shop_receipts.cbl | 56 | fixed | 4 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| 16341b472c | /mlExpAss.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 9dc06491c4 | /shop_receipt.cbl | 47 | fixed | 4 |  |  | gnucobol | retail-commerce | demo | COBOL-85 |
| 8a49c44ace | /tempLecturaInteligente.cbl | 177 | fixed | 4 |  |  | other-vendor | other | batch | COBOL-85 |
| 9f92460c2c | /Nescget.cbl | 4 | free | 0 |  |  |  |  |  |  |
| 888b91be7c | /conditions.cbl | 25 | fixed | 3 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| 31f146f35d | /control2.cbl | 36 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| df85d79ac0 | /main2.cbl | 6 | free | 0 |  |  |  |  |  |  |
| e36ddbcd79 | /HOMWRK04.cbl | 4 | fixed | 2 |  |  | unknown | education-tutorial | demo | unknown |
| 9e26dfeeb6 | /core.cbl | 1 | free | 0 |  |  |  |  |  |  |
| c83fb97f25 | /Edit5.cbl | 30 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 7cdc0f78d7 | /PROJ-PRINT-MASTER.cbl | 39 | fixed | 3 |  |  | unknown | education-tutorial | subprogram | COBOL-85 |
| b43d76c07d | /ALTCONTT.cbl | 80 | fixed | 4 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 9dd388b495 | /DeclarationPret.cbl | 42 | fixed | 0 |  |  |  |  |  |  |
| 46ea004bef | /BirthDate.cbl | 20 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 42185f096d | /Program1.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 8f472632fe | /helloworld.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 02145dc6ef | /hello.cbl | 4 | free | 2 |  |  | unknown | demo-example | demo | unknown |
| 11085a16ef | /Form1.Designer.cbl | 27 | fixed | 2 |  |  | micro-focus | utility-tooling | subprogram | COBOL-2002 |
| 98a0f97580 | /BubbleSort-Alt.cbl | 47 | free | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| a49cb461eb | /EXO09.cbl | 41 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| bcec4fd2de | /Program1.cbl | 307 | fixed | 3 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| c53d536664 | /MonfyTechLibrary.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| a797f50169 | /Inventory_Pegging.cbl | 102 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | batch | COBOL-85 |
| aca1114896 | /Minesweeper.cbl | 364 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 4d7170866b | /Control4.cbl | 31 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 7b217f37bd | /accept.cbl | 12 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 73de24dcbe | /calculator.cbl | 42 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 86b7671320 | /e.cbl | 6 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| e381b680a4 | /final1.cbl | 11 | fixed | 3 |  |  | unknown | education-tutorial | unknown | COBOL-85 |
| 5e9597b6f0 | /EXTENSO-FINALIZADO.cbl | 374 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| b89e22a90d | /code06.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | unknown |
| cd4005fee9 | /CALL370.CBL | 22 | fixed | 3 |  |  | gnucobol | test-suite | test | COBOL-85 |
| aea118b537 | /MAIN0001.cbl | 49 | fixed | 3 |  |  | unknown | banking-finance | batch | COBOL-85 |
| ea4938a5d0 | /Data3.cbl | 43 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 2d05bce556 | /SEARCH_SORT.CBL | 107 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| ecbd66906a | /CL11EJ02.cbl | 258 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 675689e709 | /cgi-list-users.cbl | 362 | fixed | 3 | ✓ |  | gnucobol | education-tutorial | online-cics | COBOL-85 |
| dc3614f093 | /hellocobol.cbl | 5 | fixed | 0 |  |  |  |  |  |  |
| fcc9423826 | /GNSBGGBK.cbl | 1 | fixed | 0 |  |  |  |  |  |  |
| 59bed98a37 | /coboltest6.cbl | 21 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| ae74ea1d0c | /user-div.cbl | 30 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| bab5668dc8 | /LGICDB01.cbl | 142 | fixed | 4 | ✓ | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| d4625fc7c7 | /epsmlist.cbl | 179 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| e6860ec6bb | /tp2.cbl | 353 | fixed | 3 |  |  | other-vendor | education-tutorial | batch | COBOL-85 |
| 470b83c89a | /GestionSpectacle2.cbl | 195 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| a4e8347dc4 | /Control1.cbl | 25 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| ff531f1d24 | /FILETEST.CBL | 233 | fixed | 4 |  |  | fujitsu-nec | utility-tooling | batch | COBOL-85 |
| 0dabbe2957 | /write-score.cbl | 47 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 71a8ad47b8 | /myfile4.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 67990af029 | /notas.cbl | 28 | fixed | 2 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 12984db56a | /plymouthemotionanimationset | 0 | unknown | 0 |  |  |  |  |  |  |
| 47055fcdc8 | /Hello.cbl | 1 | fixed | 0 |  |  |  |  |  |  |
| b179993ad7 | /tempCodeRunnerFile.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 2725671d96 | /hello.cbl | 32 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| e3a33b653d | /Custmnt2.cbl | 488 | fixed | 4 |  | ✓ | ibm-mainframe | retail-commerce | online-cics | COBOL-85 |
| 5379d46bb4 | /cxb40092.cbl | 17 | fixed | 4 |  |  | unknown | test-suite | subprogram | COBOL-85 |
| b088f739af | /ST006.COBOL.LAB(WCSRC).cbl | 158 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 51bedbb207 | /Hello-World.cbl | 12 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 4dff7b05dc | /LCM(COBOL).cbl | 66 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 18a875cba1 | /CS4080ExampleProgram.cbl | 42 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| cb97daaaae | /Program1.cbl | 14 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 5791d08c16 | /epsmpmt.cbl | 116 | fixed | 4 |  |  | ibm-mainframe | demo-example | subprogram | COBOL-85 |
| bb99440ad5 | /test9014.cbl | 176 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| f917acb270 | /MODULO-CONSULTAR.cbl | 67 | fixed | 4 |  |  | gnucobol | other | subprogram | COBOL-85 |
| dede62e67f | /coffeeshop_n_2_lookahead_1. | 3 | free | 0 |  |  |  |  |  |  |
| df203ebb9a | /HelloWorld.cbl | 21 | free | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| c0ef18e116 | /hello.cbl | 77 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b9a88dd3ca | /F7.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 78c4c0b4a3 | /prog1.cbl | 70 | fixed | 3 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| e0db28f82e | /covid.cbl | 79 | fixed | 4 |  |  | ibm-mainframe | demo-example | batch | COBOL-85 |
| 45cde20880 | /COBOLFile.CBL | 76 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 8d344816e2 | /Frete.cbl | 34 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 00c4570277 | /my-grade.cbl | 114 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| f9b347abef | /day2.cbl | 67 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-2014 |
| bb071d02fa | /lista17exercicio1.cbl | 413 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 9ea9801893 | /TECHO10.cbl | 316 | fixed | 3 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| cea1ecc741 | /menu.cbl | 83 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 534d15e5a4 | /PBOOKDB2.cbl | 428 | fixed | 4 | ✓ | ✓ | ibm-mainframe | other | online-cics | COBOL-85 |
| adfb429b03 | /Final.cbl | 27 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 2a34cd4c15 | /helloworld in cobol.cbl | 10 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| e31c4c1103 | /VIEWTRENTONFILER-NEW.CBL | 223 | fixed | 4 |  |  | other-vendor | retail-commerce | batch | COBOL-85 |
| 11ebd6b123 | /tuition2.cbl | 25 | fixed | 2 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| c1dcd8bdb9 | /tableau-2.cbl | 47 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 0f5ad5cae6 | /CaesarEncryption.cbl | 36 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 59b6a1511c | /studentrecord.cbl | 38 | fixed | 1 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 5426b41dc1 | /clock.cbl | 39 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 2b2bab71ee | /p1.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 28d10bd92a | /base.cbl | 6 | free | 3 |  |  | unknown | unknown | unknown | COBOL-85 |
| f906702889 | /regs.cbl | 19 | unknown | 0 |  |  |  |  |  |  |
| 4874fd2bbe | /tempCodeRunnerFile.cbl | 1 | fixed | 0 |  |  |  |  |  |  |
| bfca66b33d | /EMP-PAYROLL.cbl | 74 | fixed | 4 |  |  | unknown | payroll-hr | batch | COBOL-85 |
| 69b4acaf7d | /HELLOWORLD.cbl | 6 | fixed | 0 |  |  |  |  |  |  |
| 47b08d8aba | /rename.cbl | 38 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 0e1cf1ac1a | /MARBLE03.cbl | 287 | fixed | 4 | ✓ | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| 3d7e1dd95c | /ONLINE1.cbl | 199 | fixed | 4 | ✓ | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| 14732fb810 | /beep.cbl | 1 | free | 0 |  |  |  |  |  |  |
| b575684d91 | /Data5.cbl | 34 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| c1fe8776f6 | /010 - Arquivo_sequencial.cb | 114 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 90fd7b18a5 | /SOCIOS.cbl | 156 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 9c82824614 | /basicverbs.cbl | 29 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| a8f034d9d0 | /sasha.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 906e2a2a20 | /multiply.cbl | 21 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| edf23ed772 | /CounditionName.cbl | 26 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 4b21f4acd4 | /star-10-1.cbl | 27 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 79add800f7 | /projeto_pizza.cbl | 123 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| cbb05117b5 | /Program1.cbl | 112 | fixed | 2 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| 9f981b9185 | /READ5L.CBL | 30 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 7746089a26 | /data5.cbl | 71 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 9a320d95a9 | /hcipdb01.cbl | 94 | fixed | 4 | ✓ | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| 465c7a0fb9 | /TAXCAL.cbl | 93 | fixed | 4 |  |  | ibm-mainframe | government-public | batch | COBOL-85 |
| bea25be3b2 | /Jokenpo.cbl | 40 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 49f0872828 | /Z95629.CBL(PBE006HW).cbl | 136 | fixed | 4 |  |  | ibm-mainframe | other | batch | COBOL-85 |
| 87faba3380 | /hello_world.cbl | 12 | unknown | 4 |  |  | rm-cobol | demo-example | demo | COBOL-85 |
| 4d29faf1a8 | /read-emp1.cbl | 40 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 539ef97267 | /fkontrol.cbl | 38 | fixed | 4 |  |  | rm-cobol | banking-finance | batch | COBOL-85 |
| 5f8109779c | /cow.cbl | 295 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| dbcaf5a565 | /LIB2.cbl | 12 | fixed | 3 |  |  | gnucobol | demo-example | subprogram | COBOL-85 |
| 524bd6b8a9 | /test.cbl | 7 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 88944ac93a | /cblgrph.cbl | 214 | fixed | 4 |  |  | ibm-mainframe | healthcare-medical | batch | COBOL-85 |
| 6f023f5d63 | /HelloWorld.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| be997efbf6 | /Kindermishandeling.CBL | 82 | fixed | 3 | ✓ |  | micro-focus | education-tutorial | batch | COBOL-85 |
| 228fae7587 | /Sedalia.cbl | 423 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| fb637421b2 | /main.cbl | 71 | free | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 4c4b0a140c | /Program1.cbl | 200 | fixed | 4 |  |  | unknown | demo-example | batch | COBOL-85 |
| 36bd8c0856 | /base.cbl | 7 | unknown | 3 |  |  | unknown | unknown | unknown | COBOL-85 |
| 649112936c | /Aula1.cbl | 20 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| ea086c9444 | /CheckVariable.cbl | 18 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 9f7a3348f3 | /amsPoDownloadGroup.cbl | 41 | fixed | 0 |  |  |  |  |  |  |
| f29abf5e3f | /control-break1.cbl | 59 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| e15322ef03 | /PerformFormat2.cbl | 19 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| f1cacc6e7f | /Program1.cbl | 239 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| fa24dae4c2 | /setvoice.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 943bfecd4a | /two_dim.cbl | 3 | fixed | 1 |  |  |  |  |  |  |
| b8f32f1dd6 | /hello.cbl | 9 | fixed | 1 |  |  |  |  |  |  |
| b38a6b4c85 | /editor.cbl | 7 | unknown | 0 |  |  |  |  |  |  |
| 13b986b2d2 | /SAMPLE.CBL | 3 | fixed | 0 |  |  |  |  |  |  |
| 21a42fd617 | /TRANSACTIONS-IVA.cbl | 28 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 831e8baf02 | /PROGCOB04.cbl | 18 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 341ce9be81 | /branch-sale.cbl | 81 | fixed | 4 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| 67d36993cd | /return.cbl | 10 | unknown | 3 |  |  | unknown | demo-example | demo | unknown |
| 2bb6da5e90 | /PBSUB.cbl | 192 | fixed | 4 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| b25e267586 | /one_dim_init.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| cf601f2aa3 | /control-break3.cbl | 101 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| d1dbf18fcd | /22Day1.cbl | 41 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 47c374bede | /DRAKEA.cbl | 265 | fixed | 0 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| 79ffa0a7a8 | /Program1.cbl | 54 | fixed | 2 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| ed245b6171 | /BonusReport.cbl | 166 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| 081ff0414f | /cobxref.cbl | 2417 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| ce61bee5fb | /epsmlist.cbl | 178 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 854a09eaeb | /products.cbl | 13 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| f8c7889b86 | /control-break3.cbl | 101 | fixed | 3 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 4961b321b2 | /LOADACCT.cbl | 116 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| d013b0a758 | /faa3.cbl | 847 | fixed | 0 |  |  | other-vendor | government-public | batch | COBOL-74 |
| 7daf506555 | /RANDOM01.cbl | 33 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| 5987d48578 | /cobol_test.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 2b6108b2e2 | /one_dim_init.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| f66560f7bc | /LGACDB01.cbl | 218 | fixed | 4 | ✓ | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 0fa18f7871 | /comprogex2.cbl | 92 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| b6a22acc4b | /SEARCH_SORT.CBL | 98 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| bc25922587 | /EX02.CBL | 66 | fixed | 4 |  |  | other-vendor | education-tutorial | batch | COBOL-85 |
| e53505239f | /Desafio.cbl | 396 | fixed | 4 | ✓ |  | micro-focus | healthcare-medical | batch | COBOL-85 |
| 4d2204e40c | /CADDDB2.cbl | 393 | fixed | 4 | ✓ | ✓ | ibm-mainframe | other | online-cics | COBOL-85 |
| 44d242c40a | /Usage-comp2.cbl | 20 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| c89ad944e7 | /data_02.cbl | 13 | fixed | 0 |  |  |  |  |  |  |
| c0631126c6 | /waro.cbl | 127 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| dac4010795 | /Program2.cbl | 76 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 5932d1f97f | /PRGNV88.cbl | 66 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| f1fcbc509b | /shop_receipts.cbl | 54 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| b716607e90 | /test12.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 7ae1cbb921 | /CollatzTests.cbl | 47 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| 7697462726 | /CB012PCW.cbl | 106 | fixed | 4 |  |  | other-vendor | accounting-erp | batch | COBOL-85 |
| 0df134c5f2 | /COBOL.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| f7ed702c4b | /lldemo1.cbl | 140 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 003b01ea41 | /edit1.cbl | 36 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 8daad5fdc9 | /usage1.cbl | 14 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| ee3910ae3f | /hello.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 5c60ec6b23 | /MONTHINC.CBL | 112 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 8cb40aac69 | /usage-pack-decimal.cbl | 17 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| fbd202d141 | /esdumpsplitter.cbl | 212 | fixed | 4 |  |  | micro-focus | utility-tooling | batch | COBOL-85 |
| c816ac47f3 | /main.cbl | 858 | fixed | 4 |  |  | gnucobol | government-public | batch | COBOL-85 |
| fb705e7424 | /cadastro-maes.cbl | 457 | fixed | 4 | ✓ |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 1ed4c1a697 | /pw03232c.cbl | 1149 | fixed | 4 |  |  | micro-focus | manufacturing-logistics | online-cics | COBOL-85 |
| 33dcf383e3 | /desafio01.cbl | 42 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 2ca9a7376a | /SAM1.cbl | 390 | fixed | 4 |  |  | ibm-mainframe | retail-commerce | batch | COBOL-85 |
| 261b16c906 | /hello.cbl | 13 | fixed | 0 |  |  | unknown | demo-example | demo | COBOL-85 |
| cc708dfdfc | /writeUsersFile.cbl | 47 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 859ccceb57 | /part1.cbl | 36 | fixed | 0 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 7b48422844 | /hello_world.cbl | 13 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 45711e1350 | /HELLOWORLD.cbl | 9 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| fae03b595f | /epsmlist.cbl | 178 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| cea5d4fdb4 | /PALINDROME.cbl | 44 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 7762b049dd | /KWI_NSM2.CBL | 53 | fixed | 0 |  |  |  |  |  |  |
| 4307d03651 | /solution.cbl | 44 | unknown | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| ead166dc8a | /mod.cbl | 16 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 44b7abe592 | /exmedecinpatient.cbl | 387 | fixed | 4 |  |  | micro-focus | healthcare-medical | batch | COBOL-85 |
| 6444551797 | /COBOLCypher.cbl | 21 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| e6bb151ceb | /file.cbl | 2 | free | 0 |  |  |  |  |  |  |
| c428d969c6 | /Z95644.CBL(COBHW03).cbl | 118 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| e747aa3475 | /RMNTODEC.cbl | 106 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 547c374f86 | /helloworld.cbl | 12 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| e731f296b8 | /Prog6.cbl | 90 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| bd9ff78557 | /super_security_storage.CBL | 154 | unknown | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| a0207337b2 | /Control3.break.cbl | 103 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 0a585ff2b1 | /hello_world.cbl | 4 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 53728508a5 | /Gender.cbl | 23 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| ca9120ec96 | /basics.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| a7c044c07c | /TP2.cbl | 233 | fixed | 4 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 9c349203e6 | /string.cbl | 325 | free | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-2014 |
| f5be9a710a | /Principal.cbl | 292 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 51d200fbef | /Control7.cbl | 39 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 5a8dd25928 | /geo3x3_encode.cbl | 53 | fixed | 3 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| 02917a79ab | /Pg4_FHood.cbl | 35 | fixed | 3 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| ed72148d6e | /PyramidOfAhraxis.cbl | 8 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-2002 |
| 3cf20d57b0 | /tempCodeRunnerFile.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 86a8923ba2 | /day6.cbl | 100 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 6e51122308 | /arr.cbl | 83 | fixed | 3 |  |  | gnucobol | education-tutorial | test | COBOL-85 |
| 261a569231 | /write-emp1.cbl | 46 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 462acc9928 | /epsmpmt.cbl | 116 | fixed | 4 |  |  | ibm-mainframe | demo-example | subprogram | COBOL-85 |
| 3f65eb9dc5 | /Pizzaria.cbl | 241 | fixed | 2 |  |  | gnucobol | retail-commerce | demo | COBOL-85 |
| ccfec89942 | /Lista7E4.cbl | 189 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 065286fe7c | /HelloWorld.cbl | 6 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 7e69c991ee | /LGTESTP3.cbl | 241 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 34c0c057cc | /HELLO.cbl | 7 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 3411163825 | /Redefines3.cbl | 25 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 474e807d44 | /code_sample_3.cbl | 171 | unknown | 4 |  |  | micro-focus | retail-commerce | batch | COBOL-85 |
| 80def913e4 | /cpyUtf8.cbl | 7 | fixed | 0 |  |  |  |  |  |  |
| 16ef546c10 | /CS370Program2.cbl | 175 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| ab35774676 | /LCM.cbl | 66 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 2a7db1cc1f | /GameOfLifeTest.cbl | 28 | free | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| 41d0fce039 | /debugLines.cbl | 8 | fixed | 3 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 3ef3f02d74 | /CONBRE2.CBL | 196 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 93b3170100 | /desafio1.cbl | 149 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 205a1d652e | /CWBPAIF1.cbl | 188 | fixed | 4 |  |  | ibm-mainframe | retail-commerce | batch | COBOL-85 |
| fa6eaf91f1 | /triangle-2.cbl | 33 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 7d2c4ce48d | /IF-ELSE.cbl | 19 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 2d97e75772 | /write-emp1.cbl | 46 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 797ff11123 | /MENU-LIS.CBL | 145 | free | 3 |  |  | gnucobol | retail-commerce | subprogram | COBOL-85 |
| a63bf1d84a | /Control4.cbl | 29 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 90ec5645f6 | /Program1.cbl | 213 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 2cee1f1105 | /input.cbl | 371 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 6c0ee55a5c | /gestor_archivo.cbl | 122 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| 2bcfef4337 | /04productNumbers.cbl | 16 | free | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 47aae7a8fe | /first_cobol_conditionals.cb | 64 | fixed | 0 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 83ea4b61c7 | /NoCodeToCOBOL.CBL | 7 | unknown | 2 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| 2977e524d6 | /PSPPYRUN.cbl | 1156 | fixed | 4 |  |  | other-vendor | payroll-hr | batch | COBOL-85 |
| 2f7fd14baa | /data.cbl | 7 | fixed | 0 |  |  |  |  |  |  |
| b2509613c2 | /READ5.CBL | 87 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 33edbcd136 | /DataType_3_pre.cbl | 59 | fixed | 3 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| df0a1543fb | /jtvrpt.cbl | 273 | unknown | 4 |  |  | other-vendor | utility-tooling | batch | COBOL-85 |
| 5730845045 | /mcp120.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 6c326d2fed | /PIZZA-INVENTORY-PROG.cbl | 243 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 4c86fa99f4 | /welcome.cbl | 28 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| a1d6f22e0f | /EDITING.CBL | 35 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| afd5c9836a | /PAYLIB.CBL | 18 | fixed | 2 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| c04cd46cb1 | /PERFORM1.CBL | 20 | unknown | 2 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| 6dabefdf17 | /hw.cbl | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 564ec8b55f | /CCP0001.CBL | 929 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 50075926e3 | /Lab4Part2a.cbl | 4 | free | 1 |  |  |  |  |  |  |
| d8c297b333 | /test1.cbl | 10 | fixed | 2 |  |  | unknown | test-suite | test | COBOL-85 |
| 7ba05d2fb0 | /COBOL.cbl | 59 | free | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-2002 |
| f191e02d11 | /ConditionalStatements.cbl | 13 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 2e5fa8c5d9 | /PROG04 (1).cbl | 121 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 2f0abc74ab | /datbatch.cbl | 19 | fixed | 4 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 96d4d56139 | /Provacobol01.cbl | 94 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 0c5c1fae5a | /Program1.cbl | 211 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 337e7dce86 | /SaludoCobol.cbl | 6 | free | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| f57843b73a | /vary_size.cbl | 36 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 911f3af78e | /ACESSO.cbl | 342 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| 222dc0e760 | /star-10-2.cbl | 23 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| bdf81c421f | /calc.cbl | 27 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| b7b57d73a9 | /JOBI12.CBL | 2659 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 261e554c4e | /DoCalc.cbl | 18 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 5beaf3345f | /MARBLE10.cbl | 286 | fixed | 4 | ✓ | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| dfeb7f66f0 | /hello_world.cbl | 8 | free | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 3e146f93ae | /Control5.cbl | 45 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 19180d2439 | /BINARY-SWAP.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 337695054a | /trader.cbl | 18 | fixed | 3 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| de7f505a5f | /second.cbl | 143 | fixed | 0 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| bdeeec9a69 | /Z95644.CBL(FNLPRGMN).cbl | 81 | fixed | 4 |  |  | ibm-mainframe | other | batch | COBOL-85 |
| 9b7306b642 | /A1-ContactList.cbl | 53 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 89d369f652 | /test2.cbl | 85 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| a8b74db445 | /TPROG08.cbl | 119 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 2cc4e7fa2b | /2cc4e7fa2b1e0646612afa9bab9 | 5 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 6ce4df39f6 | /radioExercise.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 7bf8c6db83 | /OddOrEven.cbl | 20 | free | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 72f6038e57 | /READ5L.CBL | 30 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| ada82a806f | /BATJSON.CBL | 183 | fixed | 4 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-2014 |
| 6f3a5f9a6a | /eqSegGrau.cbl | 37 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| dff6eec65e | /HolaMundo.cbl | 9 | fixed | 4 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| 5904af71e4 | /Phnprt01.cbl | 94 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 011945de5b | /test.cbl | 8 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 82a216c547 | /1ln2hded.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 00ad563587 | /Control6.cbl | 31 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| ff7c12f6ff | /main.cbl | 9 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| fe448bca15 | /snake.cbl | 274 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 50b5961e06 | /helloworld.cbl | 8 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| ffbbce6a14 | /Program1.cbl | 21 | fixed | 2 |  |  | micro-focus | demo-example | demo | COBOL-2002 |
| 0a99f99182 | /SetToStatement.cbl | 9 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b7ed55fd0c | /triangle-2.cbl | 33 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 39cd82bd7c | /Assignment-1.cbl | 50 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| a7e444eb0f | /cobol.cbl | 13 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 493de0f712 | /tempCodeRunnerFile.cbl | 1 | free | 0 |  |  |  |  |  |  |
| bb521402ad | /Ecoli_MA.cbl | 15 | free | 0 |  |  |  |  |  |  |
| 683b5cbf5f | /FizzBuzz.cbl | 37 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| b22d1ee044 | /sbanjara_Program4.cbl | 514 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | batch | COBOL-85 |
| 18b7417d22 | /Exercicio 3 lista 5.cbl | 18 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 0af28b925c | /CobolGreeting.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 8347f1cd65 | /main.cbl | 160 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 909b3a32d4 | /custmgt.cbl | 500 | fixed | 4 |  | ✓ | ibm-mainframe | retail-commerce | online-cics | COBOL-85 |
| d6c88fad66 | /PlusTwoNumber.cbl | 15 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| a46912fb23 | /COUSR02S.cbl | 259 | fixed | 4 |  | ✓ | ibm-mainframe | other | online-cics | COBOL-85 |
| 1c3930fc92 | /PRIME.cbl | 30 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| 5c97ff5813 | /arrays.cbl | 13 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 7afa276143 | /PRODALT.cbl | 146 | fixed | 4 |  |  | other-vendor | retail-commerce | batch | COBOL-85 |
| dd182cbf80 | /rutinas1.cbl | 21 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| c85c80eb2b | /CL15EJ01.v.1.1.cbl | 335 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 9a6a7ef700 | /tempCodeRunnerFile.cbl | 1 | unknown | 0 |  |  |  |  |  |  |
| 01c115e2dc | /SALE_REPORT.CBL | 137 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 3fffefe52d | /petstore.cbl | 54 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| c4b50d5a1f | /NETCALC.cbl | 14 | fixed | 2 |  |  | unknown | payroll-hr | subprogram | COBOL-85 |
| 04db07df08 | /calc-expenses.cbl | 64 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 06de221733 | /datetime.cbl | 52 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 53f17f710d | /BossioCodingAsst.cbl | 124 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 0eb5492428 | /05-Calculadora.cbl | 70 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 5b9476ea6e | /Program4.cbl | 508 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| b05e5a2e28 | /ox.cbl | 71 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 9d33dec4e8 | /a3.cbl | 144 | free | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 1677bdced9 | /plus5numbers.cbl | 54 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 78c18948ba | /VALEMAIL.cbl | 60 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 668198fa46 | /SimpleCalculator.cbl | 27 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 3126c3cc1f | /JIM.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| 8230cc5d30 | /HELLOWORLD.cbl | 13 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 041e08a3df | /002-tablasMultiplicar.cbl | 48 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| fd98f24bea | /CREATE-BANK-ACCOUNT.cbl | 36 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 44ac89ca9e | /TRADER9.cbl | 11 | fixed | 3 |  |  | gnucobol | retail-commerce | unknown | COBOL-85 |
| 745229badc | /caesarCipher.cbl | 101 | unknown | 1 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 55a9b7fb47 | /hopper.cbl | 90 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 54e3597463 | /Program1.cbl | 352 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| f1d1169e72 | /Grade.cbl | 73 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 5a016ae256 | /operacoes.cbl | 34 | fixed | 0 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 13c9e08b91 | /calculadora3.cbl | 173 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 81ed52f089 | /HELLO.CBL | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| a97484875d | /HelloWorld.cbl | 6 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| bfcbb80bf6 | /gpar.cbl | 92 | unknown | 0 |  |  |  |  |  |  |
| d2b455c796 | /CM201M.CBL | 83 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-74 |
| bae6d26c0f | /DateTst.cbl | 9 | fixed | 0 |  |  |  |  |  |  |
| 31d74b6bd3 | /TestGetMatches.cbl | 108 | fixed | 1 |  |  | micro-focus | test-suite | test | COBOL-85 |
| 87a1ccd695 | /demo_report.cbl | 356 | fixed | 4 | ✓ |  | gnucobol | demo-example | batch | COBOL-85 |
| eef59988fc | /CBSRGDBB.cbl | 152 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| a6798cab1b | /dfuwfuhfuhfui.cbl | 18 | fixed | 3 |  |  | rm-cobol | education-tutorial | demo | COBOL-85 |
| 4c12132fc6 | /COBLSC05.cbl | 418 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 9662cef419 | /display_timing.cbl | 141 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| bd8716ee9c | /TEMPERATURA HISTÓRICA INDEX | 352 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| d8b4dfc5cc | /lol-qwop.cbl | 6 | free | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 5395f90774 | /GEN-SEC.cbl | 66 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 127e4878ef | /write-score1.cbl | 47 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| a931f66659 | /CONBOLER.cbl | 364 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| c0a5ded8b4 | /averagecalculator.cbl | 49 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| e4e76646ba | /lista16exercicio2v2.cbl | 303 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| bb2c3a879f | /CADTIPO.cbl | 264 | fixed | 3 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| c14f5fb970 | /Stack.cbl | 36 | free | 3 |  |  | gnucobol | education-tutorial | subprogram | COBOL-2002 |
| ee3f626c0e | /EMPLOYEE DATABASE.cbl | 45 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| bbdd24db25 | /Default.aspx.designer.cbl | 5 | fixed | 0 |  |  |  |  |  |  |
| cedd70be3c | /JM.CBL | 195 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 2ad5cf5d16 | /ingramDanielAsst2.cbl | 146 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 586c4882c3 | /app3.cbl | 11 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 4a664ae08d | /principal.cbl | 80 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 34a58d6a92 | /customer_record.cbl | 20 | fixed | 0 |  |  |  |  |  |  |
| 37a01ed77e | /sortandusing.cbl | 27 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d02ef3bb9d | /db_udcs.cbl | 64 | fixed | 3 |  |  | ibm-mainframe | utility-tooling | demo | COBOL-85 |
| 86ca1f3b87 | /PERFORM-RUTINAS.cbl | 21 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 8f681c483d | /ACPPRTPRMS.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 592d3e46df | /avg-cs-grade.cbl | 71 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| a1040b9230 | /calculate.cbl | 77 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-2002 |
| 06a35006bf | /IMSCBLJB.cbl | 239 | fixed | 4 |  |  | ibm-mainframe | other | batch | COBOL-85 |
| b87a56172f | /cobpg.cbl | 104 | fixed | 4 |  |  | gnucobol | utility-tooling | demo | COBOL-85 |
| e0996495b5 | /READ5.CBL | 87 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 3f504a3a1e | /CALC_EVAL.cbl | 39 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 4d1d575b99 | /Program2.cbl | 275 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| a828e33035 | /HelloWorld.cbl | 6 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| b278bd2bfc | /DECODE04.cbl | 119 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| ecb9d31291 | /MyGrade.cbl | 96 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| a8a0a8d0a1 | /amfbprint-rev-prod.cbl | 8214 | fixed | 4 |  |  | other-vendor | accounting-erp | batch | COBOL-85 |
| 5fa2d7b923 | /MARBLE07.cbl | 287 | fixed | 4 | ✓ | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| 6950b16cfe | /MAC200.CBL | 86 | unknown | 0 |  |  |  |  |  |  |
| 60194f1195 | /G3-CAP1-MONTH-END.cbl | 75 | fixed | 4 |  |  | unknown | banking-finance | batch | COBOL-85 |
| 2a3563fb3a | /ALUNO-PEGA.cbl | 21 | fixed | 3 |  |  | unknown | education-tutorial | subprogram | COBOL-85 |
| 6bd041eddf | /OccursDependingOn22.cbl | 21 | fixed | 0 |  |  |  |  |  |  |
| aa52c1190e | /day1.cbl | 63 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| dd4ea6ef11 | /hello-world.cbl | 7 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| b5b25c00c5 | /MyGrade.cbl | 95 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| eb43b77d3e | /helloworld.cbl | 9 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| 9f75a6cdf9 | /Alumnos_1.cbl | 59 | fixed | 1 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| e263b39283 | /lista11exercicio3adaptado.c | 362 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| fe7d3bba55 | /quiz.cbl | 13 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b1da3e6845 | /TODYNAM6.cbl | 14 | fixed | 3 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| e68bf3e27c | /read5.cbl | 62 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| ca9086fb31 | /Seqread.cbl | 37 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| d9c3ac7b5d | /BVZZ1.cbl | 181 | fixed | 4 |  |  | ibm-mainframe | insurance | subprogram | COBOL-85 |
| d63a269d65 | /envelopes.cbl | 47 | free | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 0fd592d83a | /hello.cbl | 5 | fixed | 2 |  |  | unknown | demo-example | demo | COBOL-74 |
| f1fa77f211 | /NestedIFExample.cbl | 27 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d299ff58ac | /Z95619.CBL(PBEGIDX).cbl | 192 | fixed | 4 |  |  | ibm-mainframe | banking-finance | subprogram | COBOL-85 |
| 0751f2d6a4 | /Data3.cbl | 46 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d467dfebba | /fibbonaci.cbl | 24 | unknown | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 90ba525193 | /PROG0010.cbl | 156 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| aee68410b6 | /File_Handling.cbl | 57 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 3092a3a8cd | /TFinal_808_JoaoLeigo.cbl | 2569 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| c1847d8664 | /mult.cbl | 38 | free | 0 |  |  |  |  |  |  |
| bab02b8a5c | /DEL-INDR.cbl | 55 | fixed | 4 |  |  | other-vendor | education-tutorial | batch | COBOL-85 |
| 1ffa68eace | /test.cbl | 0 | free | 0 |  |  |  |  |  |  |
| c44761f7e8 | /CONDICIONES.cbl | 22 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 8ccdf36303 | /honda_62.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| c9764fdf0d | /conversortemp.cbl | 29 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 3ce54b44bf | /KFTSCP3.cbl | 25 | fixed | 0 |  |  |  |  |  |  |
| 336ca5086d | /CONTROL_B3.cbl | 183 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 12af2eb176 | /menu.cbl | 60 | fixed | 2 |  |  | gnucobol | banking-finance | online-cics | COBOL-85 |
| 6bef337b5d | /test.cbl | 94 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| cc549556aa | /p4.cbl | 33 | fixed | 0 |  |  | unknown | demo-example | demo | COBOL-85 |
| 1c889f1527 | /github-cicsplex-name-detect | 615 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| f74a9c075d | /desafiopizza.cbl | 142 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 2382006a0e | /tests.cbl | 40 | fixed | 3 |  |  | gnucobol | test-suite | test | COBOL-85 |
| 5d0a7a63dd | /edit1.cbl | 37 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 73f66860fc | /026_continue.cbl | 34 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1f908aceb9 | /TSUBR19.cbl | 64 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | subprogram | COBOL-85 |
| f40955fad9 | /ZFAM005.cbl | 358 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| 0c384ff7d4 | /GildedRose.cbl | 68 | fixed | 2 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| f815813ef9 | /HELLOWORLD_INCOBOL.cbl | 9 | free | 0 |  |  |  |  |  |  |
| a2d89ecc9e | /Serpiente.cbl | 8 | fixed | 1 |  |  |  |  |  |  |
| 1f9acaf299 | /arquivo_sequencial_exc3.cbl | 124 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| e14a9ace75 | /TABLES01.cbl | 185 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 14d74d1b08 | /Program1.cbl | 9 | fixed | 3 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| 668289c6a7 | /tableauListe.cbl | 24 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| c2d32683da | /SQ103A-copy.cbl | 401 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| 40808c0ed8 | /CBSRGDBB.cbl | 152 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 8f27823d64 | /Perform4.cbl | 40 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 05ede0b52a | /candy_sale.cbl | 48 | fixed | 4 |  |  | unknown | retail-commerce | batch | COBOL-85 |
