import glm
import moderngl as gl

from .models import Model
from . import pygame

class Scene:
	def __init__(self, ctx: gl.Context, display_surf: pygame.Surface) -> None:
		self.ctx = ctx
		self.display_surf = display_surf
		self.objects: list[Model] = []

	def render(self, proj_matrix: glm.mat4x4, view_matrix: glm.mat4x4) -> None:
		for obj in self.objects:
			obj.render(proj_matrix, view_matrix)