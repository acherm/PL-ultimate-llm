# Lines beginning with # are treated as comments
#
# This gnuplot script demonstrates the use of the "world1"
# map data file.  The data is in a funny format, so we have to
# tell gnuplot how to read it.
#
set palette defined ( 0 "white", 3 "green", 6 "yellow", 9 "brown" )
set pm3d map
splot "world1_110m" using ($1==9999?1:$1):($2==9999?1:$2):3 with pm3d