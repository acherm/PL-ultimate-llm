let User = { name : Text, home : Text }

let makeUser = \(name : Text) -> { name = name, home = "/home/${name}" }

let users = [ makeUser "bill", makeUser "sally" ]

let User/show =
      \(user : User) ->
        "The user named `${user.name}` has a home directory at `${user.home}`"

in  { users = users, users-rendered = map users User User/show }