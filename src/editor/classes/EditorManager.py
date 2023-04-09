import pygame
import math
import copy
import os
from classes.World import World
from classes.objects.Player import Player
from classes.objects.Block import Block
from util.Vector2 import *

class EditorManager:
	def __init__(self):
		self.editorObjects = []
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((1920, 1080))

		self.curWorld = None
		self.mousePos = Vector2(0, 0)
		self.cameraPos = Vector2(0, 0)

		self.snap = 1
		self.placePos = Vector2(0, 0)
		self.placeSize = Vector2(0, 0)
		self.placeSprite = "red.png"
		self.placeObj = "BLOCK"

		# vars for special interactions
		self.spriteIndex = 0
		self.sprites = os.listdir("res/tex/sprites")

		self.objIndex = 1
		self.objTypes = ["PLAYER", "BLOCK"]

		self.placeBlockType = "NORMAL"
		self.blockTypeIndex = 1
		self.blockTypes = ["NO COLLISION", "NORMAL", "KILL", "WARP"]

		self.placeWarpDestName = ""
		self.warpDestNameIndex = 0
		self.maps = os.listdir("maps")
		for i in range(len(self.maps)):
			self.maps[i] = self.maps[i].removesuffix(".wld")

	def AddObject(self, object):
		self.editorObjects.append(object)

	def RemoveObject(self, object):
		self.editorObjects.remove(object)

	def LoadWorld(self, fileName):
		w = World("", [])
		w.LoadWorld(f"{fileName}")
		self.curWorld = w

	def SaveWorld(self, fileName):
		if (self.curWorld == None):
			return

		self.curWorld.SaveWorld(fileName)
	
	def SnapPos(self, pos):
		pos /= self.snap
		pos.x = math.floor(pos.x)
		pos.y = math.floor(pos.y)
		pos *= self.snap
		return pos
	
	def DrawPreviewObject(self):
		sprite = pygame.image.load(f"res/tex/sprites/{self.placeSprite}").convert_alpha()
		sprite.set_alpha(128)
		sprite = pygame.transform.scale(sprite, tuple(self.placeSize))

		self.screen.blit(sprite, tuple(self.placePos))

	def PlacePreviewObject(self):
		placePos = self.placePos + self.cameraPos
		placeSize = copy.deepcopy(self.placeSize)

		if (self.placeObj == "PLAYER"):
			self.curWorld.AddObject(
				Player(placePos, placeSize, f"res/tex/sprites/{self.placeSprite}")
			)

		elif (self.placeObj == "BLOCK"):
			self.curWorld.AddObject(
				Block(placePos, placeSize, self.blockTypeIndex, f"res/tex/sprites/{self.placeSprite}", 
	                              self.placeWarpDestName)
			)

	def DrawWorldObjects(self):
		if (self.curWorld == None):
			return

		for object in self.curWorld.objects:
			object.pos -= self.cameraPos
			object.DrawUpdate(self.screen)
			object.pos += self.cameraPos

	def Update(self):
		self.screen.fill((0, 0, 0))

		self.mousePos.x = pygame.mouse.get_pos()[0]
		self.mousePos.y = pygame.mouse.get_pos()[1]

		self.DrawWorldObjects()
		self.DrawPreviewObject()

		for object in self.editorObjects:
			object.Update(
				screen=self.screen,
				mousePos=self.mousePos
			)

		pygame.display.update()
		self.clock.tick(60)