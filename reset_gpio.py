#!/usr/bin/env python3
import os
import time

print("GPIO Reset Script (System Command version)")

# Kill any running pigpio daemon
print("Stopping any running pigpio daemon...")
os.system("sudo killall pigpiod 2>/dev/null || true")
time.sleep(1)

# Reset GPIO permissions
print("Resetting GPIO permissions...")
os.system("sudo chmod -R a+rw /sys/class/gpio 2>/dev/null || true")
os.system("sudo chmod -R a+rw /dev/gpiomem 2>/dev/null || true")

# Unexport any exported pins
print("Unexporting GPIO pins...")
os.system("echo 17 | sudo tee /sys/class/gpio/unexport 2>/dev/null || true")
os.system("echo 27 | sudo tee /sys/class/gpio/unexport 2>/dev/null || true")
time.sleep(1)

print("\nGPIO reset complete")
print("You can now restart the motor-control service with:")
print("sudo systemctl restart motor-control.service")