//#line 2 "colormaps.frag"

uniform sampler2D colormap;

vec4 mapToColor(float v)
{
    return texture2D(colormap, vec2(v, 0.5)) * 0.2;
}

vec4 colormap_default(float v)
{
    vec4 c1 = vec4(0.1, 0.01, 0.01, 1);
    vec4 c2 = vec4(0.01, 0.01, 0.1, 1);
    return mix(c1, c2, v);
}

vec4 colormap_div(float v)
{
    vec4 c1 = vec4(0.01, 0.01, 0.2, 1);
    vec4 w = vec4(0.001, 0.001, 0.001, 1);
    vec4 c2 = vec4(0.1, 0.1, 0.01, 1);
    
    if(v <= 0.5) return mix(c1, w, v * 2);
    return mix(w, c2, (v - 0.5) * 2);
}

vec4 colormap_div2(float v)
{
    vec4 c1 = vec4(0.2, 0.01, 0.01, 1);
    vec4 w = vec4(0.001, 0.001, 0.001, 1);
    vec4 c2 = vec4(0.1, 0.01, 0.1, 1);
    
    if(v <= 0.5) return mix(c1, w, v * 2);
    return mix(w, c2, (v - 0.5) * 2);
}

vec4 colormap_div3(float v)
{
    vec4 c1 = vec4(0.01, 0.2, 0.01, 1);
    vec4 w = vec4(0.001, 0.001, 0.001, 1);
    vec4 c2 = vec4(0.01, 0.1, 0.1, 1);
    
    if(v <= 0.5) return mix(c1, w, v * 2);
    return mix(w, c2, (v - 0.5) * 2);
}
/* 
*/