class Group:
	def __init__(self, objects, active = True):
		self.objects = objects
		self.active = active

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
		returnObjs = []
		for object in self.objects:
			if (type(object) == objType):
				returnObjs.append(object)
		return returnObjs

	def Update(self, **kwargs):
		if (not self.active):
			return
		
		for object in self.objects:
			object.Update(**kwargs)