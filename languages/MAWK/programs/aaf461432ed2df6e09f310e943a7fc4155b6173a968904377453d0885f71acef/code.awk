# Word frequency counter in AWK
# Counts the frequency of each word in the input

{
    for (i = 1; i <= NF; i++) {
        word = tolower($i)
        gsub(/[^a-z0-9]/, "", word)
        if (word != "") {
            count[word]++
        }
    }
}

END {
    for (word in count) {
        print word, count[word]
    }
}
