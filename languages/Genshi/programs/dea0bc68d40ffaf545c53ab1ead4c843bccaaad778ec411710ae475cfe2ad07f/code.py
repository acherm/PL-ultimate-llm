from genshi.template import TextTemplate

# Define a simple Genshi text template
tmpl = TextTemplate('''
Hello, $name!

#for item in items:
  * ${item}
#end

Your total is: $total
''')

# Render the template with data
stream = tmpl.generate(
    name='World',
    items=['apples', 'bananas', 'oranges'],
    total=42
)

print(stream.render())
