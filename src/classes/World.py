from util.Vector2 import *
from util.log import *
from classes.objects.Player import Player
from classes.objects.Block import Block

class World:
	def __init__(self, name, objects):
		self.name = name
		self.fileName = None
		self.objects = objects

	def AddObject(self, object):
		self.objects.append(object)

	def RemoveObject(self, object):
		self.objects.remove(object)

	def GetObject(self, objType):
		for object in self.objects:
			if (type(object) == objType):
				return object
		return None
	
	def GetObjects(self, objType):
		returnList = []

		for object in self.objects:
			if (type(object) == objType):
				returnList.append(object)

		return returnList

	def LoadWorld(self, fileName):
		self.fileName = fileName
		file = open(f"maps/{fileName}.wld", "r")
		lines = file.readlines()
		file.close()

		for i in range(len(lines)):
			lines[i] = lines[i].strip("\n")

		objects = []
		skipAmount = 0

		for i, line in enumerate(lines):
			if (skipAmount > 0):
				skipAmount -= 1
				continue

			if (line == "WORLD"):
				self.name = lines[i + 1]
				skipAmount = 1

			elif (line == "PLAYER"):
				pos = Vector2(float(lines[i + 1]), float(lines[i + 2]))
				size = Vector2(float(lines[i + 3]), float(lines[i + 4]))
				spritePath = lines[i + 5]

				objects.append(
					Player(pos, size, spritePath)
				)
				skipAmount = 5

			elif (line == "BLOCK"):
				pos = Vector2(float(lines[i + 1]), float(lines[i + 2]))
				size = Vector2(float(lines[i + 3]), float(lines[i + 4]))
				type = int(lines[i + 5])
				spritePath = lines[i + 6]
				warpDestName = lines[i + 7]

				objects.append(
					Block(pos, size, type, spritePath, warpDestName)
				)
				skipAmount = 7

		self.objects = objects


	def SaveWorld(self, fileName):
		file = None
		try:
			file = open(f"maps/{fileName}.wld", "x")
		except:
			file = open(f"maps/{fileName}.wld", "w")
		file.write(self.WorldString())
		file.close()

	def WorldString(self) -> str:
		worldString = ""
		worldString += "WORLD\n"
		worldString += f"{self.name}\n"
		for object in self.objects:
			if (type(object) == Player):
				worldString += "PLAYER\n"
				worldString += f"{object.pos.x}\n"
				worldString += f"{object.pos.y}\n"
				worldString += f"{object.size.x}\n"
				worldString += f"{object.size.y}\n"
				worldString += f"{object.spritePath}\n"

			if (type(object) == Block):
				worldString += "BLOCK\n"
				worldString += f"{object.pos.x}\n"
				worldString += f"{object.pos.y}\n"
				worldString += f"{object.size.x}\n"
				worldString += f"{object.size.y}\n"
				worldString += f"{object.type}\n"
				worldString += f"{object.spritePath}\n"
				worldString += f"{object.warpDestName}\n"

		return worldString