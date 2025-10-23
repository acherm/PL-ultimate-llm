/*
 * An address book is a mapping from names to addresses.
 * The address book may have multiple addresses for a name,
 * and multiple names for an address.
 *
 * This is a model of an address book, with two different
 * representations, and an assertion that they are equivalent.
 *
 * The first representation is a set of entries, each of which
 * is a pair of a name and an address.
 *
 * The second representation is a pair of relations, one from
 * book to name, and one from book to address, with a third
 * relation, "map", that ties them together.
 *
 * Daniel Jackson
 * Jan 2, 2004
 */

module examples/systems/addressBook

abstract sig Target {}
sig Name, Addr extends Target {}

// an address book is a set of name/address entries
sig Book {
  entries: Name -> Addr
}

// an address book is a pair of relations, with a mapping
sig Book' {
  names: set Name,
  addrs: set Addr,
  map: names -> addrs
}

// for every book, there is an equivalent book'
assert equiv1 {
  all b: Book | some b': Book' |
    b.entries = b'.map
}

// for every book', there is an equivalent book
assert equiv2 {
  all b': Book' | some b: Book |
    b.entries = b'.map
}

// check the assertions for a scope of 3
check equiv1 for 3
check equiv2 for 3

// a lookup operation
pred lookup (b: Book, n: Name, A: set Addr) {
  A = n.(b.entries)
}

// an add operation
pred add (b, b': Book, n: Name, a: Addr) {
  b'.entries = b.entries + n->a
}

// a delete operation
pred del (b, b': Book, n: Name, a: Addr) {
  b'.entries = b.entries - n->a
}

// some simple test cases
run lookup for 3
run add for 3
run del for 3

// show that adding an entry and then deleting it
// is not the same as doing nothing
assert add_del_same {
  all b, b': Book, n: Name, a: Addr |
    add [b, b', n, a] and del [b', b, n, a] implies b.entries = b'.entries
}
check add_del_same for 3
// counterexample: b has n->a already

// a better assertion
assert add_del_same_better {
  all b, b', b'': Book, n: Name, a: Addr |
    n->a not in b.entries and
    add [b, b', n, a] and
    del [b', b'', n, a]
  implies
    b.entries = b''.entries
}
check add_del_same_better for 3
// this one is valid

// show that adding an entry that is already there
// has no effect
assert add_redundant {
  all b, b': Book, n: Name, a: Addr |
    n->a in b.entries and
    add [b, b', n, a]
  implies
    b.entries = b'.entries
}
check add_redundant for 3
// this one is valid