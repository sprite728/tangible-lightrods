import ipdb
from pyfirmata import ArduinoMega, util
import time
import pprint

SERIAL_INPUT = '/dev/tty.usbmodem1411'

PHOTORESISTOR_THRESHOLD = 0.5
COLOR_RED = "red"
COLOR_GREEN = "green"
COLOR_BLUE = "blue"

class EventGenerator:
	def __init__(self):
		self.__event_queue = []

		self.__board = ArduinoMega(SERIAL_INPUT)
		self.__it = util.Iterator(self.__board)
		self.__it.start()

		for i in range(0, 14):	
			self.__board.analog[i].enable_reporting()

	def generateEvents(self):

		sensor_inputs = {}
		print "====== NEW CYCLE ======"
		
		for i in range(0, 14):
			# 0 - 9: LED Strips
			#	even: Led strip
			#	odd: empty
			# 10: Cup-R
			# 11: Cup-G
			# 12: Cup-B
			# 13: Cup-X
			# ipdb.set_trace()
		
			sensor_in = self.__board.analog[i].read()
			if sensor_in < PHOTORESISTOR_THRESHOLD:
				sensor_inputs[i] = True
			else:
				sensor_inputs[i] = False

			if sensor_in:
				print str(i) + " " + str(sensor_inputs[i])

		# Generate touch events
		if sensor_inputs[10] or sensor_inputs[11] or sensor_inputs[12]:
			
			#find cup color
			cup_color_index = 0
			for j in range(10, 13):
				if sensor_inputs[j]:
					cup_color_index = j
					break

			if cup_color_index == 10:
				cup_color = COLOR_RED
			elif cup_color_index == 11:
				cup_color = COLOR_GREEN
			else:
				cup_color = COLOR_BLUE

			#find light rod
			light_rod_index = -1
			for j in range(0, 10, 2):
				# look up analog pin 0, 2, 4, 8
				if sensor_inputs[j]:
					light_rod_index = j/2
					break

			if light_rod_index >= 0:
				# Generate a touch event
				event = {
					'type': 'touch',
					'light_rod': light_rod_index,
					'cup_color': cup_color
				}
				self.__event_queue.append(event)

		# print " == EVENT == "
		# pprint.pprint(event_queue)
		return self.__event_queue

	def reset(self):
		self.__event_queue = []


def main():
	# board = ArduinoMega(SERIAL_INPUT)
	# it = util.Iterator(board)
	# it.start()

	# for i in range(0, 14):
	# 	board.analog[i].enable_reporting()

	# sensor_inputs = {}
	# event_queue = []
	# while True:
	# 	print "====== NEW CYCLE ======"
	# 	event_queue = []
	# 	for i in range(0, 14):
	# 		# 0 - 9: LED Strips
	# 		#	even: Led strip
	# 		#	odd: empty
	# 		# 10: Cup-R
	# 		# 11: Cup-G
	# 		# 12: Cup-B
	# 		# 13: Cup-X
	# 		# ipdb.set_trace()
			
	# 		sensor_in = board.analog[i].read()
	# 		if sensor_in < PHOTORESISTOR_THRESHOLD:
	# 			sensor_inputs[i] = True
	# 		else:
	# 			sensor_inputs[i] = False

	# 		if sensor_in:
	# 			print str(i) + " " + str(sensor_inputs[i])

	# 	# time.sleep(1)

	# 	# Generate touch events
	# 	if sensor_inputs[10] or sensor_inputs[11] or sensor_inputs[12]:
			
	# 		#find cup color
	# 		cup_color_index = 0
	# 		for j in range(10, 13):
	# 			if sensor_inputs[j]:
	# 				cup_color_index = j
	# 				break

	# 		if cup_color_index == 10:
	# 			cup_color = COLOR_RED
	# 		elif cup_color_index == 11:
	# 			cup_color = COLOR_GREEN
	# 		else:
	# 			cup_color = COLOR_BLUE

	# 		#find light rod
	# 		light_rod_index = -1
	# 		for j in range(0, 10, 2):
	# 			# look up analog pin 0, 2, 4, 8
	# 			if sensor_inputs[j]:
	# 				light_rod_index = j/2
	# 				break

	# 		if light_rod_index >= 0:
	# 			# Generate a touch event
	# 			event = {
	# 				'type': 'touch',
	# 				'light_rod': light_rod_index,
	# 				'cup_color': cup_color
	# 			}
	# 			event_queue.append(event)

	# 	print " == EVENT == "
	# 	pprint.pprint(event_queue)
	
	eventGenerator = EventGenerator()

	while True:
		event_queue = eventGenerator.generateEvents()
		pprint.pprint(event_queue)
		time.sleep(1)





if __name__ == '__main__':
	main()