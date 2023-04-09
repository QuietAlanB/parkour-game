import pygame

class Block:
	def __init__(self, pos, size, type, spritePath, warpDestName = ""):
		self.pos = pos
		self.size = size

		# types:
		# 0 = background block (no collision)
		# 1 = regular block
		# 2 = kill block (resets world on collision)
		# 3 = warp block (teleports to another world, requires "warpDestName" to be set)
		self.type = type

		self.spritePath = spritePath
		self.sprite = pygame.image.load(self.spritePath)
		self.sprite = pygame.transform.scale(self.sprite, tuple(self.size))

		self.warpDestName = warpDestName

	def CollidingWithAABB(self, other):
		if (self.pos.x < other.pos.x + other.size.x and
      		    self.pos.x + self.size.x > other.pos.x and
		    self.pos.y < other.pos.y + other.size.y and
      		    self.pos.y + self.size.y > other.pos.y):
			return True
		return False

	def DrawUpdate(self, screen):
		screen.blit(self.sprite, tuple(self.pos))

	def Update(self, **kwargs):
		screen = kwargs["screen"]

		self.DrawUpdate(screen)

	def __class__(self):
		return Block