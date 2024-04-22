from typing import TypeVar
import moderngl as gl
import numpy as np
import glm

from .utils import create_texture
from ..shaders import load_shader
from . import Model

Cube = TypeVar("Cube")

_DATA_CUBE_VERTICES = np.array(
	[
		(-1, -1, 1), (1, -1, 1),
		(1, 1, 1), (-1, 1, 1),
		(-1, 1, -1), (-1, -1, -1),
		(1, -1, -1), (1, 1, -1)
	]
)

_DATA_CUBE_INDICES = [
	(0, 2, 3), (0, 1, 2),
	(1, 7, 2), (1, 6, 7),
	(6, 5, 4), (4, 7, 6),
	(3, 4, 5), (3, 5, 0),
	(3, 7, 4), (3, 2, 7),
	(0, 6, 1), (0, 5, 6)
]

_DATA_CUBE_VERTEX_DATA = np.array([_DATA_CUBE_VERTICES[ind] for triangle in _DATA_CUBE_INDICES for ind in triangle], dtype="f4")

_DATA_CUBE_TEXTURE_COORDS = [ # TODO: figure out what this is
	(0, 0), (1, 0),
	(1, 1), (0, 1)
]

_DATA_CUBE_TEXTURE_INDICES = [
	(0, 2, 3), (0, 1, 2),
	(0, 2, 3), (0, 1, 2),
	(0, 1, 2), (2, 3, 0),
	(2, 3, 0), (2, 0, 1),
	(0, 2, 3), (0, 1, 2),
	(3, 1, 2), (3, 0, 1)
]

_DATA_CUBE_TEXTURE_DATA = np.array([_DATA_CUBE_TEXTURE_COORDS[ind] for triangle in _DATA_CUBE_TEXTURE_INDICES for ind in triangle], dtype="f4")

_DATA_CUBE_NORMALS = np.array( # TODO: verify
	[
		(0, 0, 1)*6,
		(1, 0, 0)*6,
		(0, 0, -1)*6,
		(-1, 0, 0)*6,
		(0, 1, 0)*6,
		(0, -1, 0)*6
	],
	dtype="f4"
).reshape(36, 3)

_DATA_CUBE_VERTEX_DATA = np.hstack([_DATA_CUBE_NORMALS, _DATA_CUBE_VERTEX_DATA])

_DATA_CUBE_VBO_UNBUFFERED = np.hstack([_DATA_CUBE_TEXTURE_DATA, _DATA_CUBE_VERTEX_DATA])

class Cube(Model):
	def __init__(self, ctx: gl.Context, texture: gl.Texture, position: glm.vec3, rotation_radians: glm.vec3=glm.vec3(0, 0, 0), scale: glm.vec3=glm.vec3(1.0, 1.0, 1.0), shader_name: str="default") -> None:
		# TODO: make generic shaders for everything
		shader_fmt = "2f 3f 3f"
		shader_attrib = ["a_texture_coord", "a_normal", "a_pos"]

		vbo = ctx.buffer(_DATA_CUBE_VBO_UNBUFFERED)

		shader_program = load_shader(ctx, shader_name)

		vao = ctx.vertex_array(
			shader_program,
			[(vbo, shader_fmt, *shader_attrib)]
		)

		super().__init__(ctx, texture, vao, position, rotation_radians, scale)

	@staticmethod
	def load_from(ctx: gl.Context, texture_name: str, position: glm.vec3, rotation_radians: glm.vec3=glm.vec3(0, 0, 0), scale: glm.vec3=glm.vec3(1.0, 1.0, 1.0), shader_name: str="default") -> Cube:
		return Cube(ctx, create_texture(ctx, texture_name), position, rotation_radians, scale, shader_name)