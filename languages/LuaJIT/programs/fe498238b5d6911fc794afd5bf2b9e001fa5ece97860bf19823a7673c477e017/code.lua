local ffi = require("ffi")

ffi.cdef[[
int printf(const char *fmt, ...);
]]

local function fibonacci(n)
    if n <= 1 then
        return n
    end
    local a, b = 0, 1
    for i = 2, n do
        a, b = b, a + b
    end
    return b
end

for i = 0, 10 do
    ffi.C.printf("fibonacci(%d) = %d\n", i, fibonacci(i))
end