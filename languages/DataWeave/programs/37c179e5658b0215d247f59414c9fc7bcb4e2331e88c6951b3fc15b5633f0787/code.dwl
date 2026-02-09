%dw 2.0
output application/json

var people = [
  { name: "Alice", age: 30, city: "New York" },
  { name: "Bob", age: 25, city: "London" },
  { name: "Charlie", age: 35, city: "New York" },
  { name: "Diana", age: 28, city: "London" },
  { name: "Eve", age: 40, city: "Paris" }
]

fun averageAge(group) =
  sum(group.age) / sizeOf(group)

---
people
  groupBy ((person) -> person.city)
  mapObject ((group, city) -> {
    (city): {
      count: sizeOf(group),
      averageAge: averageAge(group),
      names: group.name
    }
  })
