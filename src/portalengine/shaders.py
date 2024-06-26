import moderngl as gl

DEFAULT_MAX_NUM_TEXTURES = 16

# todo: light
def get_default_shader(ctx: gl.Context, max_num_textures: int) -> gl.Program:
	return ctx.program(
		vertex_shader=f"""#version 330 core

layout (location = 0) in vec2 a_texture_coord; 
layout (location = 1) in vec3 a_normal; 
layout (location = 2) in vec3 a_pos; 

out vec3 color;
out vec2 texture_coord;

uniform mat4 u_proj_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_model_matrix;

void main()
{{
	gl_Position = u_proj_matrix*u_view_matrix*u_model_matrix*vec4(a_pos, 1.0);
	
	texture_coord = a_texture_coord;
}}
""",
		fragment_shader=f"""#version 330 core

in vec2 texture_coord;

layout (location = 0) out vec4 frag_color;

uniform sampler2D u_texture;

void main()
{{
	vec4 color = texture(u_texture, texture_coord);

	frag_color = color;
}}
""")

loaded_shaders: dict[str, gl.Program] = {}

def init(ctx: gl.Context):
	loaded_shaders["default"] = get_default_shader(ctx, DEFAULT_MAX_NUM_TEXTURES)

def load_shader(ctx: gl.Context, name: str) -> gl.Program:
	if name in loaded_shaders: return loaded_shaders[name]

	with open(f"assets/shaders/{name}.vert") as f:
		vert = f.read()

	with open(f"assets/shaders/{name}.frag") as f:
		frag = f.read()

	program = ctx.program(vertex_shader=vert, fragment_shader=frag)

	loaded_shaders[name] = program

	return program