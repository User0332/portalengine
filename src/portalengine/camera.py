import moderngl as gl
import glm

from .timetracker import TimeTracker
from .scene import Scene
from . import pygame

class Camera:
	def __init__(self, scene: Scene, time: TimeTracker, position: glm.vec3=glm.vec3(0, 0, 0), yaw: float=glm.radians(90), pitch: float=glm.radians(0)) -> None:
		self.scene = scene
		self.ctx = scene.ctx
		self.time = time

		win_size = scene.display_surf.get_size()

		self.aspect_ratio = win_size[0]/win_size[1]

		self.pos = glm.vec3(position)
		self.floor_y = self.pos.y # TODO: compute using physics
		self.up = glm.vec3(0, 1, 0)
		self.right = glm.vec3(1, 0, 0)
		self.forward = glm.vec3(0, 0, -1)
		self.always_forward = glm.vec3(self.forward)
		self.ALWAYS_UP = glm.vec3(self.up)
		self.yaw = yaw
		self.pitch = pitch

		self.fov = 50

		# TODO: figure out what near and far are
		self.near = 0.1
		self.far = 100

		self.view_matrix = self.get_view_matrix()
		self.proj_matrix = self.get_proj_matrix()

	def get_view_matrix(self):
		return glm.lookAt(self.pos, self.pos+self.forward, self.up)

	def get_proj_matrix(self):
		return glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near, self.far)

	def update(self) -> None:
		self.view_matrix = self.get_view_matrix()

	def update_vectors(self):
		yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

		self.forward.x = glm.cos(yaw)*glm.cos(pitch)
		self.ALWAYS_FORWARD.x = glm.cos(yaw)*glm.cos(pitch)

		self.forward.y = glm.sin(pitch)

		self.forward.z = glm.sin(yaw)*glm.cos(pitch)
		self.ALWAYS_FORWARD.z = glm.sin(yaw)*glm.cos(pitch)

		self.forward = glm.normalize(self.forward)
		self.ALWAYS_FORWARD = glm.normalize(self.ALWAYS_FORWARD)

		self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
		self.up = glm.normalize(glm.cross(self.right, self.forward))

	def rotate(self):
		rel_x, rel_y = pygame.mouse.get_rel()

		self.yaw+=rel_x*self.mouse_sensitivity
		self.pitch-=rel_y*self.mouse_sensitivity
		self.pitch = max(-89, min(89, self.pitch))

	def jump_func(self, t: float):
		if self.low_gravity: return (-(t-1.732)**2)+3

		return (-20*(t-0.387)**2)+3
		
	
	def get_floor_y(self) -> float:
		# int_pos = (floor(self.pos.x), floor(self.pos.z))

		# possible: list[int] = []

		# for obj in scene.objects:
		# 	if (obj.pos[0], obj.pos[2]) == int_pos: possible.append(obj.pos[1]+3)

		# try: return min(possible, key=lambda yval: self.pos.y-yval)
		# except ValueError: print(int_pos, [obj.pos for obj in scene.objects])

		return 0

	def move(self):
		velocity = self.move_speed*self.time.delta

		if self.sprint_enabled:
			velocity*=2

		keys = pygame.key.get_pressed()

		self.key_held = False
		
		if keys[pygame.K_w]:
			self.pos+=self.ALWAYS_FORWARD*velocity
			self.key_held = True
		if keys[pygame.K_s]:
			self.pos-=self.ALWAYS_FORWARD*velocity
			self.key_held = True
		if keys[pygame.K_d]:
			self.pos+=self.right*velocity
			self.key_held = True
		if keys[pygame.K_a]:
			self.pos-=self.right*velocity
			self.key_held = True

		self.handle_vertical_position(keys[pygame.K_SPACE])

		if keys[pygame.K_LCTRL]:
			self.sprint_enabled = True
			self.key_held = True
		elif not self.key_held: self.sprint_enabled = False

	def handle_vertical_position(self, jump_pressed: bool):
		self.floor_y = self.get_floor_y()

		height_off_ground = self.pos.y-self.floor_y

		if not self.is_jumping and jump_pressed and height_off_ground <= 0:
			self.is_jumping = True
			self.jump_started = 0

		self.jump_started+=self.time.delta_sec

		if self.is_jumping and height_off_ground < 2.9:
			self.pos.y = self.jump_func(self.jump_started)

			return
		
		self.is_jumping = False
		
		if height_off_ground > 0:
			self.pos.y = self.jump_func(self.jump_started)
			return
					
		return