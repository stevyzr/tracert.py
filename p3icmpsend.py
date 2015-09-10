"""
	Try to isolate code that can send ICMP packets

	Used library: socket

	The code is based on ping.py at https://gist.github.com/pklaus/856268
"""

import socket
import struct

ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket.getprotobyname('icmp')

def checksum(src_str):  
	# according to the original author, this function might not be very reliable, rewrite if possible
	sum = 0
	count_to = (len(src_str) / 2) * 2
	count = 0
	while count < count_to:
		this_val = ord(str(src_str[count + 1])) * 256 + ord(str(src_str[count]))
		sum = sum + this_val
		sum = sum & 0xffffffff #
		count = count + 2
	if count_to < len(src_str):
		sum = sum + ord(src_str[len(source_string) - 1])
		sum = sum & 0xffffffff #
	sum = (sum >> 16) + (sum & 0xffff)
	sum = sum + (sum >> 16)
	answer = ~sum
	answer = answer & 0xffff
	# Swap bytes. Bugger me if I know why.
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer

def create_packet(id):
	"""Create a new echo request packet based on the given "id"."""
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
	# ttl is at 0x16, id is at 0x26 0x36

	data = 64 * "A"
	
	#print(header + data)
	# Calculate the checksum on the data and the dummy header.
	my_checksum = checksum(header.decode() + data)
	# Now that we have the right checksum, we put that in. It's just easier
	# to make up a new header than to stuff it into the dummy.
	header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,	socket.htons(my_checksum), id, 1)
	return header + data.encode('utf-8')


def send_one_pack(dest_addr, id, ttl):
    """
    Sends one ping to the given "dest_addr" which can be an ip or hostname.
    "timeout" can be any integer or float except negatives and zero.
    Returns either the delay (in seconds) or None on timeout and an invalid
    address, respectively.
    """
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
        my_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    except socket.error as e:
        if e.errno in ERROR_DESCR:
            # Operation not permitted
            raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
        raise # raise the original error
    try:
        host = socket.gethostbyname(dest_addr)
    except socket.gaierror:
        return
    # Maximum for an unsigned short int c object counts to 65535 so
    # we have to sure that our packet id is not greater than that.
    packet_id = id
    packet = create_packet(packet_id)
    sent = my_socket.sendto(packet, (dest_addr, 1))
    #while packet:
        # The icmp protocol does not use a port, but the function
        # below expects it, so we just give it a dummy port.
        # sent = my_socket.sendto(packet, (dest_addr, 1))
        #packet = packet[sent:]
    delay = 0
    my_socket.close()
    return delay

#do_one("192.168.1.1", 16, 4)
send_one_pack("173.194.43.68", 16, 4)