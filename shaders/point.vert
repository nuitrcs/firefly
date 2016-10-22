// Attributes
in float x;
in float y;
in float z;

#if (DATA_MODE == 1)
    in float data;
    out float attrib_data;
#endif

#if (SIZE_MODE == 1)
    in float size;
    out float attrib_size;
#endif

#if (FILTER_MODE == 1)
    in float datafilter;
    out float attrib_filter;
#endif

// Uniforms
uniform mat4 modelView;
uniform mat4 projection;
uniform mat4 modelViewProjection;

void main(void)
{
    gl_Position = modelView * vec4(x, y, z, 1);

#if(DATA_MODE == 1)
    attrib_data = data;
#endif

#if (SIZE_MODE == 1)
    attrib_size = size;
#endif

#if (FILTER_MODE == 1)
    attrib_filter = datafilter;
#endif
}
