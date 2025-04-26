#!/bin/bash

echo "GPIO Test Script (Bash version)"

# Define the pins
PIN1=17
PIN2=27

# Function to set pin value
set_pin() {
    local pin=$1
    local value=$2
    
    # Export pin if not already exported
    echo $pin | sudo tee /sys/class/gpio/export 2>/dev/null || true
    sleep 0.1
    
    # Set direction to out
    echo out | sudo tee /sys/class/gpio/gpio$pin/direction 2>/dev/null || true
    sleep 0.1
    
    # Set value
    echo $value | sudo tee /sys/class/gpio/gpio$pin/value
    
    # Show result
    echo "Pin $pin set to $value"
}

# Function to read pin value
read_pin() {
    local pin=$1
    
    # Export pin if not already
    echo $pin | sudo tee /sys/class/gpio/export 2>/dev/null || true
    sleep 0.1
    
    # Read value
    value=$(cat /sys/class/gpio/gpio$pin/value 2>/dev/null || echo "error")
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
read_pin $PIN1
read_pin $PIN2
sleep 2

# Test 2: Pin 1 LOW (active), Pin 2 HIGH (inactive)
echo ""
echo "Test 2: Pin $PIN1 LOW (active), Pin $PIN2 HIGH (inactive)"
set_pin $PIN1 0
set_pin $PIN2 1
read_pin $PIN1
read_pin $PIN2
sleep 2

# Test 3: Pin 1 HIGH (inactive), Pin 2 LOW (active)
echo ""
echo "Test 3: Pin $PIN1 HIGH (inactive), Pin $PIN2 LOW (active)"
set_pin $PIN1 1
set_pin $PIN2 0
read_pin $PIN1
read_pin $PIN2
sleep 2

# Test 4: Both pins HIGH (inactive) again
echo ""
echo "Test 4: Both pins HIGH (inactive) again"
set_pin $PIN1 1
set_pin $PIN2 1
read_pin $PIN1
read_pin $PIN2

# Clean up
echo ""
echo "Cleaning up..."
set_pin $PIN1 1
set_pin $PIN2 1
echo $PIN1 | sudo tee /sys/class/gpio/unexport
echo $PIN2 | sudo tee /sys/class/gpio/unexport

echo ""
echo "Test complete!"