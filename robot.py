import RPi.GPIO as GPIO
import time



TILT_PIN = 36
PAN_PIN = 32
STEERING_PIN = 40

test_pin = PAN_PIN


GPIO.setmode(GPIO.BOARD)
GPIO.setup(test_pin, GPIO.OUT)

steering_angle_limit = 30 # 30 degrees left or right
steering_trim = 90 # set this number so that the car goes straight

steering = GPIO.PWM(test_pin, 50)
steering.start(0)



try:
  while True:
    #Ask user for angle and turn servo to it
    angle = float(input('Enter angle between 0 & 180: '))
    steering.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    steering.ChangeDutyCycle(0)

finally:
  #Clean things up at the end
  steering.stop()
  GPIO.cleanup()
  print("Goodbye!")

