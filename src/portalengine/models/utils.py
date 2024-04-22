import moderngl as gl
from .. import pygame

def create_texture(ctx: gl.Context, name: str, ansiotropy: float=32.0) -> gl.Texture:
	surf = pygame.transform.flip(
		pygame.image.load(f"assets/textures/{name}").convert(),
		flip_x=False,
		flip_y=True
	)

	texture = ctx.texture(
		size=surf.get_size(), components=3,
		data=pygame.image.tostring(surf, "RGB")
	)

	# mipmaps remove texture ripples in distance
	# TODO: figure out what this does
	# NOTE: build_mipmaps will be removed in version 6.x
	texture.filter = (gl.LINEAR_MIPMAP_LINEAR, gl.LINEAR)
	texture.build_mipmaps()

	# improves texture quality, TODO: figure out what this does
	texture.anisotropy = ansiotropy

	return texture