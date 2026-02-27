;redcode
;name Dwarf
;author A. K. Dewdney
;strategy Drops data bombs every four cells

ADD #4,   bomb
MOV bomb, @bomb
JMP -2,   0
bomb DAT #0, #0
