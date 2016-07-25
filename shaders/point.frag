//#line 2 "point.frag"

// Inputs
flat in float data;
in vec2 texCoord;

// Outputs
layout(location = 0) out vec4 color;

// Uniforms
uniform mat4 modelViewProjection;

// Data attributes
flat in float d0;
uniform vec2 d0Bounds;
//uniform float pointScale;
uniform int isLog;

uniform vec2 dataBounds;

void main (void)
{
    float x = texCoord.x;
    float y = texCoord.y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )
    	discard;

    float z = sqrt(zz);
    float r;
    float v;
    if (isLog == 0){
        float r = log(dataBounds[1]) - log(dataBounds[0]);
        float v = (log(data) - log(dataBounds[0])) / r;
    } else {
        float r = (dataBounds[1]) - (dataBounds[0]);
        float v = ((data) - (dataBounds[0])) / r;
    }

    color = mapToColor(v) * zz;
}

void scale_linear (void)
{
    float x = texCoord.x;
    float y = texCoord.y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )
        discard;

    float z = sqrt(zz);
    
    //float r = log(d0Bounds[1]) - log(d0Bounds[0]);
    //float v = (log(d0) - log(d0Bounds[0])) / r;
    float r = (dataBounds[1]) - (dataBounds[0]);
    float v = ((data) - (dataBounds[0])) / r;

    color = mapToColor(v) * zz;
}

void scale_log (void)
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