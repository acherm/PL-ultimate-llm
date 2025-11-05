object "adder" {
  code {
    // Parse input
    let x := calldataload(0)
    let y := calldataload(0x20)
    // Compute sum
    let sum := add(x, y)
    // Persist result in memory
    mstore(0, sum)
    // Return 32 bytes from memory starting at position 0
    return(0, 0x20)
  }
}