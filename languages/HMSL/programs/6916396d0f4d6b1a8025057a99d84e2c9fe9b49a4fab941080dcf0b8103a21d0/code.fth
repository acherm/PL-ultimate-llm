\ HMSL Demo - Play a C Major Scale
\ Hierarchical Music Specification Language (pForth-based)

variable current.pitch
variable current.dur

: ms.to.ticks  ( ms -- ticks )
    120 * 1000 /
;

: play.note  ( pitch dur.ms -- )
    ms.to.ticks >r
    dup pitch.on
    r@ task.sleep
    pitch.off
    r> drop
;

: play.scale  ( -- )
    60 200 play.note
    62 200 play.note
    64 200 play.note
    65 200 play.note
    67 200 play.note
    69 200 play.note
    71 200 play.note
    72 400 play.note
;

: demo  ( -- )
    cr ." Playing C major scale..." cr
    play.scale
    cr ." Done." cr
;

demo
