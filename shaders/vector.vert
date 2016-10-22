// Attributes
in float x;
in float y;
in float z;

#if (SIZE_MODE == 1)
    in float size;
    out float attrib_size;
#endif

#if (FILTER_MODE == 1)
    in float datafilter;
    out float attrib_filter;
#endif

in float datax;
in float datay;
in float dataz;
out vec4  attrib_vector_data;
out float  attrib_data;

// Uniforms
uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;

void main(void)
{
    gl_Position = modelView * vec4(x, y, z, 1);

#if (SIZE_MODE == 1)
    attrib_size = size;
#endif

#if (FILTER_MODE == 1)
    attrib_filter = datafilter;
#endif
    
    mat3 rotMatrix = mat3(modelView);
    vec3 v = rotMatrix * vec3(datax, datay, dataz);
    attrib_data = length(vec3(datax, datay, dataz));
    attrib_vector_data = vec4(normalize(v), 1);
}
