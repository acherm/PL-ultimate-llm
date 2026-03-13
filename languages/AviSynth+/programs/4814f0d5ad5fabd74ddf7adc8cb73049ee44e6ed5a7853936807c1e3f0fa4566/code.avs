# AviSynth+ script: Demonstrates user-defined functions and clip processing

# Recursive Fibonacci function
function Fibonacci(int n) {
    return (n <= 1) ? n : Fibonacci(n-1) + Fibonacci(n-2)
}

# Build a comma-separated list of the first n Fibonacci numbers
function FibList(int count) {
    result = ""
    for (i = 0, count - 1) {
        result = result + String(Fibonacci(i))
        result = (i < count - 1) ? result + ", " : result
    }
    return result
}

# Create a video clip displaying the Fibonacci sequence
BlankClip(width=640, height=120, length=75, fps=25, color=$001030)
Subtitle("Fibonacci: " + FibList(10), \
         x=20, y=45, size=28, \
         text_color=$FFE080, halo_color=$000000)
