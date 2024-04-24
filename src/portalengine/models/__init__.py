from typing import Protocol, TypeVar
import glm
import moderngl as gl
import numpy as np
import pywavefront

from .. import shaders
from ..shaders import get_default_shader, load_shader, loaded_shaders
from .utils import create_texture

BasicModel = TypeVar("BasicModel")

class Model(Protocol):
	def render(self, proj_matrix: glm.mat4x4, view_matrix: glm.mat4x4) -> None:
		pass

class BasicModel(Model):
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

	def render(self, proj_matrix: glm.mat4x4, view_matrix: glm.mat4x4) -> None:
		self.texture.use(0)
		self.shader_program["u_proj_matrix"].write(proj_matrix)
		self.shader_program["u_view_matrix"].write(view_matrix)
		self.shader_program["u_model_matrix"].write(self.model_matrix)

		self.vao.render()


	@staticmethod
	def load_from(ctx: gl.Context, obj_file: str, texture_file: str, position: glm.vec3, rotation_radians: glm.vec3=glm.vec3(0, 0, 0), scale: glm.vec3=glm.vec3(1.0, 1.0, 1.0), shader_name: str="default") -> BasicModel:
		shader_fmt = "2f 3f 3f" # TODO: figure out
		shader_attrib = ["a_texture_coord", "a_normal", "a_pos"]

		wvf = pywavefront.Wavefront(f"assets/objects/{obj_file}", cache=True, parse=True)

		obj = wvf.materials.popitem()[1]

		vbo = ctx.buffer(
			np.array(
				obj.vertices,
				dtype="f4"
			)
		)

		texture = create_texture(ctx, texture_file)

		shader_program = load_shader(ctx, shader_name)

		vao = ctx.vertex_array(
			shader_program,
			[(vbo, shader_fmt, *shader_attrib)]
		)

		return BasicModel(ctx, texture, vao, position, rotation_radians, scale)