program sieve(output);

const
  limit = 1000;

type
  channel = *(integer);

var
  source: channel;

procedure generate(var out: channel);
var
  i: integer;
begin
  for i := 2 to limit do
    send(out, i);
  send(out, 0)
end;

procedure filter(prime: integer; var inp, out: channel);
var
  n: integer;
begin
  receive(inp, n);
  while n <> 0 do
  begin
    if n mod prime <> 0 then
      send(out, n);
    receive(inp, n)
  end;
  send(out, 0)
end;

procedure sink(var inp: channel);
var
  prime: integer;
  next: channel;
begin
  receive(inp, prime);
  if prime <> 0 then
  begin
    writeln(prime);
    open(next);
    parallel
      filter(prime, inp, next) |
      sink(next)
    end
  end
end;

begin
  open(source);
  parallel
    generate(source) |
    sink(source)
  end
end.
