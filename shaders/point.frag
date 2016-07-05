#line 2 "point.frag"

layout(location = 0) out vec4 color;

flat in float sphere_radius;
in vec2 texCoord;
uniform mat4 modelViewProjection;

// Data attributes
flat in float d0;
uniform vec2 d0Bounds;

void main (void)
{
    float x = texCoord.x;
    float y = texCoord.y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )
    	discard;

    float z = sqrt(zz);
    
    float r = log(d0Bounds[1]) - log(d0Bounds[0]);
    float v = (log(d0) - log(d0Bounds[0])) / r;
    //float r = (d0Bounds[1]) - (d0Bounds[0]);
    //float v = ((d0) - (d0Bounds[0])) / r;

    color = colormap(v) * zz;
}
