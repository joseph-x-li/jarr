import picamera
import numpy as np
import pystreaming as ps
import zmq

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 24
    output = np.empty((240, 320, 3), dtype=np.uint8)
    with ps.Streamer("tcp://*:5556") as stream:
      i = 0
      while True:
          print(f"SEND{i}")
          camera.capture(output, 'rgb')
          stream.send(output)
          i += 1