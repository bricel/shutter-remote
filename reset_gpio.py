import RPi.GPIO as GPIO
import time
import os

# Try to kill any running pigpio daemon
os.system("sudo killall pigpiod 2>/dev/null || true")
time.sleep(1)

# Clean up any previous configuration
try:
    GPIO.cleanup()
except:
    pass

# Set mode to BCM (the same as used in the app.py)
GPIO.setmode(GPIO.BCM)

# GPIO pins we want to reset
pins = [17, 27]

# Configure pins as outputs and set to HIGH (inactive for relays)
for pin in pins:
    try:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
        print(f"GPIO {pin} set to HIGH (inactive)")
    except Exception as e:
        print(f"Error setting up GPIO {pin}: {e}")

print("Waiting 2 seconds...")
time.sleep(2)

# Verify pin states
for pin in pins:
    try:
        state = GPIO.input(pin)
        print(f"GPIO {pin} state: {'HIGH' if state else 'LOW'}")
    except Exception as e:
        print(f"Error reading GPIO {pin}: {e}")

# Clean up
GPIO.cleanup()
print("GPIO cleaned up")

print("You can now restart the motor-control service")
