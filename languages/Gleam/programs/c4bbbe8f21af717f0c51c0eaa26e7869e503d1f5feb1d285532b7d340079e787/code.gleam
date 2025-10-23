import gleam/io

pub fn main() {
  first()
  second()
}

pub fn first() {
  io.println("Hello from the first function!")
}

pub fn second() {
  io.println("Hello from the second function!")
}