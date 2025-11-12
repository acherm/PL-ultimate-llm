class Greeter
  def initialize(name)
    @name = name
  end

  def greet
    puts "Hello, #{@name}"
  end
end
greeter = Greeter.new("World")
greeter.greet