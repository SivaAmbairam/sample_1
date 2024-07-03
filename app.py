import signal
import time
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import threading
import subprocess
import os
import logging

app = Flask(__name__)

SCRIPTS_DIRECTORY = "/Users/g6-media/Webscrapping-Git/Webscrapping- Webpage/Scrapping Scripts"
stop_execution = False
script_status = {}
script_output = {}

logging.basicConfig(level=logging.DEBUG)

def stop_execution_handler(signum, frame):
    global stop_execution
    stop_execution = True

signal.signal(signal.SIGINT, stop_execution_handler)

def run_script(script_name):
    global stop_execution
    script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
    script_status[script_name] = 'Running'
    script_stopped = False
    try:
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        while True:
            if stop_execution:
                script_status[script_name] = 'Stopping'
                process.terminate()
                script_stopped = True
                break
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                logging.debug(f'Script {script_name} output: {output.strip()}')
                script_output[script_name] = script_output.get(script_name, '') + output
        rc = process.poll()
        if not script_stopped:
            script_status[script_name] = 'Completed'
        else:
            script_status[script_name] = 'Stopped'
    except Exception as e:
        script_status[script_name] = f'Error: {str(e)}'

@app.route('/')
def index():
    scripts = [f for f in os.listdir(SCRIPTS_DIRECTORY) if f.endswith('.py')]
    return render_template('index.html', scripts=scripts)

@app.route('/run_scripts', methods=['POST'])
def run_scripts():
    global stop_execution
    stop_execution = False
    selected_scripts = request.form.getlist('scripts')
    script_status.update({script: 'Queued' for script in selected_scripts})
    for script in selected_scripts:
        t = threading.Thread(target=run_script, args=(script,))
        t.start()
    return jsonify({'status': 'Scripts running'})

@app.route('/stop_scripts', methods=['POST'])
def stop_scripts():
    global stop_execution
    stop_execution = True
    return jsonify({'status': 'Stopping scripts'})

@app.route('/status', methods=['GET'])
def status():
    return jsonify(script_status)

@app.route('/output/<script_name>', methods=['GET'])
def output(script_name):
    return jsonify({'output': script_output.get(script_name, '')})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
