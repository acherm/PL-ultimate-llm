class Fibonacci
  def self.fib(n:int):int
    if n <= 1
      return n
    end
    return fib(n - 1) + fib(n - 2)
  end
  
  def self.main(args:String[]):void
    puts "Fibonacci sequence:"
    i = 0
    while i < 10
      puts "F(#{i}) = #{fib(i)}"
      i += 1
    end
  end
end
