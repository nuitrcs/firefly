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
    float data = texture(channels, TexCoords).r;

#if (LOG_MODE == 1)
    float r = log(dataBounds[1]) - log(dataBounds[0]);
    float v = (log(data) - log(dataBounds[0])) / r;
#else
    float r = (dataBounds[1]) - (dataBounds[0]);
    float v = ((data) - (dataBounds[0])) / r;
#endif

    v = clamp(v, 0.0, 1.0);
    
#if (RENDER_MODE == 0)
    fragmentColor = texture(colormap, vec2(v, 0.5));
#elif(RENDER_MODE == 1)
    fragmentColor = texture(colormap, vec2(v, 0.5)) * v;
#elif(RENDER_MODE == 2)
    int numShades = 5;
    v = ceil(v * numShades) / numShades;
    fragmentColor = texture(colormap, vec2(v, 0.5));
#endif 
}  