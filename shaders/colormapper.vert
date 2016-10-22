in vec4 vertex; // <vec2 position, vec2 texCoords>
out vec2 TexCoords;

void main()
{
    TexCoords.x = vertex.z;
    TexCoords.y = 1.0 - vertex.w;
    gl_Position = vec4(vertex.xy, 0.0, 1.0);
}