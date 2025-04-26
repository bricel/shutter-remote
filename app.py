from flask import Flask, render_template, request
import pigpio
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

# Initialize pigpio
pi = pigpio.pi()  # Connect to local Pi
if not pi.connected:
    logger.error("Failed to connect to pigpio daemon!")
else:
    logger.info("Connected to pigpio daemon successfully")

# Set up pins as outputs and initialize to LOW
pi.set_mode(MOTOR1_FORWARD_PIN, pigpio.OUTPUT)
pi.set_mode(MOTOR1_REVERSE_PIN, pigpio.OUTPUT)
pi.write(MOTOR1_FORWARD_PIN, 0)  # Set to LOW
pi.write(MOTOR1_REVERSE_PIN, 0)  # Set to LOW
logger.info("GPIO pins initialized successfully")

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
    forward_state = pi.read(MOTOR1_FORWARD_PIN)
    reverse_state = pi.read(MOTOR1_REVERSE_PIN)
    logger.debug(f"Initial pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    # Safety: Turn off reverse first
    logger.debug("Setting reverse pin to OFF")
    pi.write(MOTOR1_REVERSE_PIN, 0)
    time.sleep(0.1)  # Small delay for safety

    # Set forward pin active
    logger.debug("Setting forward pin to ON")
    pi.write(MOTOR1_FORWARD_PIN, 1)

    # Log final pin states
    forward_state = pi.read(MOTOR1_FORWARD_PIN)
    reverse_state = pi.read(MOTOR1_REVERSE_PIN)
    logger.debug(f"Final pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    return "Moving forward"

@app.route('/reverse')
def reverse():
    client_ip = request.remote_addr
    logger.info(f"REVERSE button clicked from {client_ip}")

    # Log initial pin states
    forward_state = pi.read(MOTOR1_FORWARD_PIN)
    reverse_state = pi.read(MOTOR1_REVERSE_PIN)
    logger.debug(f"Initial pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    # Safety: Turn off forward first
    logger.debug("Setting forward pin to OFF")
    pi.write(MOTOR1_FORWARD_PIN, 0)
    time.sleep(0.1)  # Small delay for safety

    # Set reverse pin active
    logger.debug("Setting reverse pin to ON")
    pi.write(MOTOR1_REVERSE_PIN, 1)

    # Log final pin states
    forward_state = pi.read(MOTOR1_FORWARD_PIN)
    reverse_state = pi.read(MOTOR1_REVERSE_PIN)
    logger.debug(f"Final pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    return "Moving reverse"

@app.route('/stop')
def stop():
    client_ip = request.remote_addr
    logger.info(f"STOP button clicked from {client_ip}")

    # Log initial pin states
    forward_state = pi.read(MOTOR1_FORWARD_PIN)
    reverse_state = pi.read(MOTOR1_REVERSE_PIN)
    logger.debug(f"Initial pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    # Turn off both pins
    logger.debug("Setting both pins to OFF")
    pi.write(MOTOR1_FORWARD_PIN, 0)
    pi.write(MOTOR1_REVERSE_PIN, 0)

    # Log final pin states
    forward_state = pi.read(MOTOR1_FORWARD_PIN)
    reverse_state = pi.read(MOTOR1_REVERSE_PIN)
    logger.debug(f"Final pin states - Forward: {forward_state}, Reverse: {reverse_state}")

    return "Stopped"

if __name__ == '__main__':
    logger.info("Motor control server starting up")
    logger.info(f"Forward pin: GPIO{MOTOR1_FORWARD_PIN}, Reverse pin: GPIO{MOTOR1_REVERSE_PIN}")

    try:
        # Try to toggle pins once on startup to verify they're working
        logger.debug("Testing pins on startup...")
        pi.write(MOTOR1_FORWARD_PIN, 1)
        time.sleep(0.2)
        pi.write(MOTOR1_FORWARD_PIN, 0)
        pi.write(MOTOR1_REVERSE_PIN, 1)
        time.sleep(0.2)
        pi.write(MOTOR1_REVERSE_PIN, 0)
        logger.debug("Pin test completed successfully")

        # Start the flask app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        logger.info("Server shutting down")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Ensure pins are turned off
        pi.write(MOTOR1_FORWARD_PIN, 0)
        pi.write(MOTOR1_REVERSE_PIN, 0)
        pi.stop()  # Release resources
        logger.info("GPIO pins set to LOW and resources released")