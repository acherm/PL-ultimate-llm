# Fibonacci sequence generator using IronRuby
class FibonacciGenerator
  def initialize(count)
    @count = count
  end

  def generate
    fib = []
    (0...@count).each do |i|
      if i <= 1
        fib << i
      else
        fib << fib[i - 1] + fib[i - 2]
      end
    end
    fib
  end
end

# Generate and display first 10 Fibonacci numbers
generator = FibonacciGenerator.new(10)
fibonacci = generator.generate
puts "First 10 Fibonacci numbers:"
fibonacci.each_with_index do |num, index|
  puts "F(#{index}) = #{num}"
end
