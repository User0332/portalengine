import moderngl

from .scene import Scene

class Player:
	def __init__(self, scene: Scene) -> None:
		self.scene = scene

	def update(self) -> None:
		pass

	def __del__(self) -> None:
		pass