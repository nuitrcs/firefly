#version 120
uniform sampler2D unif_DiffuseMap;

void main (void)
{
    gl_FragColor = texture2D(unif_DiffuseMap, gl_PointCoord) * gl_Color;
    //gl_FragColor.rgb *= gl_Color.a;
}
