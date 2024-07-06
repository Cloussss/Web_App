from flask import Flask, render_template, jsonify, request
from datetime import datetime
import logging
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

waste_types = ['plastic', 'paper', 'cellophane']
waste_status = 'No waste detected'
warning_status = ''
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

motor_active = False  # Ensure motor_active is initialized

def detect_waste():
    global waste_status
    detected_waste = random.choice(waste_types)
    waste_status = f'{detected_waste.capitalize()} detected!' if random.choice([True, False]) else 'No waste detected'
    logger.info(f"Waste status updated: {waste_status}")

def detect_warnings():
    global warning_status
    if random.choice([True, False]):
        warning_status = 'Sensor malfunction detected!'
    elif random.choice([True, False]):
        warning_status = 'System is not detecting any waste!'
    else:
        warning_status = ''
    
    if warning_status:
        backup_log(warning_status)
    logger.warning(f"Warning status updated: {warning_status}")

def backup_log(message):
    log_entry = f"{datetime.now()} - {message}"
    with open("fix_log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")
    logger.info(f"Log entry added to fix_log.txt: {log_entry}")

@app.route('/')
def index():
    global motor_active
    detect_warnings()  # Check for warnings on page load
    return render_template('index.html', motor_active=motor_active, current_time=current_time)

@app.route('/update_waste_status')
def update_waste_status():
    detect_waste()
    detect_warnings()  # Check for warnings when updating waste status
    return jsonify(waste_status=waste_status, warning_status=warning_status)

@app.route('/activate_motor', methods=['POST'])
def activate_motor():
    global motor_active
    action = request.args.get('action')
    if action == 'on':
        motor_active = True
        logger.info("Motor activated")
    elif action == 'off':
        motor_active = False
        logger.info("Motor deactivated")
    return jsonify(motor_active=motor_active)

@app.route('/fix_log')
def fix_log():
    try:
        with open("fix_log.txt", "r") as log_file:
            logs = log_file.readlines()
    except FileNotFoundError:
        logs = ["No logs found."]
    return jsonify(fix_log=logs)

@app.route('/about_us')
def about_us():
    return jsonify(about_us="Created by Jessie Gil Christian Silva")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
