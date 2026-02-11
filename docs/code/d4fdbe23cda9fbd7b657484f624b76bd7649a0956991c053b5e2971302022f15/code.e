# Copyright 2002 Combex, Inc. under the terms of the MIT X license
# found at http://www.opensource.org/licenses/mit-license.html .
#
# This is a straightforward translation of the Oz solution from
# http://www.mozart-oz.org/documentation/tutorial/node10.html
#
# To run this, you'll need a file named "e.bat" or "e.sh" on your
# path. See http://www.erights.org/ for how to get this. Then,
#
#   e dining-philosophers.e

? pragma.syntax("0.8")

/**
 * A philosopher is an active object that alternately thinks and
 * eats.
 */
def makePhilosopher(name, left, right) :any {
    def philosopher {
        to think() {
            println(`$name is thinking`)
            timer.whenPast(timer.now() + 3000,
                         def _ { eat() })
        }
        to eat() {
            println(`$name is hungry`)
            when (left <- take(), right <- take()) -> {
                println(`$name is eating`)
                timer.whenPast(timer.now() + 3000,
                             def _ {
                                 left.put()
                                 right.put()
                                 think()
                             })
            }
        }
    }
    return philosopher
}

/**
 * A fork is a shared passive object. It can be taken by only one
 * philosopher at a time.
 */
def makeFork(name) :any {
    def holder {
        to take() {
            def taken <- E.newCell(null)
            taken.put(true)
            return taken
        }
    }
    var current := holder
    def fork {
        to take() {
            def result := current.take()
            current := def broken {
                to take() { throw("already taken") }
            }
            return result
        }
        to put() {
            current := fork
        }
    }
    return fork
}

def philosophers {
    ["Plato", "Kant", "Turing", "Russel", "Socrates"]
}

# create the forks
def forks := <elib:tables.makeFlexList>()
for name in philosophers {
    forks.push(makeFork(name))
}

# create the philosophers
var i := 0
for name in philosophers {
    def p := makePhilosopher(name,
                             forks[i],
                             forks[(i + 1) % philosophers.size()])
    p.think()
    i += 1
}