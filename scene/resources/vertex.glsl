#version 330

in vec3 in_color;
in vec3 in_normal;
in vec2 in_tex_pos;
in vec3 in_vert;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec3 v_color;
out vec3 v_normal;
out vec3 v_pos;
out vec2 v_tex_pos;

void main() {
	v_color = in_color;
	v_normal = mat3(transpose(inverse(model))) * in_normal;
	v_pos = vec3(model * vec4(in_vert, 1.0));
	v_tex_pos = in_tex_pos;

	gl_Position = proj * view * model * vec4(in_vert, 1.0);
}
