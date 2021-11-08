from flask import Flask, render_template, send_file, request
import datetime
from tabulate import tabulate
import socket
import time
import _thread
import os

app = Flask(__name__)
@app.route("/")
def hello():

    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'CubeTimer!',
        'time': timeString
    }
    return render_template('index.html', **templateData)

@app.route("/solves3x3x3.txt")
def download3():
    path = "/home/pi/CubeTimer/solves/solves3x3x3.txt"
    return send_file(path, as_attachment=True)
@app.route("/solves2x2x2.txt")
def download2():
    path = "/home/pi/CubeTimer/solves/solves2x2x2.txt"
    return send_file(path, as_attachment=True)
@app.route("/solves4x4x4.txt")
def download4():
    path = "/home/pi/CubeTimer/solves/solves4x4x4.txt"
    return send_file(path, as_attachment=True)
@app.route("/solves5x5x5.txt")
def download5():
    path = "/home/pi/CubeTimer/solves/solves5x5x5.txt"
    return send_file(path, as_attachment=True)
@app.route("/solves7x7x7.txt")
def download7():
    path = "/home/pi/CubeTimer/solves/solves7x7x7.txt"
    return send_file(path, as_attachment=True)
@app.route("/screenshot")
def screenshot():
    path = "/home/pi/CubeTimer/screenschot.png"
    os.system("scrot " + path) 
    return send_file(path, as_attachment=True)

@app.route("/shutdown", methods=['GET'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."

def stop():
    resp = request.get('http://0.0.0.0:8080/shutdown')

if  __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
