// Inputs
in vec2 texCoord;

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

    fragmentColor = color;
#if (KERNEL_MODE == 1)
    fragmentColor = color * sin(z);
#else
    fragmentColor = color;
    fragmentColor.a = 1.0;
#endif
}
