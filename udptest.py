import socket

UDP_IP = "192.168.1.7"
UDP_PORT = 15005
MESSAGE = "Hello, World!"

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket.getprotobyname('icmp')) # UDP
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))