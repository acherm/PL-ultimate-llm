[top]
components : life@Cell

[life]
type : cell
dim : (20,20)
delay : transport
defaultDelayTime : 100
border : nowrapped
neighbors : life(-1,-1) life(-1,0) life(-1,1)
             life(0,-1) life(0,0) life(0,1)
             life(1,-1) life(1,0) life(1,1)
localTransition : lifeRule
initialvalue : 0

[lifeRule]
% Conway's Game of Life rules
% A live cell with 2 or 3 live neighbors survives
rule : { alive(0,0) and (neighborCount(1)=2 or neighborCount(1)=3) } 1 100
% A dead cell with exactly 3 live neighbors becomes alive
rule : { !alive(0,0) and neighborCount(1)=3 } 1 100
% All other cells die or remain dead
rule : { t } 0 100
