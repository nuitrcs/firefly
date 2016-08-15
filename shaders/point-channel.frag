//#line 2 "point.frag"

// Inputs
flat in float data;
in vec2 texCoord;

// Outputs
layout(location = 0) out vec4 fragmentColor;

// Uniforms
uniform mat4 modelViewProjection;
uniform vec2 dataBounds;

void main (void)
{
    float x = texCoord.x;
    float y = texCoord.y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )
    	discard;

    float z = sqrt(zz);
    
    fragmentColor = vec4(data, 0, 0, 1.0) * sin(z);
}
