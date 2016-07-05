layout(points) in;
layout(triangle_strip, max_vertices=4) out;

flat out float sphere_radius;

out vec2 texCoord;

uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;

// Data attributes
in float attrib_data0[];
flat out float d0;
uniform vec2 d0Filter;

// Visualization parameters
uniform float pointScale;

void main(void)
{
    d0 = float(attrib_data0[0]);
    if(d0 < d0Filter[0] || d0 > d0Filter[1]) return;

    sphere_radius =  pointScale * 2.0;
    float halfsize = sphere_radius * 0.5;
    
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
