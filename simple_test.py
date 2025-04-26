import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

# Make sure both pins are LOW (off)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
print("Both pins are now OFF")
time.sleep(2)

try:
    while True:
        # Test options
        print("\nOptions:")
        print("1: Turn GPIO 17 ON")
        print("2: Turn GPIO 17 OFF")
        print("3: Turn GPIO 27 ON")
        print("4: Turn GPIO 27 OFF")
        print("5: Turn BOTH OFF")
        print("q: Quit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            GPIO.output(17, GPIO.HIGH)
            print("GPIO 17 is ON")
        elif choice == '2':
            GPIO.output(17, GPIO.LOW)
            print("GPIO 17 is OFF")
        elif choice == '3':
            GPIO.output(27, GPIO.HIGH)
            print("GPIO 27 is ON")
        elif choice == '4':
            GPIO.output(27, GPIO.LOW)
            print("GPIO 27 is OFF")
        elif choice == '5':
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            print("Both pins are OFF")
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice")
            
except KeyboardInterrupt:
    pass
finally:
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.cleanup()
    print("\nGPIO cleaned up")
