from pyfirmata import ArduinoMega, util
import time 

SERIAL_PORT = '/dev/tty.usbmodem1411'

class SensorReader():
	def __init__(self):
		self.board = ArduinoMega(SERIAL_PORT)
		self.it = util.Iterator(self.board)
		self.it.start()
		self.board.analog[0].enable_reporting()
		# self.analog_0 = self.board.get_pin('a:0:i')

		print "Finish setup."

	def run(self):
		print "Start reading sensor input ... "
		# self.it.start()
		# self.board.analog[0].enable_reporting()
		while True:
			
			print self.board.analog[0].read()
			
			self.board.digital[13].write(0)
			time.sleep(0.5)
			self.board.digital[13].write(1)


if __name__ == '__main__':
	sensorReader = SensorReader()
	sensorReader.run()
	# board = ArduinoMega(SERIAL_PORT)

	# analog_0 = board.get_pin('a:0:i')

	# while True:
	# 	print analog_0.read()
	# 	time.sleep(0.2)
