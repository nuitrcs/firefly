layout(points) in;
layout(triangle_strip, max_vertices=4) out;

//Inputs
in float attrib_data[];
in float attrib_size[];
in float attrib_filter[];
in float focusDistance[];

// Outputs
flat out float data;
out vec2 texCoord;
flat out vec4 distanceColor;

// Uniforms
uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;
uniform vec2 filterBounds;
uniform float pointScale;

void main(void)
{    
#if (FILTER_MODE == 1)
    if(attrib_filter[0] < filterBounds[0] || attrib_filter[0] > filterBounds[1]) return;
#endif

#if (SIZE_MODE == 1)
    float radius =  attrib_size[0] * pointScale;
    float v = 4.188 * pow(radius * 0.5, 3);
    data = attrib_data[0] / v;
#else
    float radius =  pointScale * 2.0;
    data = attrib_data[0];
#endif
    
    float fd = clamp(focusDistance[0] / 20, 0, 1);
    distanceColor = mix(vec4(0, 1, 0, 1), vec4(1,0,0,1), fd); 
    distanceColor *= 1.0 - fd;
    
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
