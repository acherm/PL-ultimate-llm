-- sparks
-- by zep
--
-- a simple particle system

-- global table to store particles
parts={}

-- make a particle
function make_part(x,y,c)
 local p = {
  x=x, y=y,
  c=c,
  dx=rnd(2)-1,
  dy=rnd(2)-1,
  life=10+rnd(10)
 }
 add(parts,p)
end

function _update()
 -- make new particles at mouse
 if (btn(0)) then
  for i=1,3 do
   make_part(stat(32),stat(33),7+rnd(2))
  end
 end
 
 -- update particles
 for p in all(parts) do
  p.x+=p.dx
  p.y+=p.dy
  p.life-=1
  if (p.life < 0) del(parts,p)
 end
end

function _draw()
 cls()
 for p in all(parts) do
  pset(p.x,p.y,p.c)
 end
end