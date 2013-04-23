"""
Demonstrate generating colors in Python and using DataSender to transfer them
over Serial to the Arduino. (Optionally simulate entirely in Python.)

Low-level version, using fewer layers of abstraction (and convenience).
"""

# Set how many times to update the pattern (insert one Color) and redisplay
# on the LED strip; use None to continue forever.
TRIALS = None

# Optionally use a dummy serial device and draw to the screen. (Drawing to the
# screen does not prevent sending to the Arduino.)
DUMMY_SERIAL = False
DRAW = False

# Change this to match your Serial device. The correct value will be in the
# Arduino app's Tools > Serial Device menu. See directions for picking your
# serial device under "Uploading" at http://arduino.cc/en/Guide/Environment .
SERIAL_DEVICE = '/dev/tty.usbmodem1421'
SERIAL_INPUT =  '/dev/tty.usbmodem1411'

from Manifest import ledcontroller

from ledcontroller.Manifest import sys, time, random, math, DataSender
from ledcontroller.Manifest import SendingBuffer, Sequences
from ledcontroller.Manifest import TurtleBuffer
from ledcontroller.Manifest import Color
import ipdb
from pyfirmata import ArduinoMega, util
from sensor_controller.EventGenerator import EventGenerator
import time

if __name__ == '__main__':
	

	"""
	Setup sensor input
	"""
	
	eventGenerator = EventGenerator()


	dt = 0.0

	# Use a predefined color sequence; either random colors, or a hue
	# gradient. These are Python generators, yielding Color objects.
	#colorSequence = Sequences.GenerateRandom(limit=TRIALS,
	#	brightInterval=5)
	colorSequence = Sequences.GenerateHueGradient(limit=TRIALS)

	if DUMMY_SERIAL:
		sender = DataSender.DummySender(SERIAL_DEVICE,
			silent=True)
	else:
		sender = DataSender.Sender(SERIAL_DEVICE)
	# Open the serial connection.
	with sender:

		# SendingBuffer has a list of Color objects and encapsulates
		# requisite logic for generating bytes and sending.
		# For simulating, TurtleBuffer subclasses SendingBuffer and
		# draws to the screen using Turtle Graphics as well.
		if DRAW:
			sendingColorBuffer = TurtleBuffer(sender=sender)
		else:
			sendingColorBuffer = SendingBuffer(sender=sender)
			sendingColorBuffer1 = SendingBuffer(sender=sender)
			sendingColorBuffer2 = SendingBuffer(sender=sender)
			sendingColorBuffer3 = SendingBuffer(sender=sender)
			sendingColorBuffer4 = SendingBuffer(sender=sender)
			# sendingColorBufferCenter = SendingBufferCenter(sender=sender)

		# Put some known colors at the beginning.
		for c in Sequences.GetSentinels():
			sendingColorBuffer.insertAndPop(c)
			sendingColorBuffer1.insertAndPop(c)

		for c in colorSequence:
			t = time.time()
			# ipdb.set_trace()


			event_queue = eventGenerator.generateEvents()
			for event in event_queue:
				if event.get('type', None) == 'pour':
					# cup_color, light_rod, type
					light_rod = event.get('light_rod', None)

					if event.get('cup_color', None) == "red":
						c = Color(rgb=(0.0, 0.0, 1.0))
					elif event.get('cup_color', None) == 'green':
						c = Color(rgb=(0.0, 1.0, 0.0))
					elif event.get('cup_color', None) == 'blue':
						c = Color(rgb=(1.0, 0.0, 0.0))

					if light_rod == 0:
						sendingColorBuffer.insertAndPop(c)
						sendingColorBuffer.send(data_receiver_color_key="COLORS", reverse=True)
					if light_rod == 1:
						sendingColorBuffer1.insertAndPop(c)
						sendingColorBuffer1.send(data_receiver_color_key="COLOR1", reverse=True)
					if light_rod == 2:
						sendingColorBuffer2.insertAndPop(c)
						sendingColorBuffer2.send(data_receiver_color_key="COLOR2", reverse=True)
					if light_rod == 3:
						sendingColorBuffer3.insertAndPop(c)
						sendingColorBuffer3.send(data_receiver_color_key="COLOR3", reverse=True)
					if light_rod == 4:
						sendingColorBuffer4.insertAndPop(c)
						sendingColorBuffer4.send(data_receiver_color_key="COLOR4", reverse=True)

			eventGenerator.reset()

			# time.sleep(1)
			
			# if board.analog[0].read():
			# 	if board.analog[0].read() > 0.6:
			# 		c = Color(rgb=(0.0, 0.0, 0.0))


			# Insert the next color into one end of the strip (and
			# pop the oldest color from the other end).
			# sendingColorBuffer.insertAndPop(c)
			"""
			insertAndPop, see Buffer.py
			Insert the given Color into the beginning (index 0) of the color
			list, and pop a Color from the end (maintaining size).
			"""

			# Send the updated colors to the Arduino.
			# sendingColorBuffer4.send(data_receiver_color_key="COLOR4")
			# sendingColorBuffer3.send(data_receiver_color_key="COLOR3")
			# sendingColorBuffer2.send(data_receiver_color_key="COLOR2")
			# sendingColorBuffer1.send(data_receiver_color_key="COLOR1")
			# sendingColorBuffer.send(data_receiver_color_key="COLORS")
			sys.stdout.write('.')
			sys.stdout.flush()

			sender.readAndPrint()

			dt += time.time() - t

	print 'Elapsed per %d updates: %.2fs' % (TRIALS, dt)
	print 'Updates per second: %.2f' % (TRIALS / dt)

