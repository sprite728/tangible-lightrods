import ipdb

BASELINE_LOOP = 10
THRESHOLD_DELTA = 0.08 #0.12

class PhotoResistor:

	
	"""
	PhotoResistor needs to know which pin it belongs to
	Know the baseline via avergaging the fisrt 10 sensor inputs
	Know if an input voltage means active or not
	"""


	def __init__(self, board, pin):
		# set pin
		# ipdb.set_trace()
		self.__board = board
		self.__pin = pin
		self.__board.analog[self.__pin].enable_reporting()

		# Run a for loops, read inputs BASELINE_LOOP times
		sensor_in_cumulative = 0
		for i in range(0, BASELINE_LOOP):
			sensor_in_cumulative += self._read()

		self.__baseline = sensor_in_cumulative/BASELINE_LOOP
		self.__threshold = self.__baseline - THRESHOLD_DELTA
		# ipdb.set_trace()


	def _read(self):
		val = self.__board.analog[self.__pin].read()
		while val == None:
			print "Photoresistor %d Cannot read val " % self.getPin()
			val = self.__board.analog[self.__pin].read()
		return val

	def getBaseline(self):
		return self.__baseline
	
	def getPin(self):
		return self.__pin

	def isActive(self):
		sensor_in = self._read()

		# Darker = Active
		# Darker => sensor_in smaller
		if sensor_in < self.__threshold:
			return True
		else:
			return False

