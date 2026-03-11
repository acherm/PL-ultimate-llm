// FizzBuzz in BYOND DM (Dream Maker)

/world/New()
    var/i
    for(i = 1, i <= 30, i++)
        if(!(i % 15))
            world << "FizzBuzz"
        else if(!(i % 3))
            world << "Fizz"
        else if(!(i % 5))
            world << "Buzz"
        else
            world << i
    del(world)
