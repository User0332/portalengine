import glm
from .camera import Camera
from . import pygame

class StandardPlayer:
	def __init__(self, camera: Camera, height_before_eyes: float=2.0) -> None:
		self.ctx = camera.ctx
		self.camera = camera
		self.time = self.camera.time
		self.forward = self.camera.forward
		self.up = self.camera.up
		self.always_forward = self.camera.always_forward

		self.right = glm.vec3(1, 0, 0)
	
		self.pos = glm.vec3(self.camera.pos)
		self.height_before_eyes = height_before_eyes
		self.camera.pos.y = self.pos.y+height_before_eyes

		self.move_speed = 0.01
		self.mouse_sensitivity = 0.1

		self.is_jumping = False
		self.jump_started: int = 0
		self.sprint_enabled = False
		self.low_gravity = False

		self.forward_keys = [pygame.K_w]
		self.back_keys = [pygame.K_s]
		self.left_keys = [pygame.K_a]
		self.right_keys = [pygame.K_d]
		self.jump_keys = [pygame.K_SPACE]
		self.sprint_keys = [pygame.K_LCTRL]

	def update(self) -> None:
		self.move()
		self.rotate()
		self.update_vectors()

		self.camera.update()

		self.camera.pos = glm.vec3(self.pos.x, self.pos.y+self.height_before_eyes, self.pos.z)

	def update_vectors(self):
		yaw, pitch = glm.radians(self.camera.yaw), glm.radians(self.camera.pitch)

		self.camera.forward.x = glm.cos(yaw)*glm.cos(pitch)
		self.always_forward.x = glm.cos(yaw)*glm.cos(pitch)

		self.camera.forward.y = glm.sin(pitch)

		self.camera.forward.z = glm.sin(yaw)*glm.cos(pitch)
		self.always_forward.z = glm.sin(yaw)*glm.cos(pitch)

		self.camera.forward = glm.normalize(self.camera.forward)
		self.always_forward = glm.normalize(self.always_forward)

		self.right = glm.normalize(glm.cross(self.camera.forward, glm.vec3(0, 1, 0)))
		self.up = glm.normalize(glm.cross(self.right, self.camera.forward))

		self.forward = self.camera.forward

	def rotate(self):
		rel_x, rel_y = pygame.mouse.get_rel()

		self.camera.yaw+=rel_x*self.mouse_sensitivity
		self.camera.pitch-=rel_y*self.mouse_sensitivity
		self.camera.pitch = max(-89, min(89, self.camera.pitch))

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
	
	def is_held(self, held_keys: pygame.key.ScancodeWrapper, target_keys: list[int]):
		for key in target_keys:
			if held_keys[key]: return True

		return False

	def move(self):
		velocity = self.move_speed*self.time.delta

		if self.sprint_enabled:
			velocity*=2

		keys = pygame.key.get_pressed()

		self.key_held = False
		
		if self.is_held(keys, self.forward_keys):
			self.pos+=self.always_forward*velocity
			self.key_held = True
		if self.is_held(keys, self.back_keys):
			self.pos-=self.always_forward*velocity
			self.key_held = True
		if self.is_held(keys, self.right_keys):
			self.pos+=self.right*velocity
			self.key_held = True
		if self.is_held(keys, self.left_keys):
			self.pos-=self.right*velocity
			self.key_held = True

		self.handle_vertical_position(self.is_held(keys, self.jump_keys))

		if self.is_held(keys, self.sprint_keys):
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