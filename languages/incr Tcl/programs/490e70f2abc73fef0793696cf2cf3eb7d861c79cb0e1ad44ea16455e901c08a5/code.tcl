itcl::class simple {
  proc print {msg} {
    puts "simple::print = $msg"
  }
  public method hello {} print hello
}

simple s1
s1 hello