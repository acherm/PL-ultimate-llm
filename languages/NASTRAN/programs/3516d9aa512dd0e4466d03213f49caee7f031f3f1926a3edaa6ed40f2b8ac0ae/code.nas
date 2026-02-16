$ NASTRAN Example - Simple Cantilever Beam
$ Static Analysis
SOL 101
CEND
TITLE = CANTILEVER BEAM STATIC ANALYSIS
ECHO = NONE
DISPLACEMENT(PLOT) = ALL
STRESS(PLOT) = ALL
SPC = 1
LOAD = 100
BEGIN BULK
$ Grid Points
GRID    1               0.0     0.0     0.0
GRID    2               10.0    0.0     0.0
GRID    3               20.0    0.0     0.0
$ Beam Elements
CBAR    1       1       1       2       0.0     1.0     0.0
CBAR    2       1       2       3       0.0     1.0     0.0
$ Property
PBAR    1       1       1.0     1.0     1.0     1.0
$ Material
MAT1    1       3.0E7           0.3
$ Boundary Conditions
SPC1    1       123456  1
$ Applied Load
FORCE   100     3               1000.0  0.0     -1.0    0.0
ENDDATA