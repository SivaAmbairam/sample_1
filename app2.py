# import signal
# import time
# from flask import Flask, render_template, request, jsonify, send_from_directory
# import threading
# import subprocess
# import os
# import logging
# import jaydebeapi
# import jpype
# from scheduler import schedule_task, stop_scheduled_task, get_scheduled_tasks, schedule_monthly_task, scheduled_tasks
#
# app = Flask(__name__)
#
# SCRIPTS_DIRECTORY = r"D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts"
# stop_execution = False
# script_status = {}
# script_output = {}
#
# logging.basicConfig(level=logging.DEBUG)
#
# os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-22"
# jvm_path = os.path.join(os.environ['JAVA_HOME'], 'bin', 'server', 'jvm.dll')
#
# jdbc_driver_dir = r'C:\Program Files\sqljdbc_12.6\enu\jars'
# jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
# jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
# jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
# server = 'FSI-FSQL3-PROD'
#
# jpype.startJVM(jvm_path, f"-Djava.class.path={jdbc_driver_path}")
#
#
# def get_connection(username, password, schema):
#     connection_url = f'jdbc:sqlserver://{server};databaseName={schema};encrypt=true;trustServerCertificate=true;integratedSecurity=true;'
#     connection_properties = {
#         'user': username,
#         'password': password,
#         'integratedSecurity': 'true',
#         'authenticationScheme': 'NTLM',
#         'domain': 'fsi'
#     }
#     try:
#         connection = jaydebeapi.connect(
#             jdbc_driver_class,
#             connection_url,
#             connection_properties,
#             [jdbc_driver_path]
#         )
#         return connection
#     except jaydebeapi.DatabaseError as e:
#         logging.error(f"Error connecting to the database: {e}")
#         return None
#
#
# def stop_execution_handler(signum, frame):
#     global stop_execution
#     stop_execution = True
#
#
# signal.signal(signal.SIGINT, stop_execution_handler)
#
#
# def run_script(script_name):
#     global stop_execution, script_status, script_output
#     script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
#     script_status[script_name] = 'Running'
#     url_count = 0
#     try:
#         logging.debug(f"Starting script: {script_name}")
#         process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                                    universal_newlines=True)
#
#         while True:
#             if stop_execution or script_status[script_name] == 'Stopping':
#                 logging.debug(f"Stopping script: {script_name}")
#                 process.terminate()
#                 process.wait(timeout=5)
#                 if process.poll() is None:
#                     process.kill()
#                 script_status[script_name] = f'Stopped (URLs scraped: {url_count})'
#                 break
#             try:
#                 output = process.stdout.readline()
#                 if output == '' and process.poll() is not None:
#                     break
#                 if output:
#                     logging.debug(f'Script {script_name} output: {output.strip()}')
#                     script_output[script_name] = script_output.get(script_name, '') + output
#                     if output.strip().startswith('https://'):  # Count URLs
#                         url_count += 1
#                         script_status[script_name] = f'Running (URLs scraped: {url_count})'
#             except subprocess.TimeoutExpired:
#                 continue
#
#         stdout, stderr = process.communicate()
#         script_output[script_name] = script_output.get(script_name, '') + stdout + stderr
#         rc = process.poll()
#
#         if script_status[script_name] != f'Stopped (URLs scraped: {url_count})':
#             if rc == 0:
#                 script_status[script_name] = f'Completed (URLs scraped: {url_count})'
#                 # time.sleep(5)
#                 logging.debug("Starting Run_Comparison.py automatically...")
#                 run_script('Run_Comparison.py')
#             else:
#                 script_status[script_name] = f'Error: {stderr.strip()}'
#
#     except Exception as e:
#         logging.error(f"Exception running script {script_name}: {e}")
#         script_status[script_name] = f'Error: {str(e)}'
#     finally:
#         if script_name in script_status and 'Running' in script_status[script_name]:
#             script_status[script_name] = f'Completed (URLs scraped: {url_count})'
#
#
# # def run_script(script_name):
# #     global stop_execution, script_status, script_output
# #     script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
# #     script_status[script_name] = 'Running'
# #     url_count = 0
# #     try:
# #         logging.debug(f"Starting script: {script_name}")
# #         process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# #
# #         while True:
# #             if stop_execution or script_status[script_name] == 'Stopping':
# #                 logging.debug(f"Stopping script: {script_name}")
# #                 process.terminate()
# #                 process.wait(timeout=5)
# #                 if process.poll() is None:
# #                     process.kill()
# #                 script_status[script_name] = f'Stopped (URLs scraped: {url_count})'
# #                 break
# #             try:
# #                 output = process.stdout.readline()
# #                 if output == '' and process.poll() is not None:
# #                     break
# #                 if output:
# #                     logging.debug(f'Script {script_name} output: {output.strip()}')
# #                     script_output[script_name] = script_output.get(script_name, '') + output
# #                     if output.strip().startswith('https://') and script_name != 'Run_Comparison.py':  # Count URLs
# #                         url_count += 1
# #                         script_status[script_name] = f'Running (URLs scraped: {url_count})'
# #             except subprocess.TimeoutExpired:
# #                 continue
# #
# #         stdout, stderr = process.communicate()
# #         script_output[script_name] = script_output.get(script_name, '') + stdout + stderr
# #         rc = process.poll()
# #
# #         if script_status[script_name] not in [f'Stopped (URLs scraped: {url_count})', 'Stopped']:
# #             if rc == 0:
# #                 script_status[script_name] = f'Completed (URLs scraped: {url_count})'
# #                 # Automatically trigger Run_Comparison.py after script_name completes
# #                 if script_name in ['Flinn_vs_Frey.py', 'Flinn_vs_Nasco.py', 'Flinn_vs_Carolina.py', 'Flinn_vs_VWR.py', 'Flinn_vs_Wardsci.py']:
# #                     logging.debug("Starting Run_Comparison.py automatically...")
# #                     run_script('Run_Comparison.py')
# #             else:
# #                 script_status[script_name] = f'Error: {stderr.strip()}'
# #             time.sleep(5)
# #
# #     except Exception as e:
# #         logging.error(f"Exception running script {script_name}: {e}")
# #         script_status[script_name] = f'Error: {str(e)}'
# #     finally:
# #         if script_name in script_status and 'Running' in script_status[script_name]:
# #             script_status[script_name] = f'Completed (URLs scraped: {url_count})'
# #
# #
# #
# # def run_sequence_of_scripts(script_names):
# #     global stop_execution
# #     for script_name in script_names:
# #         if stop_execution:
# #             logging.info(f"Execution stopped before running {script_name}")
# #             break
# #         run_script(script_name)
# #
# #
# # def run_sequence_scripts():
# #     try:
# #         global stop_execution
# #         stop_execution = False
# #         data = request.get_json()
# #         scripts = data.get('scripts', [])
# #         if not scripts:
# #             return jsonify({'status': 'No scripts selected.'})
# #
# #         additional_scripts = [r'Run_Comparison.py']
# #         scripts.extend(additional_scripts)
# #
# #         # Run the sequence of scripts in a separate thread
# #         threading.Thread(target=run_sequence_of_scripts, args=(scripts,)).start()
# #         return jsonify({'status': 'Scripts are running in sequence.'})
# #     except Exception as e:
# #         logging.error(f"Error running scripts in sequence: {str(e)}")
# #         return jsonify({'status': f'Error running scripts in sequence: {str(e)}'}), 500
#
#
# UNWANTED_SCRIPTS = ['module_package.py']
# @app.route('/')
#
# def index():
#     try:
#         scripts = [f for f in os.listdir(SCRIPTS_DIRECTORY) if f.endswith('.py') and f not in UNWANTED_SCRIPTS]
#         return render_template('index.html', scripts=scripts)
#     except Exception as e:
#         logging.error(f"Error loading scripts: {str(e)}")
#         return jsonify({'status': f'Error loading scripts: {str(e)}'}), 500
#
#
# @app.route('/settings')
# def settings():
#     return render_template('settings.html')
#
#
# @app.route('/run_scripts', methods=['POST'])
# def run_scripts():
#     try:
#         global stop_execution
#         stop_execution = False
#         scripts = request.form.getlist('scripts')
#         if not scripts:
#             return jsonify({'status': 'No scripts selected.'})
#         for script in scripts:
#             threading.Thread(target=run_script, args=(script,)).start()
#             update_task_status(script, 'Running')  # Add this line
#         return jsonify({'status': 'Scripts running...'})
#     except Exception as e:
#         logging.error(f"Error running scripts: {str(e)}")
#         return jsonify({'status': f'Error running scripts: {str(e)}'}), 500
#
#
# def update_task_status(script_name, status):
#     for task in scheduled_tasks:
#         if task['script_name'] == script_name:
#             task['status'] = status
#             break
#
#
# @app.route('/stop_scripts', methods=['POST'])
# def stop_scripts():
#     try:
#         global stop_execution, script_status
#         stop_execution = True
#         # Terminate all running scripts
#         for script_name, status in script_status.items():
#             if status == 'Running':
#                 script_status[script_name] = 'Stopping'
#         return jsonify({'status': 'Stopping all running scripts...'})
#     except Exception as e:
#         logging.error(f"Error stopping scripts: {str(e)}")
#         return jsonify({'status': f'Error stopping scripts: {str(e)}'}), 500
#
#
# @app.route('/status', methods=['GET'])
# def status():
#     try:
#         return jsonify(script_status)
#     except Exception as e:
#         logging.error(f"Error getting status: {str(e)}")
#         return jsonify({'status': f'Error getting status: {str(e)}'}), 500
#
#
# @app.route('/schedule_scripts', methods=['POST'])
# def schedule_scripts():
#     global stop_execution
#     try:
#         stop_execution = False  # Reset the stop_execution flag when scheduling
#         scripts = request.form.getlist('scripts')
#         start_date = request.form.get('start-date')
#         start_time = request.form.get('start-time')
#         recurrence_type = request.form.get('recurrence-type')
#
#         unique_scripts = list(set(scripts))
#         scheduled_scripts = []
#
#         for script in unique_scripts:
#             if recurrence_type == 'monthly':
#                 schedule_monthly_task(script, start_date, start_time, run_script)
#             else:
#                 schedule_task(script, start_date, start_time, run_script)
#             scheduled_scripts.append(script)
#
#         if recurrence_type == 'monthly':
#             status = f'Scheduled {scheduled_scripts} monthly from {start_date} at {start_time}'
#         else:
#             status = f'Scheduled {scheduled_scripts} for {start_date} at {start_time}'
#
#         return jsonify({'status': status})
#     except Exception as e:
#         logging.error(f"Error scheduling script: {str(e)}")
#         return jsonify({'status': f'Error scheduling script: {str(e)}'}), 500
#
# @app.route('/stop_scheduled_scripts', methods=['POST'])
# # def stop_scheduled_scripts():
# #     try:
# #         script_name = request.form.get('script_name')
# #         if not script_name:
# #             return jsonify({'status': 'No script name provided.'}), 400
# #         response = stop_scheduled_task(script_name)
# #         return response
# #     except Exception as e:
# #         logging.error(f"Error stopping scheduled task: {str(e)}")
# #         return jsonify({'status': f'Error stopping scheduled task: {str(e)}'}), 500
#
# @app.route('/stop_scheduled_scripts', methods=['POST'])
# def stop_scheduled_scripts():
#     try:
#         response = stop_scheduled_task()
#         return response
#     except Exception as e:
#         logging.error(f"Error stopping scheduled tasks: {str(e)}")
#         return jsonify({'status': f'Error stopping scheduled tasks: {str(e)}'}), 500
#
# @app.route('/reset_state', methods=['POST'])
# def reset_state():
#     global stop_execution, script_status, script_output
#     stop_execution = False
#     script_status = {}
#     script_output = {}
#     return jsonify({'status': 'State reset successfully'})
#
#
# @app.route('/stop_all', methods=['POST'])
# def stop_all():
#     global stop_execution, script_status, scheduled_tasks
#     try:
#         # Stop all running scripts
#         stop_execution = True
#         for script_name in script_status:
#             script_status[script_name] = 'Stopped'
#
#         # Stop all scheduled tasks
#         stop_scheduled_task()
#
#         # Clear scheduled tasks
#         scheduled_tasks.clear()
#
#         return jsonify({'status': 'All scheduled tasks and running scripts have been stopped.'})
#     except Exception as e:
#         return jsonify({'status': f'Error stopping all tasks and scripts: {str(e)}'}), 500
#
#
#
# @app.route('/get_scheduling_status', methods=['GET'])
# def get_scheduling_status():
#     tasks = get_scheduled_tasks()
#     any_scheduled = len(tasks) > 0
#     any_running = any(task.get('status') == 'Running' for task in tasks)
#     return jsonify({
#         'status': 'Scheduled' if any_scheduled else 'Not Scheduled',
#         'tasks': [{'script_name': task['script_name'], 'run_date': task['run_date'], 'run_time': task['run_time'],
#                    'status': task.get('status', 'Scheduled')} for task in tasks],
#         'any_scheduled': any_scheduled,
#         'any_running': any_running
#     })
#
# @app.route('/check_running_scripts', methods=['GET'])
# def check_running_scripts():
#     any_running = any(status == 'Running' for status in script_status.values())
#     return jsonify({'any_running': any_running})
#
#
# @app.route('/get_scheduled_tasks', methods=['GET'])
# def get_scheduled_tasks_route():
#     try:
#         tasks = get_scheduled_tasks()
#         return jsonify(tasks)
#     except Exception as e:
#         logging.error(f"Error getting scheduled tasks: {str(e)}")
#         return jsonify({'status': f'Error getting scheduled tasks: {str(e)}'}), 500
#
#
# @app.route('/styles.css')
# def styles():
#     return send_from_directory('static', 'styles.css')
#
#
# @app.route('/writefile', methods=['POST'])
# def write_visited_log():
#     data = request.get_json()
#     if data:
#         formatted_data = f"user-name: {data['user-name']}\npassword: {data['password']}\nschema: {data['schema']}\n"
#         output_directory = os.path.join(SCRIPTS_DIRECTORY, 'Output', 'temp')
#         file_path = os.path.join(output_directory, 'db_connection_file.txt')
#         os.makedirs(output_directory, exist_ok=True)
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.write(formatted_data)
#         return jsonify({"message": "Data written successfully"}), 200
#     else:
#         return jsonify({"error": "No data received"}), 400
#
#
# @app.route('/db_connection', methods=['POST'])
# def db_connection():
#     try:
#         username = request.form.get('user-name')
#         password = request.form.get('password')
#         schema = request.form.get('schema')
#
#         connection = get_connection(username, password, schema)
#         if connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT @@version;")
#             row = cursor.fetchone()
#             version_info = row[0] if row else "Unknown"
#             cursor.close()
#             connection.close()
#             return jsonify({'status': 'success', 'version': version_info})
#         else:
#             return jsonify({'status': 'failed', 'error': 'Unable to connect to the database'}), 500
#     except Exception as e:
#         logging.error(f"Error in connection: {str(e)}")
#         return jsonify({'status': f'Error in connection: {str(e)}'}), 500
#
#
# if __name__ == '__main__':
#     app.run(host='192.168.20.61', port=5000, debug=True)


