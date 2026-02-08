#!/bin/ash
# Simple factorial calculator in Ash

factorial() {
    n=$1
    if [ "$n" -le 1 ]; then
        echo 1
    else
        prev=$(factorial $((n - 1)))
        echo $((n * prev))
    fi
}

# Main program
echo "Factorial Calculator"
for i in 1 2 3 4 5 6 7 8 9 10; do
    result=$(factorial $i)
    echo "$i! = $result"
done
