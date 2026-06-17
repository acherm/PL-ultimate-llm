# COBOL-in-SWH exploratory study — summary

_Generated 2026-06-17T18:33:25Z · 100 samples (100 text, 0 non-text), 46 LLM-judged._

## Lines of code (code lines, excl. blank/comment)

- min **1** · median **2.0** · mean **720.6** · max **19807** · total **72058**

## Source format (mechanical heuristic)

- free: 53
- fixed: 47

## Feature prevalence (mechanical, over text files)

- EXEC SQL: 5 (5.0%)
- EXEC CICS: 6 (6.0%)
- COMP-3: 9 (9.0%)
- COPY: 32 (32.0%)
- CALL: 31 (31.0%)

## Is COBOL? (judge)

  - true: 46 (100.0%)

## Dialect family (judge)

  - gnucobol: 25 (54.3%)
  - ibm-mainframe: 12 (26.1%)
  - micro-focus: 7 (15.2%)
  - fujitsu-nec: 1 (2.2%)
  - rm-cobol: 1 (2.2%)

## COBOL standard (judge)

  - COBOL-85: 44 (95.7%)
  - COBOL-2002: 2 (4.3%)

## Source format (judge)

  - fixed: 42 (91.3%)
  - free: 4 (8.7%)

## Domain (judge)

  - healthcare-medical: 20 (43.5%)
  - education-tutorial: 9 (19.6%)
  - banking-finance: 6 (13.0%)
  - accounting-erp: 4 (8.7%)
  - demo-example: 3 (6.5%)
  - payroll-hr: 1 (2.2%)
  - unknown: 1 (2.2%)
  - utility-tooling: 1 (2.2%)
  - other: 1 (2.2%)

## Program type (judge)

  - batch: 24 (52.2%)
  - online-cics: 8 (17.4%)
  - subprogram: 8 (17.4%)
  - demo: 4 (8.7%)
  - test: 2 (4.3%)

## Maturity (judge)

  - production-like: 38 (82.6%)
  - student-exercise: 4 (8.7%)
  - snippet: 3 (6.5%)
  - toy-or-hello-world: 1 (2.2%)

_Judge tokens: 273818 prompt + 32088 completion._

## Samples

