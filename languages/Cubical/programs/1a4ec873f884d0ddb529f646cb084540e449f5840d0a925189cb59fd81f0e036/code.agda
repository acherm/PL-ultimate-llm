{-# OPTIONS --cubical #-}

module Example where

open import Cubical.Core.Everything
open import Cubical.Foundations.Prelude

-- Proof that addition is commutative for natural numbers
+-comm : (m n : ℕ) → m + n ≡ n + m
+-comm zero n = sym (+-zero n)
+-comm (suc m) n =
  suc (m + n)   ≡⟨ cong suc (+-comm m n) ⟩
  suc (n + m)   ≡⟨ sym (+-suc n m) ⟩
  n + suc m     ∎

-- Simple path equality example
refl-path : {A : Type} (x : A) → x ≡ x
refl-path x = refl