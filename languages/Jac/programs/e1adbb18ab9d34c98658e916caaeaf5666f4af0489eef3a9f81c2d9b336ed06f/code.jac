node person {
    has name: str;
    has age: int;
}

walker greet {
    can visit_person with `root entry {
        print(f"Hello, {here.name}!");
    }
}

with entry {
    p = person(name="World", age=0);
    greet() spawn p;
}