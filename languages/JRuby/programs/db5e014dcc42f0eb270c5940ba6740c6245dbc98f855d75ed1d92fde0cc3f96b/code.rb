# JRuby example demonstrating Java integration
require 'java'

java_import 'java.util.ArrayList'
java_import 'java.util.HashMap'

# Create Java ArrayList
list = ArrayList.new
list.add("Hello")
list.add("from")
list.add("JRuby")

# Create Java HashMap
map = HashMap.new
map.put("language", "JRuby")
map.put("platform", "JVM")

# Iterate through ArrayList
puts "ArrayList contents:"
list.each { |item| puts "  #{item}" }

# Access HashMap
puts "\nHashMap contents:"
map.each { |key, value| puts "  #{key}: #{value}" }

# Call Java String methods
str = "jruby".to_java_string
puts "\nUppercase: #{str.toUpperCase}"
