// Simple 4Test program demonstrating test automation
testcase HelloTest()
  // This testcase prints a message and performs basic validation
  Print("Hello from 4Test!")

  // Variable declaration and initialization
  STRING sMessage = "Test automation with 4Test"
  INTEGER iCount = 42
  BOOLEAN bPassed = TRUE

  // Output test information
  Print("Message: {sMessage}")
  Print("Count: {iCount}")

  // Simple assertion
  if (bPassed)
    Print("Test PASSED")
  else
    Print("Test FAILED")