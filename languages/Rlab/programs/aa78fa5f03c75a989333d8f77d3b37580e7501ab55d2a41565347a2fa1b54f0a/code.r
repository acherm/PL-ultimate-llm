// Matrix operations in Rlab
// Create a matrix
A = [1, 2, 3; 4, 5, 6; 7, 8, 9];

// Create another matrix
B = [9, 8, 7; 6, 5, 4; 3, 2, 1];

// Matrix addition
C = A + B;
printf("Matrix C (A + B):\n");
disp(C);

// Matrix multiplication
D = A * B;
printf("Matrix D (A * B):\n");
disp(D);

// Transpose
E = A';
printf("Matrix E (A transpose):\n");
disp(E);

// Determinant
det_A = det(A);
printf("Determinant of A: %f\n", det_A);
