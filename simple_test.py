import pigpio
import time
import os

print("Simple GPIO Test Script using pigpio")

# Make sure pigpio daemon is running
os.system("sudo killall pigpiod 2>/dev/null || true")
time.sleep(1)
os.system("sudo pigpiod")
time.sleep(1)

# Create pi instance
pi = pigpio.pi()

if not pi.connected:
    print("Could not connect to pigpio daemon. Is it running?")
    exit(1)

print("Connected to pigpio daemon")

# We'll test with the same pins used in the application
pin1 = 17
pin2 = 27

# Set up pins
pi.set_mode(pin1, pigpio.OUTPUT)
pi.set_mode(pin2, pigpio.OUTPUT)

# Initial state - set both pins HIGH (inactive for relays)
pi.write(pin1, 1)
pi.write(pin2, 1)
print(f"Pin {pin1} current state: {pi.read(pin1)}")
print(f"Pin {pin2} current state: {pi.read(pin2)}")

try:
    while True:
        # Test options
        print("\nOptions:")
        print(f"1: Set pin {pin1} HIGH (inactive)")
        print(f"2: Set pin {pin1} LOW (active)")
        print(f"3: Set pin {pin2} HIGH (inactive)")
        print(f"4: Set pin {pin2} LOW (active)")
        print("5: Set BOTH HIGH (inactive)")
        print("6: Test automatic sequence")
        print("q: Quit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            pi.write(pin1, 1)
            print(f"Pin {pin1} is HIGH (inactive)")
        elif choice == '2':
            pi.write(pin1, 0)
            print(f"Pin {pin1} is LOW (active)")
        elif choice == '3':
            pi.write(pin2, 1)
            print(f"Pin {pin2} is HIGH (inactive)")
        elif choice == '4':
            pi.write(pin2, 0)
            print(f"Pin {pin2} is LOW (active)")
        elif choice == '5':
            pi.write(pin1, 1)
            pi.write(pin2, 1)
            print("Both pins are HIGH (inactive)")
        elif choice == '6':
            print("\nRunning automatic test sequence...")
            # Both HIGH (inactive)
            pi.write(pin1, 1)
            pi.write(pin2, 1)
            print("Both pins HIGH (inactive)")
            time.sleep(2)
            
            # Pin 1 LOW (active), Pin 2 HIGH (inactive)
            pi.write(pin1, 0)
            pi.write(pin2, 1)
            print(f"Pin {pin1} LOW (active), Pin {pin2} HIGH (inactive)")
            time.sleep(2)
            
            # Pin 1 HIGH (inactive), Pin 2 LOW (active)
            pi.write(pin1, 1)
            pi.write(pin2, 0)
            print(f"Pin {pin1} HIGH (inactive), Pin {pin2} LOW (active)")
            time.sleep(2)
            
            # Both HIGH (inactive) again
            pi.write(pin1, 1)
            pi.write(pin2, 1)
            print("Both pins HIGH (inactive) again")
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice")
        
        # Display current state after each action
        print(f"Current states - Pin {pin1}: {pi.read(pin1)}, Pin {pin2}: {pi.read(pin2)}")
            
except KeyboardInterrupt:
    print("\nTest interrupted")
finally:
    # Set both pins to HIGH (inactive) before exiting
    pi.write(pin1, 1)
    pi.write(pin2, 1)
    pi.stop()
    print("\nPins set to HIGH (inactive) and resources released")
