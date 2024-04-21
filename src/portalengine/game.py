import moderngl

from .timetracker import TimeTracker
from .player import Player
from .scene import Scene
from . import pygame

class Game:
	def __init__(self, display_size: tuple[int, int]=(500, 500), title: str="Portal Game", icon_path: str=None, gl_version: tuple[int, int]=(3, 3)) -> None:
		pygame.init()

		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, gl_version[1])
		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

		self.display = pygame.display.set_mode(display_size, pygame.DOUBLEBUF | pygame.OPENGL)

		pygame.display.set_caption(title)
		
		if icon_path: pygame.display.set_icon(pygame.image.load(icon_path))

		pygame.event.set_grab(True)
		pygame.mouse.set_visible(False)

		self.ctx = moderngl.create_context()
		self.clock = pygame.time.Clock()

		self.background_color = (0.08, 0.16, 0.18)
		self.framerate = 60

		self.scene = Scene()
		self.player = Player(self.scene)
		self.time_tracker = TimeTracker()

	def run(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.mouse.set_visible(True)
						pygame.event.set_grab(False)
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_ESCAPE:
						pygame.mouse.set_visible(False)
						pygame.event.set_grab(True)

			self.time_tracker.passed = pygame.time.get_ticks()

			self.ctx.clear(color=self.background_color)

			self.player.update()
			self.scene.render()

			pygame.display.flip()

			self.time_tracker.delta = self.clock.tick(self.framerate)