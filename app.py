from flask import Flask, render_template, request
from gpiozero import OutputDevice
import logging
import time

# Set up more detailed logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# GPIO setup
MOTOR1_FORWARD_PIN = 17
MOTOR1_REVERSE_PIN = 27

# Create output devices with detailed logging
logger.debug(f"Setting up GPIO {MOTOR1_FORWARD_PIN} and {MOTOR1_REVERSE_PIN} as outputs")
forward_relay = OutputDevice(MOTOR1_FORWARD_PIN, active_high=True, initial_value=False)
reverse_relay = OutputDevice(MOTOR1_REVERSE_PIN, active_high=True, initial_value=False)
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
    logger.debug(f"Initial pin states - Forward: {forward_relay.value}, Reverse: {reverse_relay.value}")

    # Safety: Turn off reverse first
    logger.debug("Setting reverse pin to OFF")
    reverse_relay.off()
    time.sleep(0.1)  # Small delay for safety

    # Set forward pin active
    logger.debug("Setting forward pin to ON")
    forward_relay.on()

    # Log final pin states
    logger.debug(f"Final pin states - Forward: {forward_relay.value}, Reverse: {reverse_relay.value}")

    return "Moving forward"

@app.route('/reverse')
def reverse():
    client_ip = request.remote_addr
    logger.info(f"REVERSE button clicked from {client_ip}")

    # Log initial pin states
    logger.debug(f"Initial pin states - Forward: {forward_relay.value}, Reverse: {reverse_relay.value}")

    # Safety: Turn off forward first
    logger.debug("Setting forward pin to OFF")
    forward_relay.off()
    time.sleep(0.1)  # Small delay for safety

    # Set reverse pin active
    logger.debug("Setting reverse pin to ON")
    reverse_relay.on()

    # Log final pin states
    logger.debug(f"Final pin states - Forward: {forward_relay.value}, Reverse: {reverse_relay.value}")

    return "Moving reverse"

@app.route('/stop')
def stop():
    client_ip = request.remote_addr
    logger.info(f"STOP button clicked from {client_ip}")

    # Log initial pin states
    logger.debug(f"Initial pin states - Forward: {forward_relay.value}, Reverse: {reverse_relay.value}")

    # Turn off both pins
    logger.debug("Setting both pins to OFF")
    forward_relay.off()
    reverse_relay.off()

    # Log final pin states
    logger.debug(f"Final pin states - Forward: {forward_relay.value}, Reverse: {reverse_relay.value}")

    return "Stopped"

@app.route('/status')
def status():
    # Get current pin states
    forward_state = forward_relay.value
    reverse_state = reverse_relay.value

    logger.debug(f"Status check - Forward pin: {forward_state}, Reverse pin: {reverse_state}")

    # Determine motor status
    if forward_state and not reverse_state:
        status = "Moving forward"
    elif reverse_state and not forward_state:
        status = "Moving reverse"
    elif not forward_state and not reverse_state:
        status = "Stopped"
    else:
        status = "Error: Both pins active!"
        logger.error("ERROR: Both pins are active simultaneously - forcing both OFF")
        # Safety: Turn off both pins if both are somehow active
        forward_relay.off()
        reverse_relay.off()

    return status

@app.route('/debug')
def debug_info():
    # A new endpoint to get detailed debug information
    forward_state = forward_relay.value
    reverse_state = reverse_relay.value

    debug_info = {
        "forward_pin": MOTOR1_FORWARD_PIN,
        "reverse_pin": MOTOR1_REVERSE_PIN,
        "forward_state": "HIGH" if forward_state else "LOW",
        "reverse_state": "HIGH" if reverse_state else "LOW",
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    return str(debug_info)

if __name__ == '__main__':
    logger.info("Motor control server starting up")
    logger.info(f"Forward pin: GPIO{MOTOR1_FORWARD_PIN}, Reverse pin: GPIO{MOTOR1_REVERSE_PIN}")

    try:
        # Try to toggle pins once on startup to verify they're working
        logger.debug("Testing pins on startup...")
        forward_relay.on()
        time.sleep(0.2)
        forward_relay.off()
        reverse_relay.on()
        time.sleep(0.2)
        reverse_relay.off()
        logger.de