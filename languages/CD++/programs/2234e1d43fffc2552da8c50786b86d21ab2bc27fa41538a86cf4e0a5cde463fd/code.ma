[top]
components : traffic

[traffic]
type : cell
dim : (5,5)
delay : transport
defaultDelayTime : 1000
border : wrapped
neighbors : traffic(-1,0)
neighbors : traffic(0,-1) traffic(0,0) traffic(0,1)
neighbors : traffic(1,0) traffic(1,1)
initialvalue : 0
initialrowvalue : 0 01011
initialrowvalue : 1 00210
initialrowvalue : 2 20102
initialrowvalue : 3 00200
initialrowvalue : 4 00120
localtransition : traffic-rule

# NOTA: Usamos 1 para representar autos que van hacia la derecha, y 2 para
# representar autos que van hacia arriba. 0 significa que no hay autos
# en esa casilla.

[traffic-rule]
rule : 2 1000 { (0,0) = 2 and (-1,0) != 0 }
rule : 0 1000 { (0,0) = 2 and (-1,0) = 0 }
rule : 2 1000 { (0,0) = 0 and (1,0) = 2 }
rule : 1 1000 { (0,0) = 1 and (0,1) = 0 and (1,1) = 2 }
rule : 1 1000 { (0,0) = 1 and (0,1) != 0 }
rule : 0 1000 { (0,0) = 1 and (0,1) = 0 }
rule : 1 1000 { (0,0) = 0 and (0,-1) = 1 }
rule : 0 1000 { (0,0) = 0 }
