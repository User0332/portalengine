from typing import TypeVar
import numpy as np
import pywavefront
import moderngl as gl
import glm
import pywavefront.material
import pywavefront.mesh

from ..shaders import load_shader
from .utils import create_texture
from . import Model

CompoundModel = TypeVar("CompoundModel")

class CompoundModel(Model):
	def __init__(self, ctx: gl.Context, textures: list[gl.Texture], vaos: list[gl.VertexArray], positon: glm.vec3, rotation_radians: glm.vec3=glm.vec3(0, 0, 0), scale: glm.vec3=glm.vec3(1.0, 1.0, 1.0)) -> None:
		self.ctx = ctx
		self.textures = textures
		self.vaos = vaos
		self.shader_program = vaos[0].program

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
		self.shader_program["u_proj_matrix"].write(proj_matrix)
		self.shader_program["u_view_matrix"].write(view_matrix)
		self.shader_program["u_model_matrix"].write(self.model_matrix)

		for texture, vao in zip(self.textures, self.vaos):
			texture.use(0)
			vao.render()


	@staticmethod
	def load_from(ctx: gl.Context, obj_file: str, texture_filenames: list[str], position: glm.vec3, rotation_radians: glm.vec3=glm.vec3(0, 0, 0), scale: glm.vec3=glm.vec3(1.0, 1.0, 1.0), shader_names: list[str]=[]) -> CompoundModel:
		shader_fmt = "2f 3f 3f" # TODO: figure out
		shader_attrib = ["a_texture_coord", "a_normal", "a_pos"]

		vaos: list[gl.VertexArray] = []
		textures: list[gl.Texture] = []

		wvf = pywavefront.Wavefront(f"assets/objects/{obj_file}", cache=True, parse=True)

		test = pywavefront.material.Material("")

		for i, mat in enumerate(wvf.materials.values()):
			if i > len(texture_filenames)-1:
				manual_texture = None
			else:
				manual_texture = texture_filenames[i]

			if i > len(shader_names)-1:
				shader_name = "default"
			else:
				shader_name = shader_names[i]

			if manual_texture:
				texture = create_texture(ctx, manual_texture)
			elif mat.texture:
				texture = create_texture(ctx, manual_texture)
			else: raise ValueError(f"Could not find a texture for sub-object #{i}")

			shader_program = load_shader(ctx, shader_name)

			vbo = ctx.buffer(
				np.array(
					mat.vertices,
					dtype="f4"
				)
			)

			vao = ctx.vertex_array(
				shader_program,
				[(vbo, shader_fmt, *shader_attrib)]
			)

			vaos.append(vao)
			textures.append(texture)

		return CompoundModel(ctx, textures, vaos, position, rotation_radians, scale)
	
class GroupedModel(Model):
	def __init__(self, models: list[Model]) -> None:
		self.models = models

	def render(self, proj_matrix: glm.mat4x4, view_matrix: glm.mat4x4) -> None:
		for model in self.models:
			model.render(proj_matrix, view_matrix)