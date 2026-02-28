#pragma version(1)
#pragma rs_fp_relaxed

void root(const uchar4 *v_in, uchar4 *v_out) {
    float4 f4 = rsUnpackColor8888(*v_in);
    float3 mono = dot(f4.rgb, (float3){0.299f, 0.587f, 0.114f});
    *v_out = rsPackColorTo8888(mono.r, mono.r, mono.r, f4.a);
}
