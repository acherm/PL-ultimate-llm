-- | Cubical Agda example: paths, symmetry, and function extensionality
{-# OPTIONS --cubical #-}

module PathExamples where

open import Cubical.Core.Everything

-- In Cubical Agda, a path of type x ≡ y is a function from the
-- interval I to A, sending i0 to x and i1 to y.

-- Symmetry: reverse a path using interval negation (~)
sym' : {A : Set} {x y : A} → x ≡ y → y ≡ x
sym' p i = p (~ i)

-- Function extensionality holds by construction:
-- if f x = g x for all x, we get a path f ≡ g
funExt' : {A B : Set} {f g : A → B}
        → ((x : A) → f x ≡ g x)
        → f ≡ g
funExt' h i x = h x i

-- A simple boolean type with a non-trivial path
data Bool' : Set where
  tt ff : Bool'

-- Proof that double negation is the identity, using a path
not : Bool' → Bool'
not tt = ff
not ff = tt

not-not : (b : Bool') → not (not b) ≡ b
not-not tt = refl
not-not ff = refl
