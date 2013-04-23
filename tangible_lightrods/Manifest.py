# Set up paths to include the ledcontroller Python library.
import os, sys

ledControllerLibPath = os.path.abspath(
	os.path.join(os.path.dirname(__file__), '..', 'libraries', 'ledcontroller', 'python'))
sys.path.append(ledControllerLibPath)

import ledcontroller

