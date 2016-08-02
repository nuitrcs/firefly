// Inputs
in vec2 TexCoords;

// Outputs
layout(location = 0) out vec4 fragmentColor;

// Uniforms
uniform sampler2D channels;
uniform sampler2D colormap;
uniform vec2 dataBounds;

void main()
{    
    float data = texture(channels, TexCoords).r / 200;
    float r = dataBounds[1] - dataBounds[0];
    float v = (data - dataBounds[0]) / r;
    v = clamp(v, 0.0, 1.0);
    fragmentColor.rgb = texture(colormap, vec2(v, 0.5)).rgb;
    fragmentColor.a=1.0;
}  