circuit Top :
  module Top :
    input clock : Clock
    input reset : UInt<1>
    input a : UInt<8>
    input b : UInt<8>
    output c : UInt<8>

    node sum = add(a, b)
    c <= sum
