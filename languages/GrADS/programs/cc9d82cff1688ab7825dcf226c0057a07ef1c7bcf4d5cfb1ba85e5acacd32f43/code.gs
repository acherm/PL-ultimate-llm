* GrADS Script: Plot multi-level wind vectors and temperature
* Demonstrates loops, user-defined functions, and GrADS display commands

function plotlevel(lev)
  'set lev ' lev
  'set gxout shaded'
  'c'
  'd t'
  'set gxout vector'
  'd u;v'
  'draw title Temperature and Wind at ' lev ' hPa'
return

function main(args)
  'reinit'
  'open data.ctl'
  'set lon -180 180'
  'set lat -90 90'
  'set t 1'

  levels = '850 500 250'
  i = 1
  while (i <= 3)
    lv = subwrd(levels, i)
    rc = plotlevel(lv)
    'printim winds_' lv '.png x800 y600'
    say 'Plotted level ' lv ' hPa'
    i = i + 1
  endwhile

  say 'Done plotting all levels.'
return