import signal
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import subprocess
import os
import logging
import jaydebeapi
import jpype
from scheduler import schedule_task, stop_scheduled_task, get_scheduled_tasks, schedule_monthly_task, scheduled_tasks

app = Flask(__name__)

# Global state object
global_state = {
    'run_button_disabled': False,
    'stop_button_disabled': True,
    'schedule_button_disabled': False,
    'stop_schedule_button_disabled': True,
    'scripts_running': False,
    'scheduled_tasks': []
}

state_lock = threading.Lock()

SCRIPTS_DIRECTORY = r"D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts"
stop_execution = False
script_status = {}
script_output = {}

logging.basicConfig(level=logging.DEBUG)

os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-22"
jvm_path = os.path.join(os.environ['JAVA_HOME'], 'bin', 'server', 'jvm.dll')

jdbc_driver_dir = r'C:\Program Files\sqljdbc_12.6\enu\jars'
jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
server = 'FSI-FSQL3-PROD'

jpype.startJVM(jvm_path, f"-Djava.class.path={jdbc_driver_path}")


def get_connection(username, password, schema):
    connection_url = f'jdbc:sqlserver://{server};databaseName={schema};encrypt=true;trustServerCertificate=true;integratedSecurity=true;'
    connection_properties = {
        'user': username,
        'password': password,
        'integratedSecurity': 'true',
        'authenticationScheme': 'NTLM',
        'domain': 'fsi'
    }
    try:
        connection = jaydebeapi.connect(
            jdbc_driver_class,
            connection_url,
            connection_properties,
            [jdbc_driver_path]
        )
        return connection
    except jaydebeapi.DatabaseError as e:
        logging.error(f"Error connecting to the database: {e}")
        return None


