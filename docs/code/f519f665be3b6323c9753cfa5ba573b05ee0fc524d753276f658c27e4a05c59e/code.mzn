include "globals.mzn";

int: n_letters = 26;
set of int: LETTERS = 1..n_letters;

array[LETTERS] of int: scores =
  [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10];
array[LETTERS] of int: counts =
  [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1];

int: n_tiles = sum(counts);
array[1..n_tiles] of int: tiles =
  [ l | l in LETTERS for i in 1..counts[l] ];

int: n_words;
set of int: WORDS = 1..n_words;
int: max_len;
set of int: POS = 1..max_len;
array[WORDS, POS] of int: word_letters;
array[WORDS] of int: word_len;

array[LETTERS] of var 0..9: letter_value;
var int: score;

constraint assert(sum(counts) == 98, "sum of counts is not 98");

constraint
    alldifferent(letter_value) /\
    letter_value[1] > 0;

constraint
    score = sum(w in WORDS) (
              sum(p in 1..word_len[w]) (
                letter_value[word_letters[w,p]]
              )
            );

array[LETTERS] of var 0..max(counts): used;

constraint
    forall(l in LETTERS) (
        used[l] = sum(w in WORDS) (
                      count(word_letters[w,p] | p in 1..word_len[w], l)
                  )
    );

constraint
    forall(l in LETTERS) (
        used[l] <= counts[l]
    );

solve maximize score;

output ["The score is \(score)\n"] ++
       ["\(l) = \(fix(letter_value[l]));\n" | l in LETTERS];