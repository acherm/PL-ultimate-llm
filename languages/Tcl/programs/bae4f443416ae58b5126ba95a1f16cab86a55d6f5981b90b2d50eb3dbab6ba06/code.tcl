#!/usr/bin/env tclsh
package require Tk

wm title . Calculator

set font {Arial 14}
set value 0
set op ""
set newnum 1

grid [entry .e -textvariable value -justify right \
    -font $font] -row 0 -column 0 -columnspan 4 -sticky nsew

foreach row {1 2 3 4} {
    grid rowconfigure . $row -weight 1
}
foreach col {0 1 2 3} {
    grid columnconfigure . $col -weight 1
}

proc click {s} {
    global value newnum op
    if {$s in {0 1 2 3 4 5 6 7 8 9 .}} {
        if {$newnum} {
            set value $s
            set newnum 0
        } else {
            append value $s
        }
    } elseif {$s in {+ - * /}} {
        set op $s
        set newnum 1
    } elseif {$s eq "="} {
        set value [expr $value]
        set newnum 1
    } elseif {$s eq "C"} {
        set value 0
        set newnum 1
    }
}

foreach {row col txt} {
    1 0 7  1 1 8  1 2 9  1 3 /
    2 0 4  2 1 5  2 2 6  2 3 *
    3 0 1  3 1 2  3 2 3  3 3 -
    4 0 0  4 1 .  4 2 =  4 3 +
} {
    grid [button .$row$col -text $txt -command [list click $txt] \
        -font $font] -row $row -column $col -sticky nsew
}

grid [button .c -text C -command {click C} -font $font] \
    -row 5 -column 0 -columnspan 4 -sticky nsew