def stop_execution_handler(signum, frame):
    global stop_execution
    stop_execution = True


signal.signal(signal.SIGINT, stop_execution_handler)


# def run_script(script_name):
#     global stop_execution, script_status, script_output
#     script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
#     script_status[script_name] = 'Running'
#     url_count = 0
#     try:
#         logging.debug(f"Starting script: {script_name}")
#         process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#
#         while True:
#             if stop_execution or script_status[script_name] == 'Stopping':
#                 logging.debug(f"Stopping script: {script_name}")
#                 process.terminate()
#                 process.wait(timeout=5)
#                 if process.poll() is None:
#                     process.kill()
#                 script_status[script_name] = f'Stopped (URLs scraped: {url_count})'
#                 break
#             try:
#                 output = process.stdout.readline()
#                 if output == '' and process.poll() is not None:
#                     break
#                 if output:
#                     logging.debug(f'Script {script_name} output: {output.strip()}')
#                     script_output[script_name] = script_output.get(script_name, '') + output
#                     if output.strip().startswith('https://'):  # Count URLs
#                         url_count += 1
#                         script_status[script_name] = f'Running (URLs scraped: {url_count})'
#             except subprocess.TimeoutExpired:
#                 continue
#
#         stdout, stderr = process.communicate()
#         script_output[script_name] = script_output.get(script_name, '') + stdout + stderr
#         rc = process.poll()
#
#         if script_status[script_name] != f'Stopped (URLs scraped: {url_count})':
#             # script_status[script_name] = f'Completed (URLs scraped: {url_count})' if rc == 0 else f'Error: {stderr.strip()}'
#             # logging.debug("Starting Run_Comparison.py automatically...")
#             # run_script('Run_Comparison.py')
#             if rc == 0:
#                 script_status[script_name] = f'Completed (URLs scraped: {url_count})'
#                 # time.sleep(5)
#                 logging.debug("Starting Run_Comparison.py automatically...")
#                 run_script('Run_Comparison.py')
#             else:
#                 script_status[script_name] = f'Error: {stderr.strip()}'
#
#     except Exception as e:
#         logging.error(f"Exception running script {script_name}: {e}")
#         script_status[script_name] = f'Error: {str(e)}'
#     finally:
#         if script_name in script_status and 'Running' in script_status[script_name]:
#             script_status[script_name] = f'Completed (URLs scraped: {url_count})'
#             # logging.debug("Starting Run_Comparison.py automatically...")
#             # run_script('Run_Comparison.py')

