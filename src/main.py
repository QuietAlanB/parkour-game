import pygame
from classes.World import World
from classes.GameManager import GameManager
from classes.objects.Player import Player
from classes.objects.Block import Block
from util.Vector2 import *

gm = GameManager()
running = True

w = World("", [])
w.LoadWorld("tutorial1")
gm.AddWorld(w)

gm.SetWorld("tutorial1")

while running:
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			running = False

	gm.Update()