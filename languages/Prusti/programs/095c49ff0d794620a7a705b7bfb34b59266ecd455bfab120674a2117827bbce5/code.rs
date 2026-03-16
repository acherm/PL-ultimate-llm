use prusti_contracts::*;

#[ensures(result >= a && result >= b)]
#[ensures(result == a || result == b)]
fn max(a: i32, b: i32) -> i32 {
    if a < b {
        b
    } else {
        a
    }
}

#[requires(n >= 0)]
#[ensures(result == n)]
fn identity(n: i32) -> i32 {
    n
}

fn main() {
    let m = max(3, 7);
    assert!(m == 7);
    let m2 = max(5, 2);
    assert!(m2 == 5);
}
