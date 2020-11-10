import socket
import time as t


UDP_IP = '127.0.0.1'
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SEP = " "

while True:

    val = raw_input("Input Val:")
    direction = raw_input("Direction:")

    buff = val + SEP + direction

    sock.sendto(buff, (UDP_IP, UDP_PORT))
    #print(buff)
    t.sleep(0.5)