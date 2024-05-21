#version 330 core
in vec3 color;
in vec3 normal;
in vec3 fragpos;
in vec3 view_pos;
in vec2 uv;
uniform sampler2D tex;
out vec4 FragColor;

struct Light {
    vec3 position;
    vec3 color;
};

#define NUM_LIGHTS 2
uniform Light light_data[NUM_LIGHTS];

vec4 CreateLight(vec3 light_pos, vec3 light_color, vec3 normal, vec3 fragpos, vec3 view_dir) {
    //ambient
    float a_stength = 0.1;
    vec3 ambient = light_color * a_stength;

    //diffuse
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - fragpos);
    float diff = max(dot(norm, light_dir), 0.0);
    vec3 diffuse = light_color * diff;

    //specular
    float s_strength = 0.3;
    vec3 reflect_dir = normalize(-light_dir - norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
    vec3 specular = light_color * spec * s_strength;

    return vec4(color * (ambient + diffuse + specular), 1);
    
}

void main() {

    vec3 view_dir = normalize(view_pos - fragpos);

    for (int i = 0; i < NUM_LIGHTS; i++) {
        FragColor += CreateLight(light_data[i].position, light_data[i].color, normal, fragpos, view_dir);
    }
    FragColor = FragColor * texture(tex, uv);

}
