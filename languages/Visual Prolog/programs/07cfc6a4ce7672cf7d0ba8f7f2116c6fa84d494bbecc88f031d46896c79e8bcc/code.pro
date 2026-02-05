implement main
    open core

class predicates
    classInfo : core::classInfo.
clauses
    classInfo("hello", "1.0").

clauses
    run():-
        console::init(),
        stdio::write("Hello, World!"),
        stdio::nl.
