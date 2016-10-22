layout(points) in;
layout(triangle_strip, max_vertices=4) out;

// Attributes
#if (DATA_MODE == 1)
    in float attrib_data[];
#endif

#if (SIZE_MODE == 1)
    in float attrib_size[];
#endif

#if (FILTER_MODE == 1)
    in float attrib_filter[];
#endif

out vec2 texCoord;
flat out float data;

// Uniforms
uniform vec2 filterBounds;
uniform float pointScale;
uniform mat4 projection;
uniform mat4 modelViewProjection;
uniform mat4 modelView;
uniform int decimation;

void main(void)
{    
    if(gl_PrimitiveIDIn % decimation != 0) return;
    
#if (FILTER_MODE == 1)
    if(attrib_filter[0] < filterBounds[0] || attrib_filter[0] > filterBounds[1]) return;
#endif

#if (SIZE_MODE == 1)
    float radius =  attrib_size[0] * pointScale * 0.1;
    float v = 4.188 * pow(radius * 0.5, 3);
    #if (DATA_MODE == 1)
        data = attrib_data[0] / v;
    #endif
#else
    float radius =  pointScale * 2.0;
    #if (DATA_MODE == 1)
        data = attrib_data[0];
    #endif
#endif

    //float halfsize = radius * 0.5 * sqrt(decimation);
    float halfsize = radius * 0.5;
    
    texCoord = vec2(1.0,-1.0);
    gl_Position = gl_in[0].gl_Position;
    gl_Position.xy += vec2(halfsize, -halfsize);
    gl_Position = projection * gl_Position;
    EmitVertex();

    texCoord = vec2(1.0,1.0);
    gl_Position = gl_in[0].gl_Position;
    gl_Position.xy += vec2(halfsize, halfsize);
    gl_Position = projection * gl_Position;
    EmitVertex();

    texCoord = vec2(-1.0,-1.0);
    gl_Position = gl_in[0].gl_Position;
    gl_Position.xy += vec2(-halfsize, -halfsize);
    gl_Position = projection * gl_Position;
    EmitVertex();

    texCoord= vec2(-1.0,1.0);
    gl_Position = gl_in[0].gl_Position;
    gl_Position.xy += vec2(-halfsize, halfsize);
    gl_Position = projection * gl_Position;
    EmitVertex();

    EndPrimitive();
}
