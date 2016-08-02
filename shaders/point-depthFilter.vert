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
out float focusDistance;

// Uniforms
uniform mat4 view;
uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;
uniform vec3 focusPosition;

void main(void)
{
    gl_Position = modelView * vec4(x, y, z, 1);
    vec4 vfp = view * vec4(focusPosition.xyz, 1);
    focusDistance = distance(gl_Position, vfp);
    attrib_data = data;
    attrib_size = size;
    attrib_filter = filter;
}