def run_script(script_name):
    global stop_execution, script_status, script_output
    script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
    script_status[script_name] = 'Running'
    url_count = 0

    def check_and_run_comparison():
        if script_status[script_name].startswith('Completed') and script_name != 'Run_Comparison.py':
            logging.debug("Script completed. Starting Run_Comparison.py.")
            run_script('Run_Comparison.py')

    try:
        logging.debug(f"Starting script: {script_name}")
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            if stop_execution or script_status[script_name] == 'Stopping':
                logging.debug(f"Stopping script: {script_name}")
                process.terminate()
                process.wait(timeout=5)
                if process.poll() is None:
                    process.kill()
                script_status[script_name] = f'Stopped (URLs scraped: {url_count})'
                break
            try:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    logging.debug(f'Script {script_name} output: {output.strip()}')
                    script_output[script_name] = script_output.get(script_name, '') + output
                    if output.strip().startswith('https://'):  # Count URLs
                        url_count += 1
                        script_status[script_name] = f'Running (URLs scraped: {url_count})'
            except subprocess.TimeoutExpired:
                continue

        stdout, stderr = process.communicate()
        script_output[script_name] = script_output.get(script_name, '') + stdout + stderr
        rc = process.poll()

        if rc == 0:
            script_status[script_name] = f'Completed (URLs scraped: {url_count})'
            check_and_run_comparison()
        else:
            script_status[script_name] = f'Error: {stderr.strip()}'

    except Exception as e:
        logging.error(f"Exception running script {script_name}: {e}")
        script_status[script_name] = f'Error: {str(e)}'

    finally:
        if script_status[script_name].startswith('Running'):
            script_status[script_name] = f'Completed (URLs scraped: {url_count})'
            check_and_run_comparison()

    return script_status[script_name].startswith('Completed')



