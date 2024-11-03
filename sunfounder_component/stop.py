import RPi.GPIO as GPIO
import time

# GPIO control
pump_channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_channel, GPIO.OUT)

def start_motor(pin):
    try:
        # my pump+relay works with GPIO.LOW
        print(f'- start motor {pin}')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    except KeyboardInterrupt:
        print('exception')
        GPIO.cleanup()

def stop_motor():
    print('- stop motor')
    GPIO.cleanup()

#start_motor(pump_channel)
stop_motor()
