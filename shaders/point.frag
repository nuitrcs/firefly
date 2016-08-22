// Inputs
#if(DATA_MODE == 1)
    flat in float data;
#endif
in vec2 texCoord;

// Outputs
layout(location = 0) out vec4 fragmentColor;

// Uniforms
uniform mat4 modelViewProjection;

// Data attributes
flat in float d0;
uniform vec2 d0Bounds;
//uniform float pointScale;
uniform int isLog;

uniform vec2 dataBounds;

// Colormap
uniform sampler2D colormap;

vec4 mapToColor(float v)
{
    return texture(colormap, vec2(v, 0.5)) * 0.2;
}

void main (void)
{
    float x = texCoord.x;
    float y = texCoord.y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )
    	discard;

    float z = sqrt(zz);
#if(DATA_MODE == 1)    
    #if (LOG_MODE == 1)
        float r = log(dataBounds[1]) - log(dataBounds[0]);
        float v = ((data) - log(dataBounds[0])) / r;
    #else
        float r = (dataBounds[1]) - (dataBounds[0]);
        float v = ((data) - (dataBounds[0])) / r;
    #endif
#else
    float v = 0;
#endif

#if (KERNEL_MODE == 1)
    fragmentColor = mapToColor(v) * sin(z);
#else
    fragmentColor = mapToColor(v);
    fragmentColor.a = 1.0;
#endif
}
