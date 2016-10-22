// Inputs
flat in float data;
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
    return texture(colormap, vec2(v, 0.5)) * v;
}

void main (void)
{
#if (LOG_MODE == 1)
    float v = clamp(log(data) / 20.0, 0, 1);
#else
    float v = clamp(data / 20.0, 0, 1);
#endif
    fragmentColor = mapToColor(v) * texCoord.x;
}
