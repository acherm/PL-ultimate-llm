# Word frequency counter
# Counts occurrences of each word in the input

BEGIN {
    FS = "[^a-zA-Z]+"
}

{
    for (i = 1; i <= NF; i++) {
        if ($i != "") {
            word = tolower($i)
            count[word]++
        }
    }
}

END {
    for (word in count) {
        printf "%s: %d\n", word, count[word]
    }
}