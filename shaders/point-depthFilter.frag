//#line 2 "point.frag"

// Inputs
flat in float data;
in vec2 texCoord;
flat in vec4 distanceColor;

// Outputs
layout(location = 0) out vec4 fragmentColor;

// Uniforms
uniform vec4 color;

void main (void)
{
    float x = texCoord.x;
    float y = texCoord.y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )
    	discard;

    float z = sqrt(zz);

    fragmentColor = distanceColor;
}
