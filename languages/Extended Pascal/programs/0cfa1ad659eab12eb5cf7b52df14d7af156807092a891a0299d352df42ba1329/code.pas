program StringDemo;

var
  name: string(50);
  greeting: string(100);
  i: integer;

begin
  writeln('Enter your name:');
  readln(name);
  
  greeting := 'Hello, ' + name + '!';
  writeln(greeting);
  
  writeln('Your name has ', length(name), ' characters.');
  
  writeln('Characters in reverse:');
  for i := length(name) downto 1 do
    write(name[i]);
  writeln;
end.
