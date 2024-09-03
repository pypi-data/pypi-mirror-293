
# -------------------------------------------------------------
# This is not production code but I am losing the will to live
# Provide the path to the module so that the tests can run
import os
import sys
import piexif
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# --------------------------------------------------------------

from picamzero import Camera
from time import sleep

cam = Camera()
cam.take_video_and_still("aye.jpg", duration=18, still_interval=2)
#cam.capture_sequence("whatever", num_images=10)
