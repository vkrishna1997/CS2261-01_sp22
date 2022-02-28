from flask import Flask, request
from datetime import datetime
import requests
import socket
import sys

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

def parse_registration(data):
    data = data.split("\n")
    print(data)
    keys = []
    vals = []
    for ii in range(len(data)):
        if len(data[ii]) != 0:
            keys.append(data[ii].split("=")[0])
            vals.append(data[ii].split("=")[1])

    return {
        keys[0]: vals[0],
        keys[1]: vals[1],
        keys[2]: vals[2],
        keys[3]: vals[3]
    }


def send(hostname, self_ip, self_port, as_ip, as_port):

    query = "TYPE=A\nNAME=%s\n" % (hostname)

    print("UDP target IP:", as_ip)
    print("UDP target port:", as_port)
    print(query)

    try :
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        server_address = (self_ip, self_port)
        sock.bind(server_address)
        sock.sendto(query.encode(), ("127.0.0.1", 53533))

        while True:
            print("####### Client is listening #######")
            data, address = sock.recvfrom(1024)
            data = data.decode('utf-8')
            print("\n\n 2. Client received: ", data, "\n\n")
            break

    except e:
        print("Failed to send UDP request")
        throw(e)

    return parse_registration(data)


@app.route('/fibonacci')
def fib():
    USER_IP = "127.0.0.1"
    USER_PORT = 53535
    args = request.args
    # Sample URL
    # http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=10&as_ip=127.0.0.1&as_port=53533

    try:
        hostname = args['hostname']
        fs_port = args['fs_port']
        number = int(args['number'])
        as_ip = args['as_ip']
        as_port = args['as_port']
        print(args)
    except:
        print("All parameters not provided")
        return "Atleast one parameter missing", 400

    try :
        host = send(hostname, USER_IP, USER_PORT, as_ip, as_port)
        print(host)
    except:
        print("Failed to send UDP request")
        return "Failed to send udp request", 500

    content = requests.get("http://%s:%s/fibonacci?number=%d" % (host['VALUE'], str(fs_port), number)).content
    print(content)

    return content



app.run(host='0.0.0.0',
        port=8080,
        debug=True)
