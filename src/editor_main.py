import pygame
import os
from util.Vector2 import *
from classes.objects.Player import Player
from editor.classes.EditorManager import EditorManager
from editor.classes.objects.Text import Text
from editor.classes.objects.Rect import Rect
from editor.classes.Group import Group

mapName = input("enter map to load/create: ")

em = EditorManager()
pygame.font.init()
running = True

try:
	em.LoadWorld(mapName)
except FileNotFoundError:
	open(f"maps/{mapName}.wld", "x", -1, "utf-8").close()
	em.LoadWorld(mapName)

snapIcons = Group([
	Rect(Vector2(10, 30), Vector2(50, 30), (160, 160, 100)),
	Text(Vector2(13, 5), "Snap", 20, (255, 255, 255)),
	Text(Vector2(13, 30), f"{em.snap}", 20, (255, 255, 255))
])

fixSnapIcons = Group([
	Rect(Vector2(10, 100), Vector2(50, 30), (160, 160, 100)),
	Text(Vector2(10, 80), "Fix snap", 12, (255, 255, 255)),
	Text(Vector2(18, 100), f"Fix", 20, (255, 255, 255))
])

sizeXIcons = Group([
	Rect(Vector2(100, 30), Vector2(50, 30), (160, 100, 100)),
	Text(Vector2(93, 5), "X size", 20, (255, 255, 255)),
	Text(Vector2(103, 30), f"{em.placeSize.x}", 20, (255, 255, 255))
])

sizeYIcons = Group([
	Rect(Vector2(100, 100), Vector2(50, 30), (100, 100, 160)),
	Text(Vector2(93, 75), "Y size", 20, (255, 255, 255)),
	Text(Vector2(103, 100), f"{em.placeSize.y}", 20, (255, 255, 255))
])

spriteIcons = Group([
	Rect(Vector2(190, 30), Vector2(250, 30), (100, 160, 160)),
	Text(Vector2(193, 5), "Sprite", 20, (255, 255, 255)),
	Text(Vector2(193, 33), f"{em.placeSprite}", 15, (255, 255, 255))
])

objIcons = Group([
	Rect(Vector2(190, 100), Vector2(120, 30), (100, 160, 160)),
	Text(Vector2(193, 75), "Object", 20, (255, 255, 255)),
	Text(Vector2(193, 103), f"{em.placeObj}", 15, (255, 255, 255))
])

typeIcons = Group([
	Rect(Vector2(10, 170), Vector2(120, 30), (100, 160, 160)),
	Text(Vector2(13, 145), "Block type", 20, (255, 255, 255)),
	Text(Vector2(13, 173), f"{em.placeBlockType}", 15, (255, 255, 255))
], False)

warpDestNameIcons = Group([
	Rect(Vector2(10, 240), Vector2(200, 30), (100, 160, 160)),
	Text(Vector2(13, 215), "Warp destination name", 20, (255, 255, 255)),
	Text(Vector2(13, 243), f"{em.placeWarpDestName}", 15, (255, 255, 255))
], False)

saveIcons = Group([
	Rect(Vector2(480, 30), Vector2(50, 30), (160, 100, 160)),
	Text(Vector2(458, 5), "Save file", 20, (255, 255, 255)),
	Text(Vector2(483, 30), f"Save", 20, (255, 255, 255))
])

undoIcons = Group([
	Rect(Vector2(350, 100), Vector2(50, 30), (100, 160, 100)),
	Text(Vector2(353, 75), "Undo", 20, (255, 255, 255)),
	Text(Vector2(353, 103), f"Undo", 20, (255, 255, 255))
])

multiplePlayerWarning = Group([
	Text(Vector2(900, 900), "this world has more than 1 player", 20, (255, 0, 0))
], False)

em.AddObject(snapIcons)
em.AddObject(fixSnapIcons)

em.AddObject(sizeXIcons)
em.AddObject(sizeYIcons)

em.AddObject(spriteIcons)
em.AddObject(objIcons)

em.AddObject(undoIcons)

em.AddObject(typeIcons)
em.AddObject(warpDestNameIcons)

em.AddObject(saveIcons)
em.AddObject(undoIcons)

em.AddObject(multiplePlayerWarning)

