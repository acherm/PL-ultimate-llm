using import struct

struct Example plain
    value : i32

    fn get_add_value (self n)
        self.value + n

    fn print_value_plus_one (self)
        print ('get_add_value self 1)

fn use_example (example)
    'print_value_plus_one example
