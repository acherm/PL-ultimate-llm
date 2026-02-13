; Simple sine wave oscillator
Oscillator(freq) {
    phase = Accumulate(freq / Rate-of(#1) * 2 * #pi)
    Sin(phase)
}

; Main program: 440 Hz sine wave (A4 note)
Main() {
    Oscillator(440)
}
