import RPi.GPIO as GPIO
import time
import zmq


PAN_PIN = 32
TILT_PIN = 36
STEERING_PIN = 40

in1 = 31
in2 = 33
in3 = 35
in4 = 37


GPIO.setmode(GPIO.BOARD)
GPIO.setup(PAN_PIN, GPIO.OUT)
GPIO.setup(TILT_PIN, GPIO.OUT)
GPIO.setup(STEERING_PIN, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

steering = GPIO.PWM(STEERING_PIN, 50)
steering.start(0)

pan = GPIO.PWM(PAN_PIN, 50)
pan.start(0)

tilt = GPIO.PWM(TILT_PIN, 50)
tilt.start(0)

# listen on TCP port 5555 for incoming zmq PUSH messages

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")

try:
  while True:
    #Ask user for angle and turn servo to it
    try:
      keyboard_state = socket.recv_pyobj()
      
      # handle wasd for forward and back
      if keyboard_state["w"]:
        GPIO.output(in1, True)
        GPIO.output(in2, False)
        GPIO.output(in3, True)
        GPIO.output(in4, False)
      elif keyboard_state["s"]:
        GPIO.output(in1, False)
        GPIO.output(in2, True)
        GPIO.output(in3, False)
        GPIO.output(in4, True)
      else:
        GPIO.output(in1, False)
        GPIO.output(in2, False)
        GPIO.output(in3, False)
        GPIO.output(in4, False)

      # handle wasd for left and right
      if keyboard_state["a"]:
        STEERING_LEFT_ANGLE = 50
        steering.ChangeDutyCycle(2+(STEERING_LEFT_ANGLE/18))
      elif keyboard_state["d"]:
        STEERING_RIGHT_ANGLE = 110
        steering.ChangeDutyCycle(2+(STEERING_RIGHT_ANGLE/18))
      else:
        STEERING_CENTER_ANGLE = 80
        steering.ChangeDutyCycle(2+(STEERING_CENTER_ANGLE/18))

      # handle pan by checking "Left" and "Right" keys
      if keyboard_state["Left"]:
        PAN_LEFT_ANGLE = 45
        pan.ChangeDutyCycle(2+(PAN_LEFT_ANGLE/18))
      elif keyboard_state["Right"]:
        PAN_RIGHT_ANGLE = 135
        pan.ChangeDutyCycle(2+(PAN_RIGHT_ANGLE/18))
      else:
        PAN_CENTER_ANGLE = 90
        pan.ChangeDutyCycle(2+(PAN_CENTER_ANGLE/18))

      # handle tilt by checking "Up" and "Down" keys
      if keyboard_state["Up"]:
        TILT_UP_ANGLE = 45
        tilt.ChangeDutyCycle(2+(TILT_UP_ANGLE/18))
      elif keyboard_state["Down"]:
        TILT_DOWN_ANGLE = 135
        tilt.ChangeDutyCycle(2+(TILT_DOWN_ANGLE/18))
      else:
        TILT_CENTER_ANGLE = 90
        tilt.ChangeDutyCycle(2+(TILT_CENTER_ANGLE/18))

    except zmq.ZMQError:
      print("WTF???")
      continue

finally:
  #Clean things up at the end
  steering.stop()
  pan.stop()
  tilt.stop()
  GPIO.output(in1, False)
  GPIO.output(in2, False)
  GPIO.output(in3, False)
  GPIO.output(in4, False)
  GPIO.cleanup()
  print("Goodbye!")

