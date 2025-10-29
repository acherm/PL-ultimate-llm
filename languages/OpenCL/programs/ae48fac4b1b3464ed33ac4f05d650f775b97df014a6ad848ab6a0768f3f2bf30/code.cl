// OpenCL kernel code
__kernel void saxpy( __global float *restrict output,
                    __global const float *restrict input,
                    const float a,
                    const int n)
{
    // Get our index in the array
    unsigned int i = get_global_id(0);

    // Check array boundary
    if(i < n)
        output[i] = a * input[i] + output[i];
}