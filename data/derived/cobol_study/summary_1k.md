# COBOL-in-SWH exploratory study — summary

_Generated 2026-07-08T10:21:56Z · 1000 samples (993 text, 7 non-text), 526 LLM-judged._

## Lines of code (code lines, excl. blank/comment)

- min **1** · median **29** · mean **938.9** · max **29182** · total **932370**

## Source format (mechanical heuristic)

- fixed: 532
- free: 454
- unknown: 7

## Feature prevalence (mechanical, over text files)

- EXEC SQL: 18 (1.8%)
- EXEC CICS: 15 (1.5%)
- COMP-3: 42 (4.2%)
- COPY: 331 (33.3%)
- CALL: 332 (33.4%)

## Is COBOL? (judge)

  - true: 525 (99.8%)
  - false: 1 (0.2%)

## Dialect family (judge)

  - gnucobol: 343 (65.2%)
  - unknown: 66 (12.5%)
  - ibm-mainframe: 58 (11.0%)
  - micro-focus: 37 (7.0%)
  - acucobol: 14 (2.7%)
  - other-vendor: 5 (1.0%)
  - rm-cobol: 2 (0.4%)
  - fujitsu-nec: 1 (0.2%)

## COBOL standard (judge)

  - COBOL-85: 515 (97.9%)
  - COBOL-2014: 6 (1.1%)
  - COBOL-2002: 4 (0.8%)
  - unknown: 1 (0.2%)

## Source format (judge)

  - fixed: 473 (89.9%)
  - free: 53 (10.1%)

## Domain (judge)

  - healthcare-medical: 211 (40.1%)
  - education-tutorial: 98 (18.6%)
  - accounting-erp: 38 (7.2%)
  - demo-example: 37 (7.0%)
  - retail-commerce: 29 (5.5%)
  - banking-finance: 28 (5.3%)
  - utility-tooling: 24 (4.6%)
  - other: 17 (3.2%)
  - test-suite: 17 (3.2%)
  - insurance: 14 (2.7%)
  - payroll-hr: 9 (1.7%)
  - manufacturing-logistics: 3 (0.6%)
  - unknown: 1 (0.2%)

## Program type (judge)

  - batch: 235 (44.7%)
  - subprogram: 108 (20.5%)
  - demo: 86 (16.3%)
  - online-cics: 74 (14.1%)
  - test: 21 (4.0%)
  - copybook: 1 (0.2%)
  - unknown: 1 (0.2%)

## Maturity (judge)

  - production-like: 343 (65.2%)
  - student-exercise: 126 (24.0%)
  - snippet: 30 (5.7%)
  - toy-or-hello-world: 27 (5.1%)

_Judge tokens: 3550999 prompt + 281522 completion._

## Samples

