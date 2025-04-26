import os
import time
import pigpio

print("GPIO Reset Script")

# Kill any running pigpio daemon
print("Stopping any running pigpio daemon...")
os.system("sudo killall pigpiod 2>/dev/null || true")
time.sleep(1)

# Start pigpio daemon
print("Starting pigpio daemon...")
os.system("sudo pigpiod")
time.sleep(1)

# Connect to pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit(1)

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

# Stop pigpio daemon
print("\nStopping pigpio daemon again...")
os.system("sudo killall pigpiod")
time.sleep(1)

print("\nGPIO reset complete")
print("You can now restart the motor-control service with:")
print("sudo systemctl restart motor-control.service")