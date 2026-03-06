/proc/fibonacci(n)
	if(n <= 1)
		return n
	return fibonacci(n - 1) + fibonacci(n - 2)

/world/New()
	var/i
	for(i = 0, i <= 10, i++)
		world.log << "fib([i]) = [fibonacci(i)]"
