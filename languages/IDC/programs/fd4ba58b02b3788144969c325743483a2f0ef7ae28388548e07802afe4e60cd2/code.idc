#include <idc.idc>

// List all functions in the binary with their addresses
static main()
{
    auto ea, name, count;

    count = 0;
    Message("=== Function List ===\n");

    for (ea = NextFunction(0); ea != BADADDR; ea = NextFunction(ea))
    {
        name = GetFunctionName(ea);
        auto size = GetFunctionSize(ea);
        Message("0x%08X  %-40s  size=%d\n", ea, name, size);
        count = count + 1;
    }

    Message("=== Total: %d functions ===\n", count);
}
