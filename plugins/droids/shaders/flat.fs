#version 130

precision highp float;

in vec3 color;

out vec4 outputColor;

void main(void)
{
	outputColor = vec4(color, 1.0f);
}
