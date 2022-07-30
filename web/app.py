import os
import subprocess
from time import sleep

from flask import Flask, request, render_template, redirect, send_file

os.chdir('../')

app = Flask(__name__)

global process

process = None


def setProcess(pro):
    global process
    process = pro


@app.route("/script-start", methods=['POST'])
def script_start():
    pro = subprocess.Popen(['python3', './main.py'])
    setProcess(pro)
    return redirect('/')


@app.route("/script-kill", methods=['POST'])
def script_kill():
    process.kill()
    sleep(2)
    return redirect('/')


@app.route("/profiles", methods=['POST'])
def profiles():
    with open('./profiles.txt', 'w') as profiles:
        profiles.write(request.form['profiles'])
    return redirect('/')


@app.route("/proceed", methods=['POST'])
def proceed():
    with open('./proceed.txt', 'w') as profiles:
        profiles.write(request.form['proceed'])
    return redirect('/')


@app.route("/failed", methods=['POST'])
def failed():
    with open('./failed.txt', 'w') as profiles:
        profiles.write(request.form['failed'])
    return redirect('/')


@app.route("/download-logs", methods=['POST'])
def download_logs():
    if request.method == 'POST':
        return send_file('./logs.log', mimetype='application/octet-stream')


@app.route("/clear-logs", methods=['POST'])
def clear_logs():
    if request.method == 'POST':
        with open('./logs.log', 'w') as logs:
            logs.write('')
    return redirect('/')


@app.route("/")
def index():
    status = 'Offline'
    if process == None:
        status = 'Offline'
    elif process.poll() == None:
        status = 'Online'
    elif process.poll == 0:
        status = 'Offline'
    if not os.path.exists('./logs.log'):
        with open('./logs.log', 'w') as file:
            file.write('')
    if not os.path.exists('./profiles.txt'):
        with open('./profiles.txt', 'w') as file:
            file.write('')
    if not os.path.exists('./proceed.txt'):
        with open('./proceed.txt', 'w') as file:
            file.write('')
    if not os.path.exists('./failed.txt'):
        with open('./failed.txt', 'w') as file:
            file.write('')
    with open('./profiles.txt', 'r') as profiles_file:
        profiles = ''
        for profile in profiles_file:
            profiles += profile
    with open('./proceed.txt', 'r') as proceed_file:
        proceeds = ''
        for proceed in proceed_file:
            proceeds += proceed
    with open('./failed.txt', 'r') as failed_file:
        faileds = ''
        for failed in failed_file:
            faileds += failed
    with open('./logs.log', 'r') as logs:
        logs_arr = []
        for log in logs:
            logs_arr.insert(0, log)
        logs_arr = logs_arr[:200:]

    return render_template('index.html', logs_arr=logs_arr, profiles=profiles, status=status, failed=faileds, proceed=proceeds)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
