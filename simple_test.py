#!/usr/bin/env python3
import os
import time

print("Simple GPIO Test Script (System Command version)")

# Define the pins we're working with
bcm_pins = [17, 27]

# Function to write to a GPIO pin
def set_pin(pin, value):
    # First export the pin if not already
    os.system(f"echo {pin} | sudo tee /sys/class/gpio/export 2>/dev/null || true")
    time.sleep(0.1)
    
    # Set direction to out
    os.system(f"echo out | sudo tee /sys/class/gpio/gpio{pin}/direction 2>/dev/null || true")
    time.sleep(0.1)
    
    # Set the value
    os.system(f"echo {value} | sudo tee /sys/class/gpio/gpio{pin}/value 2>/dev/null || true")
    
    # Read back the value to verify
    return get_pin_value(pin)

# Function to read a GPIO pin
def get_pin_value(pin):
    # Make sure the pin is exported
    os.system(f"echo {pin} | sudo tee /sys/class/gpio/export 2>/dev/null || true")
    time.sleep(0.1)
    
    # Try to read the value
    try:
        return os.popen(f"cat /sys/class/gpio/gpio{pin}/value").read().strip()
    except:
        return "error"

# Setup pins
print("Setting up pins...")
for pin in bcm_pins:
    set_pin(pin, 1)  # Start with pins HIGH (inactive)

# Display initial states
print(f"Pin {bcm_pins[0]} initial state: {get_pin_value(bcm_pins[0])}")
print(f"Pin {bcm_pins[1]} initial state: {get_pin_value(bcm_pins[1])}")

try:
    print("\nRunning automatic test sequence...")
    
    # Both pins HIGH (inactive)
    print("Setting both pins HIGH (inactive)")
    set_pin(bcm_pins[0], 1)
    set_pin(bcm_pins[1], 1)
    print(f"Pin {bcm_pins[0]} state: {get_pin_value(bcm_pins[0])}")
    print(f"Pin {bcm_pins[1]} state: {get_pin_value(bcm_pins[1])}")
    time.sleep(2)
    
    # First pin LOW (active), second HIGH
    print(f"Setting pin {bcm_pins[0]} LOW (active), pin {bcm_pins[1]} HIGH (inactive)")
    set_pin(bcm_pins[0], 0)
    set_pin(bcm_pins[1], 1)
    print(f"Pin {bcm_pins[0]} state: {get_pin_value(bcm_pins[0])}")
    print(f"Pin {bcm_pins[1]} state: {get_pin_value(bcm_pins[1])}")
    time.sleep(2)
    
    # First pin HIGH, second LOW (active)
    print(f"Setting pin {bcm_pins[0]} HIGH (inactive), pin {bcm_pins[1]} LOW (active)")
    set_pin(bcm_pins[0], 1)
    set_pin(bcm_pins[1], 0)
    print(f"Pin {bcm_pins[0]} state: {get_pin_value(bcm_pins[0])}")
    print(f"Pin {bcm_pins[1]} state: {get_pin_value(bcm_pins[1])}")
    time.sleep(2)
    
    # Both pins HIGH (inactive) again
    print("Setting both pins HIGH (inactive) again")
    set_pin(bcm_pins[0], 1)
    set_pin(bcm_pins[1], 1)
    print(f"Pin {bcm_pins[0]} state: {get_pin_value(bcm_pins[0])}")
    print(f"Pin {bcm_pins[1]} state: {get_pin_value(bcm_pins[1])}")
    
    print("\nTest sequence complete!")
    
except KeyboardInterrupt:
    print("\nTest interrupted")
    
finally:
    # Clean up - set pins HIGH and unexport
    print("\nCleaning up...")
    for pin in bcm_pins:
        set_pin(pin, 1)  # Set HIGH (inactive)
        time.sleep(0.1)
        os.system(f"echo {pin} | sudo tee /sys/class/gpio/unexport 2>/dev/null || true")
    
    print("GPIO pins set to inactive and unexported")