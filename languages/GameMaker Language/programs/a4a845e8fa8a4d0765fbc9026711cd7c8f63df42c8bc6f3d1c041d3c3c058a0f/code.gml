for (var i = 1; i <= 100; i++) {
    if (i mod 15 == 0) {
        show_debug_message("FizzBuzz");
    } else if (i mod 3 == 0) {
        show_debug_message("Fizz");
    } else if (i mod 5 == 0) {
        show_debug_message("Buzz");
    } else {
        show_debug_message(string(i));
    }
}
