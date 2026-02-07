use vstd::prelude::*;

verus! {

spec fn factorial(n: nat) -> nat
    decreases n
{
    if n == 0 { 1 } else { n * factorial((n - 1) as nat) }
}

proof fn lemma_factorial_positive(n: nat)
    ensures factorial(n) > 0,
    decreases n,
{
    if n > 0 {
        lemma_factorial_positive((n - 1) as nat);
    }
}

fn compute_factorial(n: u64) -> (result: u64)
    requires n <= 20,
    ensures result == factorial(n as nat),
{
    if n == 0 {
        1
    } else {
        let prev = compute_factorial(n - 1);
        n * prev
    }
}

} // verus!
