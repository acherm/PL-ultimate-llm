#include <metal_stdlib>
#include <simd/simd.h>

using namespace metal;

// A structure that defines the vertex inputs sent from the app to the vertex
// function.
struct VertexIn {
    float3 position [[attribute(0)]];
    float2 texCoord [[attribute(1)]];
};

// A structure that defines the outputs from the vertex function, which are
// then interpolated and passed to the fragment function.
struct VertexOut {
    float4 position [[position]];
    float2 texCoord;
};

// The vertex function, which is executed for each vertex in the pipeline.
vertex VertexOut vertex_main(const VertexIn in [[stage_in]]) {
    VertexOut out;
    out.position = float4(in.position, 1.0);
    out.texCoord = in.texCoord;
    return out;
}

// The fragment function, which is executed for each fragment in the pipeline.
fragment float4 fragment_main(VertexOut in [[stage_in]],
                              texture2d<float> tex2D [[texture(0)]],
                              sampler sampler2D [[sampler(0)]]) {
    // Sample the texture to get the color for the fragment.
    return tex2D.sample(sampler2D, in.texCoord);
}