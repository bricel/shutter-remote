import RPi.GPIO as GPIO
import time
import os

# Set up GPIO
GPIO.setmode(GPIO.BCM)
pins_to_monitor = [17, 27]  # GPIO pins to monitor

# Set up pins as inputs to monitor their state
for pin in pins_to_monitor:
    # First clean up any previous configuration
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

try:
    print("Monitoring GPIO pins. Press CTRL+C to exit.")
    print("Pin states: HIGH = 1, LOW = 0")
    print("-" * 30)
    
    while True:
        os.system('clear')  # Clear the screen
        print("LIVE GPIO PIN STATUS:")
        print("-" * 30)
        
        for pin in pins_to_monitor:
            state = GPIO.input(pin)
            status = "HIGH" if state else "LOW"
            # Use colors for better visibility
            if state:
                # Red for HIGH
                print(f"GPIO {pin}: \033[91m{status}\033[0m (1)")
            else:
                # Green for LOW
                print(f"GPIO {pin}: \033[92m{status}\033[0m (0)")
        
        print("-" * 30)
        print("Press CTRL+C to exit")
        time.sleep(0.5)  # Update every half second

except KeyboardInterrupt:
    print("\nMonitoring stopped by user")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")

