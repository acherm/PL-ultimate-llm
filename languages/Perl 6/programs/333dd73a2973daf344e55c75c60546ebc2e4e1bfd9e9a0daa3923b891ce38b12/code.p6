sub quicksort (@a) {
    return @a if @a <= 1;
    my $pivot = @a[0];
    my @rest  = @a[1..*];
    return flat quicksort(@rest.grep: * < $pivot),
                $pivot,
                quicksort(@rest.grep: * >= $pivot);
}

say quicksort(<3 1 4 1 5 9 2 6 5 3 5>).join(", ");
