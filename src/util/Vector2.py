class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other):
		return Vector2(self.x - other.x, self.y - other.y)
	
	def __mul__(self, other):
		if (type(other) == Vector2):
			return Vector2(self.x * other.x, self.y * other.y)
		else:
			return Vector2(self.x * other, self.y * other)
	
	def __truediv__(self, other):
		if (type(other) == Vector2):
			return Vector2(self.x / other.x, self.y / other.y)
		else:
			return Vector2(self.x / other, self.y / other)
		
	def __iter__(self):
		coords = [self.x, self.y]
		for coord in coords:
			yield coord
		
	def __str__(self):
		return f"({self.x}, {self.y})"