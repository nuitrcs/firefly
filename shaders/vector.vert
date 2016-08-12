// Inputs
in float x;
in float y;
in float z;
in float data;
in float size;
in float filter;
in float datax;
in float datay;
in float dataz;

// Outputs
out float attrib_data;
out float attrib_size;
out float attrib_filter;
out vec4  attrib_vector_data;

// Uniforms
uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;

void main(void)
{
    gl_Position = modelView * vec4(x, y, z, 1);
    //attrib_data = data;
    attrib_size = size;
    attrib_filter = filter;
    
    mat3 rotMatrix = mat3(modelView);
    vec3 v = rotMatrix * vec3(datax, datay, dataz);
    attrib_data = length(vec3(datax, datay, dataz));
    attrib_vector_data = vec4(normalize(v), 1);
}
