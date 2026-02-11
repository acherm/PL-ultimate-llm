/* SnapFront.rexx - Snap the front window */

options results

address command 'wait 5'

address 'SCREENSNAP'
'SNAP'
if rc <> 0 then do
   say result
   exit 20
end

parse var result . 'CLIPUNIT=' unit .
if unit = '' then do
   say 'Could not find clipunit'
   exit 20
end

address 'MULTIVIEW'
'OPEN' 'CLIP:'unit
if rc <> 0 then do
   say result
   exit 20
end