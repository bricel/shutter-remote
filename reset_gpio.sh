#!/bin/bash

echo "GPIO Reset Script (Bash version)"

# Kill any running pigpio daemon
echo "Stopping any running pigpio daemon..."
sudo killall pigpiod 2>/dev/null || true
sleep 1

# Reset GPIO permissions
echo "Resetting GPIO permissions..."
sudo chmod -R a+rw /sys/class/gpio 2>/dev/null || true
sudo chmod -R a+rw /dev/gpiomem 2>/dev/null || true

# Unexport any exported pins
echo "Unexporting GPIO pins..."
echo 17 | sudo tee /sys/class/gpio/unexport 2>/dev/null || true
echo 27 | sudo tee /sys/class/gpio/unexport 2>/dev/null || true
sleep 1

echo ""
echo "GPIO reset complete"
echo "You can now restart the motor-control service with:"
echo "sudo systemctl restart motor-control.service"