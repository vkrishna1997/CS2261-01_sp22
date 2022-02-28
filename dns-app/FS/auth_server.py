import socket
import sys

UDP_IP = "0.0.0.0"
UDP_PORT = 53533
MESSAGE = "Hello, World!"

def rcv():

    print("In RCV func")

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = (UDP_IP, UDP_PORT)
    s.bind(server_address)
    print("Do Ctrl+c to exit the program !!")

    while True:
        print("####### Server is listening #######")
        data, address = s.recvfrom(4096)
        print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")
        send_data = input("Rcvd some data")
        # s.sendto(send_data.encode('utf-8'), address)
        # print("\n\n 1. Server sent : ", send_data,"\n\n")

# START RCV SOCKET
rcv()