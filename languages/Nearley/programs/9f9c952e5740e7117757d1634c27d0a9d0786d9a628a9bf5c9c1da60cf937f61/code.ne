# Arithmetic grammar in Nearley
# Demonstrates operator precedence parsing
# Reference: https://github.com/kach/nearley/blob/master/examples/arithmetic.ne

main -> _ AS _       {% function(d) {return d[1]; } %}

# Addition and subtraction
AS -> AS _ "+" _ MD  {% function(d) {return d[0]+d[4]; } %}
   | AS _ "-" _ MD   {% function(d) {return d[0]-d[4]; } %}
   | MD               {% id %}

# Multiplication and division
MD -> MD _ "*" _ E   {% function(d) {return d[0]*d[4]; } %}
   | MD _ "/" _ E    {% function(d) {return d[0]/d[4]; } %}
   | E                {% id %}

# Exponentiation
E -> F _ "^" _ E     {% function(d) {return Math.pow(d[0], d[4]); } %}
  | F                 {% id %}
  | "-" E             {% function(d) {return -d[1]; } %}

# Parentheses and integers
F -> "(" _ AS _ ")"  {% function(d) {return d[2]; } %}
  | int              {% id %}

int -> [0-9]:+       {% function(d) {return parseInt(d[0].join("")); } %}

# Whitespace
_ -> [\s]:*          {% function(d) {return null; } %}
