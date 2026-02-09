#!/usr/local/bin/spar

procedure fibonacci is
  n : constant positive := 20;
  a : natural := 0;
  b : natural := 1;
  temp : natural;
begin
  for i in 1..n loop
    put_line( a );
    temp := a + b;
    a := b;
    b := temp;
  end loop;
end fibonacci;
