// Inputs
in float x;
in float y;
in float z;
in float data;
in float size;
in float filter;

// Outputs
out float attrib_data;
out float attrib_size;
out float attrib_filter;

// Uniforms
uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;

void main(void)
{
    gl_Position = modelView * vec4(x, y, z, 1);
    attrib_data = data;
    attrib_size = size;
    attrib_filter = filter;
}
