version 1.0
task Hello {
  String name
  command {
    echo "Hello ${name}!"
  }
  output {
    String salutation = read_string(stdout())
  }
}

workflow HelloWorld {
  call Hello {
    input: name = "world"
  }
}