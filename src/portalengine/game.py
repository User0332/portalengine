import moderngl as gl

from .exceptions import GLException
from .events import EventHandlingDelegator
from .timetracker import TimeTracker
from .camera import Camera
from .player import StandardPlayer
from .scene import Scene
from . import shaders
from . import pygame

class Game:
	def __init__(self, display_size: tuple[int, int]=(500, 500), title: str="Portal Game", icon_path: str=None, player_type: type[StandardPlayer]=StandardPlayer, gl_version: tuple[int, int]=(3, 3), pygame_flags: int=0) -> None:
		pygame.init()

		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, gl_version[1])
		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

		self.display = pygame.display.set_mode(display_size, pygame.DOUBLEBUF | pygame.OPENGL | pygame_flags)

		pygame.display.set_caption(title)
		
		if icon_path: pygame.display.set_icon(pygame.image.load(icon_path))

		pygame.event.set_grab(True)
		pygame.mouse.set_visible(False)

		self.ctx = gl.create_context()

		self.ctx.enable(gl.DEPTH_TEST | gl.CULL_FACE)

		shaders.init(self.ctx)

		self.clock = pygame.time.Clock()

		self.background_color = (0.08, 0.16, 0.18)
		self.framerate = 60
		self.debug = True

		self.scene = Scene(self.ctx, self.display)
		self.time_tracker = TimeTracker()
		self.camera = Camera(self.scene, self.time_tracker)
		self.player = player_type(self.camera)
		self.event_handler = EventHandlingDelegator()

	def run(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				
				self.event_handler.send(event)

			self.time_tracker.passed = pygame.time.get_ticks()

			self.ctx.clear(color=self.background_color)

			self.player.update()
			self.scene.render(self.camera.proj_matrix, self.camera.view_matrix)

			if self.debug and self.ctx.error != "GL_NO_ERROR":
				raise GLException(self.ctx.error)

			pygame.display.flip()

			self.time_tracker.delta = self.clock.tick(self.framerate)

	def quit(self):
		pygame.quit()