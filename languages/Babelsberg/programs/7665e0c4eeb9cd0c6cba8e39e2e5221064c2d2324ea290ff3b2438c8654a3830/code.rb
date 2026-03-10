require 'babelsberg/all'

# Temperature conversion with bidirectional constraints
class Temperature
  include Babelsberg
  attr_accessor :celsius, :fahrenheit

  def initialize(c)
    @celsius = c.to_f
    @fahrenheit = c * 9.0 / 5.0 + 32.0
    always { fahrenheit == celsius * 9.0 / 5.0 + 32.0 }
  end
end

temp = Temperature.new(0)
puts "0C = #{temp.fahrenheit}F"   # => 32.0F

temp.celsius = 100
puts "100C = #{temp.fahrenheit}F" # => 212.0F

temp.fahrenheit = 98.6
puts "98.6F = #{temp.celsius}C"   # => 37.0C
