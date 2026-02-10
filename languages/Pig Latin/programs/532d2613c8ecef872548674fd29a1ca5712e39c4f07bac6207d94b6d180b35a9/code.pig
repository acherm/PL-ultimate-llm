-- Word Count in Pig Latin
-- Load input data from a file
input_lines = LOAD 'input.txt' AS (line:chararray);

-- Tokenize each line into words
words = FOREACH input_lines GENERATE FLATTEN(TOKENIZE(line)) AS word;

-- Group by word
grouped_words = GROUP words BY word;

-- Count occurrences of each word
word_count = FOREACH grouped_words GENERATE group AS word, COUNT(words) AS count;

-- Order by count descending
ordered = ORDER word_count BY count DESC;

-- Store the result
STORE ordered INTO 'output';
