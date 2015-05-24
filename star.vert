#version 120
uniform float pointScale;
uniform vec2 windowSize;
uniform vec4 color;

void main(void)
{
    gl_Position = ftransform();
    
    vec4 eyePos = gl_ModelViewMatrix * gl_Vertex;
    vec4 projVoxel = gl_ProjectionMatrix * vec4(pointScale, pointScale, eyePos.z, eyePos.w);
    vec2 projSize = windowSize * projVoxel.xy / projVoxel.w;
    
    float ps = pointScale * projSize.x;
    gl_FrontColor = color;
    gl_FrontColor.a = ps * gl_Color.g;
    gl_PointSize =  ps * gl_Color.r * 10;
}
