from Manifest import ledcontroller
from ledcontroller.Manifest import Color

class MyColor(Color):
		# Chuan-Che Huang
	def blend(self, c):
		self.__r += c.__r/BLENDING_CONSTANT
		self.__g += c.__g/BLENDING_CONSTANT
		self.__b += c.__b/BLENDING_CONSTANT

		# Normalize the color 
		# find max
		maxVal = 0
		for c in self.getRgb():
			if c > maxVal:
				maxVal = c

		self.__r /= maxVal
		self.__g /= maxVal
		self.__b /= maxVal