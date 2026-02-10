# IBM 650 Assembly Program - Add Two Numbers
# This program adds two numbers stored in memory

00 70 0010 0000  # RAU (Reset and Add Upper) - Clear accumulator
01 69 0100 0000  # RAL (Reset and Add Lower) - Load first number
02 10 0101 0000  # AU (Add Upper) - Add second number
03 24 0200 0000  # STU (Store Upper) - Store result
04 01 0000 0000  # HALT - Stop execution

# Data section
0100 +0000000042  # First number (42)
0101 +0000000058  # Second number (58)
0200 +0000000000  # Result location
