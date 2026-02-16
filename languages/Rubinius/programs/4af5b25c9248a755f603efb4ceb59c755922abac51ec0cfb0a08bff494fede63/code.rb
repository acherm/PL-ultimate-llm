def fibonacci(n)
  return n if n <= 1
  fibonacci(n - 1) + fibonacci(n - 2)
end

puts "Fibonacci sequence:"
(0..10).each do |i|
  puts "F(#{i}) = #{fibonacci(i)}"
end
