in double x;
in double y;
in double z;

// Data attributes
in double data0;
out double attrib_data0;

uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;

void main(void)
{
    gl_Position = modelView * vec4(x, y, z, 1);
    attrib_data0 = data0;
}
