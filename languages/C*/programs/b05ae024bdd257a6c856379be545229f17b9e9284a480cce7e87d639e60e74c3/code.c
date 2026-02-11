domain parallel_domain = [0:999];

void vector_add()
{
    shape [1000] float A, B, C;

    [parallel_domain] A = 1.0;
    [parallel_domain] B = 2.0;

    [parallel_domain] C = A + B;
}
