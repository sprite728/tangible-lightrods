"""
Demonstrate generating colors in Python and using DataSender to transfer them
over Serial to the Arduino. (Optionally simulate entirely in Python.)

Use abstracting classes to manage lists of Patterns, and writing.
"""

# Configuration options. See the low-level demo for details.
DUMMY_SERIAL = True
DRAW = True
SERIAL_DEVICE = '/dev/tty.usbmodemfa141'

from Manifest import ledcontroller, sys

from ledcontroller.Manifest import time, DataSender
from ledcontroller.Manifest import SendingPatternList, Color, \
	TurtleBuffer, Sequences
from ledcontroller.patterns.Manifest import InterpolatedMarquee, Pulser

if __name__ == '__main__':
	# A SendingPatternList holds the list of Patterns (which create the
	# colors), and manages writing them to the Arduino.
	if not DRAW:
		# Create a SendingBuffer with defaults.
		sender = SendingPatternList()
	else:
		sender = SendingPatternList(sendingBuffer=TurtleBuffer())

	# Add some Patterns.
	#sender.append(InterpolatedMarquee(
	#	Sequences.GenerateRandom(brightInterval=6),
	#		speed=15))
	sender.append(InterpolatedMarquee(
		Sequences.GenerateHueGradient(repeatInterval=10)))
	sender.append(Pulser(color=Color(rgb=(0, 0, 1)), reverse=True))

	# Open the serial device (connection to the Arduino).
	if DUMMY_SERIAL:
		dataSender = DataSender.DummySender(SERIAL_DEVICE, silent=True)
	else:
		dataSender = DataSender.Sender(SERIAL_DEVICE)

	with dataSender:
		sender.setSender(dataSender)

		t = time.time()
		actualTrials = 0

		# Continue updating until all the Patterns expire.
		# If this does not happen, wait for control-C.
		print 'Type ^C (hold control, press c) to stop.'
		try:
			while True:
				sender.updateAndSend()
				sys.stdout.write('.')
				sys.stdout.flush()
				dataSender.readAndPrint()
				actualTrials += 1
		except KeyboardInterrupt:
			print 'Got ^C, exiting.'

		dt = time.time() - t

	print 'Elapsed per %d updates: %.2fs' % (actualTrials, dt)
	print 'Updates per second: %.2f' % (actualTrials / dt)

