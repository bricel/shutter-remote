#!/bin/bash

echo "GPIO Reset Script (Active-LOW logic for relays)"

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
echo "Resetting pins with pigpio utility (active-LOW logic)..."
# Configure pins as outputs
sudo pigs m 17 w  # Set pin 17 as output
sudo pigs m 27 w  # Set pin 27 as output

# Set pins to HIGH (inactive for relay with active-LOW logic)
sudo pigs w 17 1  # Set pin 17 HIGH (inactive)
sudo pigs w 27 1  # Set pin 27 HIGH (inactive)

# Read back values to verify
PIN17=$(sudo pigs r 17)
PIN27=$(sudo pigs r 27)
echo "Pin 17 value: $PIN17 (HIGH=inactive for active-LOW logic)"
echo "Pin 27 value: $PIN27 (HIGH=inactive for active-LOW logic)"

# For clarity, let's explain what these values mean
echo ""
echo "With active-LOW logic:"
echo "  HIGH (1) = Relay INACTIVE (default/safe state)"
echo "  LOW (0) = Relay ACTIVE"
echo ""
echo "Default state is now set to INACTIVE (HIGH)"

# Stop pigpio daemon
echo "Stopping pigpio daemon..."
sudo killall pigpiod
sleep 1

echo ""
echo "GPIO reset complete with INACTIVE (HIGH) state"
echo "You can now restart the motor-control service with:"
echo "sudo systemctl restart motor-control.service"