# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
ledRedPin = 18 # Broadcom pin 23 (P1 pin 16)
ledBluePin = 25 # Broadcom pin 23 (P1 pin 16)
ledGreenPin = 12 # Broadcom pin 23 (P1 pin 16)
butPin = 17 # Broadcom pin 17 (P1 pin 11)
speakerPin = 6

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledRedPin, GPIO.OUT) # LED pin set as output
GPIO.setup(ledBluePin, GPIO.OUT) # LED pin set as output
GPIO.setup(ledGreenPin, GPIO.OUT) # LED pin set as output
GPIO.setup(speakerPin, GPIO.OUT) 
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

def resetLEDs():
  # Initial state for LEDs:
  GPIO.output(ledRedPin, GPIO.LOW)
  GPIO.output(ledBluePin, GPIO.LOW)
  GPIO.output(ledGreenPin, GPIO.LOW)

resetLEDs()
print("Here we go! Press CTRL+C to exit")
try:
    start = 0
    while 1:
        if not GPIO.input(butPin): # button is pressed
          if start != 0:
            print("resetting")
            resetLEDs()
            start = 0
            time.sleep(0.5)
            continue
          print("starting")
          start = time.time()
          p = GPIO.PWM(speakerPin, 250)   
          p.start(50)       
          time.sleep(0.5)
          p.stop()
          lastColor = ledRedPin
        elif start > 0:
          elapsed = time.time() - start
          if elapsed < 120:
            color = ledGreenPin
          elif elapsed < 240:
            color = ledBluePin
          else:
            color = ledRedPin
          if lastColor != color:
            GPIO.output(ledRedPin, GPIO.LOW)
            GPIO.output(ledBluePin, GPIO.LOW)
            GPIO.output(ledGreenPin, GPIO.LOW)
            print("Color: "+str(color))
            GPIO.output(color, GPIO.HIGH)
            lastColor = color
          if elapsed > 300:
            print("DONE!")
            p = GPIO.PWM(speakerPin, 50)   
            p.start(50)       
            GPIO.output(ledRedPin, GPIO.HIGH)
            GPIO.output(ledBluePin, GPIO.HIGH)
            GPIO.output(ledGreenPin, GPIO.HIGH)
            time.sleep(2)
            start=-1
            p.stop()
            
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
