from __future__ import absolute_import
import multiprocessing
import subprocess
import time
import os
import webbrowser
import requests
import socket
import psutil
import sys
from solox.view.apis import api
from solox.view.pages import page
from logzero import logger
from threading import Lock
from flask_socketio import SocketIO, disconnect
from flask import Flask
from pyfiglet import Figlet
from solox import __version__

app = Flask(__name__, template_folder='templates', static_folder='static')
app.register_blueprint(api)
app.register_blueprint(page)

# socketio = SocketIO(app, cors_allowed_origins="*")
# thread = True
# thread_lock = Lock()


# @socketio.on('connect', namespace='/logcat')
# def connect():
#     socketio.emit('start connect', {'data': 'Connected'}, namespace='/logcat')
#     logDir = os.path.join(os.getcwd(),'adblog')
#     if not os.path.exists(logDir):
#         os.mkdir(logDir)
#     global thread
#     thread = True
#     with thread_lock:
#         if thread:
#             thread = socketio.start_background_task(target=backgroundThread)


# def backgroundThread():
#     global thread
#     try:
#         # logger.info('Initializing adb environment ...')
#         # os.system('adb kill-server')
#         # os.system('adb start-server')
#         current_time = time.strftime("%Y%m%d%H", time.localtime())
#         logPath = os.path.join(os.getcwd(),'adblog',f'{current_time}.log')
#         logcat = subprocess.Popen(f'adb logcat *:E > {logPath}', stdout=subprocess.PIPE,
#                                   shell=True)
#         with open(logPath, "r") as f:
#             while thread:
#                 socketio.sleep(1)
#                 for line in f.readlines():
#                     socketio.emit('message', {'data': line}, namespace='/logcat')
#         if logcat.poll() == 0:
#             thread = False
#     except Exception:
#         pass


# @socketio.on('disconnect_request', namespace='/logcat')
# def disconnect():
#     global thread
#     logger.warning('Logcat client disconnected')
#     thread = False
#     disconnect()

def ip() -> str:
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = '127.0.0.1'    
    return ip

def listen(port):
    net_connections = psutil.net_connections()
    conn = [c for c in net_connections if c.status == "LISTEN" and c.laddr.port == port]
    if conn:
        pid = conn[0].pid
        logger.warning('Port {} is used by process {}'.format(port, pid))
        logger.info('you can start solox : python -m solox --host={ip} --port={port}')
        return False
    return True

def status(host: str, port: int):
    r = requests.get('http://{}:{}'.format(host, port), timeout=2.0)
    flag = (True, False)[r.status_code == 200]
    return flag


def open_url(host: str, port: int):
    flag = True
    while flag:
        logger.info('start solox server ...')
        f = Figlet(font="slant", width=300)
        print(f.renderText("SOLOX {}".format(__version__)))
        flag = status(host, port)
    webbrowser.open('http://{}:{}/?platform=Android&lan=en'.format(host, port), new=2)
    logger.info('Running on http://{}:{}/?platform=Android&lan=en (Press CTRL+C to quit)'.format(host, port))


def start(host: str, port: int):
    logger.info('Running on http://{}:{}/?platform=Android&lan=en (Press CTRL+C to quit)'.format(host, port))
    app.run(host=host, port=port, debug=True)

def main():
    start(ip(), 50003)      


if __name__ == '__main__':
    main()