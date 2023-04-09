import pygame
from classes.World import World
from classes.objects.Player import Player
from util.Vector2 import *
from util.log import *

class GameManager:
	def __init__(self):
		self.screen = pygame.display.set_mode((1920, 1080))
		self.clock = pygame.time.Clock()
		self.curWorld = None
		self.worldList = []

	def AddWorld(self, world):
		self.worldList.append(world)

	def RemoveWorld(self, world):
		self.worldList.remove(world)

	def SetWorld(self, name):
		for world in self.worldList:
			if (world.name == name):
				self.curWorld = world
				return

		WARN(f"world \"{name}\" not found in world list")

	def NextWorld(self):
		self.curWorld += 1

	def Update(self):
		self.screen.fill((0, 0, 0))
		pressed = pygame.key.get_pressed()

		for object in self.curWorld.objects:
			object.Update(
				screen=self.screen,
				pressed=pressed,
				world=self.curWorld,
				gm=self
			)

		pygame.display.update()
		self.clock.tick(60)