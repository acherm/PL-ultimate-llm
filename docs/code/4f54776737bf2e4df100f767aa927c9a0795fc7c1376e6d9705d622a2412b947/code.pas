type buffer = monitor
  var contents: array [0..9] of integer;
      count, in_ptr, out_ptr: integer;
  
  procedure entry deposit(item: integer);
  begin
    if count = 10 then delay;
    contents[in_ptr] := item;
    in_ptr := (in_ptr + 1) mod 10;
    count := count + 1;
    continue
  end;
  
  procedure entry fetch(var item: integer);
  begin
    if count = 0 then delay;
    item := contents[out_ptr];
    out_ptr := (out_ptr + 1) mod 10;
    count := count - 1;
    continue
  end;
  
begin
  count := 0;
  in_ptr := 0;
  out_ptr := 0
end;
