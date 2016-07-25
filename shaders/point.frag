//#line 2 "point.frag"

// Inputs
flat in float data;
in vec2 texCoord;

// Outputs
layout(location = 0) out vec4 color;

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
    
    float r = log(dataBounds[1]) - log(dataBounds[0]);
    float v = (log(data) - log(dataBounds[0])) / r;
    //float r = (dataBounds[1]) - (dataBounds[0]);
    //float v = ((data) - (dataBounds[0])) / r;

    color = mapToColor(v) * sin(z);
}
