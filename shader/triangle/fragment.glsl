#version 330 core

layout (location = 0) out vec4 fragColor;
in vec3 out_color;

void main() {
    vec3 color = out_color;
    fragColor = vec4(color, 1.0);
}

