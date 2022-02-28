from flask import Flask, request
from datetime import datetime
import json
import socket
import sys

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world this is fib server!'

@app.route('/time')
def get_time():
    date = datetime.now()
    return 'Time: ' + str(date)

@app.route('/register', methods=['POST'])

def reg():
    # Sample URL
    # http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=K&number=X&as_ip=Y&as_port=Z
    UDP_IP = "127.0.0.1"
    UDP_PORT = 53533

    try:
        json_data = request.get_json()
        hostname = json_data["hostname"]
        ip = json_data["ip"]
        as_ip = json_data["as_ip"]
        as_port = json_data["as_port"]
    except:
        print("All parameters not provided")
        return "Atleast one parameter missing", 400

    msg = "TYPE=A\nNAME=%s\nVALUE=%s\nTTL=10\n" % (hostname, ip)

    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    print(msg)

    try :
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    except:
        print("Failed to send UDP request")
        return "Failed to send udp request", 500


    return "Successfully sent request", 201 # TODO: Replace placeholder seq number



def fibonacci(n):
    a = 0
    b = 1
     
    # Check is n is less
    # than 0
    if n < 0:
        print("Incorrect input")
         
    # Check is n is equal
    # to 0
    elif n == 0:
        return 0
       
    # Check if n is equal to 1
    elif n == 1:
        return b
    else:
        for i in range(1, n):
            c = a + b
            a = b
            b = c
        return b

@app.route('/fibonacci', methods=['GET'])
def fib():

    args = request.args
    try:
        number = int(args['number'])
    except:
        print("Invalid number provided")
        return "Invalid number provided", 400


    return "Fibonacci number: %s" % str(fibonacci(number))



app.run(host='0.0.0.0',
        port=9090,
        debug=True)