| sha1_git | file | LOC | fmt | divs | SQL | CICS | family | domain | type | std |
|---|---|---:|---|---:|:-:|:-:|---|---|---|---|
| e3bbcc6e87 | /ga020.cbl | 6864 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| 58200bf483 | /WBC_77549_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9355faa34a | /EJER19.CBL | 101 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 610a2c5290 | /WBC_46442_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c6bed41c57 | /ORCS02.CBL | 6453 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 80a15fdf82 | /WBC_84322_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 76e67f224e | /[Marvel] 004-4 The Screamin | 26 | fixed | 0 |  |  |  |  |  |  |
| f1542e264d | /ECS029E.cbl | 728 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| abaffc9b92 | /WBC_34062_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c97f4df6b0 | /Lista7E4.cbl | 269 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| ffadea52bb | /WBC_17941_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 69baaba3b5 | /WBC_91228_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 961bfefecf | /WBC_31295_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a0187b5f39 | /WBC_92167_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fbcfa24f68 | /ORCRRECEMAIN.CBL | 2140 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 241d35a3a4 | /WBC_29066_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 63f8daf05b | /EX05.CBL | 60 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| e2f70b20c7 | /WBC_18657_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 480776cb53 | /WBC_48437_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 66fb48906b | /ECS086.cbl | 1197 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| c7a22ad9f4 | /WBC_68378_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1c3e5c2067 | /WBC_43537_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a96274ecce | /ORCSAPIFMTERM.CBL | 170 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| c9d478b5af | /Parte1A.cbl | 51 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| e1af761035 | /admin-server.cbl | 203 | fixed | 4 |  |  | gnucobol | other | online-cics | COBOL-85 |
| 3c3057b9ad | /D88KUF.cbl | 35 | fixed | 0 |  |  |  |  |  |  |
| 4378bf52fc | /SaludoCobol.cbl | 6 | free | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 9e95cbe0f5 | /FunDeclare.cbl | 123 | fixed | 1 |  |  | gnucobol | education-tutorial | test | COBOL-2014 |
| bd261c8d1f | /WBC_45333_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a0614d6437 | /WBC_20963_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a7695d4324 | /gorbitsa.cbl | 111 | fixed | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 617bc50a91 | /sales.cbl | 540 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 9dd4da118a | /OPENMOCA.CBL | 167 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| cec93565b9 | /bams.cbl | 499 | fixed | 4 |  |  | gnucobol | other | online-cics | COBOL-85 |
| c8cb037b24 | /WBC_9562_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 9980478d37 | /WBC_95806_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 67af1c8581 | /WBC_29894_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c5444218c3 | /procesar.cbl | 163 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| 6f0bcf5976 | /WBC_90990_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 63135b0c8d | /triangle-1.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 13747c5a0a | /WBC_7821_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 6d2c13737c | /ORCBC010.CBL | 3958 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 09518e49fa | /ORCR0640.CBL | 16718 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 7d86f4987a | /WBC_34360_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f5046ef32d | /ORCSCNYUIN.CBL | 2129 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 9adb5b2026 | /WBC_71346_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cc109bd6f7 | /report.cbl | 1 | free | 1 |  |  |  |  |  |  |
| 363ee6df86 | /WBC_80300_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a08a11af2e | /cgp001t.cbl | 139 | fixed | 4 |  |  | micro-focus | other | online-cics | COBOL-85 |
| 6fc98b74f5 | /BANK2.cbl | 138 | fixed | 4 |  |  | gnucobol | banking-finance | subprogram | COBOL-85 |
| 727b87fd3d | /WBC_64054_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e0f1e5466c | /WBC_8051_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| b14a84dbe6 | /EL309AHL.cbl | 1990 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 4200c43e36 | /edit3.cbl | 26 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 62676aacba | /cadcli.cbl | 295 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| b2bd24b36b | /WBC_87243_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| eee28c1c06 | /WBC_26279_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 449dcce278 | /Control2.cbl | 36 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 7f000f015f | /ORCR0600.CBL | 1930 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| bbb308332f | /AVG-SCI-GRADE.cbl | 64 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| a38dface8e | /L5E5.cbl | 88 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| a2acc1d112 | /WBC_43264_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e146ebf84f | /WBC_72822_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 526e682ae3 | /SEARCH.cbl | 8 | unknown | 0 |  |  |  |  |  |  |
| 4013be22d6 | /WBC_98833_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a0e3547da4 | /WBC_51797_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 643d158096 | /ORCGZ99.CBL | 673 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 1fa9407403 | /PP01221C.cbl | 364 | fixed | 4 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| 2f7e980345 | /ORCR0956.CBL | 2422 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 5450aee554 | /WBC_29685_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 02019e9fef | /ORCR0710.CBL | 4655 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 491b57004c | /WBC_67110_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d44f987760 | /EDI-selordini.cbl | 17957 | fixed | 4 |  |  | acucobol | retail-commerce | batch | COBOL-85 |
| 724da8ca9b | /SOKATU4210.CBL | 2088 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a9c994f7dd | /galhoCGD011-2.cbl | 299 | fixed | 4 |  |  | micro-focus | education-tutorial | batch | COBOL-85 |
| 6ecd6c7c86 | /KEI_KYOCHO_CD.CBL | 10 | free | 0 |  |  |  |  |  |  |
| 2774c1ca05 | /WBC_3558_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 5ed27b8d87 | /menu03.cbl | 44 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 89e3bd68ed | /WBC_317_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7401b85ca9 | /SEIKYU4017.CBL | 1128 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| df74a43594 | /CL15EJ01.v.1.1.cbl | 335 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 7fdad2e2fc | /WBC_54253_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e97d0857e2 | /WBC_95359_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fde9090ee8 | /CUSTCTRL.cbl | 152 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| d3454b9751 | /COBARQ03.cbl | 70 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| c908fd449d | /ORCR0300.CBL | 6322 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 6162b15925 | /WBC_49264_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 22455bb530 | /WBC_97806_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9236cd1258 | /ORCGK02.CBL | 9553 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 92c4a629ff | /WBC_59379_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 871b25a9a8 | /WBC_79203_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 41d7fadb0b | /WBC_25957_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7936514f69 | /ORCR0500.CBL | 1422 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ffac046e98 | /ORCR0640.CBL | 27998 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 30bee8d07f | /Lista5E9.cbl | 62 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| efcd66ec03 | /WBC_45493_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6a01789e9f | /ORCSYAKINTOKU.CBL | 246 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 5ebc4fa05d | /ORCSNYUACCT.CBL | 3229 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| bc58996354 | /MENUS.cbl | 115 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 557481bac2 | /WBC_8584_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| f9dd9e44c9 | /rdab0258.cbl | 257 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 6c2e8efc5f | /WBC_12257_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9b30ead113 | /ORCGW01.CBL | 1966 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| abe97629e8 | /hello.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 15df1c45ac | /WBC_88471_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b6ab857e14 | /extenso.cbl | 270 | fixed | 4 |  |  | unknown | utility-tooling | subprogram | COBOL-85 |
| 2381b39932 | /ORCR0730.CBL | 10741 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 396b9642de | /WBC_17492_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6f42d168b6 | /WBC_37399_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1ae7deea04 | /ORCGT01.CBL | 6146 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| fb0cd97127 | /WBC_90230_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3cd15a14f3 | /WBC_9535_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 65cef33d2d | /ORCR0650.CBL | 374 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 2a93060a7c | /ZBNKPRT1.CBL | 545 | fixed | 4 |  |  | micro-focus | banking-finance | batch | COBOL-85 |
| f44a3a14b9 | /MENU01.cbl | 16 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 5452727c82 | /lgicdb01.cbl | 141 | fixed | 4 | ✓ | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 72916f4d0d | /WBC_1023_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| ec6cda5c4b | /CSADDBL.cbl | 238 | fixed | 3 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 50152e3859 | /ORCR0025.CBL | 523 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4ea175a8e2 | /WBC_52087_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2a0d2df665 | /pw00757s.cbl | 319 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 3cbd5b9545 | /S04P028.CBL | 156 | fixed | 4 | ✓ |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| 327cf57d34 | /WBC_75177_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0e83bded3f | /WBC_44277_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3443fdbb23 | /ORCR0810.CBL | 1482 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 5738c776d5 | /WBC_19961_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 98abe4475e | /ORCGX01.CBL | 2000 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 003a4c9f53 | /SOKATU2705.CBL | 1314 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3b92ff7e5b | /triangle-1.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 88532d0f80 | /FunDeclareWithExec.rdz.cbl | 164 | fixed | 3 | ✓ |  | ibm-mainframe | other | demo | COBOL-85 |
| 0de49f2e56 | /JU8EXE12.CBL | 30 | free | 0 |  |  |  |  |  |  |
| 58631158a8 | /ORCGDID2.CBL | 80 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 1db5fc5db5 | /finana.cbl | 4769 | fixed | 4 | ✓ |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 324c509d95 | /WBC_19373_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 65c6bdcb44 | /ORCS02.CBL | 9753 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 64abffec29 | /read-score-to-grade_2022080 | 51 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 5c22d9e538 | /WBC_88038_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| df5d9393bd | /WHENCodeElements.rdz.cbl | 12 | fixed | 0 |  |  |  |  |  |  |
| 5a3e3bd52c | /WBC_52819_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e514ac0e93 | /procedures_gotos.cbl | 27 | fixed | 3 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| 982332e014 | /BANK9.cbl | 597 | fixed | 4 |  |  | gnucobol | banking-finance | online-cics | COBOL-85 |
| 8444c0aaf2 | /WBC_16027_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| dbf69e1946 | /ORCSSYU40.CBL | 683 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| d4ce34a067 | /lista8E2Programa01.cbl | 116 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 6951a65181 | /write-emp1.cbl | 35 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| c1f05ef3f9 | /hellow42_level_88_variables | 29 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| d9740fad15 | /gctestsetup.cbl | 231 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| cac3f7e958 | /WBC_7608_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 40e9642158 | /gctestrun2.cbl | 1089 | fixed | 4 |  |  | gnucobol | utility-tooling | test | COBOL-85 |
| 657392a250 | /ORCBS02.CBL | 200 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4dc31f72a4 | /WBC_1880_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 9726afdce7 | /test9011.cbl | 9 | fixed | 3 |  |  | unknown | test-suite | test | COBOL-85 |
| c0dc07b199 | /CPBIS091.CBL | 10 | free | 0 |  |  |  |  |  |  |
| 5f795a0535 | /WBC_71901_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5707f35c20 | /PW01112C.cbl | 1400 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| ace9ff4419 | /ORCGXAERR.CBL | 63 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| dca734f9c7 | /ORCGI0SUB02.CBL | 819 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 07271b244d | /WBC_58840_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 39bd6bf5ea | /genrep.CBL | 256 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| a29c498e53 | /IVP20001.cbl | 24 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 0160017975 | /ORCBM032.CBL | 935 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 6c0bccf58e | /tp2ej1.cbl | 45 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| f5a79cd4f4 | /sqlaprep.cbl | 514 | fixed | 0 |  |  | ibm-mainframe | utility-tooling | copybook | COBOL-85 |
| cb25ea8837 | /WBC_54537_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 120bc6118d | /rrmbs196.cbl | 25 | fixed | 4 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-85 |
| 67bd984111 | /ORCGL99.CBL | 440 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| e12125b970 | /WBC_6446_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f06645145c | /principal.cbl | 97 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 180415e085 | /IBS_DATE.cbl | 10 | free | 0 |  |  |  |  |  |  |
| d11a9f543d | /ESEGUI.CBL | 88 | fixed | 4 |  |  | micro-focus | utility-tooling | subprogram | COBOL-85 |
| a10011263a | /ORCGX01.CBL | 1075 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 0525917637 | /WBC_65449_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f7263b61f0 | /playpen.cbl | 43 | fixed | 0 |  |  | unknown | demo-example | demo | COBOL-85 |
| a4e7dacfef | /WBC_89189_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7bfad06d2f | /testm.cbl | 53 | fixed | 3 |  |  | acucobol | demo-example | demo | COBOL-85 |
| 4c699ec092 | /WBC_97464_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6d1d3d539e | /ORCHCM35.CBL | 244 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 3410570b1a | /ORCGK05.CBL | 4838 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d0d9f01acb | /main.cbl | 26 | free | 4 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 209dfa5a1c | /Parte1B.cbl | 381 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 40a3824bd4 | /CPBIS112.CBL | 20 | fixed | 0 |  |  |  |  |  |  |
| 54e93d6273 | /SEIKYU1903.CBL | 1847 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 0c1f4fde5c | /ORCGI41.CBL | 7533 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a3f0523623 | /2-CANDID.CBL | 252 | fixed | 4 |  |  | micro-focus | other | subprogram | COBOL-85 |
| 95232ef766 | /tempCodeRunnerFile.cbl | 37 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 7a6276238f | /ORCSNYURECEDEN.CBL | 12083 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| efb6681be0 | /WBC_67459_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4e4db9f3bb | /WBC_65362_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| afe01ef974 | /ORCGS02.CBL | 4559 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| e1e0a18a31 | /DayOfWeek.cbl | 16 | free | 3 |  |  | gnucobol | demo-example | subprogram | COBOL-2002 |
| d238cdf665 | /ORCR1240.CBL | 4601 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ee3f3809e8 | /WBC_6537_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 9e3867c5ae | /WBC_86843_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4d951aa0e1 | /pwc0917a.cbl | 1263 | fixed | 4 |  |  | micro-focus | manufacturing-logistics | batch | COBOL-85 |
| 11e88d5764 | /SALEPARAM.CBL | 52 | fixed | 0 |  |  |  |  |  |  |
| 3ae721d3f1 | /HEAD.CBL | 39 | fixed | 3 |  |  | gnucobol | other | subprogram | COBOL-2002 |
| 39bcc335ae | /ORCGTID1.CBL | 81 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| b01ef53db0 | /WBC_49176_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ce42cd9ae1 | /ORCGK02NYU.CBL | 7806 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 579f40ba2d | /WBC_93986_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f4d413cad5 | /codtname.cbl | 30 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 2e303732f9 | /WBC_82586_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1a400d6934 | /llvm-override-function-not- | 1 | free | 0 |  |  |  |  |  |  |
| d31326f634 | /WBC_77462_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0c9ae3ef77 | /Project1.cbl | 55 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 84a2d83112 | /WBC_1087_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6ff1b96771 | /test9038.cbl | 61 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-2014 |
| 38f60a9099 | /WBC_48784_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9a0f92ac43 | /cheet_cheat.cbl | 44 | fixed | 0 |  |  |  |  |  |  |
| 42b8c68d1c | /WBC_8521_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 66db0fcb17 | /WBC_28968_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 344de83aee | /HBSIS06P.cbl | 352 | fixed | 4 |  |  | gnucobol | retail-commerce | subprogram | COBOL-85 |
| d107349872 | /WBC_23069_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 31c0f17956 | /MoveOnlyToLargeEnoughVariab | 8 | unknown | 3 |  |  | unknown | test-suite | test | COBOL-85 |
| 80fa15e5f0 | /STBEFD776.CBL | 458 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| d24ef95169 | /tempcbl.cbl | 186 | fixed | 4 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-85 |
| 4d42b7a1b2 | /pwpa6115.cbl | 211 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| 6ff3c78eff | /EXEC84.2.cbl | 1846 | fixed | 4 |  |  | unknown | test-suite | batch | COBOL-85 |
| 0004c5cef2 | /SuffixLineOverflow.rdz.cbl | 9 | fixed | 2 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| f968c5d9f1 | /videostp.cbl | 593 | fixed | 4 |  |  | acucobol | retail-commerce | online-cics | COBOL-85 |
| 3c4c92e93b | /selordini.cbl | 3241 | fixed | 4 |  |  | acucobol | retail-commerce | online-cics | COBOL-85 |
| 605c2e9454 | /AROMA96.CBL | 150 | fixed | 4 |  |  | micro-focus | education-tutorial | batch | COBOL-85 |
| b71d4ce7a9 | /D181KKN.cbl | 10 | free | 0 |  |  |  |  |  |  |
| c5425aa816 | /ORCSC60200804.CBL | 3257 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| d7f198c14d | /Option.cbl | 121 | fixed | 1 |  |  |  |  |  |  |
| 53e21220a6 | /WBC_76531_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 77ee6923ac | /main.cbl | 2 | free | 0 |  |  |  |  |  |  |
| 8d8a106ac3 | /WBC_4918_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 861ba32331 | /WBC_18297_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ad0247648e | /FIXINV.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| d9ff102f72 | /FAVRPT.cbl | 218 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 35e9b9d1fd | /cop050.cbl | 863 | fixed | 4 |  |  | micro-focus | retail-commerce | online-cics | COBOL-85 |
| c4060319b1 | /WBC_51616_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c0f75d60d0 | /ORCSSKYGET.CBL | 518 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 88a5bc3408 | /WBC_61456_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9a5f27aa4f | /WBC_92994_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f2e0f1587f | /ctxml000.cbl | 4996 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| fd1d042e69 | /Phnadd01.cbl | 81 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 6ea350ce2d | /STMF03.CBL | 2357 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 7365e7a2d3 | /6-FIRMES.CBL | 82 | fixed | 4 |  |  | acucobol | accounting-erp | subprogram | COBOL-85 |
| ad8778d614 | /WBC_607_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 6df8d6a20b | /triangle-2.cbl | 32 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| cc2046f5a5 | /ORCGX04.CBL | 4767 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e26dcaca45 | /STBEFW372.CBL | 458 | fixed | 4 |  |  | micro-focus | banking-finance | batch | COBOL-85 |
| 95b03a2cae | /[DC Comics] Zero Hour (WEB- | 161 | free | 0 |  |  |  |  |  |  |
| 8ae84d3bfb | /pw02124c.cbl | 1536 | fixed | 4 |  |  | micro-focus | banking-finance | online-cics | COBOL-85 |
| 5df6067b61 | /WBC_18609_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e2e49d2840 | /WBC_77580_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 19f414f443 | /WBC_17538_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7a4a321439 | /CISUF450.CBL | 10 | free | 0 |  |  |  |  |  |  |
| b87ae9c318 | /WBC_38733_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6575f8c464 | /SEQWRITE.CBL | 38 | fixed | 4 |  |  | micro-focus | education-tutorial | demo | COBOL-85 |
| 7f7c29d5e3 | /ORCGSAPI01S99.CBL | 410 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| c86df1ee6b | /WBC_56940_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fb34b38e24 | /ORCR0090.CBL | 1857 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4155d23301 | /WBC_92678_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 99710f63a3 | /WBC_52757_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 8a34e2c300 | /WBC_25550_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 412671c32b | /ORCSFTNJGNCHK.CBL | 2689 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 2d1bf789bb | /WBC_53498_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f4cd11bcdb | /WBC_2053_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 6ab92455a7 | /write-post-string.cbl | 88 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| e0985af785 | /ORCGZ03.CBL | 3329 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 8874a90147 | /WBC_85564_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 8feb5b044a | /WBC_28693_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 77f8c98816 | /ORCGWID1.CBL | 129 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| fb6a5d4e86 | /WBC_44851_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bcb5edcfa1 | /ZUTZCPC.CBL | 3506 | fixed | 4 | ✓ | ✓ | ibm-mainframe | utility-tooling | batch | COBOL-85 |
| 88bfa462a5 | /mainfile2.cbl | 18 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 591f970915 | /sl950.cbl | 568 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| e854e52389 | /cobranza.cbl | 1538 | fixed | 3 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| b0d2b7b541 | /G3-VISA-MER-EDIT.cbl | 121 | fixed | 2 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 0ef06d746e | /lgipol01.cbl | 101 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| b5d0b89bcf | /WBC_27980_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1ef986fabb | /WBC_11624_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 40e51a5378 | /WBC_48775_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 31194fde5e | /EL568.cbl | 807 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| cd39f90fb5 | /ricalfor-bat.cbl | 940 | fixed | 3 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 9d053244ee | /WBC_76459_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5c7ae2414e | /WBC_75748_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 24dba86f78 | /3-MAL.CBL | 494 | fixed | 4 |  |  | acucobol | payroll-hr | batch | COBOL-85 |
| 7b49d82931 | /WBC_62854_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0fbafcd7e5 | /WBC_53027_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7ec45238c9 | /ORCGO01.CBL | 1058 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| fc67d9d1ce | /WBC_27245_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5bcd85896b | /Data1.cbl | 16 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d25cbf2e4e | /ORCGW30.CBL | 1229 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 5176c9fa54 | /PP01219C.cbl | 250 | fixed | 4 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| 5d4df3bad2 | /ORCGW06.CBL | 3341 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| e4c753ecec | /triangle-4.cbl | 38 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 81162fa996 | /EL6401.cbl | 3424 | fixed | 4 |  | ✓ | ibm-mainframe | insurance | online-cics | COBOL-85 |
| 217c653440 | /ADETAKT.CBL | 66 | fixed | 4 |  |  | rm-cobol | accounting-erp | subprogram | COBOL-85 |
| dfdbe425df | /Z95768.CBL(DAYCALC).cbl | 84 | fixed | 4 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-85 |
| 3c3260bbea | /WBC_24852_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 30935ddca5 | /ORCS01.CBL | 29182 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 81f9f9933a | /cbl0005.cbl | 114 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 3f3d381722 | /WBC_22225_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bac7ee4551 | /WBC_3572_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2f753d5c99 | /WBC_87559_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6be84e0397 | /pwpe0352.cbl | 407 | fixed | 4 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| 71aaf03855 | /PAYLIB.CBL | 18 | fixed | 2 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| 4fba0498ce | /Check-box.cbl | 31 | fixed | 4 |  |  | acucobol | demo-example | demo | COBOL-85 |
| 8f4e283c38 | /STBEFW082.CBL | 456 | fixed | 4 |  |  | micro-focus | retail-commerce | batch | COBOL-85 |
| 42db3b11a1 | /WBC_3257_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| bac818cefa | /WBC_95286_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 342f45e9a2 | /ORCR0090.CBL | 3731 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3f7995e35a | /CISPF003.CBL | 10 | free | 0 |  |  |  |  |  |  |
| a4229df2c1 | /WBC_88967_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c7de7fb2a1 | /base.cbl | 9 | free | 3 |  |  | unknown | unknown | unknown | unknown |
| 9f4ee00fb5 | /WBC_61450_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a1bd230a2c | /SalesDataValidation.cbl | 195 | fixed | 3 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 725bcfdc90 | /py050128.cbl | 113 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 09a4a843b2 | /ORCSC80201404.CBL | 3084 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 8741c6f87c | /case24.cbl | 15 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b92670e810 | /WBC_80177_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 43a91e02a4 | /WBC_31347_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 81a5996fa5 | /WBC_48562_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5304f5fd13 | /ORCR0640.CBL | 15322 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| f52b12d5df | /D571HNS.cbl | 22 | fixed | 0 |  |  |  |  |  |  |
| 7cd093cd56 | /WBC_39580_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 69ad328359 | /ORCGK02.CBL | 10239 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 40106887fe | /WBC_95166_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cfa0a0b616 | /[DC Comics] Batman- War Gam | 119 | free | 0 |  |  |  |  |  |  |
| 5ca3e463ba | /WBC_31032_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3cde1384a9 | /WBC_11042_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3f582b103c | /WBC_5897_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 70a2b123c0 | /data-rec-example.cbl | 26 | free | 1 |  |  |  |  |  |  |
| 7a912db8af | /ORCGPERR.CBL | 72 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 0bf7cd1def | /ORCR0105.CBL | 10275 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3507fa4c83 | /test.cbl | 53 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| cd546517e8 | /[Marvel] 2015-2018 Part 11. | 87 | fixed | 0 |  |  |  |  |  |  |
| cbb70e3846 | /insmov.cbl | 61 | fixed | 3 | ✓ |  | gnucobol | banking-finance | subprogram | COBOL-85 |
| 102828accb | /WBC_66781_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e63336aebc | /WBC_2216_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4b8df87f65 | /WBC_46156_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 865e7eb20c | /WBC_96297_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ae3c376284 | /ORCMUP0131.CBL | 489 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| a878dc76c5 | /TP_ALGOIIII.cbl | 552 | free | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 8d33b7b38f | /WBC_30900_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e99ab43a65 | /ORCGW12.CBL | 1651 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| d9049029a9 | /WBC_11623_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0f17d9e5c3 | /WBC_60646_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 899dd0155d | /WBC_64572_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5ac15dd688 | /WBC_32524_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b995321c6f | /OTAMESHI.cbl | 14 | fixed | 4 |  |  | fujitsu-nec | demo-example | demo | COBOL-85 |
| effdfd57c9 | /WBC_60347_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| af0fcbe417 | /ORCSKOHPLUS.CBL | 291 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| f3cdc6228e | /ORCGG100.CBL | 989 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| eb8a570a75 | /cobolGreeting.cbl | 11 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| b0486fcebe | /WBC_14868_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4ca0094d19 | /WBC_76928_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1f39546df1 | /WBC_43285_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f60328df69 | /WBC_7908_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 820e184dba | /sl910.cbl | 1475 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 5f7b36d6e6 | /Codegen.rdz.cbl | 54 | fixed | 3 |  |  | micro-focus | utility-tooling | demo | COBOL-85 |
| 5859fab7dd | /3-NATMET.CBL | 341 | fixed | 4 |  |  | acucobol | payroll-hr | batch | COBOL-85 |
| d50edd9756 | /ORCGI4API02.CBL | 1388 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| e20a974fbf | /CT900.CBL | 3617 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 9e3b228c07 | /ORCGJ04.CBL | 6509 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 033186e79e | /SSGROLE.CBL | 784 | fixed | 2 |  |  | gnucobol | accounting-erp | subprogram | COBOL-85 |
| 447927e3c8 | /ORCR0035.CBL | 463 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 37c118216c | /29TenderChangev2.cbl | 32 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| cd07c435d1 | /Lab2c.cbl | 64 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 17b73273a2 | /hellow81_address_received.c | 16 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 88ad71fbfb | /ORCBD999.CBL | 1288 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 27837bd54d | /WBC_72489_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 27c4f438e7 | /ORCR0630.CBL | 3324 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e8510c8290 | /G3-VFX-3-PUR.cbl | 237 | fixed | 3 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| e021dda680 | /WBC_45185_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 65d7133393 | /CLO.TIP39.ACCT_POSITION.CBL | 70 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| ff5ebada91 | /UNSTRING_01.cbl | 126 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| f35e6b12f5 | /LTRKRN.cbl | 10 | free | 0 |  |  |  |  |  |  |
| 70bebabd54 | /ORCGK03.CBL | 4380 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 97ff2839a3 | /WBC_28928_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f8b00a02a6 | /WBC_55802_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 92d614f19e | /ORCR0104.CBL | 4396 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ec85f60b63 | /GNSWICIC.cbl | 31 | fixed | 0 |  |  |  |  |  |  |
| 8e46dd6b31 | /ORCSODRNACCT.CBL | 5419 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 1af4fd81ae | /ORCSCHKTCHK.CBL | 1962 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 6630eca01a | /PAYRPTRB.cbl | 416 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| e594b193d3 | /triangle1.cbl | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 7752e32f42 | /WBC_73534_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 95d0dc2dd7 | /ORCR0470.CBL | 383 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9832ee75a2 | /ORCR0840.CBL | 4281 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 79817bb779 | /WBC_72393_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9f8ee2be45 | /2-APPR.CBL | 399 | fixed | 4 |  |  | micro-focus | payroll-hr | online-cics | COBOL-85 |
| 12cf47bb5a | /SOKATU3415.CBL | 1539 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 43fc5065bd | /CSIMPCL.cbl | 84 | fixed | 0 |  |  | unknown | other | demo | COBOL-85 |
| 7e9434824c | /ORCBPTNUMCHG.CBL | 1218 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a7b6f31b2d | /ORCSROUNYUIN.CBL | 578 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| a764c54976 | /cgi-edit-user.cbl | 287 | fixed | 3 | ✓ |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 493add7fa4 | /Cobol005.cbl | 27 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| 19a42c3d49 | /WBC_8111_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a975fbd976 | /MyGrade.cbl | 66 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 075180f5c7 | /ORCS02.CBL | 17667 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 994faa302d | /WBC_40344_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 98ddb706d4 | /CONBRE3.CBL | 61 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 5ee48b2162 | /ORCGZ100.CBL | 512 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 5acc9523a7 | /WBC_28184_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 8984ad3726 | /WBC_90129_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| dc0bb1fc08 | /ORCSNYURECEDEN.CBL | 1713 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 181483da4b | /ORCGI20.CBL | 2249 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 4d5fb5885f | /RW301M.CBL | 71 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| 305186169d | /WBC_4742_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ea2ac2d71c | /WBC_5191_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7fbef89925 | /WBC_14798_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| be93e55007 | /pw01431r.cbl | 538 | fixed | 4 |  |  | gnucobol | manufacturing-logistics | batch | COBOL-85 |
| 19edb364eb | /WBC_85541_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c7e41eb2a0 | /WBC_99103_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 60f2f508de | /MAKEFORM.CBL | 859 | fixed | 3 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 40989fd864 | /WBC_41513_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 413364b303 | /WBC_40597_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b0126e1311 | /trmtsrch.cbl | 337 | fixed | 4 |  |  | ibm-mainframe | healthcare-medical | batch | COBOL-85 |
| 066029f0d6 | /WBC_72908_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| db3362e014 | /ORAPI021S2V3.CBL | 3451 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| aea3e19ab3 | /SBA011010S.cbl | 843 | fixed | 4 |  |  | ibm-mainframe | retail-commerce | subprogram | COBOL-85 |
| c90a96cd2e | /ORCBG006.CBL | 1044 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 7826c079aa | /ORCGU02.CBL | 4008 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3c83f408a5 | /ORCMUP0061.CBL | 466 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| a623e93b30 | /WBC_44778_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| da22337f63 | /WBC_69080_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9ecaabb50b | /WBC_40202_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0352dcb881 | /index.cbl | 6 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| fca7be9e0e | /WBC_68206_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c88743eeaa | /A00000C115.CBL | 1283 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d62ee85551 | /cntlines.cbl | 114 | free | 3 |  |  | gnucobol | utility-tooling | batch | COBOL-2014 |
| 62180c55cb | /ORCGP02W1.CBL | 5890 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 3dc0db3f44 | /CSLS_N.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| 382f3b1693 | /SEIKYU2205.CBL | 1226 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| f684f51934 | /WBC_65851_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c631ce9c25 | /ixread01.cbl | 103 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| c0183eee0f | /WBC_70866_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f078196b29 | /WBC_25406_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| db798a47f7 | /WBC_11829_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6b1df67caf | /WBC_94875_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1533532996 | /two_dim_table.cbl | 31 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| d982edad4d | /WBC_42642_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fed0436828 | /ORCDTCHK008.CBL | 422 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 24aa7c3bad | /SQ211A.CBL | 454 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| 8202ea06e4 | /DCCVTCLPT.cbl | 105 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 38a44386b3 | /WBC_40780_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b331cb4663 | /SOKATU4400.CBL | 956 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| af126f4e77 | /datsub.cbl | 10 | fixed | 4 |  |  | gnucobol | demo-example | subprogram | COBOL-85 |
| 21f70827e7 | /STBEFD358.CBL | 456 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 9ea4c61036 | /TODOHANDLER.CBL | 96 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| ea869751cf | /WBC_72040_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e63c40040e | /EXERCICIO-3-LISTA-6.cbl | 33 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 8507bb4451 | /WBC_60572_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c55cd53ba1 | /WBC_48370_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b5dc2ff661 | /BANK1.cbl | 269 | fixed | 4 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| f287a52892 | /ORCSROUNYUIN.CBL | 2644 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 7cc6cacd82 | /WBC_98093_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3627eb6161 | /sqlca.cbl | 20 | fixed | 0 |  |  |  |  |  |  |
| 08db46b62c | /readEspecFile.cbl | 50 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 791c8d5eaf | /MainInPackage.cbl | 14 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| fe52c80a1a | /WBC_56080_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cfcd27b442 | /WBC_43153_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4f7006881b | /WBC_76499_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 499136f4e8 | /WBC_43591_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5b874fc846 | /l7-4-gadgets-stock.cbl | 49 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 070c6e37b7 | /ORCR0660.CBL | 2914 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 077ceaa694 | /SNT99.CBL | 57 | fixed | 3 |  |  | other-vendor | banking-finance | batch | COBOL-85 |
| 82e00b42fc | /WKREFPGM.CBL | 5 | fixed | 0 |  |  |  |  |  |  |
| 1d36c5cf5e | /WBC_29725_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 33d82bd633 | /ORCR0481.CBL | 2838 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| a21529fc01 | /WBC_417_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 4eec3c9e17 | /WBC_92926_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6f2bcabbcc | /LDBS2650.cbl | 443 | fixed | 4 | ✓ |  | ibm-mainframe | insurance | subprogram | COBOL-85 |
| 7378661474 | /WBC_5609_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fa38ab8b10 | /ORCGK02NYU.CBL | 7305 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 84b82dd6d7 | /ORCSNYUFTN.CBL | 1739 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 24b5c2d6a3 | /WBC_42104_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4b3f9c0998 | /ORCHCN31.CBL | 1504 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 13ed3036ba | /weather.cbl | 184 | fixed | 3 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 795f385a18 | /WBC_24059_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ae04571a15 | /ORCGP02H.CBL | 421 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 2833b74a91 | /CPBD381SSM.cbl | 10 | free | 0 |  |  |  |  |  |  |
| fdcaf2e8a0 | /Bad03fix.cbl | 9 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b36cb4f7aa | /findingana.cbl | 17 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 528ba849ce | /WBC_37018_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3454830507 | /factorialCalc.cbl | 21 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| ae92b54262 | /WBC_82617_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7a8cb7e0d6 | /WBC_82680_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 062bc89061 | /PROGCOLE.cbl | 204 | fixed | 4 |  |  | gnucobol | education-tutorial | subprogram | COBOL-85 |
| f630846193 | /code_sample_2.cbl | 232 | fixed | 4 |  |  | micro-focus | education-tutorial | batch | COBOL-85 |
| d1dd050ef3 | /Deathstroke 002 (New 52_Reb | 355 | fixed | 0 |  |  |  |  |  |  |
| d7c75622ef | /ORCS01.CBL | 22526 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 75bda9a294 | /ORCBM550.CBL | 1748 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 11496b1de3 | /WBC_65030_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 44e35566ba | /WBC_18768_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| aacccbf983 | /WBC_4656_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 812dbc6739 | /GABDEBIT.CBL | 368 | fixed | 3 |  |  | micro-focus | accounting-erp | subprogram | COBOL-85 |
| 016f09dce4 | /WBC_77565_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| df1a727d13 | /WBC_37135_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 75809d31f5 | /glpostingRES.cbl | 101 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| b1caf8c384 | /Z95644.CBL(COBHW02).cbl | 82 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| d4984d04c6 | /WBC_63513_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1c00f5a393 | /ASYNCPNT.cbl | 243 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 468b917c5e | /WBC_79877_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 653af18951 | /YOSHINNYUKIN.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| a306143221 | /WBC_69225_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 20c6f62f4c | /WBC_99519_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3b443de680 | /triangle-2.cbl | 32 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| dec6b06efd | /ORCGI41.CBL | 7647 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 26e0351ff9 | /U2.CBL | 1618 | fixed | 0 |  |  |  |  |  |  |
| 29a0ae7a4b | /SWP_CCYMST.CBL | 10 | fixed | 0 |  |  |  |  |  |  |
| 6f1eb63a49 | /WBC_19819_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 01577d684d | /1991 - War of the Gods.cbl | 85 | fixed | 0 |  |  |  |  |  |  |
| 26d99a93ac | /WBC_66088_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4e70921bc4 | /WBC_85942_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e2229c19e4 | /MAIN-MENU.cbl | 196 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 65ae39cfbb | /WBC_56613_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5ffa18640a | /ORCSJGNGET.CBL | 803 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 7010393ed1 | /ORCGK021.CBL | 439 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| e42aa6e474 | /WBC_29301_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c60cb91396 | /WBC_12119_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 25f4223e56 | /WBC_67399_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ca5a045b3e | /WBC_9599_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ba1ecbca57 | /ORCGR02.CBL | 3231 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| fd2afde18c | /DBBTEST.cbl | 24 | fixed | 4 |  |  | ibm-mainframe | demo-example | test | COBOL-85 |
| 811e700739 | /day8.cbl | 95 | free | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 45b004b549 | /ORCR0555.CBL | 5189 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 75981973ae | /SOKATU3700.CBL | 1192 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| aefbc13253 | /PRP057.CBL | 575 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| 5ef32a3174 | /WBC_91673_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4b3b30f7ea | /ORCR0300.CBL | 2745 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e8627cf3d5 | /IX120A.CBL | 567 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| 098c8e1bd1 | /sendhtml.cbl | 22 | fixed | 3 |  |  | unknown | utility-tooling | subprogram | COBOL-85 |
| 3e6efab93f | /WBC_3042_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 85b8e7e3ef | /ORCR0660.CBL | 2675 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| c7f24c27f4 | /WBC_30853_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 741ceae559 | /ORCGK05.CBL | 4712 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d3378d08ca | /ORCR1260.CBL | 2876 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| c14ec34646 | /WBC_44251_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4c717dc6ef | /[2012-2013] Death of the Fa | 89 | free | 0 |  |  |  |  |  |  |
| bae14308c2 | /KSL_KEI_LPWK_CHOHYO.cbl | 10 | free | 0 |  |  |  |  |  |  |
| b677a88e64 | /ORCGE02.CBL | 1313 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| d78600d254 | /ORCS01.CBL | 11909 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 392f3140b9 | /ORCXRMST3.CBL | 390 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 82f71ff2ba | /WBC_20077_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7ee6018eba | /WBC_69783_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4766286f16 | /WBC_58831_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9e0814d400 | /Usage_comp2.cbl | 20 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 38f3563f54 | /WBC_78641_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| aefa98c4d0 | /WBC_28217_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 276a696aed | /HelloWorld.cbl | 6 | unknown | 2 |  |  | unknown | demo-example | demo | COBOL-85 |
| a81ef086dd | /DataManipulation.cbl | 65 | unknown | 4 |  |  | unknown | banking-finance | demo | COBOL-85 |
| ef00e5f599 | /WBC_15128_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3b7719c5b2 | /ORCHC30.CBL | 1461 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 5ce21a6d73 | /WBC_93_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 3cdc789702 | /059 House of M (2005).cbl | 205 | fixed | 0 |  |  |  |  |  |  |
| fd1f2ef006 | /MOCKTEST.CBL | 103 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| 442bc961b4 | /WBC_98764_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| df157ed26a | /hct1bi01.cbl | 1 | free | 0 |  |  |  |  |  |  |
| 33004f57f7 | /ORCRCP400.CBL | 4016 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| c166b2ee77 | /WBC_33662_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e155cf64e6 | /TIPSEC.CBL | 253 | fixed | 4 |  |  | rm-cobol | other | subprogram | COBOL-85 |
| c68b32dc60 | /sl020.cbl | 698 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| d42c1b4862 | /ORCR0030.CBL | 3271 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ebec829214 | /ORCGI02.CBL | 944 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 9c67dcaa88 | /ORCR0501.CBL | 3115 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9b2845035d | /WBC_97320_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fe1b62ef54 | /WBC_28558_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7338bf00c4 | /WBC_50738_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 53fbd358a5 | /HCV1BI01.cbl | 153 | fixed | 4 |  | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| 6bb9f31c9a | /Condition_name_Condition.cb | 19 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| c890b82e9b | /ORCGK08.CBL | 5432 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 0d077bdeb1 | /WBC_72131_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f7032a71a3 | /fatmanvar.cbl | 8510 | fixed | 4 |  |  | acucobol | retail-commerce | online-cics | COBOL-85 |
| deebe2f43b | /WBC_35349_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f93d1b4922 | /ORCR0460.CBL | 2088 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| b19e70c5bc | /WBC_94948_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1540902697 | /WBC_98891_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 94402563e5 | /WBC_24431_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4f0365ca70 | /WBC_21188_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 84dc1c3997 | /WBC_75777_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6fbccd0b1e | /py050090.cbl | 1183 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 6a6719ec85 | /WBC_77918_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d3aac53b6b | /Program1.cbl | 8 | fixed | 3 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| df7d02538c | /WBC_31906_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a75f5407dc | /test1.cbl | 48 | fixed | 3 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| fbd57fd63f | /QualifiedNames.rdz.cbl | 40 | fixed | 2 |  |  | micro-focus | test-suite | test | COBOL-2014 |
| 29cd3f31a5 | /WBC_22281_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| dea7d8df47 | /WBC_3175_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fd4537a461 | /WBC_7852_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 91bb8f2e39 | /WBC_94528_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a3676d1e86 | /WBC_50061_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 07e0dfaa05 | /WBC_71164_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6163d4a5e9 | /Redefines.rdz.cbl | 29 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| e6c96b8e36 | /WBC_8858_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 626a53bbeb | /WBC_77274_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 88f29ab363 | /IDBSMOV0.cbl | 986 | fixed | 4 | ✓ |  | ibm-mainframe | insurance | subprogram | COBOL-85 |
| cef23d4d30 | /CADASTRO-USUARIO.cbl | 37 | fixed | 3 |  |  | gnucobol | other | batch | COBOL-85 |
| 28680cbff2 | /STMF05.CBL | 2616 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 46bfc05df5 | /ORCSSAIKEISAN.CBL | 2576 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| ea108d303e | /Program1.cbl | 117 | fixed | 4 |  |  | gnucobol | payroll-hr | batch | COBOL-85 |
| cadfa46341 | /WBC_3967_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 915c5e9de3 | /Firestorm 002 - New52_Rebir | 98 | fixed | 0 |  |  |  |  |  |  |
| 82ed8850e6 | /postData-environmentdivisio | 3 | free | 0 |  |  |  |  |  |  |
| f36441c24b | /WBC_9581_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| a5d32761a0 | /G3-BLD-VISA-ISS.cbl | 29 | fixed | 3 |  |  | gnucobol | banking-finance | batch | COBOL-85 |
| 2c0bdf0292 | /WBC_37134_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4a5f55faa4 | /WBC_10307_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5b6acff8f0 | /WBC_50207_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2837f65353 | /ALM_EXCEL_0001.cbl | 10 | free | 0 |  |  |  |  |  |  |
| 0f67c45c87 | /irsnominalUNL.cbl | 106 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| f0763f05bb | /WBC_10958_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 69e284df26 | /WBC_28401_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4f70eb1efe | /WBC_26046_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4bfaa768ae | /ORCGK03.CBL | 5293 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 289d72f11e | /WBC_20298_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7cf6b0c318 | /WBC_96671_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c138b7751b | /EL565.cbl | 342 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 4958ef60a8 | /control-break3.cbl | 101 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 9b61c40930 | /WBC_58105_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 96f84932d5 | /FIZZBUZZ.CBL | 18 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 9e94a9429e | /FCBOOK.cbl | 38 | fixed | 1 |  | ✓ | ibm-mainframe | other | online-cics | COBOL-85 |
| a5a300670e | /WBC_29898_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ee434bf329 | /CWXTSUBC.cbl | 79 | fixed | 4 |  |  | ibm-mainframe | demo-example | subprogram | COBOL-85 |
| 5a2eb927e9 | /WBC_19696_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d58debd2e8 | /WBC_24113_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 74d12e8688 | /WBC_31317_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bc658e4e14 | /WBC_18927_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| da3c2982c3 | /LEITURA.cbl | 87 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 263f5dba01 | /PEMGRC1.cbl | 108 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| f9871964bc | /WBC_49973_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 14d21fea50 | /WBC_96453_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1275cbe649 | /WBC_12377_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c8a5708d17 | /LENGTH_01.cbl | 19 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 8a49784536 | /ORCGT07.CBL | 66 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 51924033ec | /WBC_63935_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 62bd6b6e71 | /DCBIUHLD.cbl | 189 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 15c7c8f81e | /ORCSC10S201307.CBL | 5219 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 3465e06476 | /ORCXRMST1.CBL | 385 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 44067e630d | /ORCGI04.CBL | 2703 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 645d138a98 | /star-100.cbl | 22 | fixed | 3 |  |  | unknown | demo-example | demo | COBOL-85 |
| 2725f97d68 | /WBC_79060_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5a8d92f549 | /ORCGI01.CBL | 8051 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3957edd713 | /WBC_87156_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3199963a99 | /WBC_3116_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| a40a1cd93e | /hello-world.cbl | 6 | fixed | 2 |  |  | gnucobol | demo-example | demo | COBOL-85 |
| 079d81de1d | /WBC_74851_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 31b59e6573 | /deliveryRES.cbl | 109 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-2002 |
| 70af5340a6 | /ORCS02.CBL | 26915 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| f97e11161a | /6.1 黑进三卒.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| df0edf4f24 | /ORCGN21.CBL | 2131 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 5d2f5296eb | /LOCKLIST.CBL | 108 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| e709a2a7c6 | /variables.cbl | 78 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 61492f4fb8 | /ORCR0810.CBL | 1749 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 059c9f0164 | /WBC_85893_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 93f279d79d | /WBC_52992_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ab051b1aa1 | /WBC_44353_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bbc2b82c04 | /WBC_20_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 87f9aefbab | /WBC_16535_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0dc7e16022 | /PW01033C.cbl | 366 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 25757febbb | /Program1.cbl | 9 | fixed | 3 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| fa458dc965 | /DebuggingMode.cbl | 5 | unknown | 2 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| d872ef611f | /3-DHSOC.CBL | 693 | fixed | 4 |  |  | acucobol | payroll-hr | online-cics | COBOL-85 |
| b3bc3d573a | /SOKATU1700.CBL | 1276 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9a09795f32 | /numbers1.cbl | 21 | fixed | 0 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| c53d5e6320 | /WBC_1570_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 61038d4dcc | /PGMDBZ.cbl | 698 | fixed | 0 | ✓ |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| dc2cbf85cf | /ORCGQAPI01S02.CBL | 1071 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 4850ed3cc2 | /EDIT1.CBL | 36 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 2d0117ae26 | /AVG-GRADE.cbl | 95 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 8b66e86e74 | /A01014M01.CBL | 2140 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 3c8eaee63a | /SQ223A.CBL | 676 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| 4f59d0c7dd | /pwpa6100.cbl | 485 | fixed | 4 |  |  | micro-focus | other | online-cics | COBOL-85 |
| 6c94c01ac8 | /WBC_64176_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b04c4e0cce | /DC81 - New 52 Futures End.c | 277 | fixed | 0 |  |  |  |  |  |  |
| 779d0b0ff2 | /BBANK30P.CBL | 435 | fixed | 3 |  |  | micro-focus | banking-finance | online-cics | COBOL-85 |
| c0a5b50a46 | /ORCR0640.CBL | 9588 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 51546fc4a2 | /cics02.cbl | 32 | fixed | 3 |  | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| ab8eb69c3b | /WBC_61387_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6859e319c0 | /Final.cbl | 20 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 3fdc413f7c | /WBC_29348_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bac209b60e | /WBC_26032_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 23920cf757 | /DB2CBLEV.cbl | 216 | fixed | 4 | ✓ |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 5950bfb5e5 | /ORCR0410.CBL | 2436 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 7801d9c579 | /ORCSNYURECEDEN.CBL | 3946 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 0c5204e36f | /ORCR0035.CBL | 371 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9174ee9486 | /CIDCRC1.cbl | 139 | fixed | 4 |  |  | ibm-mainframe | insurance | batch | COBOL-85 |
| 3569e0efb8 | /ORCR0460.CBL | 2741 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 79175ad0b6 | /ORCGU01.CBL | 1491 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| f0b41d80ca | /WBC_74400_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a50eeb8da9 | /apply.cbl | 20 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| cc3a17e7dd | /ORCSC10S200204.CBL | 3104 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 68717db88e | /ORCGLID2.CBL | 84 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 17d9ce90ca | /assert.cbl | 85 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-85 |
| 1cd7b9d3f2 | /WBC_55198_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 84df2dd3e9 | /WBC_26503_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6943d7e39e | /colorDetection.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| 98864fdb65 | /DATABASE.cbl | 56 | fixed | 4 |  |  | unknown | manufacturing-logistics | subprogram | COBOL-85 |
| d85ea9eb58 | /ORCGD02.CBL | 4916 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 698ae6dc9c | /7-HPJ.CBL | 739 | fixed | 4 |  |  | acucobol | healthcare-medical | batch | COBOL-85 |
| 04039f85c6 | /WBC_89242_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 705d84401a | /WBC_781_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 28c7ab10af | /WBC_18837_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 74e10e3f11 | /programaTeste.cbl | 136 | fixed | 3 |  |  | unknown | payroll-hr | batch | COBOL-85 |
| eebf6cdaba | /WBC_78518_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7affba5aab | /ORCSIRYOKNS.CBL | 293 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| e9bb0af5e5 | /ORCMUP0091.CBL | 542 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| fa5f11c2c3 | /MainProgram.cbl | 22 | fixed | 4 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 54374c9873 | /VOCPROC.CBL | 13 | fixed | 2 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| fd74c23758 | /ORCR0720.CBL | 6669 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| b214e76fd9 | /WBC_50005_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1a55f8f9ed | /ORCR0690.CBL | 3399 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 12043ff8bf | /WBC_75245_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| da87db7e35 | /WBC_67415_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c700e3d3d2 | /pw03241r.cbl | 788 | fixed | 4 |  |  | micro-focus | accounting-erp | online-cics | COBOL-85 |
| 9add1bd977 | /WBC_44233_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d36ff82abe | /ORCGW24.CBL | 2076 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| bebc7e5136 | /EDI-selordini.cbl | 16189 | fixed | 4 |  |  | acucobol | retail-commerce | batch | COBOL-85 |
| 1e30e0d391 | /CL17EJ1A_Completar.cbl | 202 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 270e18dbc0 | /Help.Designer.cbl | 72 | fixed | 1 |  |  |  |  |  |  |
| 53c0096900 | /ORCGI03.CBL | 1705 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 987965ebe9 | /SOKATU1215.CBL | 1618 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 8008bbf7d4 | /ORCSCKNKCHK.CBL | 1003 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 3f7e1b0449 | /WBC_93084_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2fdfa9642d | /WBC_16764_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b2c2099452 | /WBC_6686_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| f0d537068b | /datbatch.cbl | 20 | fixed | 4 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 6ef43eb1ac | /WBC_3626_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 084ad3e825 | /table.cbl | 42 | fixed | 0 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| b86d538bb2 | /ph070064.cbl | 173 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 5835aa3065 | /testantlr361.cbl | 16 | fixed | 0 |  | ✓ |  |  |  |  |
| b676eb8d9b | /FICHA3_EX1_0807.cbl | 15 | fixed | 2 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| b5911d5992 | /Z95636.CBL(UNIFY01).cbl | 133 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| 433e5b913e | /CobDB2_Curs.cbl | 301 | fixed | 0 | ✓ |  | ibm-mainframe | retail-commerce | batch | COBOL-85 |
| 1d6cac6bf0 | /WBC_86185_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ba61796dc3 | /[Marvel] Shattered Heroes ( | 230 | free | 0 |  |  |  |  |  |  |
| 588656923a | /RE.CBL | 40 | fixed | 2 |  |  | micro-focus | demo-example | demo | COBOL-85 |
| aee8ad5369 | /ORCR0483.CBL | 2339 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 26c0fb7c78 | /WBC_77236_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6cb81672f6 | /MarcaPaginaMenu.cbl | 87 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| 72c87093d5 | /TESTPM3.CBL | 62 | fixed | 4 |  |  | gnucobol | utility-tooling | batch | COBOL-85 |
| 865b05524f | /my-grade.cbl | 94 | fixed | 4 |  |  | unknown | education-tutorial | batch | COBOL-85 |
| 41a4b569b8 | /3.2 黑左炮封车-红挺七兵.CBL | 0 | unknown | 0 |  |  |  |  |  |  |
| 94241c0263 | /WBC_61126_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 03572e8bb3 | /CDISP.CBL | 66 | fixed | 1 |  |  |  |  |  |  |
| e8cfc0a4b7 | /WBC_72786_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b41f4bb57b | /Supergirl 003 (Post Crisis  | 337 | fixed | 0 |  |  |  |  |  |  |
| d29da08c21 | /WBC_34606_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cc287b36aa | /ORCR0640.CBL | 10805 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ad49187be6 | /WBC_1442_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 1894f7db82 | /WBC_6356_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 06cf98b81f | /WBC_36570_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 87504df408 | /Data1.cbl | 16 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| 13b7943727 | /replace-letter.cbl | 35 | fixed | 3 |  |  | gnucobol | education-tutorial | subprogram | COBOL-2002 |
| eda75761af | /WBC_13638_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1a3e9ee7c2 | /sale-report.cbl | 190 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 5b9cc3e296 | /WBC_20860_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fbb476223a | /ricalimp-art.cbl | 261 | fixed | 3 |  |  | gnucobol | accounting-erp | subprogram | COBOL-85 |
| 5b81deddbe | /WBC_37846_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 74b9a2ec1e | /ORCGK08.CBL | 4660 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| f4e0169205 | /A00000M500.CBL | 2408 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e532dffdd4 | /WBC_40341_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 580decebe9 | /WBC_5572_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f4477920e8 | /Z95640.CBL(DAYCALC).cbl | 80 | fixed | 4 |  |  | ibm-mainframe | utility-tooling | batch | COBOL-85 |
| 069be72f01 | /WBC_19387_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 244e8d935b | /pw00212p.cbl | 321 | fixed | 4 |  |  | gnucobol | other | online-cics | COBOL-85 |
| 2f5b108728 | /ORCGR01.CBL | 1712 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 0bcd255a58 | /fr-date.cbl | 20 | fixed | 4 |  |  | gnucobol | demo-example | subprogram | COBOL-85 |
| 3742e11083 | /CBLDB23.CBL | 117 | fixed | 4 | ✓ |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| ece42f248b | /ORCSNYUACCT.CBL | 3269 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 18c56b03c6 | /PROGRAMB.CBL | 58 | fixed | 4 |  |  | micro-focus | demo-example | subprogram | COBOL-85 |
| 976e5eacc4 | /WBC_61155_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 8bc9dfbfb5 | /WBC_29380_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b7ecf8ae46 | /WBC_1851_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 1cb15b87ca | /SEIKYU2407.CBL | 1818 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| f381719154 | /ATV00.cbl | 201 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| 12303cfb85 | /npc.cbl | 58 | free | 0 |  |  |  |  |  |  |
| 390fdfb3a6 | /WBC_3008_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7761930d69 | /WBC_769_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| c59e558fc5 | /WBC_56721_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 22abf864e3 | /ph070022.cbl | 117 | fixed | 4 |  |  | gnucobol | retail-commerce | online-cics | COBOL-85 |
| 1ae6db26cf | /Vndrpt04.cbl | 237 | fixed | 4 |  |  | unknown | accounting-erp | batch | COBOL-85 |
| 1e8bd5034d | /WBC_41550_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a695f66f61 | /cbp105.cbl | 269 | fixed | 4 |  |  | micro-focus | banking-finance | online-cics | COBOL-85 |
| 287600b3dc | /sorx.cbl | 73 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 2f3ec727e2 | /ORCR0030.CBL | 8380 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 0fde0041e5 | /listen15.cbl | 170 | fixed | 4 |  |  | gnucobol | utility-tooling | test | COBOL-85 |
| cebd364ec5 | /WBC_74704_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7bbbaa5635 | /EDI-impord.cbl | 971 | fixed | 4 |  |  | acucobol | retail-commerce | batch | COBOL-85 |
| 268d517ade | /WBC_29597_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 346bb59b8a | /WBC_32987_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cf730d5c41 | /ORCSODRS01.CBL | 203 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| f4365698e2 | /WBC_54500_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 14fb9f09a7 | /WBC_98127_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e85d850f39 | /WBC_2721_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| e69fc04c12 | /WBC_32091_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e0cd30d076 | /sl930.cbl | 747 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 3517ea1138 | /WBC_84027_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b8f8ac90bd | /RADTP009.cbl | 627 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| ba0a462beb | /ORCR0420.CBL | 5014 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| fab0e0af13 | /SEIKYU47BYOMEI1.CBL | 667 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 44a44605a8 | /WBC_81513_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5bb5d596a0 | /indexer.cbl | 106 | unknown | 0 |  |  |  |  |  |  |
| b8508e6362 | /ORCR0425.CBL | 388 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 5550574703 | /WBC_50946_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f1f8a5ea9f | /Form1.cbl | 9 | fixed | 1 |  |  |  |  |  |  |
| 48a4ab9a81 | /FDVND02.CBL | 12 | fixed | 0 |  |  |  |  |  |  |
| 61b2e78fa4 | /WBC_28022_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 662848efe6 | /ORCBM501.CBL | 1427 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 16fd46cd67 | /WBC_6306_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 8f1dc50614 | /ORCHC02QV02.CBL | 4163 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| f25386791a | /MODULO-ALT-CAD.cbl | 81 | fixed | 4 |  |  | gnucobol | other | subprogram | COBOL-85 |
| 90de52ce84 | /WBC_6330_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| becbf27276 | /WBC_24201_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0a7a13afb7 | /WBC_92615_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d774410efa | /WBC_25092_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ae30103090 | /WBC_912_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 0d5a100f71 | /ORCR0640.CBL | 15122 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| ef3d922c71 | /WBC_23399_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1a646a31bc | /WBC_63423_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 06760f5842 | /ORCHCN03V02.CBL | 1258 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 8ae6c9479c | /ORCR0840.CBL | 7666 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9d37ba7ab5 | /ORCDTCHK010.CBL | 506 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 3eb47fc5a3 | /WBC_99028_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b16a721c9a | /WBC_29366_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 695e30b528 | /WBC_23250_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d45f6bfd1f | /ORCSC60200404.CBL | 2591 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 0e98e3e192 | /glistini.cbl | 3901 | fixed | 4 |  |  | acucobol | retail-commerce | online-cics | COBOL-85 |
| 3d0d52ffb8 | /ORCGSID1.CBL | 85 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 91143a2773 | /ORCGE03.CBL | 541 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| fe5f583b4c | /WBC_28415_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 603ad1b1b7 | /WBC_45415_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c091679452 | /WBC_43080_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 82555d0900 | /WBC_38931_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 690e55d412 | /ORCGW16.CBL | 679 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| d83239b89f | /helloworld.cbl | 7 | fixed | 2 |  |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| 65193d4403 | /WBC_64223_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6b27206320 | /ORCMUP0092.CBL | 546 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| eaf2125fe3 | /WBC_73414_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 103f935295 | /WBC_14159_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 01e862c2f4 | /EX01.CBL | 141 | fixed | 4 |  |  | other-vendor | education-tutorial | batch | COBOL-85 |
| 324bd7ab30 | /WBC_6427_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| bfec214106 | /ORCSPRVDBDEL.CBL | 209 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 1bf35cfbf4 | /WBC_30685_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0394fb118e | /WBC_53470_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d223a9bb4a | /ORCGW35.CBL | 942 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 7505d7767a | /WBC_98822_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 57d4149458 | /WBC_98771_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7bc371c175 | /NUMBERST.CBL | 1123 | fixed | 4 |  |  | gnucobol | test-suite | test | COBOL-85 |
| d021202f8f | /PROG05.cbl | 173 | fixed | 4 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| eb5ae030a0 | /Program3.cbl | 106 | fixed | 4 |  |  | unknown | retail-commerce | batch | COBOL-85 |
| d339da4658 | /WBC_84479_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7cb5d26003 | /ORCGH01.CBL | 2549 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 1918b10268 | /WBC_6671_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| d9c17735c0 | /WBC_80506_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 14693508e9 | /U2.CBL | 981 | fixed | 0 |  |  |  |  |  |  |
| 52c30a3fd7 | /ORCGI47.CBL | 2265 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| e22f63a7a0 | /WBC_1892_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| ab53ea9f69 | /load_program.cbl | 522 | fixed | 4 |  |  | gnucobol | utility-tooling | subprogram | COBOL-2014 |
| 33b08071a9 | /WBC_62841_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| f20b06ff26 | /D048PHJ.cbl | 0 | unknown | 0 |  |  |  |  |  |  |
| d3d041e289 | /CGPRG02M.cbl | 63 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 613b05979b | /TP01.cbl | 77 | fixed | 4 |  |  | gnucobol | payroll-hr | demo | COBOL-85 |
| 5a8d7f3494 | /ORCGP97.CBL | 1353 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 116a0759d8 | /WBC_65364_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bec1e69715 | /WBC_12789_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9ad7040c7c | /slinvoiceRES.cbl | 101 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 23d384b77c | /trabalho.cbl | 1012 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 9ee3152d0f | /WBC_57593_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a0ca4ee65a | /WBC_67521_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ce5fc876ae | /archNovedades.cbl | 112 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 8e95c09dba | /ORCGP02A.CBL | 490 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| c26d4268fa | /WBC_57636_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 348b7ca596 | /log4mas.cbl | 346 | fixed | 3 |  |  | gnucobol | retail-commerce | batch | COBOL-85 |
| 9715533fdc | /V12C20J.CBL | 522 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| e366d91999 | /ORCR0030.CBL | 23572 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 1f9d30cc6c | /WBC_27745_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a9fa17c77b | /ORCL0012P.CBL | 125 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| cdaf0e14d9 | /[Marvel] 2004-2012 Part 15. | 89 | free | 0 |  |  |  |  |  |  |
| ebce588b46 | /WBC_68795_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2cb0a7facd | /WBC_60576_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| df85e1997b | /WBC_84948_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a791a695c6 | /WBC_6107_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c4ac474a64 | /WBC_84641_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1b39117859 | /WBC_16117_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 29c7e2f9ed | /Justice League 002 (Post Cr | 713 | fixed | 0 |  |  |  |  |  |  |
| 11e01754a7 | /1-DIM-TABLE(2).CBL | 35 | fixed | 3 |  |  | unknown | education-tutorial | demo | COBOL-85 |
| dae981e561 | /ORCGS02.CBL | 2910 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| b5108248f8 | /WBC_91693_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| e887f7fbe2 | /declare-in-override.ppc32.c | 16 | free | 0 |  |  |  |  |  |  |
| 668063c1e5 | /WBC_88787_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 05453a1850 | /CBL0012.cbl | 138 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 1f75570a09 | /ORCL0031.CBL | 3446 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 27cb5e8d6d | /WBC_3240_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2c7fbb61f2 | /WBC_19476_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 107a9b6ee1 | /sl070.cbl | 625 | free | 4 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| a8eb1441ff | /programaTeste.cbl | 136 | fixed | 3 |  |  | unknown | payroll-hr | batch | COBOL-85 |
| a2b36ad7fe | /WBC_3294_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fb7780eddf | /ORCGK08.CBL | 5231 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 74a1e33e85 | /ORCGWID1.CBL | 107 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 320138ff6e | /CONBRE3.cbl | 155 | fixed | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 105085aa93 | /ORCR0720.CBL | 7355 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 014274ddc4 | /WBC_38687_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 25458d80f1 | /ORCGT01.CBL | 2205 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 22bf92652e | /WBC_27785_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 33d9b53fa1 | /ORCGI04.CBL | 5113 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| b4eba25475 | /ORCR0030.CBL | 23946 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 0e41092f2d | /Listing5-1.cbl | 36 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 1933db4e42 | /cobvs3.cbl | 60 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | demo | COBOL-85 |
| 5c523f82e9 | /WBC_1531_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 86c9360bbf | /ORCXRMST2.CBL | 698 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 85aacd0a7b | /WBC_65757_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0765059e44 | /CWXTCOB.cbl | 508 | fixed | 4 |  |  | ibm-mainframe | demo-example | batch | COBOL-85 |
| cec3f00dd8 | /IF1324.2.cbl | 940 | fixed | 2 |  |  | ibm-mainframe | test-suite | test | COBOL-85 |
| e6fec5d818 | /star-10perform-until-3.cbl | 23 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 2f4f25d962 | /ORCVTPTHKNINF.CBL | 1866 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d2a51c48a5 | /db2pgm.cbl | 16 | fixed | 4 | ✓ |  | ibm-mainframe | demo-example | demo | COBOL-85 |
| e3da475cec | /WBC_12649_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9a101945ab | /WBC_74779_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b1571db8d5 | /WBC_36429_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 73fb0e0a35 | /TABLE.cbl | 43 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| df9532c369 | /WBC_99819_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c812707886 | /server.cbl | 2471 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 2ecb7c845c | /RDB457.CBL | 182 | fixed | 4 |  |  | ibm-mainframe | banking-finance | batch | COBOL-85 |
| d7bbb69a09 | /WBC_19067_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2b0d9e1c6b | /ORCSC10S200604.CBL | 4104 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 18124ae6f6 | /variants.cbl | 19 | unknown | 0 |  |  |  |  |  |  |
| e46833d601 | /prog.cbl | 52 | fixed | 3 | ✓ |  | gnucobol | demo-example | demo | COBOL-85 |
| 356f96dca2 | /ORCR0840.CBL | 10945 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d418ccc03e | /WBC_76052_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0b338138b3 | /intrinsics.cbl | 153 | fixed | 0 |  |  | gnucobol | education-tutorial | test | COBOL-85 |
| 529c264b2b | /5E1.cbl | 62 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 58eeae7dd1 | /WBC_15790_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5781f13c1c | /WBC_76066_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 547ff928a0 | /PW04267R.cbl | 995 | fixed | 4 |  |  | gnucobol | accounting-erp | online-cics | COBOL-85 |
| 5c9ff94182 | /WBC_67305_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 26eebe6a4f | /EM07.CBL | 77 | fixed | 4 |  |  | other-vendor | education-tutorial | batch | COBOL-85 |
| adebc96133 | /WBC_44924_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 141d9c78af | /ORCGM01.CBL | 779 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 70c8f2ecfa | /WBC_54677_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b8d9002295 | /WBC_7218_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 00e475ea44 | /BANK2.cbl | 144 | fixed | 4 |  |  | gnucobol | banking-finance | subprogram | COBOL-85 |
| 331a9516c8 | /WBC_15939_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d66944150c | /COACTUPC.cbl | 3368 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 0d331fa539 | /ORCR0030.CBL | 4993 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| be2cd1efcc | /WBC_50295_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 1bd96c0980 | /WBC_8675_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| aa3d01ca2f | /WBC_10885_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b1437f17af | /KEI_LPWK_EDA_KIHON.CBL | 72 | fixed | 0 |  |  |  |  |  |  |
| cafe217e29 | /[Marvel] Avengers Disassemb | 110 | free | 0 |  |  |  |  |  |  |
| 7ed5156e4a | /ORCHC30.CBL | 1078 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| b42d0c45cc | /WBC_6257_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 69cb114feb | /ORCR0487.CBL | 2327 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| eafe7d1755 | /STBCRD068.CBL | 456 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| c7dcefc1d9 | /ORCGDSUB02.CBL | 514 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 489485c66a | /WBC_87597_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 05fe4e7142 | /WBC_14803_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4306f51074 | /WBC_35676_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 91c8c5591c | /WBC_22301_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fab0e16851 | /WBC_20146_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 81fea1fdfb | /A00000D123.CBL | 3079 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| b41c34f3df | /ORCR0600.CBL | 2005 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| e05ab9dd3c | /WBC_39545_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fb0ae960d7 | /IC114A.CBL | 426 | fixed | 4 |  |  | unknown | test-suite | test | COBOL-85 |
| c7dd5c8ba9 | /WBC_42880_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| fa5fdc1366 | /WBC_63680_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 7a10ea4f0b | /WBC_38385_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 76bb153357 | /WBC_57882_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4ca7c2ad3c | /WBC_10938_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 261accbd54 | /WBC_59625_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bc17869723 | /WBC_94385_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0d20466d70 | /ConditionNames.cbl | 27 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 8e7a44ca9a | /WBC_77841_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c025b087d6 | /WBC_11663_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 24dab03fe7 | /ORAPI044R3V3.CBL | 3221 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 35993f6b50 | /sqle819b.cbl | 257 | fixed | 0 |  |  |  |  |  |  |
| 967eb01ea7 | /SAM2.cbl | 119 | fixed | 4 |  |  | ibm-mainframe | retail-commerce | subprogram | COBOL-85 |
| de0cf7ad4d | /WBC_69976_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 14c0d9ff6f | /WBC_96424_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c30635af67 | /ALTERNAS.CBL | 60 | fixed | 4 |  |  | other-vendor | education-tutorial | demo | COBOL-85 |
| b947bc88be | /SOKATU1010.CBL | 1546 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9c03197cec | /oualidprecision.cbl | 19 | fixed | 4 |  |  | unknown | demo-example | demo | COBOL-85 |
| 44ec45b3ee | /irsdfltLD.cbl | 266 | free | 4 | ✓ |  | gnucobol | accounting-erp | batch | COBOL-85 |
| 374abff390 | /trader.cbl | 80 | fixed | 4 |  |  | gnucobol | education-tutorial | batch | COBOL-85 |
| 92d634a614 | /ACCTPTNR.cbl | 58 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 2da598687b | /WBC_31438_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 74cba23781 | /WBC_55277_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| da1a1e3af4 | /WBC_64205_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 134f315e36 | /ORCGW96.CBL | 1154 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| a141eaa14b | /WBC_80274_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a4948ee34a | /KOK_HOUMON.CBL | 24 | fixed | 0 |  |  |  |  |  |  |
| d937b217a9 | /WBC_15627_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| d32f36283b | /G3-VFX-MAIN.cbl | 26 | fixed | 4 |  |  | gnucobol | demo-example | batch | COBOL-85 |
| 461f877257 | /ORCGN11ID1.CBL | 74 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| aea1d35b9f | /member_report.cbl | 84 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| d30945188d | /WBC_47750_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bbb9c11634 | /irs020.cbl | 638 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-85 |
| b8dda69ffa | /SEIKYU0609.CBL | 2049 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| da7fecbdf4 | /CBLEXIT.cbl | 11 | fixed | 4 |  |  | other-vendor | utility-tooling | subprogram | COBOL-85 |
| aa9dc8cf57 | /WBC_14609_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 390316e382 | /WBC_3935_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| cf628d37db | /sl970.cbl | 744 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-2014 |
| 67aa16ead0 | /WBC_75167_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| aaf69fc369 | /String.cbl | 12 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 5b95f4a50c | /SALE_REPORT.cbl | 61 | fixed | 4 |  |  | unknown | retail-commerce | batch | COBOL-85 |
