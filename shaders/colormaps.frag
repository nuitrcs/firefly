//#line 2 "colormaps.frag"

uniform sampler2D colormap;

vec4 mapToColor(float v)
{
    return texture2D(colormap, vec2(v, 0.5)) * 0.2;
}
