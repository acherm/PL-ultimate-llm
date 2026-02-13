#!/usr/bin/env bb

(ns fizzbuzz)

(defn fizz-buzz [n]
  (condp (fn [a b] (zero? (mod b a))) n
    15 "FizzBuzz"
    3  "Fizz"
    5  "Buzz"
    n))

(doseq [n (range 1 101)]
  (println (fizz-buzz n)))
