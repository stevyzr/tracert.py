import socket

UDP_IP = "192.168.1.7"
UDP_PORT = 15005
icmp = socket.getprotobyname('icmp')
udp = socket.getprotobyname('udp')

sock = socket.socket(socket.AF_INET,socket.SOCK_RAW, icmp)
sock.bind(("",UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    if addr[0] != "192.168.1.7":
        print ("Recieved message:", data)
        print (addr[0])