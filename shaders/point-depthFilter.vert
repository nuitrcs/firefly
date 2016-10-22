// Inputs
in float x;
in float y;
in float z;
#if (DATA_MODE == 1)
    in float data;
#endif

#if (SIZE_MODE == 1)
    in float size;
    out float attrib_size;
#endif

#if (FILTER_MODE == 1)
    in float datafilter;
    out float attrib_filter;
#endif

// Outputs
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

#if (SIZE_MODE == 1)
    attrib_size = size;
#endif

#if (FILTER_MODE == 1)
    attrib_filter = datafilter;
#endif
}
