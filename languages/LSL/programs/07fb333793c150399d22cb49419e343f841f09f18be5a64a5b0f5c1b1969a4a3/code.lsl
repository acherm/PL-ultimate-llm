default
{
    state_entry()
    {
        integer i;
        for (i = 1; i <= 100; ++i)
        {
            if (!(i % 15))
                llOwnerSay("FizzBuzz");
            else if (!(i % 3))
                llOwnerSay("Fizz");
            else if (!(i % 5))
                llOwnerSay("Buzz");
            else
                llOwnerSay((string)i);
        }
    }
}
