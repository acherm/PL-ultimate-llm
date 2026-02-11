#!/usr/bin/env raku
unit sub MAIN ($word? is copy);
my @words = 'share/dict'.IO.lines.grep(/^<[a..z]>**5$/); 
my @possible = @words;
my $try = 1;
while @possible > 1 {
    my $guess = $try == 1 ?? 'stare' !! smart-guess(@possible);
    my $result;
    with $word {
        $result = compare($word, $guess);
        say "$guess -> $result";
    }
    else {
        say "Try $try: $guess";
        $result = prompt 'Result: ';
        last if $result eq 'done';
    }
    @possible = filter-words(@possible, $guess, $result);
    $try++;
}
say @possible[0] if @possible == 1;
sub smart-guess(@words) {
    @words.sort(*.comb.unique.elems).[*-1]
}
sub compare($word, $guess) {
    my @result;
    my @word = $word.comb;
    my @guess = $guess.comb;
    for ^5 -> $i {
        if @word[$i] eq @guess[$i] {
            @result[$i] = '+';
            @word[$i] = @guess[$i] = Nil;
        }
    }
    for ^5 -> $i {
        next unless @guess[$i];
        if (my $j = @word.first(@guess[$i], :k)) {
            @result[$i] = '?';
            @word[$j] = Nil;
        }
        else {
            @result[$i] = '-';
        }
    }
    @result.join
}
sub filter-words(@words, $guess, $result) {
    my @guess = $guess.comb;
    my @result = $result.comb;
    my %must-have;
    my %must-not-have;
    my %exact;
    for ^5 -> $i {
        given @result[$i] {
            when '+' {
                %exact{$i} = @guess[$i];
                %must-have{@guess[$i]}++;
            }
            when '?' {
                %must-have{@guess[$i]}++;
                %must-not-have{$i}{@guess[$i]} = 1;
            }
            when '-' {
                %must-not-have<all>{@guess[$i]} = 1;
            }
        }
    }
    return @words.grep: -> $word {
        my @word = $word.comb;
        next False if %exact.first: -> $p {
            @word[$p.key] ne $p.value;
        };
        next False if %must-not-have.first: -> $p {
            $p.key eq 'all'
                ?? $word.contains($p.value.any)
                !! @word[$p.key] eq $p.value.any;
        };
        next False if %must-have.first: -> $p {
            $word.comb.grep($p.key) != $p.value;
        };
        True;
    };
}