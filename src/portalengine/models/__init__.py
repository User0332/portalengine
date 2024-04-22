from typing import TypeVar
import glm
import moderngl as gl

from ..shaders import load_shader

Model = TypeVar("Model")

class Model:
	def __init__(self, ctx: gl.Context, texture: gl.Texture, vao: gl.VertexArray, positon: glm.vec3, rotation_radians: glm.vec3=glm.vec3(0, 0, 0), scale: glm.vec3=glm.vec3(1.0, 1.0, 1.0)) -> None:
		self.ctx = ctx
		self.texture = texture	
		self.vao = vao
		self.shader_program = vao.program

		self.pos = positon
		self.rotation = rotation_radians
		self.scale = scale

		matrix = glm.mat4()

		matrix = glm.translate(matrix, self.pos)

		matrix = glm.rotate(matrix, self.rotation.x, glm.vec3(1, 0, 0))
		matrix = glm.rotate(matrix, self.rotation.y, glm.vec3(0, 1, 0))
		matrix = glm.rotate(matrix, self.rotation.z, glm.vec3(0, 0, 1))

		self.model_matrix = glm.scale(matrix, scale)

		self.shader_program["u_texture"] = 0
		self.texture.use()

	def render(self, proj_matrix: glm.mat4x4, view_matrix: glm.mat4x4) -> None:
		self.texture.use()

		self.shader_program["u_proj_matrix"].write(proj_matrix)
		self.shader_program["u_view_matrix"].write(view_matrix)
		self.shader_program["u_model_matrix"].write(self.model_matrix)

		self.vao.render()


	@staticmethod
	def load_from(obj_file: str, texture_file: str, position: glm.vec3, rotation_radians: glm.vec3=glm.vec3(0, 0, 0), scale: glm.vec3=glm.vec3(1.0, 1.0, 1.0), shader_name: str="default") -> Model:
		pass # use pywavefront to load