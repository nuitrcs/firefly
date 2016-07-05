in float x;
in float y;
in float z;

// Data attributes
in float data0;
out float attrib_data0;

uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;

void main(void)
{
    gl_Position = modelView * vec4(x, y, z, 1);
    attrib_data0 = data0;
}
