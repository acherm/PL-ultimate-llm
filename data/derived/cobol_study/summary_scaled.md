# COBOL-in-SWH exploratory study — summary

_Generated 2026-06-17T18:33:24Z · 350 samples (344 text, 6 non-text), 317 LLM-judged._

## Lines of code (code lines, excl. blank/comment)

- min **5** · median **596.5** · mean **2039.7** · max **27378** · total **701654**

## Source format (mechanical heuristic)

- fixed: 318
- free: 22
- unknown: 4

## Feature prevalence (mechanical, over text files)

- EXEC SQL: 16 (4.7%)
- EXEC CICS: 21 (6.1%)
- COMP-3: 18 (5.2%)
- COPY: 237 (68.9%)
- CALL: 223 (64.8%)

## Is COBOL? (judge)

  - true: 317 (100.0%)

## Dialect family (judge)

  - gnucobol: 227 (71.6%)
  - micro-focus: 43 (13.6%)
  - ibm-mainframe: 40 (12.6%)
  - fujitsu-nec: 4 (1.3%)
  - acucobol: 3 (0.9%)

## COBOL standard (judge)

  - COBOL-85: 308 (97.2%)
  - COBOL-2002: 8 (2.5%)
  - COBOL-2014: 1 (0.3%)

## Source format (judge)

  - fixed: 290 (91.5%)
  - free: 27 (8.5%)

## Domain (judge)

  - healthcare-medical: 156 (49.2%)
  - education-tutorial: 68 (21.5%)
  - accounting-erp: 21 (6.6%)
  - banking-finance: 17 (5.4%)
  - retail-commerce: 14 (4.4%)
  - utility-tooling: 11 (3.5%)
  - insurance: 11 (3.5%)
  - other: 8 (2.5%)
  - payroll-hr: 4 (1.3%)
  - manufacturing-logistics: 3 (0.9%)
  - telecom: 2 (0.6%)
  - demo-example: 1 (0.3%)
  - government-public: 1 (0.3%)

## Program type (judge)

  - batch: 144 (45.4%)
  - online-cics: 67 (21.1%)
  - subprogram: 61 (19.2%)
  - demo: 34 (10.7%)
  - test: 11 (3.5%)

## Maturity (judge)

  - production-like: 240 (75.7%)
  - student-exercise: 56 (17.7%)
  - toy-or-hello-world: 16 (5.0%)
  - snippet: 5 (1.6%)

_Judge tokens: 1958886 prompt + 218953 completion._

## Samples

