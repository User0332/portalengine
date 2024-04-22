from portalengine import pygame
from portalengine.game import Game
from portalengine.events import PyGameEvent
from portalengine.models.prefabricated import Cube
from glm import vec3

game = Game((1200, 600), "Cube Render Test")

@game.event_handler.on(pygame.KEYDOWN)
def handle(event: PyGameEvent):
	if event.key == pygame.K_q:
		game.quit()
		exit(0)

game.player.forward_keys.append(pygame.K_UP)
game.player.back_keys.append(pygame.K_DOWN)
game.player.left_keys.append(pygame.K_LEFT)
game.player.right_keys.append(pygame.K_RIGHT)

cube = Cube.load_from(game.ctx, "crate.jpg", vec3(0))

game.scene.objects.append(cube)

game.run()