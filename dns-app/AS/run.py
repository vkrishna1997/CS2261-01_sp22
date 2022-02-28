import socket
import sys
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 53533
MESSAGE = "Hello, World!"

def send(sock, msg, addr):

    try :
        print(addr)
        sock.sendto(msg.encode(), (addr))
    except:
        print("Failed to send UDP request")
        return "Failed to send udp request", 500

    return

def parse_query(data):
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
        keys[1]: vals[1]
    }


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

def create_response(host):
        return "TYPE=A\nNAME=%s\nVALUE=%s\nTTL=10\n" % (host['NAME'], host['VALUE'])


def rcv():
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = (UDP_IP, UDP_PORT)
    s.bind(server_address)
    print("Do Ctrl+c to exit the program !!")

    with open('data.json', 'w') as f:
        json.dump({"hosts": []}, f)


    while True:
        print("####### Server is listening #######")
        data, address = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("\n\n 2. Server received: ", data, "\n\n")

        with open('data.json', 'r') as f:
            json_data = json.load(f)

        hosts = json_data['hosts']
        data = str(data)
        print(data)
        if "VALUE" in data:
            print("REGISTER")
            # Treat as register
            save_data = parse_registration(data)
            hosts.append(save_data)
            with open('data.json', 'w') as f:
                json.dump({'hosts': hosts}, f)
        else:
            query_data = parse_query(data)
            for host in hosts:
                if host['NAME'] == query_data['NAME']:
                    found_host = host
                    print(found_host)
                    break

            resp = create_response(found_host)
            print(resp)
            send(s, resp, address)

# START RCV SOCKET
rcv()