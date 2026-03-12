-- PL/Tcl: count vowels and check palindromes

CREATE OR REPLACE FUNCTION count_vowels(str text) RETURNS integer AS $$
    set count 0
    foreach ch [split [string tolower $str] ""] {
        if {[string match {[aeiou]} $ch]} {
            incr count
        }
    }
    return $count
$$ LANGUAGE pltcl;

CREATE OR REPLACE FUNCTION is_palindrome(str text) RETURNS boolean AS $$
    set lower [string tolower $str]
    set reversed [string reverse $lower]
    return [expr {$lower eq $reversed}]
$$ LANGUAGE pltcl;

SELECT word, count_vowels(word) AS vowels, is_palindrome(word) AS palindrome
FROM (VALUES ('racecar'), ('hello'), ('level'), ('world')) AS t(word);
