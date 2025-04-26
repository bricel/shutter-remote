import RPi.GPIO as GPIO
import time
import os
import pigpio  # Add pigpio to directly control the pins too

# Try to kill any running pigpio daemon
print("Stopping any running pigpio daemon...")
os.system("sudo killall pigpiod 2>/dev/null || true")
time.sleep(1)

# Clean up any previous configuration
try:
    GPIO.cleanup()
    print("GPIO cleaned up")
except Exception as e:
    print(f"Cleanup error (can be ignored): {e}")

# We'll use both RPi.GPIO and pigpio to make sure the pins are released

# 1. First use RPi.GPIO with BOARD mode
print("\n--- Using RPi.GPIO with BOARD mode ---")
GPIO.setmode(GPIO.BOARD)

# Convert BCM pins 17, 27 to BOARD pins 11, 13
board_pins = {
    17: 11,  # BCM 17 = BOARD 11
    27: 13   # BCM 27 = BOARD 13
}

# Map for better output
bcm_to_board = {
    11: 17,  # BOARD 11 = BCM 17
    13: 27   # BOARD 13 = BCM 27
}

# Configure pins as outputs and set to HIGH (inactive for relays)
for board_pin in board_pins.values():
    try:
        GPIO.setup(board_pin, GPIO.OUT, initial=GPIO.HIGH)
        print(f"BOARD pin {board_pin} (BCM {bcm_to_board[board_pin]}) set to HIGH (inactive)")
    except Exception as e:
        print(f"Error setting up BOARD pin {board_pin}: {e}")

time.sleep(1)

# Clean up to release pins
GPIO.cleanup()
print("RPi.GPIO pins cleaned up")

# 2. Now use pigpio directly
print("\n--- Using pigpio directly ---")

# Start pigpio daemon
print("Starting pigpio daemon...")
os.system("sudo pigpiod")
time.sleep(1)

# Connect to pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
else:
    print("Connected to pigpio daemon")
    
    # BCM pin numbers
    bcm_pins = [17, 27]
    
    # Initialize pins as outputs and set to HIGH (inactive for relays)
    for pin in bcm_pins:
        try:
            pi.set_mode(pin, pigpio.OUTPUT)
            pi.write(pin, 1)  # Set to HIGH (inactive)
            print(f"BCM pin {pin} set to HIGH (inactive)")
        except Exception as e:
            print(f"Error setting up BCM pin {pin}: {e}")
    
    # Verify pin states
    print("\nVerifying pin states:")
    for pin in bcm_pins:
        try:
            state = pi.read(pin)
            print(f"BCM pin {pin} state: {'HIGH' if state else 'LOW'}")
        except Exception as e:
            print(f"Error reading BCM pin {pin}: {e}")
    
    # Stop pigpio to release resources
    pi.stop()
    print("pigpio resources released")

# Stop pigpio daemon again
print("\nStopping pigpio daemon...")
os.system("sudo killall pigpiod")
time.sleep(1)

print("\nGPIO reset complete")
print("You can now restart the motor-control service with:")
print("sudo systemctl restart motor-control.service")
