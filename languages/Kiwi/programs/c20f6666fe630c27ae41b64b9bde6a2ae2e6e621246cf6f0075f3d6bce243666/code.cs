// Kiwi hardware synthesis example: Simple counter
// Kiwi takes C# programs and synthesises them to FPGA hardware

using System;

[KiwiSystem]
public class SimpleCounter
{
    static int count = 0;

    [Kiwi.HardwareEntryPoint()]
    static void Main()
    {
        while (true)
        {
            count = count + 1;
            Kiwi.Pause();
        }
    }
}