# def run_sequence_of_scripts(script_names):
#     global stop_execution
#     for script_name in script_names:
#         if stop_execution:
#             logging.info(f"Execution stopped before running {script_name}")
#             break
#         run_script(script_name)
#
#
# def run_sequence_scripts():
#     try:
#         global stop_execution
#         stop_execution = False
#         data = request.get_json()
#         scripts = data.get('scripts', [])
#         if not scripts:
#             return jsonify({'status': 'No scripts selected.'})
#
#         additional_scripts = ['Run_comparison.py']
#         scripts.extend(additional_scripts)
#
#         # Run the sequence of scripts in a separate thread
#         threading.Thread(target=run_sequence_of_scripts, args=(scripts,)).start()
#         return jsonify({'status': 'Scripts are running in sequence.'})
#     except Exception as e:
#         logging.error(f"Error running scripts in sequence: {str(e)}")
#         return jsonify({'status': f'Error running scripts in sequence: {str(e)}'}), 500


UNWANTED_SCRIPTS = ['module_package.py', 'Run_Comparison.py']
@app.route('/')

def index():
    try:
        scripts = [f for f in os.listdir(SCRIPTS_DIRECTORY) if f.endswith('.py') and f not in UNWANTED_SCRIPTS]
        return render_template('index.html', scripts=scripts)
    except Exception as e:
        logging.error(f"Error loading scripts: {str(e)}")
        return jsonify({'status': f'Error loading scripts: {str(e)}'}), 500


