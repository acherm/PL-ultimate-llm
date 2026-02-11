program hello;
begin
    write(0, 160, 100, 1, "Hello, World!");
    while (!key(_esc))
        frame;
    end
end