| sha1_git | file | LOC | fmt | divs | SQL | CICS | family | domain | type | std |
|---|---|---:|---|---:|:-:|:-:|---|---|---|---|
| 35e449a2a7 | /WBC_54739_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0bffa88ce5 | /WBC_71608_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 85714d2d71 | /ORCBM043.CBL | 1106 | fixed | 4 |  |  | fujitsu-nec | healthcare-medical | batch | COBOL-85 |
| 76c72e39ca | /WBC_4068_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 6c2bc9b43a | /WBC_1591_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 43bdd25397 | /WBC_33751_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 31a73c3a55 | /ORCGM97.CBL | 640 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 2a2107eab7 | /WBC_28515_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cc77a61808 | /ORCGU02.CBL | 6073 | fixed | 4 |  |  | gnucobol | healthcare-medical | online-cics | COBOL-85 |
| 0f4049eb24 | /ORCL0012.CBL | 135 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 0e519037c9 | /WBC_14451_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2d5ccc032e | /WBC_20087_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 69fc2ccc95 | /Account.cbl | 26 | fixed | 1 |  |  |  |  |  |  |
| 70cf5440af | /CommentLine.cbl | 3 | fixed | 1 |  |  |  |  |  |  |
| f4e06d99fb | /WBC_42197_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0cc014ad91 | /WBC_84497_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 605e3b6851 | /WBC_62013_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cb475a815a | /WBC_26345_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6ad1015633 | /SOKATU0200.CBL | 1409 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| d9ab86147d | /ORCSNYUACCT.CBL | 2041 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 86feed803b | /WBC_79061_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 031a757631 | /ORCBM029.CBL | 1720 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4d68f91eb5 | /WBC_32110_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cccb8ef697 | /V12C11Z.CBL | 398 | fixed | 4 | ✓ | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| a507e6e7f7 | /5-J.CBL | 450 | fixed | 4 |  |  | micro-focus | payroll-hr | batch | COBOL-85 |
| 86d5c0cd6f | /otm3RES.cbl | 112 | free | 4 |  |  | gnucobol | accounting-erp | batch | COBOL-2002 |
| 4b64397402 | /WBC_25528_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 68551caa54 | /BKPXXC2.cbl | 216 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| a336598284 | /CWXTDATE.cbl | 99 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | subprogram | COBOL-85 |
| 3181a1d5c6 | /WBC_25742_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2cef6059ad | /ifElse.cbl | 20 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| b827b15086 | /SEIKYU4317.CBL | 1375 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 2edb0f5f5f | /HCIPDB01.cbl | 94 | fixed | 4 | ✓ | ✓ | ibm-mainframe | healthcare-medical | online-cics | COBOL-85 |
| adf744111a | /WBC_29382_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| a6cfc958b1 | /triangle-4.cbl | 36 | fixed | 3 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| 80498df742 | /WBC_87697_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 14dd668b01 | /ORCSBTUSENTEI.CBL | 416 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| de9a7a2893 | /WBC_15614_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 3c7f51604e | /CBL0001.cbl | 61 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| b777f6c11f | /POSTCHQ.CBL | 2371 | fixed | 4 |  |  | micro-focus | banking-finance | batch | COBOL-85 |
| 262a5c55d9 | /OBSQ3A.CBL | 603 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | batch | COBOL-85 |
| 8e3100c2af | /OINV12.CBL | 2473 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| af430073e3 | /WBC_22998_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 5d2cf0adb9 | /WBC_8840_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 2197db137b | /WBC_35586_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 15f8b84608 | /WBC_35545_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6e829311a8 | /WBC_97027_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 8c644b6bae | /rrmbs196.cbl | 25 | fixed | 4 |  |  | ibm-mainframe | unknown | batch | COBOL-85 |
| 26a23e8cfe | /WBC_8843_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 70e1037a5d | /ORCRDPC10.CBL | 4715 | fixed | 4 |  |  | micro-focus | healthcare-medical | batch | COBOL-85 |
| 30f2ac63d7 | /WBC_4039_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b842652675 | /WBC_40681_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 86e0dec29b | /WBC_80209_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| dbb86a1fb9 | /WBC_40870_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b0d75804a7 | /WBC_44850_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4eebf56f8d | /Program1.cbl | 12 | fixed | 4 |  |  | gnucobol | education-tutorial | demo | COBOL-85 |
| b370894ea6 | /WBC_67236_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| ac36fd049f | /WBC_55729_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 65771b0c89 | /CW08DEMO.cbl | 806 | fixed | 4 | ✓ | ✓ | ibm-mainframe | demo-example | online-cics | COBOL-85 |
| 817dfe31b9 | /WBC_77652_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 228a4ce379 | /crp9102C.cbl | 1094 | fixed | 4 |  |  | micro-focus | banking-finance | batch | COBOL-85 |
| 531ad2c0ad | /WBC_84896_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 76beeaf5d9 | /ORCR0430.CBL | 3848 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4f465c53d7 | /acas023.cbl | 301 | free | 4 | ✓ |  | gnucobol | accounting-erp | subprogram | COBOL-85 |
| dfff1438a8 | /WBC_31500_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| b7e85e3ce0 | /SQ141A.CBL | 482 | fixed | 4 |  |  | gnucobol | education-tutorial | test | COBOL-85 |
| 82e8684b69 | /samos2.cbl | 65 | fixed | 4 |  |  | ibm-mainframe | education-tutorial | subprogram | COBOL-85 |
| 6a6cbe0dd6 | /ORCR0030.CBL | 19807 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 9d44cabb7f | /ORCBM028.CBL | 1130 | fixed | 4 |  |  | gnucobol | healthcare-medical | subprogram | COBOL-85 |
| 1afde1edf2 | /CRP023.CBL | 542 | fixed | 4 |  |  | micro-focus | accounting-erp | batch | COBOL-85 |
| 6f0590b7c7 | /WBC_12617_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 0f6ca3cdf5 | /WBC_10451_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 9906138d5b | /WBC_22173_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| c26acff321 | /ORCSC70201004.CBL | 2696 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 81de52c34a | /WBC_94171_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 200127d051 | /WBC_81516_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6627cebd93 | /WBC_5191_FOO.CBL | 2 | free | 0 |  |  |  |  |  |  |
| 98a507dc37 | /WBC_25882_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 66fd7d3479 | /acpx121.CBL | 9 | fixed | 0 |  |  |  |  |  |  |
| f1d5c97209 | /WBC_30499_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| bfb5f8d33c | /ixverify.cbl | 56 | fixed | 3 |  |  | rm-cobol | utility-tooling | batch | COBOL-85 |
| de548ef773 | /WBC_29360_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 455a8775e8 | /SEIKYU2307.CBL | 1428 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 807655eb48 | /ORCR0620.CBL | 3577 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 43c94d413d | /ORCBT010.CBL | 2491 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 7793055c5e | /ACESSO.cbl | 344 | fixed | 4 |  |  | gnucobol | other | batch | COBOL-85 |
| 7f6d3496d5 | /WBC_57918_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| cf96fb3c14 | /TSQL034A.cbl | 17 | fixed | 3 |  |  | ibm-mainframe | education-tutorial | test | COBOL-85 |
| c1924b09f4 | /WBC_82899_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| af6e210fc1 | /WBC_52920_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 6a4c4747b5 | /SOKATU1150.CBL | 1380 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 4325cb2eeb | /FunDeclareWithExec-PublicPr | 109 | fixed | 3 | ✓ |  | ibm-mainframe | demo-example | subprogram | COBOL-85 |
| f7034b4016 | /WBC_7064_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| eef8c1cc24 | /ORCGW02.CBL | 3157 | fixed | 4 |  |  | gnucobol | healthcare-medical | batch | COBOL-85 |
| 2c0519f4ac | /WBC_30424_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 169ff23ebb | /PyramidOfAhraxis.cbl | 653 | fixed | 3 |  |  | gnucobol | demo-example | demo | COBOL-2002 |
| 351485a83c | /WBC_70579_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
| 4a274f5a59 | /BNK1DCS.cbl | 1316 | fixed | 4 |  | ✓ | ibm-mainframe | banking-finance | online-cics | COBOL-85 |
| 4d912bcf91 | /DBANK01P.CBL | 66 | fixed | 4 |  | ✓ | micro-focus | banking-finance | online-cics | COBOL-85 |
| cc97500b8f | /WBC_95785_FOO.CBL | 1 | free | 0 |  |  |  |  |  |  |
