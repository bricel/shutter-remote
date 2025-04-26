#!/bin/bash

echo "GPIO Reset Script (Bash version with pigpio utility)"

# Kill any running pigpio daemon
echo "Stopping any running pigpio daemon..."
sudo killall pigpiod 2>/dev/null || true
sleep 1

# Clean permissions
echo "Resetting GPIO permissions..."
sudo chmod -R a+rw /dev/gpiomem 2>/dev/null || true

# Start pigpio daemon fresh
echo "Starting pigpio daemon..."
sudo pigpiod
sleep 1

# Use pigs (pigpio utility) to reset pins
echo "Resetting pins with pigpio utility..."
# Configure pins as outputs
sudo pigs m 17 w  # Set pin 17 as output
sudo pigs m 27 w  # Set pin 27 as output

# Set pins to HIGH (inactive for relays)
sudo pigs w 17 1  # Set pin 17 HIGH
sudo pigs w 27 1  # Set pin 27 HIGH

# Read back values to verify
PIN17=$(sudo pigs r 17)
PIN27=$(sudo pigs r 27)
echo "Pin 17 value: $PIN17"
echo "Pin 27 value: $PIN27"

# Stop pigpio daemon
echo "Stopping pigpio daemon..."
sudo killall pigpiod
sleep 1

echo ""
echo "GPIO reset complete"
echo "You can now restart the motor-control service with:"
echo "sudo systemctl restart motor-control.service"