while running:
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			running = False

		if (event.type == pygame.KEYDOWN):
			if (event.key == pygame.K_SPACE):
				em.PlacePreviewObject()

			if (event.key == pygame.K_w):
				em.cameraPos.y -= em.snap

			if (event.key == pygame.K_a):
				em.cameraPos.x -= em.snap

			if (event.key == pygame.K_s):
				em.cameraPos.y += em.snap

			if (event.key == pygame.K_d):
				em.cameraPos.x += em.snap

		if (event.type == pygame.MOUSEBUTTONDOWN):
			snapClicked = snapIcons.GetObject(Rect).PointInside(em.mousePos)
			fixSnapClicked = fixSnapIcons.GetObject(Rect).PointInside(em.mousePos)
			sizeXClicked = sizeXIcons.GetObject(Rect).PointInside(em.mousePos)
			sizeYClicked = sizeYIcons.GetObject(Rect).PointInside(em.mousePos)
			spriteClicked = spriteIcons.GetObject(Rect).PointInside(em.mousePos)
			objClicked = objIcons.GetObject(Rect).PointInside(em.mousePos)
			typeClicked = typeIcons.GetObject(Rect).PointInside(em.mousePos) and typeIcons.active
			warpDestNameClicked = warpDestNameIcons.GetObject(Rect).PointInside(em.mousePos)
			warpDestNameClicked = warpDestNameClicked and warpDestNameIcons.active
			saveClicked = saveIcons.GetObject(Rect).PointInside(em.mousePos)
			undoClicked = undoIcons.GetObject(Rect).PointInside(em.mousePos)

			if (event.button == 1):
				# FIX SNAP
				if (fixSnapClicked):
					em.placeSize = em.SnapPos(em.placeSize)
					em.cameraPos = em.SnapPos(em.cameraPos)
				
				if (saveClicked):
					em.curWorld.name = mapName
					em.curWorld.SaveWorld(mapName)

				if (undoClicked):
					if (len(em.curWorld.objects) == 0):
						continue

					lastIndex = len(em.curWorld.objects) - 1
					em.curWorld.RemoveObject(em.curWorld.objects[lastIndex])

			if (event.button == 4):
				# SNAP
				if (snapClicked): em.snap += 1
				if (em.snap > 9999): em.snap = 9999

				# X SIZE
				if (sizeXClicked): em.placeSize.x += em.snap
				if (em.placeSize.x > 9999): em.placeSize.x = 9999

				# Y SIZE
				if (sizeYClicked): em.placeSize.y += em.snap
				if (em.placeSize.y > 9999): em.placeSize.y = 9999

				# SPRITE CHANGE
				if (spriteClicked):
					em.spriteIndex += 1

					if (em.spriteIndex > len(em.sprites) - 1): em.spriteIndex = 0
					em.placeSprite = em.sprites[em.spriteIndex]

				# OBJECT CHANGE
				if (objClicked):
					em.objIndex += 1

					if (em.objIndex > len(em.objTypes) - 1): em.objIndex = 0
					em.placeObj = em.objTypes[em.objIndex]

				# TYPE CHANGE
				if (typeClicked):
					em.blockTypeIndex += 1

					if (em.blockTypeIndex > len(em.blockTypes) - 1): em.blockTypeIndex = 0
					em.placeBlockType = em.blockTypes[em.blockTypeIndex]

				# WARP DEST NAME CHANGE
				if (warpDestNameClicked):
					em.warpDestNameIndex += 1
					
					if (em.warpDestNameIndex > len(em.maps) - 1): em.warpDestNameIndex = 0
					em.placeWarpDestName = em.maps[em.warpDestNameIndex]
			
			if (event.button == 5):
				# SNAP
				if (snapClicked): em.snap -= 1
				if (em.snap < 1): em.snap = 1

				# X SIZE
				if (sizeXClicked): em.placeSize.x -= em.snap
				if (em.placeSize.x < 0): em.placeSize.x = 0

				# Y SIZE
				if (sizeYClicked): em.placeSize.y -= em.snap
				if (em.placeSize.y < 0): em.placeSize.y = 0

				# SPRITE CHANGE
				if (spriteClicked):
					em.spriteIndex -= 1

					if (em.spriteIndex < 0): em.spriteIndex = len(em.sprites) - 1
					em.placeSprite = em.sprites[em.spriteIndex]

				# OBJECT CHANGE
				if (objClicked):
					em.objIndex -= 1

					if (em.objIndex < 0): em.objIndex = len(em.objTypes) - 1
					em.placeObj = em.objTypes[em.objIndex]

				# TYPE CHANGE
				if (typeClicked):
					em.blockTypeIndex -= 1

					if (em.blockTypeIndex < 0): em.blockTypeIndex = len(em.blockTypes) - 1
					em.placeBlockType = em.blockTypes[em.blockTypeIndex]

				# WARP DEST NAME CHANGE
				if (warpDestNameClicked):
					em.warpDestNameIndex -= 1
					
					if (em.warpDestNameIndex < 0): em.warpDestNameIndex = len(em.maps) - 1
					em.placeWarpDestName = em.maps[em.warpDestNameIndex]

	em.placePos = em.SnapPos(em.mousePos)

	if (em.placeObj == "BLOCK"): typeIcons.active = True
	else: typeIcons.active = False

	if (em.placeBlockType == "WARP" and em.placeObj == "BLOCK"): warpDestNameIcons.active = True
	else: warpDestNameIcons.active = False

	if (len(em.curWorld.GetObjects(Player)) > 1):
		multiplePlayerWarning.active = True
	else:
		multiplePlayerWarning.active = False

	snapIcons.GetObjects(Text)[1].text = f"{em.snap}"

	sizeXIcons.GetObjects(Text)[1].text = f"{em.placeSize.x}"
	sizeYIcons.GetObjects(Text)[1].text = f"{em.placeSize.y}"

	spriteIcons.GetObjects(Text)[1].text = f"{em.placeSprite}"
	objIcons.GetObjects(Text)[1].text = f"{em.placeObj}"

	typeIcons.GetObjects(Text)[1].text = f"{em.placeBlockType}"
	warpDestNameIcons.GetObjects(Text)[1].text = f"{em.placeWarpDestName}"

	em.Update()