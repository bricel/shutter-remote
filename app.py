from flask import Flask, render_template
from gpiozero import OutputDevice
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# GPIO setup
MOTOR1_FORWARD_PIN = 17
MOTOR1_REVERSE_PIN = 27

# Create output devices
forward_relay = OutputDevice(MOTOR1_FORWARD_PIN, active_high=True, initial_value=False)
reverse_relay = OutputDevice(MOTOR1_REVERSE_PIN, active_high=True, initial_value=False)
logger.info("GPIO pins initialized successfully")

@app.route('/')
def index():
    logger.info("Web interface accessed")
    return render_template('index.html')

@app.route('/forward')
def forward():
    logger.info("FORWARD button clicked - Setting motor to forward")
    # Safety: Turn off reverse first
    reverse_relay.off()
    # Set forward pin active
    forward_relay.on()
    return "Moving forward"

@app.route('/reverse')
def reverse():
    logger.info("REVERSE button clicked - Setting motor to reverse")
    # Safety: Turn off forward first
    forward_relay.off()
    # Set reverse pin active
    reverse_relay.on()
    return "Moving reverse"

@app.route('/stop')
def stop():
    logger.info("STOP button clicked - Stopping motor")
    # Turn off both pins
    forward_relay.off()
    reverse_relay.off()
    return "Stopped"

@app.route('/status')
def status():
    # Get current pin states
    forward_state = forward_relay.value
    reverse_state = reverse_relay.value
    
    # Determine motor status
    if forward_state and not reverse_state:
        status = "Moving forward"
    elif reverse_state and not forward_state:
        status = "Moving reverse"
    elif not forward_state and not reverse_state:
        status = "Stopped"
    else:
        status = "Error: Both pins active!"
        # Safety: Turn off both pins if both are somehow active
        forward_relay.off()
        reverse_relay.off()
    
    return status

if __name__ == '__main__':
    logger.info("Motor control server starting up")
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        logger.info("Server shutting down")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Ensure pins are turned off
        forward_relay.off()
        reverse_relay.off()
        logger.info("GPIO pins set to LOW")
