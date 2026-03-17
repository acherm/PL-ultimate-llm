use PDL;

# Create two matrices
my $a = pdl( [1, 2, 3], [4, 5, 6] );
my $b = pdl( [7, 8], [9, 10], [11, 12] );

# Matrix multiplication using the x operator
my $c = $a x $b;

print "Matrix A:\n$a\n";
print "Matrix B:\n$b\n";
print "A x B:\n$c\n";

# Element-wise operations
my $d = pdl(1, 4, 9, 16, 25);
my $e = sqrt($d);
print "Square roots of [", join(", ", list($d)), "]: $e\n";
