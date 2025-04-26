#!/bin/bash

echo "GPIO Test Script (pigpio utility version)"

# Define the pins
PIN1=17
PIN2=27

# Make sure pigpio daemon is running
echo "Starting pigpio daemon..."
sudo killall pigpiod 2>/dev/null || true
sleep 1
sudo pigpiod
sleep 1

# Function to set pin value
set_pin() {
    local pin=$1
    local value=$2
    
    # Configure as output and set value
    sudo pigs m $pin w  # Set as output
    sudo pigs w $pin $value  # Write value
    
    # Read back to verify
    local current=$(sudo pigs r $pin)
    echo "Pin $pin set to $value, current value: $current"
}

# Function to read pin value
read_pin() {
    local pin=$1
    local value=$(sudo pigs r $pin)
    echo "Pin $pin current value: $value"
}

# Initial setup - set both pins to 1 (HIGH/inactive)
echo "Setting up pins..."
set_pin $PIN1 1
set_pin $PIN2 1

echo ""
echo "Running test sequence..."

# Test 1: Both pins HIGH (inactive)
echo ""
echo "Test 1: Both pins HIGH (inactive)"
set_pin $PIN1 1
set_pin $PIN2 1
sleep 2

# Test 2: Pin 1 LOW (active), Pin 2 HIGH (inactive)
echo ""
echo "Test 2: Pin $PIN1 LOW (active), Pin $PIN2 HIGH (inactive)"
set_pin $PIN1 0
set_pin $PIN2 1
sleep 2

# Test 3: Pin 1 HIGH (inactive), Pin 2 LOW (active)
echo ""
echo "Test 3: Pin $PIN1 HIGH (inactive), Pin $PIN2 LOW (active)"
set_pin $PIN1 1
set_pin $PIN2 0
sleep 2

# Test 4: Both pins HIGH (inactive) again
echo ""
echo "Test 4: Both pins HIGH (inactive) again"
set_pin $PIN1 1
set_pin $PIN2 1

# Clean up
echo ""
echo "Cleaning up..."
set_pin $PIN1 1
set_pin $PIN2 1

# Stop pigpio daemon
echo "Stopping pigpio daemon..."
sudo killall pigpiod
sleep 1

echo ""
echo "Test complete!
You can now restart the motor-control service with:
sudo systemctl restart motor-control.service"