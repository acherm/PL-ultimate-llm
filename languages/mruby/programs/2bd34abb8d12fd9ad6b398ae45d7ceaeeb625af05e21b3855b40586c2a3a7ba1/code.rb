def fibonacci(n)
  return n if n <= 1
  a, b = 0, 1
  (n - 1).times do
    a, b = b, a + b
  end
  b
end

# Print first 10 Fibonacci numbers
10.times do |i|
  puts "F(#{i}) = #{fibonacci(i)}"
end
