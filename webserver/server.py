from flask import Flask, render_template, send_file
import datetime
from tabulate import tabulate
import socket
import time
import _thread

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


if __name__ == "__main__":
    app.run(host='192.168.1.217', port=8080, debug=True)
