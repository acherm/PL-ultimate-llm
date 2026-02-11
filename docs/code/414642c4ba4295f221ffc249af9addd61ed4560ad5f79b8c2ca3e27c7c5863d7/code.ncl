let Machine = {
  name: String,
  power: Num,
  wheels: Num | default = 0,
} in

let Car = Machine & {
  wheels | default = 4,
} in

Car {name = "Toyota", power = 100}