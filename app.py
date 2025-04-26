from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import logging
import time

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# GPIO setup
MOTOR1_FORWARD_PIN = 17
MOTOR1_REVERSE_PIN = 27

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up pins as outputs and initialize to HIGH (inactive for active-low logic)
GPIO.setup(MOTOR1_FORWARD_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(MOTOR1_REVERSE_PIN, GPIO.OUT, initial=GPIO.HIGH)
logger.info("GPIO pins initialized successfully with active-low logic")

@app.route('/')
def index():
    client_ip = request.remote_addr
    logger.info(f"Web interface accessed from {client_ip}")
    return render_template('index.html')

@app.route('/forward')
def forward():
    client_ip = request.remote_addr
    logger.info(f"FORWARD button clicked from {client_ip}")

    # Log initial pin states
    forward_state = GPIO.input(MOTOR1_FORWARD_PIN)
    reverse_state = GPIO.input(MOTOR1_REVERSE_PIN)
    logger.debug(f"Initial pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    # Safety: Make sure reverse is inactive first (HIGH for active-low logic)
    logger.debug("Setting reverse pin to INACTIVE (HIGH)")
    GPIO.output(MOTOR1_REVERSE_PIN, GPIO.HIGH)
    time.sleep(0.1)  # Small delay for safety

    # Set forward pin active (LOW for active-low logic)
    logger.debug("Setting forward pin to ACTIVE (LOW)")
    GPIO.output(MOTOR1_FORWARD_PIN, GPIO.LOW)

    # Log final pin states
    forward_state = GPIO.input(MOTOR1_FORWARD_PIN)
    reverse_state = GPIO.input(MOTOR1_REVERSE_PIN)
    logger.debug(f"Final pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    return "Moving forward"

@app.route('/reverse')
def reverse():
    client_ip = request.remote_addr
    logger.info(f"REVERSE button clicked from {client_ip}")

    # Log initial pin states
    forward_state = GPIO.input(MOTOR1_FORWARD_PIN)
    reverse_state = GPIO.input(MOTOR1_REVERSE_PIN)
    logger.debug(f"Initial pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    # Safety: Make sure forward is inactive first (HIGH for active-low logic)
    logger.debug("Setting forward pin to INACTIVE (HIGH)")
    GPIO.output(MOTOR1_FORWARD_PIN, GPIO.HIGH)
    time.sleep(0.1)  # Small delay for safety

    # Set reverse pin active (LOW for active-low logic)
    logger.debug("Setting reverse pin to ACTIVE (LOW)")
    GPIO.output(MOTOR1_REVERSE_PIN, GPIO.LOW)

    # Log final pin states
    forward_state = GPIO.input(MOTOR1_FORWARD_PIN)
    reverse_state = GPIO.input(MOTOR1_REVERSE_PIN)
    logger.debug(f"Final pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    return "Moving reverse"

@app.route('/stop')
def stop():
    client_ip = request.remote_addr
    logger.info(f"STOP button clicked from {client_ip}")

    # Log initial pin states
    forward_state = GPIO.input(MOTOR1_FORWARD_PIN)
    reverse_state = GPIO.input(MOTOR1_REVERSE_PIN)
    logger.debug(f"Initial pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    # Turn off both pins (HIGH for active-low logic)
    logger.debug("Setting both pins to INACTIVE (HIGH)")
    GPIO.output(MOTOR1_FORWARD_PIN, GPIO.HIGH)
    GPIO.output(MOTOR1_REVERSE_PIN, GPIO.HIGH)

    # Log final pin states
    forward_state = GPIO.input(MOTOR1_FORWARD_PIN)
    reverse_state = GPIO.input(MOTOR1_REVERSE_PIN)
    logger.debug(f"Final pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    return "Stopped"

@app.route('/status')
def status():
    # Get current pin states
    forward_state = GPIO.input(MOTOR1_FORWARD_PIN)
    reverse_state = GPIO.input(MOTOR1_REVERSE_PIN)

    logger.debug(f"Status check - Forward pin: {forward_state}, Reverse pin: {reverse_state}")

    # Determine motor status (for active-low logic)
    if forward_state == 0 and reverse_state == 1:
        status = "Moving forward"
    elif forward_state == 1 and reverse_state == 0:
        status = "Moving reverse"
    elif forward_state == 1 and reverse_state == 1:
        status = "Stopped"
    else:
        status = "Error: Both pins active!"
        logger.error("ERROR: Both pins are active simultaneously - forcing both inactive")
        # Safety: Set both pins inactive
        GPIO.output(MOTOR1_FORWARD_PIN, GPIO.HIGH)
        GPIO.output(MOTOR1_REVERSE_PIN, GPIO.HIGH)

    return status

@app.route('/debug')
def debug_info():
    # A debug endpoint to get detailed information
    forward_state = GPIO.input(MOTOR1_FORWARD_PIN)
    reverse_state = GPIO.input(MOTOR1_REVERSE_PIN)

    debug_info = {
        "forward_pin": MOTOR1_FORWARD_PIN,
        "reverse_pin": MOTOR1_REVERSE_PIN,
        "forward_state": "LOW (active)" if forward_state == 0 else "HIGH (inactive)",
        "reverse_state": "LOW (active)" if reverse_state == 0 else "HIGH (inactive)",
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    return str(debug_info)

if __name__ == '__main__':
    logger.info("Motor control server starting up")
    logger.info(f"Forward pin: GPIO{MOTOR1_FORWARD_PIN}, Reverse pin: GPIO{MOTOR1_REVERSE_PIN}")
    logger.info("Using active-LOW logic for relay control")

    try:
        # Try to toggle pins once on startup to verify they're working
        logger.debug("Testing pins on startup...")
        # Test forward
        GPIO.output(MOTOR1_FORWARD_PIN, GPIO.LOW)  # Active
        time.sleep(0.2)
        GPIO.output(MOTOR1_FORWARD_PIN, GPIO.HIGH)  # Inactive
        # Test reverse
        GPIO.output(MOTOR1_REVERSE_PIN, GPIO.LOW)  # Active
        time.sleep(0.2)
        GPIO.output(MOTOR1_REVERSE_PIN, GPIO.HIGH)  # Inactive
        logger.debug("Pin test completed")

        # Start the flask app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        logger.info("Server shutting down")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Ensure pins are set to inactive
        GPIO.output(MOTOR1_FORWARD_PIN, GPIO.HIGH)
        GPIO.output(MOTOR1_REVERSE_PIN, GPIO.HIGH)
        GPIO.cleanup()
        logger.info("GPIO pins set to inactive (HIGH) and cleaned up")