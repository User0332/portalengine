from portalengine import pygame
from portalengine.game import Game
from portalengine.player import FlyingPlayer
from portalengine.events import PyGameEvent
from portalengine.models.compound import CompoundModel
from portalengine.models.prefabricated import Cube
from glm import vec3


game = Game((1200, 600), "Cube Render Test", player_type=FlyingPlayer)

@game.event_handler.on(pygame.KEYDOWN)
def handle(event: PyGameEvent):
	if event.key == pygame.K_q:
		game.quit()
		exit(0)

for x in range(-20, 20):
	for z in range(-20, 20):
		cube = Cube.load_from(game.ctx, "crate.jpg", vec3(x, -1, z))

		game.scene.objects.append(cube)

game.scene.objects.append(CompoundModel.load_from(game.ctx, "tree.obj", ["green.png", "brown.png", "brown.png"], vec3(0, 0, 0), scale=vec3(0.05, 0.05, 0.05)))

game.run()