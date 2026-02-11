entity resistor is
  generic (r : real := 1.0);
  port (terminal p, m : electrical);
end entity resistor;

architecture ideal of resistor is
  quantity v across i through p to m;
begin
  i == v / r;
end architecture ideal;
