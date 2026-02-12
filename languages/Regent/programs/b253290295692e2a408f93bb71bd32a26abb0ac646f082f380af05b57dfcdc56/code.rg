import "regent"

task hello()
  regentlib.c.printf("Hello from Regent!\n")
end

task main()
  hello()
end

regentlib.start(main)
