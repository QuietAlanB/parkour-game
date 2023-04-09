import pygame

class Text:
	def __init__(self, pos, text, textSize, color):
		self.pos = pos
		self.text = text
		self.textSize = textSize
		self.color = color

		self.font = pygame.font.Font("res/font/CamingoCode-Regular.ttf", self.textSize)

	def DrawUpdate(self, screen):
		surface = self.font.render(self.text, True, self.color)

		screen.blit(surface, tuple(self.pos))

	def Update(self, **kwargs):
		screen = kwargs["screen"]

		self.DrawUpdate(screen)