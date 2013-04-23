import ipdb
from pyfirmata import ArduinoMega, util
import time
import pprint
from sensor_controller.PhotoResistor import PhotoResistor

SERIAL_INPUT = '/dev/tty.usbmodem1411'

# PHOTORESISTOR_THRESHOLD = 0.64
COLOR_RED = "red"
COLOR_GREEN = "green"
COLOR_BLUE = "blue"
COLOR_X = "x"

# class NewEventGenerator:
# 	def __init__(self):
# 		self.__event_queue = []

# 		self.__board = ArduinoMega(SERIAL_INPUT)
# 		self.__it = util.Iterator(self.__board)
# 		self.__it.start()

# 		# A dictionary stores the active/disactive state of photo-resistors
# 		self.__sensor_inputs = {}

# 		# Init photoresistors
# 		self.__photoresistors = []
# 		print "Setup Photoresistors ... "
# 		for i in range(0, 14):
# 			print "Photoresistor %d" % i
# 			photoresistor = PhotoResistor(self.__board, i)
# 			photoresistors.append(photoresistor)
# 		print "... Finish"

# 	def generateEvents(self):
# 		print "====== NEW CYCLE ====== "
		
# 		for photoresistor in photoresistors:
# 			self.__sensor_inputs[photoresistor.getPin()] = photoresistor.isActive()

# 		# Generate empty events
# 		if self.__sensor_inputs[10] or self.__sensor_inputs[11]


class EventGenerator:
	def __init__(self, board):
		self.__event_queue = []

		self.__board = board
		self.__it = util.Iterator(self.__board)
		self.__it.start()

		self.__sensor_inputs = {}

		self.__photoresistors = []
		print "Setup Photoresistors ... "
		for i in range(0, 14):
			print "Photoresistor %d" % i
			photoresistor = PhotoResistor(self.__board, i)
			self.__photoresistors.append(photoresistor)
		print "... Finish"

		# Init PHOTORESISTOR_THRESHOLD


	def generateEvents(self):

		# print "====== NEW CYCLE ======"
		# 0 - 9: LED Strips
		#	even: Led strip
		#	odd: empty
		# 10: Cup-R
		# 11: Cup-G
		# 12: Cup-B
		# 13: Cup-X
		# ipdb.set_trace()
		
		# Read sensor data to self.__sensor_inputs dictionary
		for photoresistor in self.__photoresistors:
			self.__sensor_inputs[photoresistor.getPin()] = photoresistor.isActive()			

		# Generate pour events
		if self.__sensor_inputs[10] or self.__sensor_inputs[11] or self.__sensor_inputs[12] or self.__sensor_inputs[13]:
			
			#find cup color
			cup_color_index = 0
			for j in range(10, 14):
				if self.__sensor_inputs[j]:
					cup_color_index = j
					break

			if cup_color_index == 10:
				cup_color = COLOR_RED
			elif cup_color_index == 11:
				cup_color = COLOR_GREEN
			elif cup_color_index == 12:
				cup_color = COLOR_BLUE
			else:
				cup_color = COLOR_X

			#find light rod
			light_rod_index = -1
			for j in range(0, 10, 2):
				# look up analog pin 0, 2, 4, 8
				if self.__sensor_inputs[j]:
					light_rod_index = j/2
					break

			if light_rod_index >= 0:
				# Generate a touch event
				event = {
					'type': 'pour',
					'light_rod': light_rod_index,
					'cup_color': cup_color
				}
				self.__event_queue.append(event)

		# print " == EVENT == "
		# pprint.pprint(event_queue)

		#  Generate empty event
		if self.__sensor_inputs[13]:

			# find empty rod
			light_rod_index = -1
			for j in range(1, 10, 2):
				# ipdb.set_trace()
				# look up analog pin 1, 3, 5, 7, 9
				# print "Photoresistor %s, active = %s" % (j, str(self.__sensor_inputs[j]))
				if self.__sensor_inputs[j]:
					light_rod_index = (j-1) /2
					break

			if light_rod_index >= 0:
				event = {
					'type': 'empty',
					'light_rod': light_rod_index
					# Empty event always involve Cup-X
				}
				self.__event_queue.append(event)

				# pprint.pprint(self.__event_queue)

		return self.__event_queue

	def generatePourEvents(self):
		pass

	def generateEmptyEvents(self):
		pass

	def generateShakeEvents(self):
		pass

	def generateTiltEvents(self):
		pass

	def reset(self):
		self.__event_queue = []