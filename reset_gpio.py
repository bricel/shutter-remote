import RPi.GPIO as GPIO
import time

# Clean up any previous configuration
GPIO.cleanup()

# Set mode and configure pins with pull-down resistors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

print("GPIO pins 17 and 27 have been reset to LOW state")
print("Waiting 5 seconds to verify...")
time.sleep(5)

# Verify pins are still LOW
print("GPIO 17 state:", "HIGH" if GPIO.input(17) else "LOW")
print("GPIO 27 state:", "HIGH" if GPIO.input(27) else "LOW")

GPIO.cleanup()
print("GPIO cleaned up")
