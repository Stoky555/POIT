from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect  
import math
import time
import random
import MySQLdb       
import configparser as ConfigParser
import serial

async_mode = None

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')
print(myhost)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock() 

ser = serial.Serial("/dev/ttyUSB0", 9600)
ser.baudrate=9600

read_ser = ser.readline()

def background_thread(args):
    count = 0    
    btnV = 0
    while True:
        if args:
            A = dict(args).get('A')
        else:
            A = 1

        btnV = dict(args).get('btn_value')
        print(A)
        print(args)
        print(btnV)
        socketio.sleep(2)
        count += 1
        value = ser.readline()
        if btnV:
            print(dataDict)
            socketio.emit('my_response',
                          {'data': dataDict, 'count': count},
                          namespace='/test')  

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)
  
@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['A'] = message['value']    
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})
    ser.write(message['value'])
 
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('click_eventStart', namespace='/test')
def db_message(message):   
    session['btn_value'] = 1
    #print(session['click_eventStart'])
    print(session)

@socketio.on('click_eventStop', namespace='/test')
def db_message(message):   
    session['btn_value'] = 0
    #print(session['click_eventStop'])
    print(session)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)