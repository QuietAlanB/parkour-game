import pygame

class Rect:
	def __init__(self, pos, size, color):
		self.pos = pos
		self.size = size
		self.color = color

	def PointInside(self, point):
		if (point.x > self.pos.x and
      		    point.x < self.pos.x + self.size.x and
		    point.y > self.pos.y and
      		    point.y < self.pos.y + self.size.y):
			return True
		return False

	def DrawUpdate(self, screen):
		pygame.draw.rect(
			screen, self.color,
			(self.pos.x, self.pos.y, self.size.x, self.size.y)
		)

	def Update(self, **kwargs):
		screen = kwargs["screen"]

		self.DrawUpdate(screen)