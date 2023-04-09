import pygame
from classes.objects.Block import *
from util.Vector2 import *
from util.log import *

class Player:
	def __init__(self, pos, size, spritePath):
		self.pos = pos
		self.size = size

		self.spritePath = spritePath
		self.sprite = pygame.image.load(self.spritePath)
		self.sprite = pygame.transform.scale(self.sprite, tuple(self.size))

		self.speed = 0.75
		self.speedOpp = 5
		self.gravity = 0.3
		self.jumpForce = 6

		self.health = 100
		self.stamina = 100
		self.velocity = Vector2(0, 0)

		self.onGround = False
		self.wallclimbBoostReady = True
		self.wallBoostReady = True
		self.dashReady = True
		self.dashTicks = 0

	def Dash(self, pressed):
		if (self.dashReady and self.wallBoostReady and pressed[pygame.K_RCTRL] and self.stamina > 30 and 
      		    (pressed[pygame.K_a] or pressed[pygame.K_d])):
			self.dashReady = False
			self.dashTicks = 60
			self.stamina -= 30
			self.velocity.y -= self.jumpForce / 4
			if (pressed[pygame.K_a]): self.velocity.x = -self.speed * 20
			if (pressed[pygame.K_d]): self.velocity.x = self.speed * 20

	def ResetDash(self):
		if (self.dashTicks > 0):
			self.dashTicks -= 1
		else:
			self.dashReady = True

	def WallBoost(self, pressed, xDir):
		if (self.wallBoostReady and pressed[pygame.K_RCTRL] and self.stamina > 20):
			if (self.velocity.y > 11):
				self.health -= self.velocity.y ** 1.5

			if (not pressed[pygame.K_a] and not pressed[pygame.K_d]): pass
			elif (xDir == -1): self.velocity.x = -self.jumpForce * 2.5
			elif (xDir == 1): self.velocity.x = self.jumpForce * 2.5
			self.wallBoostReady = False
			self.velocity.y = -self.jumpForce * 0.9
			self.stamina -= 20

	def ResetWallBoost(self):
		if (self.onGround):
			self.wallBoostReady = True

	def WallclimbBoost(self, pressed):
		if (self.wallclimbBoostReady and abs(self.velocity.y) < 3.5 and 
                    pressed[pygame.K_w] and (pressed[pygame.K_a] or pressed[pygame.K_d]) and self.stamina > 25):
			self.wallclimbBoostReady = False
			self.velocity.y = -self.jumpForce * 1.3
			self.stamina -= 25

	def ResetWallclimbBoost(self):
		if (self.onGround):
			self.wallclimbBoostReady = True
 
	def TrackFall(self, pressed):
		if (pressed[pygame.K_LSHIFT]):
			if (self.onGround and self.velocity.y > 17):
				self.health -= self.velocity.y ** 1.5

		else:
			if (self.onGround and self.velocity.y > 11):
				self.health -= self.velocity.y ** 1.5

	def Move(self, pressed):
		if (pressed[pygame.K_w] and self.onGround and self.stamina > 12): 
			if (pressed[pygame.K_a]): self.velocity.x += -self.speed * 2
			if (pressed[pygame.K_d]): self.velocity.x += self.speed * 2
			self.velocity.y = -self.jumpForce
			self.onGround = False
			self.stamina -= 12

		if (pressed[pygame.K_a]): self.velocity.x += -self.speed
		if (pressed[pygame.K_d]): self.velocity.x += self.speed

	def Collide(self, block, world, gm, pressed):
		if (not block.CollidingWithAABB(self)):
			return
		
		if (block.type == 0):
			return
		
		if (block.type == 1):
			xDir = 0
			yDir = 0

			xDepth = 0
			yDepth = 0

			selfCenter = self.pos + self.size / 2
			blockCenter = block.pos + block.size / 2

			if (selfCenter.x < blockCenter.x): xDir = -1
			else: xDir = 1
			if (selfCenter.y < blockCenter.y): yDir = -1
			else: yDir = 1

			# x depth
			if (xDir == -1):
				xDepth = (self.pos.x + self.size.x) - block.pos.x
			else:
				xDepth = self.pos.x - (block.pos.x + block.size.x)

			# y depth
			if (yDir == -1):
				yDepth = (self.pos.y + self.size.y) - block.pos.y
			else:
				yDepth = self.pos.y - (block.pos.y + block.size.y)
			
			xDepth = abs(xDepth)
			yDepth = abs(yDepth)

			if (xDepth < yDepth):
				self.pos.x += xDepth * xDir

				self.WallclimbBoost(pressed)
				self.WallBoost(pressed, xDir)
			else:
				self.pos.y += yDepth * yDir

				if (yDir == -1): self.onGround = True

		if (block.type == 2):
			world.LoadWorld(world.fileName)

		if (block.type == 3):
			gm.SetWorld(block.warpDestName)

	def DrawBars(self, screen):
		# health
		pygame.draw.rect(
			screen, (110, 110, 110), 
			(755, 10, 400 + 10, 40)
			)
		pygame.draw.rect(
			screen, (255, 0, 0), 
			(760, 15, self.health * 4, 30)
			)
		
		# stamina
		pygame.draw.rect(
			screen, (110, 110, 110), 
			(805, 45, 300 + 10, 25)
			)
		pygame.draw.rect(
			screen, (0, 255, 0), 
			(810, 50, self.stamina * 3, 15)
			)

	def UpdateStats(self, world):
		self.stamina += 0.25

		if (self.stamina > 100): self.stamina = 100

		if (self.health > 100): self.health = 100
		if (self.health < 0): 
			self.health = 0
			world.LoadWorld(world.fileName)

	def PhysicsUpdate(self, blocks, world, gm, pressed):
		self.velocity.x -= self.velocity.x / self.speedOpp
		if (not self.onGround):
			self.velocity.y += self.gravity

		if (self.onGround):
			self.velocity.y = 0

		self.ResetWallclimbBoost()
		self.ResetWallBoost()
		self.ResetDash()

		self.Dash(pressed)

		self.pos += self.velocity

		self.onGround = False
		for block in blocks:
			self.Collide(block, world, gm, pressed)
			  
	def DrawUpdate(self, screen):
		screen.blit(self.sprite, tuple(self.pos))

		self.DrawBars(screen)

	def Update(self, **kwargs):
		screen = kwargs["screen"]
		pressed = kwargs["pressed"]
		world = kwargs["world"]
		gm = kwargs["gm"]

		blocks = world.GetObjects(Block)
		
		self.Move(pressed)
		self.UpdateStats(world)
		self.PhysicsUpdate(blocks, world, gm, pressed)
		self.TrackFall(pressed)

		self.DrawUpdate(screen)