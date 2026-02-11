module Nat where

data Nat : Set where
  zero : Nat
  suc  : Nat → Nat

{-# BUILTIN NATURAL Nat #-}

infixl 6 _+_

_+_ : Nat → Nat → Nat
zero  + m = m
suc n + m = suc (n + m)

infixl 7 _*_

_*_ : Nat → Nat → Nat
zero  * m = zero
suc n * m = m + n * m

infixl 6 _∸_

_∸_ : Nat → Nat → Nat
m     ∸ zero  = m
zero  ∸ suc n = zero
suc m ∸ suc n = m ∸ n

data _≤_ : Nat → Nat → Set where
  z≤n : ∀ {n}                 → zero  ≤ n
  s≤s : ∀ {m n} (m≤n : m ≤ n) → suc m ≤ suc n

infix 4 _≤_

≤-refl : ∀ {n} → n ≤ n
≤-refl {zero}  = z≤n
≤-refl {suc n} = s≤s ≤-refl

≤-trans : ∀ {l m n} → l ≤ m → m ≤ n → l ≤ n
≤-trans z≤n       _         = z≤n
≤-trans (s≤s l≤m) (s≤s m≤n) = s≤s (≤-trans l≤m m≤n)

≤-antisym : ∀ {m n} → m ≤ n → n ≤ m → m ≡ n
≤-antisym z≤n       z≤n       = refl
≤-antisym (s≤s m≤n) (s≤s n≤m) = cong suc (≤-antisym m≤n n≤m)

data _≡_ {A : Set} (x : A) : A → Set where
  refl : x ≡ x

infix 4 _≡_

{-# BUILTIN EQUALITY _≡_ #-}

sym : ∀ {A : Set} {x y : A} → x ≡ y → y ≡ x
sym refl = refl

trans : ∀ {A : Set} {x y z : A} → x ≡ y → y ≡ z → x ≡ z
trans refl refl = refl

cong : ∀ {A B : Set} (f : A → B) {x y} → x ≡ y → f x ≡ f y
cong f refl = refl

+-assoc : ∀ m n p → (m + n) + p ≡ m + (n + p)
+-assoc zero    n p = refl
+-assoc (suc m) n p = cong suc (+-assoc m n p)

+-identity : ∀ n → n + zero ≡ n
+-identity zero    = refl
+-identity (suc n) = cong suc (+-identity n)

+-suc : ∀ m n → m + suc n ≡ suc (m + n)
+-suc zero    n = refl
+-suc (suc m) n = cong suc (+-suc m n)

+-comm : ∀ m n → m + n ≡ n + m
+-comm m zero    = +-identity m
+-comm m (suc n) = trans (+-suc m n) (cong suc (+-comm m n))