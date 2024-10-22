#version 330

in vec3 v_color;
in vec3 v_normal;
in vec3 v_pos;
in vec2 v_tex_pos;

uniform vec3 ambient_value;
uniform vec3 diffuse_value;
uniform vec3 specular_value;

uniform float ambient_strength;
uniform float shininess;
uniform float transparency;

uniform vec3 light_color;
uniform vec3 light_pos;
uniform vec3 view_pos;

uniform bool has_color;
uniform bool has_normal;
uniform bool has_texture;

uniform sampler2D sampler;

out vec4 f_color;

vec3 ambient;
vec3 diffuse;
vec3 specular;
vec3 color;

void main() {
	if (has_normal) {
		ambient = light_color * (ambient_strength * ambient_value);

		vec3 normal = normalize(v_normal);
		vec3 light_dir = normalize(light_pos - v_pos);

		float diffuse_strength = max(dot(normal, light_dir), 0);
		diffuse = light_color * (diffuse_strength * diffuse_value);

		vec3 view_dir = normalize(view_pos - v_pos);
		vec3 reflect_dir = reflect(-light_dir, normal);

		float specular_strength = pow(max(dot(view_dir, reflect_dir), 0), shininess);
		specular = light_color * (specular_strength * specular_value);

		color = ambient + diffuse + specular;
	} else {
		color = light_color * diffuse_value;
	}
	if (has_texture) {
		color *= vec3(texture(sampler, v_tex_pos));
	} else if (has_color) {
		color *= v_color;
	}
	f_color = vec4(color, transparency);
}
