import socket

def main(dest):
    
    destIP =  socket.gethostbyname(dest)
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    port = 33434
    max_hop = 64
    #print("init")
    print(destIP)

    while True:
        # Open connection
        recv_sckt = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket.IPPROTO_ICMP)
        send_sckt = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, udp)
        send_sckt.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        recv_sckt.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
        try:
            recv_sckt.bind(('192.168.1.7', port))
        except IOError:
            print("fail to bind")

        send_sckt.sendto(bytes(0), (destIP, port)) 
        curr_addr = None
        curr_name = None
        #print("enter loop")
        #print(ttl)


        try:
            
            #print("start listen")
            recv_sckt.settimeout(100.0)
            data,curr_addr = recv_sckt.recvfrom(2048)
            
            #print(data)
            #print("Current address:", curr_addr)
                #Assign the value of the 2nd element in tuple to curr_addr
                # _, means that value of the 1st element is ignored
            curr_addr = curr_addr[0]
            #print (curr_addr)

            # try to convert IP to domain names
            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except socket.error:
                curr_name = "Unknown"

        except socket.error:
            pass
        finally:
            send_sckt.close()
            recv_sckt.close()

        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = "*"

        # print data
        
        print ("%d \t %s" % (ttl, curr_host))
        ttl += 1
        
        # break if get result or reach max hop
        if curr_addr == destIP or ttl > max_hop:
            break


        pass # this is just a placeholder


if __name__== "__main__":
    print ("start")
    main('tieba.baidu.com')
