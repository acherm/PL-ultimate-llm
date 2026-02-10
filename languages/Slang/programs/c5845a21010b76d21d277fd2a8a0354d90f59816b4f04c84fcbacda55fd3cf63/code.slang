// Simple vertex shader in Slang
struct VertexInput
{
    float3 position : POSITION;
    float2 texCoord : TEXCOORD;
};

struct VertexOutput
{
    float4 position : SV_Position;
    float2 texCoord : TEXCOORD;
};

cbuffer uniforms
{
    float4x4 modelViewProjection;
};

[shader("vertex")]
VertexOutput vertexMain(VertexInput input)
{
    VertexOutput output;
    output.position = mul(modelViewProjection, float4(input.position, 1.0));
    output.texCoord = input.texCoord;
    return output;
}

[shader("fragment")]
float4 fragmentMain(VertexOutput input) : SV_Target
{
    return float4(input.texCoord, 0.0, 1.0);
}