@app.route('/run_scripts', methods=['POST'])
def run_scripts():
    try:
        global global_state, stop_execution  # Add stop_execution to the global declaration
        print("Run scripts route called")
        with state_lock:
            global_state['run_button_disabled'] = True
            global_state['stop_button_disabled'] = False
            global_state['schedule_button_disabled'] = True
            global_state['stop_schedule_button_disabled'] = True
            global_state['scripts_running'] = True

        stop_execution = False  # Reset the stop_execution flag

        scripts = request.form.getlist('scripts')
        if not scripts:
            return jsonify({'status': 'No scripts selected.', **global_state})

        for script in scripts:
            threading.Thread(target=run_script, args=(script,)).start()
            update_task_status(script, 'Running')

        return jsonify({'status': 'Scripts running...', **global_state})
    except Exception as e:
        logging.error(f"Error running scripts: {str(e)}")
        return jsonify({'status': f'Error running scripts: {str(e)}', **global_state}), 500

def update_task_status(script_name, status):
    for task in scheduled_tasks:
        if task['script_name'] == script_name:
            task['status'] = status
            break

@app.route('/update_state', methods=['POST'])
def update_state():
    global global_state
    try:
        new_state = request.json
        if new_state is None:
            raise ValueError("No JSON data received")
        app.logger.info(f"Received state update: {new_state}")
        with state_lock:
            global_state.update(new_state)
        app.logger.info(f"Updated global state: {global_state}")
        return jsonify(global_state)
    except Exception as e:
        app.logger.error(f"Error updating state: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/stop_scripts', methods=['POST'])
def stop_scripts():
    try:
        global global_state
        with state_lock:
            global_state['run_button_disabled'] = False
            global_state['stop_button_disabled'] = True
            global_state['schedule_button_disabled'] = False
            global_state['scripts_running'] = False

        global stop_execution, script_status
        stop_execution = True
        for script_name, status in script_status.items():
            if status == 'Running':
                script_status[script_name] = 'Stopping'
        return jsonify({'status': 'Stopping all running scripts...'})
    except Exception as e:
        logging.error(f"Error stopping scripts: {str(e)}")
        return jsonify({'status': f'Error stopping scripts: {str(e)}'}), 500

@app.route('/status', methods=['GET'])
def status():
    try:
        return jsonify(script_status)
    except Exception as e:
        logging.error(f"Error getting status: {str(e)}")
        return jsonify({'status': f'Error getting status: {str(e)}'}), 500


@app.route('/schedule_scripts', methods=['POST'])
def schedule_scripts():
    global stop_execution
    try:
        global global_state
        with state_lock:
            global_state['run_button_disabled'] = True
            global_state['stop_button_disabled'] = True
            global_state['schedule_button_disabled'] = True
            global_state['stop_schedule_button_disabled'] = False

        stop_execution = False
        scripts = request.form.getlist('scripts')
        start_date = request.form.get('start-date')
        start_time = request.form.get('start-time')
        recurrence_type = request.form.get('recurrence-type')

        unique_scripts = list(set(scripts))
        scheduled_scripts = []

        for script in unique_scripts:
            if recurrence_type == 'monthly':
                schedule_monthly_task(script, start_date, start_time, run_script)
            else:
                schedule_task(script, start_date, start_time, run_script)
            scheduled_scripts.append(script)

        if recurrence_type == 'monthly':
            status = f'Scheduled {scheduled_scripts} monthly from {start_date} at {start_time}'
        else:
            status = f'Scheduled {scheduled_scripts} for {start_date} at {start_time}'

        # Return the updated task list immediately
        tasks = get_scheduled_tasks()
        return jsonify({'status': status, 'tasks': tasks})
    except Exception as e:
        logging.error(f"Error scheduling script: {str(e)}")
        return jsonify({'status': f'Error scheduling script: {str(e)}'}), 500

@app.route('/stop_scheduled_scripts', methods=['POST'])
# def stop_scheduled_scripts():
#     try:
#         script_name = request.form.get('script_name')
#         if not script_name:
#             return jsonify({'status': 'No script name provided.'}), 400
#         response = stop_scheduled_task(script_name)
#         return response
#     except Exception as e:
#         logging.error(f"Error stopping scheduled task: {str(e)}")
#         return jsonify({'status': f'Error stopping scheduled task: {str(e)}'}), 500

@app.route('/stop_scheduled_scripts', methods=['POST'])
def stop_scheduled_scripts():
    try:
        response = stop_scheduled_task()
        return response
    except Exception as e:
        logging.error(f"Error stopping scheduled tasks: {str(e)}")
        return jsonify({'status': f'Error stopping scheduled tasks: {str(e)}'}), 500

@app.route('/reset_state', methods=['POST'])
def reset_state():
    global stop_execution, script_status, script_output
    stop_execution = False
    script_status = {}
    script_output = {}
    return jsonify({'status': 'State reset successfully'})


@app.route('/stop_all', methods=['POST'])
def stop_all():
    global stop_execution, script_status, scheduled_tasks
    try:
        global global_state
        with state_lock:
            global_state['run_button_disabled'] = False
            global_state['stop_button_disabled'] = True
            global_state['schedule_button_disabled'] = False
            global_state['stop_schedule_button_disabled'] = True
            global_state['scripts_running'] = False
            global_state['scheduled_tasks'] = []




        # Stop all running scripts
        stop_execution = True
        for script_name in script_status:
            script_status[script_name] = 'Stopped'

        # Stop all scheduled tasks
        stop_scheduled_task()

        # Clear scheduled tasks
        scheduled_tasks.clear()

        return jsonify({'status': 'All scheduled tasks and running scripts have been stopped.'})
    except Exception as e:
        return jsonify({'status': f'Error stopping all tasks and scripts: {str(e)}'}), 500


@app.route('/get_state', methods=['GET'])
def get_state():
    global global_state
    with state_lock:
        return jsonify(global_state)

@app.route('/get_scheduling_status', methods=['GET'])
def get_scheduling_status():
    tasks = get_scheduled_tasks()
    any_scheduled = len(tasks) > 0
    any_running = any(task.get('status') == 'Running' for task in tasks)
    return jsonify({
        'status': 'Scheduled' if any_scheduled else 'Not Scheduled',
        'tasks': [{'script_name': task['script_name'], 'run_date': task['run_date'], 'run_time': task['run_time'],
                   'status': task.get('status', 'Scheduled')} for task in tasks],
        'any_scheduled': any_scheduled,
        'any_running': any_running
    })

@app.route('/check_running_scripts', methods=['GET'])
def check_running_scripts():
    any_running = any(status == 'Running' for status in script_status.values())
    return jsonify({'any_running': any_running})

@app.route('/get_scheduled_tasks', methods=['GET'])
def get_scheduled_tasks_route():
    try:
        tasks = get_scheduled_tasks()
        return jsonify(tasks)
    except Exception as e:
        logging.error(f"Error getting scheduled tasks: {str(e)}")
        return jsonify({'status': f'Error getting scheduled tasks: {str(e)}'}), 500


@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css')

@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/writefile', methods=['POST'])
def write_visited_log():
    data = request.get_json()
    if data:
        formatted_data = f"user-name: {data['user-name']}\npassword: {data['password']}\nschema: {data['schema']}\n"
        output_directory = os.path.join(SCRIPTS_DIRECTORY, 'Output', 'temp')
        file_path = os.path.join(output_directory, 'db_connection_file.txt')
        os.makedirs(output_directory, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_data)
        return jsonify({"message": "Data written successfully"}), 200
    else:
        return jsonify({"error": "No data received"}), 400


@app.route('/db_connection', methods=['POST'])
def db_connection():
    try:
        username = request.form.get('user-name')
        password = request.form.get('password')
        schema = request.form.get('schema')

        connection = get_connection(username, password, schema)
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT @@version;")
            row = cursor.fetchone()
            version_info = row[0] if row else "Unknown"
            cursor.close()
            connection.close()
            return jsonify({'status': 'success', 'version': version_info})
        else:
            return jsonify({'status': 'failed', 'error': 'Unable to connect to the database'}), 500
    except Exception as e:
        logging.error(f"Error in connection: {str(e)}")
        return jsonify({'status': f'Error in connection: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='192.168.20.61', port=5000, debug=True)

