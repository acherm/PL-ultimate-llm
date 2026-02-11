#!/usr/bin/gawk -f
# Word frequency counter
# Counts the frequency of each word in the input

{
    # Convert to lowercase and split into words
    for (i = 1; i <= NF; i++) {
        word = tolower($i)
        # Remove punctuation
        gsub(/[^a-z0-9]/, "", word)
        if (length(word) > 0) {
            freq[word]++
        }
    }
}

END {
    # Print words and their frequencies, sorted by frequency
    n = asorti(freq, sorted_words, "@val_num_desc")
    print "Word Frequency Report"
    print "===================="
    for (i = 1; i <= n && i <= 20; i++) {
        word = sorted_words[i]
        printf "%-20s %5d\n", word, freq[word]
    }
}