| sha1_git | file | LOC | fmt | divs | SQL | CICS | family | domain | type | std |
|---|---|---:|---|---:|:-:|:-:|---|---|---|---|
| 824e23cbe7 | /EM0206.CBL | 220 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 3c73c21216 | /cop999.CBL | 2651 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 9ec4cf01bc | /square-star.cbl | 31 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 133ab28cd9 | /ORCSNYUFTN.CBL | 4363 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 1cfe30b1a3 | /ORCSCKTKNKCHK.CBL | 1081 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| d7504e31cf | /ORAPI023R1V2.CBL | 2078 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 25b9b82bd8 | /ORCSC92.CBL | 2023 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 931c60e0d0 | /H3.cbl | 106 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| ea1539e1ca | /ORCR0030.CBL | 5839 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 1702857871 | /Program1.cbl | 13 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| cbdaf8f521 | /ORCGJ02.CBL | 11717 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 565fce844b | /ORCR0655.CBL | 659 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 0ef7f1e5a8 | /LOADEMPL.CBL | 197 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| 22732c113c | /branch_sale.cbl | 81 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| ae6c8d9429 | /ORCBM510.CBL | 601 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a8386cc8d3 | /ORCGP02.CBL | 2689 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 1be6a7b1cb | /ORCGLERR.CBL | 66 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 60babe3c93 | /bnotavar.cbl | 8531 | fixed | 4 |  |  | acucobol | accounting-erp | online-cics | COBOL-85 |
| 2456bdbde3 | /3-ENTREE.CBL | 346 | fixed | 4 |  |  | micro-focus | payroll-hr | subprogram | COBOL-85 |
| dd67713339 | /ZFAM002.cbl | 2839 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| aac28b4dff | /stockvalorise.cbl | 170 | fixed | 3 | ✓ |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 17708a9284 | /ORCGM96.CBL | 935 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| e334a9dd4d | /ORCBD008.CBL | 980 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 31a5c8c403 | /PGMENULS.CBL | 26 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 59b93c95a7 | /VSRS9999.cbl | 179 | fixed | 4 |  | ✓ | ibm-mainframe | telecom | online-cics | COBOL-85 |
| fdabbb2c64 | /ORCR0030.CBL | 27378 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| fc6802575d | /ORCS02.CBL | 10367 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| ea33850cd1 | /STBEFW101.CBL | 458 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 1898d418f9 | /getonestore_test.cbl | 33 | fixed | 3 |  |  | gnucobol | retail-commerce | test | COBOL-85 |
| e7c0dfc98c | /五七炮.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| eb39b3bc78 | /mar-handler.cbl | 680 | fixed | 4 |  |  | micro-focus | utility-tooling | batch | COBOL-85 |
| 9f8ef25a44 | /Data1.cbl | 16 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 13bf4a9a6b | /ORCR0910.CBL | 2741 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 58dcb1b3e8 | /ORCGW13.CBL | 2748 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 12948db6a1 | /ORCS02.CBL | 25128 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| dfb05401ed | /member.cbl | 84 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 3558f0086d | /ORCGZ07.CBL | 1234 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 748237e9b3 | /15b.cbl | 166 | fixed | 3 |  |  | gnucobol | education-tutorial | batch | COBOL-2002 |
| a89317fce3 | /SEIKYU1805.CBL | 1586 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 39d7d4a310 | /ORCGJ022.CBL | 323 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| d9432e73de | /RMV_FRST_LST_CH.CBL | 20 | fixed | 3 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| 2f4a6dac35 | /ORCGT06.CBL | 3422 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| e54a2f5b10 | /ORCSC40200203.CBL | 506 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 7c192ade38 | /ORCSP02.CBL | 2853 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| e1202738b1 | /A00000D126.CBL | 2815 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 48a8e4b81b | /ICKE02701.CBL | 182 | fixed | 4 |  |  | fujitsu-nec | insurance | batch | COBOL-85 |
| 29599d2d80 | /ORCR0840.CBL | 8316 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e997ba7842 | /glistini.cbl | 7721 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| e5676c8c74 | /DUMMBOT_T.CBL | 115 | fixed | 0 |  |  |  |  |  |  |
| 4b6a764222 | /FDEMENU.CBL | 27 | fixed | 0 |  |  |  |  |  |  |
| 95d7bcff27 | /ORCGW62.CBL | 721 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 27136fb2d1 | /Assign1.cbl | 118 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| dc1b7a71c4 | /plinvoiceMT.cbl | 2412 | free | 4 | ✓ |  | gnucobol | accounting-erp | subprogram | COBOL-2002 |
| 18fa2daf25 | /pw02130r.cbl | 2464 | fixed | 4 |  |  | micro-focus | manufacturing-logistics | online-cics | COBOL-85 |
| e2bcfeb80e | /ORCSMISAVE.CBL | 191 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 17a6793706 | /ORCR0460.CBL | 1927 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| f90618f7ca | /ORCR0420.CBL | 5715 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 52d06b73fe | /ORCGK02NYU.CBL | 8109 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| c785bb2a01 | /FunDeclareWithExec-PublicPr | 109 | fixed | 3 | ✓ |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| d59df2b484 | /Control7.cbl | 40 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| ac08374268 | /ORAPI012R1.CBL | 493 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 7e6022087b | /ORCGJ02.CBL | 9009 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| bb3d626256 | /ORCGO01.CBL | 1017 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| eb3b52912b | /sql1252a.cbl | 257 | fixed | 0 |  |  |  |  |  |  |
| b641945a9b | /PlusTwonumber.cbl | 15 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 9172408694 | /ORCSC95SUB.CBL | 1228 | fixed | 4 |  |  | micro-focus | healthcare-medical | subprogram | COBOL-85 |
| 7892e2f376 | /DBBTEST.cbl | 20 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | test | COBOL-85 |
| 63d54884fa | /sqlda.cbl | 26 | fixed | 0 |  |  |  |  |  |  |
| 4850dbbe0d | /ZINKOMITSUDO2.cbl | 98 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 62175e870f | /NOconvert_brad+rma.cbl | 1131 | unknown | 4 |  |  | micro-focus | healthcare-medical | batch | COBOL-85 |
| 20bf619d9f | /CRP019.CBL | 1153 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| e6b29f3b7a | /ORCSNYUFTN.CBL | 6238 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 78c481a912 | /ORCR0430.CBL | 2083 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d2f86f1805 | /ORCR0010.CBL | 2835 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| c7014065d1 | /EXERCICIO_01.cbl | 54 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 8a3199923e | /SOCK08.cbl | 1126 | fixed | 4 | ✓ | ✓ | micro-focus | insurance | online-cics | COBOL-85 |
| b48acd68f1 | /acpx010.CBL | 11 | fixed | 0 |  |  |  |  |  |  |
| 73d7f5ac7d | /BMI.cbl | 29 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| f4c8706dc3 | /TSQL022C.cbl | 19 | fixed | 3 | ✓ |  | micro-focus | other | test | COBOL-85 |
| 1d4a24239b | /CLADRILD.cbl | 889 | fixed | 4 | ✓ |  | ibm-mainframe | manufacturing-logistics | batch | COBOL-85 |
| 2f6c6d236a | /ORCGG03.CBL | 992 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| cdb6c3da56 | /ORCR1200.CBL | 1966 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a8345aa320 | /ORCDTCHK003.CBL | 427 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 4245844f82 | /ORCR0840.CBL | 3660 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 89a0cfb293 | /msnsearc.cbl | 259 | fixed | 4 |  | ✓ | ibm-mainframe | telecom | online-cics | COBOL-85 |
| 3ce4fe78c2 | /BCASH01P.CBL | 61 | fixed | 3 |  |  | micro-focus | banking-finance | online-cics | COBOL-85 |
| c49317bebf | /2006 - 52.cbl | 191 | free | 0 |  |  |  |  |  |  |
| a9a059d25d | /ORCGK02NYU.CBL | 9272 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 0fa13dc9e5 | /epscmort.cbl | 203 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 1f0a3d16af | /ORCGI01.CBL | 16030 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e045fd5719 | /ORCR0420.CBL | 7477 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e622265128 | /ORCDBAPIV3.CBL | 86 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 7e3d93afde | /D413KTK.cbl | 10 | free | 0 |  |  |  |  |  |  |
| 88d6b02e4c | /A00000D123.CBL | 2721 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 8cdbedae45 | /ORCHCM31.CBL | 849 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| eea444f328 | /ProgramEnd.rdz.cbl | 6 | fixed | 2 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| c7a2d8c924 | /ORCGI01.CBL | 18225 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e8e31c1d22 | /MST_NOFU.cbl | 10 | free | 0 |  |  |  |  |  |  |
| b77487b2f5 | /ORCR0420.CBL | 5170 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 1b714c5a6f | /CobolFinal.cbl | 16 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 257f2cc403 | /DY3230.CBL | 230 | fixed | 4 |  |  | micro-focus | other | online-cics | COBOL-85 |
| 6c8848c863 | /ORCGK02.CBL | 10243 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| be98e164eb | /JOM_FORM_0018.CBL | 10 | free | 0 |  |  |  |  |  |  |
| 19e5dc617b | /COACTVWS.cbl | 636 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 181254057d | /gagenti.cbl | 6300 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| 7c88a2a545 | /SOKATU0710.CBL | 1501 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e8142e257d | /gctestrun5.cbl | 258 | fixed | 4 |  |  | gnucobol | utility-tooling | test | COBOL-85 |
| b33c131bdf | /DB2CBLEX.cbl | 216 | fixed | 4 | ✓ |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 7281cf8d6c | /ORCHC02V02.CBL | 3831 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9b3de71faa | /lgapdb01.cbl | 446 | fixed | 4 | ✓ | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 8b9a9582e1 | /purchRES.cbl | 101 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-2002 |
| 08fb28fdee | /ORCBG017S.CBL | 1767 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| b9b27c277d | /COBOL007.cbl | 33 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 8f0692ef9b | /ORCGM00.CBL | 1080 | fixed | 4 |  |  | micro-focus | healthcare-medical | online-cics | COBOL-85 |
| 43952712bf | /ORCSC54201004.CBL | 1170 | fixed | 4 |  |  | fujitsu-nec | healthcare-medical | subprogram | COBOL-85 |
| f5a8e97543 | /tcaudisb.cbl | 2272 | fixed | 4 |  |  | acucobol | accounting-erp | online-cics | COBOL-85 |
| 2f02fe4e2a | /part2-take2.cbl | 51 | fixed | 0 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| c6746cb969 | /ORCR0480.CBL | 2434 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 176018d0a0 | /sudoku.cbl | 548 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 57c56a8372 | /ORCSCKNKCHK.CBL | 1003 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 73a0815968 | /ORCR0640.CBL | 8375 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 33d2c3e633 | /ORCR0840.CBL | 5127 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 637e47424f | /sl910.cbl | 1491 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| a0063f53a5 | /GLP002.CBL | 852 | fixed | 4 |  |  | gnucobol | banking-finance | online-cics | COBOL-85 |
| 9d43f4dbb9 | /ORCRDPC10.CBL | 5653 | fixed | 4 |  |  | fujitsu-nec | healthcare-medical | batch | COBOL-85 |
| c78ec7446d | /SEIKYU1805.CBL | 1467 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 203cb3f105 | /ORCSC40200204.CBL | 1110 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 42e7cde495 | /ORCGW28.CBL | 1307 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| b4b844040b | /MOVE-01.cbl | 32 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| a187d86aec | /gestor_archivo.cbl | 153 | fixed | 4 |  |  | gnucobol | other | subprogram | COBOL-85 |
| dccbf632ea | /ORCSCNYUIN.CBL | 2711 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 6fb931c024 | /ORCT0010.CBL | 1341 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 36e7388a9e | /[Marvel] [2018-2020] Tony S | 83 | free | 0 |  |  |  |  |  |  |
| ad2dab170a | /ARRPARTI.CBL | 1083 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| dd16637384 | /ricaldin-bat.cbl | 1825 | fixed | 3 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 6ff7c63a01 | /Date04.cbl | 46 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| a7144bbfc6 | /A00000C100.CBL | 244 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9054209d92 | /epsmlist.cbl | 178 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 99142f771f | /ORCSC93.CBL | 1046 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 5cc776b413 | /GRF00000.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 3c7c2c9353 | /ORCR0103.CBL | 2478 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 21325f320c | /ORCR1010.CBL | 4478 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 46e3fc954e | /cgi-list-betygelev.cbl | 262 | fixed | 4 | ✓ |  | gnucobol | education-tutorial | online-cics | COBOL-85 |
| 3ca42c8e02 | /Test.cbl | 25 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 5d3ea739a1 | /server.cbl | 2075 | fixed | 4 |  |  | gnucobol | demo-example | online-cics | COBOL-85 |
| 5dcfe0a426 | /ref1.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 04daba4c27 | /Vnddsp02.cbl | 160 | fixed | 4 |  |  | micro-focus | education-tutorial | batch | COBOL-85 |
| c2f00ee4eb | /fullatbat.aspx.cbl | 1114 | fixed | 2 |  |  | micro-focus | other | online-cics | COBOL-2002 |
| eca497a69c | /ORCGKID2.CBL | 106 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 4949fefb09 | /TSUBR47.cbl | 64 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | subprogram | COBOL-85 |
| 699c248d25 | /PAY_DATREC.CBL | 27 | fixed | 0 |  |  |  |  |  |  |
| 71681ce8e0 | /STBEFD343.CBL | 456 | fixed | 4 |  |  | micro-focus | banking-finance | batch | COBOL-85 |
| 01a308123e | /NC237A.CBL | 619 | fixed | 4 |  |  | gnucobol | education-tutorial | test | COBOL-85 |
| 3a667f90ce | /Lista5E1.cbl | 38 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| a882047d3b | /ORCGI01.CBL | 6572 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d6d015ac56 | /EITestCpyList3A.rdz.cbl | 9 | fixed | 3 |  |  | ibm-mainframe | education-tutorial | test | COBOL-85 |
| 9496d8e8ba | /ORCBINF1.CBL | 1149 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| f528a17fb7 | /ORCGM00.CBL | 1297 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| e38a518b59 | /GNSBRCIC.cbl | 32 | fixed | 0 |  |  |  |  |  |  |
| 80345eea94 | /sincsqf04b.cbl | 131 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 324dc8576a | /LGTESTP1.cbl | 259 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| cf13eef25c | /KEI_TOKUYAKU.CBL | 10 | free | 0 |  |  |  |  |  |  |
| f86655d02f | /perform.cbl | 21 | unknown | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 156358ae54 | /ORCSCWKSRY.CBL | 3501 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| b79d8716cb | /ORCGS02.CBL | 7486 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e0b6ffe5a9 | /ORCGS03N.CBL | 1503 | fixed | 4 |  |  | micro-focus | healthcare-medical | online-cics | COBOL-85 |
| 9dd4146862 | /ORCR0030.CBL | 16287 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a019c6552b | /FunDeclare.rdz.cbl | 128 | fixed | 2 |  |  | micro-focus | education-tutorial | test | COBOL-2014 |
| a0723e9c21 | /JOJO.cbl | 11 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 9e84140a61 | /pw03155r.cbl | 973 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 298ff2c474 | /hello.cbl | 5 | fixed | 2 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| c19447261a | /ORCSC96.CBL | 2244 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| ff2976925e | /gameSummary.aspx.designer.c | 102 | fixed | 0 |  |  |  |  |  |  |
| a1107ecd7e | /ORCBG016.CBL | 1337 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 18bc58933f | /竹香斋.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| 4c7d3aec0a | /SOKATU3100.CBL | 1073 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 1ad84662c7 | /[DC] 2016-2021 Part 1.3 Wel | 335 | free | 0 |  |  |  |  |  |  |
| 53f72d1790 | /ORCR0600.CBL | 1631 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| b13de34ad6 | /ORCSSKJKEEP.CBL | 1296 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 41304ed96d | /ORCR0900.CBL | 372 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 2c1cdf7a5b | /SEIKYU1005.CBL | 2010 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 88d166b9b3 | /FRAUDMOD.cbl | 53 | fixed | 3 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| f1428616bb | /ORCGM01N.CBL | 1009 | fixed | 4 |  |  | micro-focus | healthcare-medical | online-cics | COBOL-85 |
| 14e749526e | /EL6331.cbl | 3387 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 2918d2efa9 | /CPBD472KYS.cbl | 145 | fixed | 0 |  |  |  |  |  |  |
| 0013240c03 | /ORCR0640.CBL | 7497 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e3b7dfceb9 | /SOKATU0815.CBL | 1549 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3c9ffbb4bd | /pw06030c.cbl | 599 | fixed | 4 |  |  | micro-focus | banking-finance | online-cics | COBOL-85 |
| d797f169c0 | /P3SRSE21.cbl | 414 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| 28b834f98f | /ORCGPID1.CBL | 88 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 92560a48b9 | /ZFAM004.cbl | 474 | fixed | 4 |  | ✓ | ibm-mainframe | utility-tooling | online-cics | COBOL-85 |
| f6dbcca54b | /stbefw626.cbl | 458 | fixed | 4 |  |  | micro-focus | banking-finance | batch | COBOL-85 |
| 0a2d070540 | /STP033.CBL | 820 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| 1c130fbcf1 | /Vchmnt01.cbl | 548 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 53ad867742 | /VGETKEYLABELS.cbl | 36 | free | 4 |  |  | gnucobol | other | subprogram | COBOL-2002 |
| f6ff67ae4d | /twodim.cbl | 21 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 9760ca6107 | /ORCGS09.CBL | 891 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 3b98f7fbf4 | /ORCR0030.CBL | 11893 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ff35a3a828 | /ORCGC04.CBL | 1627 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 655599b436 | /RASDA010.cbl | 39 | fixed | 3 |  |  | ibm-mainframe | utility-tooling | subprogram | COBOL-85 |
| 8bc354f093 | /ORCGS03N.CBL | 2021 | fixed | 4 |  |  | micro-focus | healthcare-medical | online-cics | COBOL-85 |
| f1fa77f211 | /NestedIFExample.cbl | 27 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 928f2db09c | /ORCGKID2.CBL | 114 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| be9d9c2bed | /ORCR0486.CBL | 2878 | fixed | 4 |  |  | fujitsu-nec | healthcare-medical | batch | COBOL-85 |
| 3145019934 | /SQ205A.CBL | 501 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | test | COBOL-85 |
| 2e543a562c | /ORCGR02.CBL | 4462 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| c4321075fc | /SQ220A.CBL | 680 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | test | COBOL-85 |
| bb689cebb7 | /ORCGW07.CBL | 8219 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| c12dee230d | /HCMADB02.cbl | 277 | fixed | 4 | ✓ | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| c27d8e80d0 | /ORCBZ001.CBL | 574 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 7d732bd6cd | /ordforn-sol.cbl | 3161 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| 226b6e5f58 | /email2.cbl | 521 | fixed | 4 |  |  | micro-focus | utility-tooling | subprogram | COBOL-85 |
| 39c781b278 | /lgucdb01.cbl | 141 | fixed | 4 | ✓ | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 2907c17012 | /MONTHINC.CBL | 98 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 89d5c993a8 | /ORCGP02.CBL | 3316 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 6a682702bc | /ORCS01.CBL | 25865 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| c075d27296 | /write-emp1.cbl | 46 | fixed | 3 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 40cb2714e4 | /ORCS02.CBL | 8353 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| cf730d5c41 | /ORCSODRS01.CBL | 203 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 092b2b006e | /ORCGP02X.CBL | 415 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 5286026571 | /ORCBG014.CBL | 4073 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d4367a9df4 | /ORCHCM34.CBL | 6435 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 91854d2cb3 | /pl900.cbl | 119 | free | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 3ac308e689 | /ORCR0961.CBL | 2632 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| da3b7873d2 | /PRIME.cbl | 30 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| 0ac140ebd6 | /ORCGW122.CBL | 1533 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| d42771de59 | /write-grade1.cbl | 46 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 77ef0fc2ef | /PIOWEB.CBL | 464 | fixed | 0 |  |  |  |  |  |  |
| 24767ba0a7 | /SCASH20P.CBL | 250 | fixed | 4 |  | ✓ | micro-focus | banking-finance | online-cics | COBOL-85 |
| 68f27ecd1a | /[Marvel] CMRO Essential Rea | 2816 | free | 0 |  |  |  |  |  |  |
| d044e2c294 | /ORCR0103.CBL | 3201 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 937f6d1d36 | /Spider-Man 005 (Clone Years | 865 | fixed | 0 |  |  |  |  |  |  |
| 43319828bb | /ORCGW11.CBL | 2557 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 8f1ac07330 | /P1.cbl | 391 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 598f4b41ee | /main.cbl | 1675 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| d5f9bb0fd1 | /branch_sales.cbl | 80 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| d999ca259c | /DBCBEX16.cbl | 231 | fixed | 4 | ✓ |  | gnucobol | education-tutorial | batch | COBOL-85 |
| c9efea0a7c | /agarcob.cbl | 2154 | fixed | 3 |  |  | gnucobol | utility-tooling | subprogram | COBOL-2002 |
| 84a7ec2102 | /ORCBMRCSV09.CBL | 2119 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 59a66c4fea | /SUB01.cbl | 17 | fixed | 3 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| f6a1288f32 | /ORCR0040.CBL | 5068 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4e6bc6060f | /ORCGW13.CBL | 1976 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 60394e2e70 | /OPENDELE.CBL | 165 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| a127a57fc7 | /IFdeClaseOtipo.cbl | 37 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 5b1ded1fda | /ORCR0640.CBL | 6615 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 504fe95954 | /CONBRE2.CBL | 195 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| cff0806641 | /Trunc03.cbl | 49 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| c61feb12d1 | /SEIKYU4707.CBL | 1134 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 8f118ae770 | /irs.cbl | 594 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 0b84972727 | /Yesno05.cbl | 49 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 0b1957cd9b | /ExecSqlWithFromClause.rdz.c | 14 | fixed | 3 | ✓ |  | ibm-mainframe | education-tutorial | test | COBOL-85 |
| 705e647138 | /ORCGXG04.CBL | 950 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| bdd6aee417 | /gl070.cbl | 356 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 681f7e90c1 | /add_examples.cbl | 73 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 4db6b9e892 | /ORCGJ02.CBL | 4417 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| f31de6846d | /ONE-DIM-TABLE.cbl | 28 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 8a87c21e94 | /G3-VISA-MAIN.cbl | 40 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| b3ed464fa5 | /assignment8.cbl | 69 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 8c9cf04cb7 | /finaltrader2.cbl | 69 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 92bc389c17 | /A00000L103.CBL | 1445 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 2035a19ab0 | /ORCGS10.CBL | 577 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 589fa4f288 | /stclienti.cbl | 467 | fixed | 3 |  |  | micro-focus | accounting-erp | subprogram | COBOL-85 |
| 290394dfb3 | /ORCSCHKTCHK.CBL | 2065 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 5b26fee86a | /ORCSPTNUM.CBL | 384 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| bd009b6869 | /ORCGW20.CBL | 9829 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4f072b9b31 | /ORCR0040.CBL | 10489 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 87e9485557 | /zoom-gt.cbl | 8271 | fixed | 1 |  |  | acucobol | accounting-erp | subprogram | COBOL-85 |
| 5225677d43 | /day04p2.cbl | 75 | fixed | 0 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| c205485498 | /usecase1.CBL | 11 | unknown | 0 |  |  |  |  |  |  |
| fb14ab169f | /dummy-rdbmsMT.cbl | 51 | free | 4 |  |  | gnucobol | banking-finance | subprogram | COBOL-85 |
| f55c845239 | /ORCGQSUB03.CBL | 247 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 00b9b1062d | /IC2254.2.cbl | 186 | free | 0 |  |  |  |  |  |  |
| c0cec74caf | /ORCR0435.CBL | 534 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 8a691f3d97 | /RoutBTDLIUP.cbl | 90 | fixed | 4 |  |  | ibm-mainframe | other | subprogram | COBOL-85 |
| 21e9e89fa6 | /8-CSMUL.CBL | 549 | fixed | 4 |  |  | micro-focus | payroll-hr | online-cics | COBOL-85 |
| 302127edda | /CPBIS049.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 9c57370659 | /ORCGJ02.CBL | 5891 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 50111024f2 | /susesqf02b.cbl | 251 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| c039e04c98 | /ORCGH99.CBL | 904 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 47cfe94c3e | /ORCR0300.CBL | 4553 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ae8817c34d | /cllpg637.cbl | 848 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| ffc566e211 | /PRINTUTL.CBL | 1100 | fixed | 4 |  |  | micro-focus | utility-tooling | subprogram | COBOL-85 |
| 85d7492712 | /SOKATU1515.CBL | 1546 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 22c2f85430 | /EMC_WK_GIMEN.CBL | 16 | fixed | 0 |  |  |  |  |  |  |
| 9f33c0a465 | /TPROG16.cbl | 119 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| ba512b1185 | /ORCR0485.CBL | 2395 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a16ded90f5 | /ORCBNYUALL.CBL | 1998 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 21fd28a16d | /EmptyLines.cbl | 9 | fixed | 2 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 3fc5742265 | /CEXM502B.cbl | 34 | fixed | 0 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| 446040701f | /ORCGP02W2.CBL | 3884 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 32ed70d294 | /Program04_Type_R_Processing | 219 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 0af679890c | /LGICUS01.cbl | 109 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 3c95bc4134 | /ORCGI04.CBL | 2039 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| ed565741eb | /PWPE0105.cbl | 592 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| bb25cede88 | /LGICVS01.cbl | 180 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 3a963b149e | /顺炮横车对直车.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| f5edac85e1 | /[2012] Night of the Owls (D | 50 | free | 0 |  |  |  |  |  |  |
| ef459d4620 | /hellopgm.cbl | 15 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| beb1e44b22 | /breakdown.aspx.cbl | 1032 | fixed | 1 |  |  |  |  |  |  |
| 8cf0525443 | /CreateDataFile.cbl | 35 | fixed | 3 |  |  | micro-focus | retail-commerce | batch | COBOL-85 |
| 3e8336d4ed | /X-Men - Part 005.cbl | 932 | fixed | 0 |  |  |  |  |  |  |
| dc76353f91 | /ORCBPRVPRT.CBL | 506 | fixed | 4 |  |  | micro-focus | healthcare-medical | batch | COBOL-85 |
| dc5216205c | /ORCR1030.CBL | 6956 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3471d18454 | /ACAS.cbl | 375 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 08817533dd | /wumpus.cbl | 206 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 05b8d15a6a | /LGICUS01.cbl | 135 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 2942ed92c1 | /float-demo.cbl | 172 | fixed | 0 |  |  | gnucobol | education-tutorial | demo | COBOL-2002 |
| d382964883 | /STBEFW310.CBL | 458 | fixed | 4 |  |  | micro-focus | banking-finance | batch | COBOL-85 |
| 37da13c346 | /SOKATU0210.CBL | 1672 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ae7d89a389 | /ORCBZ003.CBL | 800 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4e40f13a37 | /PARTSUPP.cbl | 57 | fixed | 0 |  |  |  |  |  |  |
| 54e7c8e148 | /BYHV36.cbl | 262 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 0b21992ac3 | /irspostingMT.cbl | 967 | free | 4 | ✓ |  | gnucobol | accounting-erp | subprogram | COBOL-2002 |
| 6525db765f | /ORCGP02W1.CBL | 5424 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 559650b143 | /ORCSPRTNM.CBL | 476 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 75ddcf21b2 | /PW01069R.cbl | 262 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| c95eb175c8 | /SQ130A.CBL | 392 | fixed | 4 |  |  | gnucobol | education-tutorial | test | COBOL-85 |
| 60af960cbc | /XZ0D0006.CBL | 3519 | fixed | 4 | ✓ | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| eb8956b315 | /hello.cbl | 5 | free | 2 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 831d2e77d7 | /CUSUPD.cbl | 290 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 682fcfc922 | /stsottoc-p.cbl | 784 | fixed | 3 |  |  | micro-focus | retail-commerce | batch | COBOL-85 |
| dabf3e2d29 | /SOKATU4020.CBL | 1569 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a8861a1623 | /LISPRE13.CBL | 610 | fixed | 4 |  |  | micro-focus | retail-commerce | batch | COBOL-85 |
| 34796930c7 | /ORCR0500.CBL | 974 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 18281cae4a | /[DC Comics] DC Master Readi | 2195 | free | 0 |  |  |  |  |  |  |
| 8e534db0ed | /DueSubsRpt.CBL | 232 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| b8474226c1 | /ORCGZ03.CBL | 3817 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ea559971b5 | /ORCS02.CBL | 17847 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| cf9be8858f | /ORCGW03.CBL | 1377 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| a9244c1348 | /ORCGK02.CBL | 11005 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| c9892fb0ae | /pw00200p.cbl | 501 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| 345e80bb26 | /ORCBD999.CBL | 1307 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d5a88dc0d6 | /ORCGW06.CBL | 3462 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3cd7a50ee0 | /ORCR0670.CBL | 555 | fixed | 4 |  |  | ibm-mainframe | healthcare-medical | batch | COBOL-85 |
| d252882f77 | /ORCR0620.CBL | 3606 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| cd2721a833 | /ORCSP02.CBL | 3435 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 077744637f | /ORCSC80201204.CBL | 2933 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| b10310c3da | /FRAUDMOD.cbl | 43 | fixed | 3 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 499b414ba7 | /adscbl301.cbl | 155 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | subprogram | COBOL-85 |
| f49c413a6a | /0-FKEYS.CBL | 354 | fixed | 4 |  |  | micro-focus | payroll-hr | subprogram | COBOL-85 |
| 01925e7292 | /cash-register.cbl | 49 | unknown | 2 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 3c0bf85bf2 | /ORCGX100.CBL | 69 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 45583e8af0 | /assignment2.cbl | 303 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 38d0a10219 | /ORCR0104.CBL | 5415 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| be5ad7de23 | /ORCGQ01.CBL | 5178 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| f90cbc7117 | /PW01062R.cbl | 306 | fixed | 4 |  |  | micro-focus | government-public | online-cics | COBOL-85 |
| 3050ab595e | /ORCGXGERR.CBL | 62 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| df954e2aca | /LGBAT003.cbl | 825 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 188ce32417 | /ORCGW20.CBL | 4130 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 831c4bf186 | /EM0204.CBL | 157 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
